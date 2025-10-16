#!/usr/bin/env python3
"""
MediScan - AI-Powered Barcode Scanner for Medicines and Perishable Items

Main application entry point
"""

import sys
import argparse
from pathlib import Path
from datetime import date, datetime, timedelta
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.product import Product, Medicine, PerishableItem, ProductCategory, MedicineType
from src.models.manufacturing_log import ManufacturingLog, LogStatus
from src.services.barcode_scanner import BarcodeScanner
from src.services.product_service import ProductService
from src.services.verification_service import VerificationService
from src.services.expiry_tracker import ExpiryTracker
from src.services.notification_service import NotificationService
from src.ai.recipe_generator import RecipeGenerator
from src.ai.medicine_analyzer import MedicineAnalyzer
from src.ai.counterfeit_detector import CounterfeitDetector
from src.utils.config import Config
from src.utils.data_loader import DataLoader

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    console = Console()
except ImportError:
    # Fallback if rich is not installed
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()


class MediScanApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.config = Config()
        self.scanner = BarcodeScanner()
        self.product_service = ProductService()
        self.verification_service = VerificationService(self.config.manufacturing_log_path)
        self.expiry_tracker = ExpiryTracker(self.config.notification_lead_time_days)
        self.notification_service = NotificationService()
        self.recipe_generator = RecipeGenerator(self.config.openai_api_key)
        self.medicine_analyzer = MedicineAnalyzer(self.config.openai_api_key)
        self.counterfeit_detector = CounterfeitDetector(self.config.openai_api_key)
    
    def scan_product(self, barcode: Optional[str] = None) -> Optional[Product]:
        """
        Scan a product by barcode
        
        Args:
            barcode: Barcode string (if None, will attempt camera scan)
            
        Returns:
            Product if found, None otherwise
        """
        if not barcode:
            console.print("[yellow]Attempting to scan from camera...[/yellow]")
            console.print("[yellow]Note: Camera scanning requires a connected camera device[/yellow]")
            return None
        
        # Validate barcode
        if not self.scanner.validate_barcode(barcode):
            console.print(f"[red]Invalid barcode format: {barcode}[/red]")
            return None
        
        # Look up product
        product = self.product_service.get_product(barcode)
        
        if product:
            self._display_product(product)
            self._verify_and_check_product(product)
        else:
            console.print(f"[yellow]Product not found in database: {barcode}[/yellow]")
            console.print("[cyan]You can add this product using the 'add' command[/cyan]")
        
        return product
    
    def _display_product(self, product: Product):
        """Display product information"""
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]{product.name}[/bold cyan]\n"
            f"Manufacturer: {product.manufacturer}\n"
            f"Category: {product.category.value}\n"
            f"Barcode: {product.barcode}\n"
            f"Batch: {product.batch_number}",
            title="Product Information",
            border_style="cyan"
        ))
        
        # Display dates and expiry
        days_until_expiry = product.days_until_expiry()
        expiry_color = "red" if days_until_expiry < 0 else \
                      "yellow" if days_until_expiry <= 7 else "green"
        
        console.print(f"Manufacturing Date: {product.manufacturing_date}")
        console.print(f"Expiry Date: [{expiry_color}]{product.expiry_date}[/{expiry_color}]")
        console.print(f"Days Until Expiry: [{expiry_color}]{days_until_expiry}[/{expiry_color}]")
        
        # Display medicine-specific info
        if isinstance(product, Medicine):
            console.print("\n[bold]Medicine Information:[/bold]")
            console.print(f"Type: {product.medicine_type.value}")
            console.print(f"Dosage: {product.dosage or 'Not specified'}")
            console.print(f"Prescription Required: {'Yes' if product.prescription_required else 'No'}")
            if product.active_ingredients:
                console.print(f"Active Ingredients: {', '.join(product.active_ingredients)}")
        
        # Display perishable item info
        elif isinstance(product, PerishableItem):
            console.print("\n[bold]Perishable Item Information:[/bold]")
            console.print(f"Storage: {product.storage_instructions or 'Standard'}")
            if product.allergens:
                console.print(f"Allergens: {', '.join(product.allergens)}")
    
    def _verify_and_check_product(self, product: Product):
        """Verify product and check for issues"""
        console.print()
        
        # Verify against manufacturing logs
        is_verified, message = self.verification_service.verify_product(product)
        
        if is_verified:
            console.print(f"[green]✓ {message}[/green]")
        else:
            console.print(f"[red]✗ {message}[/red]")
            product.is_counterfeit = True
        
        # Check for counterfeits
        log = self.verification_service.get_log(product.barcode, product.batch_number)
        counterfeit_analysis = self.counterfeit_detector.analyze_product(product, log)
        
        if counterfeit_analysis['is_counterfeit']:
            console.print(f"[bold red]⚠️ COUNTERFEIT ALERT: {counterfeit_analysis['recommendation']}[/bold red]")
        elif counterfeit_analysis['is_suspicious']:
            console.print(f"[yellow]⚠️ {counterfeit_analysis['recommendation']}[/yellow]")
        
        # Check expiry status
        expiry_status = self.expiry_tracker.check_expiry_status(product)
        if expiry_status['needs_warning']:
            console.print(f"[{expiry_status['urgency']}]⚠️ {expiry_status['message']}[/{expiry_status['urgency']}]")
    
    def list_expiring_products(self, days: int = 7):
        """List products expiring soon"""
        products = self.product_service.list_products()
        expiring = self.expiry_tracker.get_expiring_products(products, days)
        
        if not expiring:
            console.print(f"[green]No products expiring within {days} days[/green]")
            return
        
        console.print(f"\n[bold]Products Expiring Within {days} Days:[/bold]\n")
        
        table = Table(box=box.ROUNDED)
        table.add_column("Product", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Days Left", justify="right")
        table.add_column("Urgency", justify="center")
        
        for item in expiring:
            urgency_color = {
                'expired': 'red',
                'critical': 'red',
                'high': 'yellow',
                'medium': 'yellow',
                'none': 'green'
            }.get(item['urgency'], 'white')
            
            table.add_row(
                item['name'],
                item.get('category', 'N/A'),
                str(item['days_until_expiry']),
                f"[{urgency_color}]{item['urgency'].upper()}[/{urgency_color}]"
            )
        
        console.print(table)
    
    def check_medicine_interactions(self):
        """Check for medicine interactions"""
        medicines = self.product_service.get_medicines()
        
        if len(medicines) < 2:
            console.print("[yellow]Need at least 2 medicines to check interactions[/yellow]")
            return
        
        console.print(f"\n[bold]Checking interactions for {len(medicines)} medicines...[/bold]\n")
        
        result = self.medicine_analyzer.check_interactions(medicines)
        
        if result['has_interactions']:
            console.print(f"[red]⚠️ Found {len(result['interactions'])} potential interaction(s):[/red]\n")
            
            for interaction in result['interactions']:
                console.print(Panel(
                    f"[bold]{interaction['medicine1']}[/bold] ↔ [bold]{interaction['medicine2']}[/bold]\n"
                    f"Severity: [{interaction['severity']}]{interaction['severity'].upper()}[/{interaction['severity']}]\n"
                    f"Description: {interaction['description']}\n"
                    f"Recommendation: {interaction['recommendation']}",
                    border_style="red"
                ))
        else:
            console.print("[green]✓ No interactions detected[/green]")
    
    def generate_recipes(self, max_recipes: int = 3):
        """Generate recipe suggestions for expiring items"""
        perishables = self.product_service.get_perishable_items()
        expiring = [p for p in perishables if 0 <= p.days_until_expiry() <= 7]
        
        if not expiring:
            console.print("[yellow]No perishable items expiring soon[/yellow]")
            return
        
        console.print(f"\n[bold]Generating recipes for {len(expiring)} expiring item(s)...[/bold]\n")
        
        result = self.recipe_generator.generate_recipe(expiring)
        
        if result.get('success') and result.get('recipes'):
            for recipe in result['recipes'][:max_recipes]:
                console.print(Panel(
                    f"[bold cyan]{recipe['title']}[/bold cyan]\n"
                    f"{recipe['description']}\n\n"
                    f"[bold]Prep Time:[/bold] {recipe['prep_time']}\n"
                    f"[bold]Cook Time:[/bold] {recipe['cook_time']}\n"
                    f"[bold]Servings:[/bold] {recipe['servings']}\n\n"
                    f"[bold]Priority Ingredients:[/bold] {', '.join(recipe['priority_items'])}",
                    border_style="green"
                ))
    
    def show_dashboard(self):
        """Show application dashboard"""
        console.print("\n[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]        MediScan - Product Management Dashboard      [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════════[/bold cyan]\n")
        
        # Get statistics
        all_products = self.product_service.list_products()
        medicines = self.product_service.get_medicines()
        perishables = self.product_service.get_perishable_items()
        
        summary = self.expiry_tracker.get_expiry_summary(all_products)
        
        # Display statistics
        console.print(f"[bold]Total Products:[/bold] {summary['total_products']}")
        console.print(f"  • Medicines: {len(medicines)}")
        console.print(f"  • Perishable Items: {len(perishables)}")
        console.print()
        
        console.print(f"[bold]Expiry Status:[/bold]")
        console.print(f"  • [red]Expired: {summary['expired_count']}[/red]")
        console.print(f"  • [yellow]Critical (≤1 day): {summary['critical_count']}[/yellow]")
        console.print(f"  • [yellow]High Priority (2-3 days): {summary['high_priority_count']}[/yellow]")
        console.print(f"  • Medium Priority (4-7 days): {summary['medium_priority_count']}")
        console.print()
        
        # Show recent notifications
        unread = self.notification_service.get_unread_notifications()
        if unread:
            console.print(f"[bold]Unread Notifications:[/bold] {len(unread)}")
    
    def initialize_sample_data(self):
        """Initialize application with sample data"""
        console.print("[cyan]Initializing sample data...[/cyan]")
        
        # Create sample manufacturing logs
        DataLoader.create_sample_manufacturing_logs()
        
        # Create sample products
        DataLoader.create_sample_products()
        
        # Reload services
        self.product_service = ProductService()
        self.verification_service = VerificationService(self.config.manufacturing_log_path)
        
        console.print("[green]✓ Sample data initialized successfully[/green]")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MediScan - AI-Powered Barcode Scanner for Medicines and Perishable Items'
    )
    
    parser.add_argument(
        'command',
        choices=['scan', 'list', 'expiring', 'interactions', 'recipes', 'dashboard', 'init'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--barcode',
        help='Barcode to scan'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days for expiring items (default: 7)'
    )
    
    args = parser.parse_args()
    
    app = MediScanApp()
    
    try:
        if args.command == 'scan':
            app.scan_product(args.barcode)
        
        elif args.command == 'list':
            app.show_dashboard()
        
        elif args.command == 'expiring':
            app.list_expiring_products(args.days)
        
        elif args.command == 'interactions':
            app.check_medicine_interactions()
        
        elif args.command == 'recipes':
            app.generate_recipes()
        
        elif args.command == 'dashboard':
            app.show_dashboard()
        
        elif args.command == 'init':
            app.initialize_sample_data()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
