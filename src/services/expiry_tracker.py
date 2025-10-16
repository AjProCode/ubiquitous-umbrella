"""Expiry tracking service"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

from ..models.product import Product, Medicine, PerishableItem


class ExpiryTracker:
    """Service for tracking product expiry"""
    
    def __init__(self, warning_days: int = 7):
        """
        Initialize expiry tracker
        
        Args:
            warning_days: Days before expiry to trigger warnings
        """
        self.warning_days = warning_days
        self.expiry_callbacks = []
    
    def register_callback(self, callback):
        """Register callback for expiry events"""
        self.expiry_callbacks.append(callback)
    
    def check_expiry_status(self, product: Product) -> Dict[str, any]:
        """
        Check expiry status of product
        
        Args:
            product: Product to check
            
        Returns:
            Dictionary with expiry status information
        """
        days_until_expiry = product.days_until_expiry()
        is_expired = product.is_expired()
        
        status = {
            'barcode': product.barcode,
            'name': product.name,
            'days_until_expiry': days_until_expiry,
            'is_expired': is_expired,
            'expiry_date': product.expiry_date.isoformat(),
            'needs_warning': False,
            'urgency': 'none'
        }
        
        if is_expired:
            status['needs_warning'] = True
            status['urgency'] = 'expired'
            status['message'] = f"{product.name} has expired on {product.expiry_date}"
        elif 0 <= days_until_expiry <= self.warning_days:
            status['needs_warning'] = True
            if days_until_expiry == 0:
                status['urgency'] = 'critical'
                status['message'] = f"{product.name} expires today!"
            elif days_until_expiry <= 3:
                status['urgency'] = 'high'
                status['message'] = f"{product.name} expires in {days_until_expiry} days"
            else:
                status['urgency'] = 'medium'
                status['message'] = f"{product.name} expires in {days_until_expiry} days"
        else:
            status['message'] = f"{product.name} expires in {days_until_expiry} days"
        
        return status
    
    def get_expiring_products(
        self,
        products: List[Product],
        days_threshold: Optional[int] = None
    ) -> List[Dict[str, any]]:
        """
        Get products expiring within threshold
        
        Args:
            products: List of products to check
            days_threshold: Days threshold (uses warning_days if None)
            
        Returns:
            List of expiry status dictionaries
        """
        threshold = days_threshold if days_threshold is not None else self.warning_days
        
        expiring = []
        for product in products:
            status = self.check_expiry_status(product)
            if status['needs_warning'] or (0 <= status['days_until_expiry'] <= threshold):
                expiring.append(status)
        
        # Sort by urgency and days until expiry
        urgency_order = {'expired': 0, 'critical': 1, 'high': 2, 'medium': 3, 'none': 4}
        expiring.sort(key=lambda x: (urgency_order[x['urgency']], x['days_until_expiry']))
        
        return expiring
    
    def get_expired_products(self, products: List[Product]) -> List[Product]:
        """
        Get expired products
        
        Args:
            products: List of products to check
            
        Returns:
            List of expired products
        """
        return [p for p in products if p.is_expired()]
    
    def categorize_by_expiry(self, products: List[Product]) -> Dict[str, List[Product]]:
        """
        Categorize products by expiry urgency
        
        Args:
            products: List of products
            
        Returns:
            Dictionary of products categorized by urgency
        """
        categories = {
            'expired': [],
            'critical': [],  # Expires today or tomorrow
            'high': [],      # Expires in 2-3 days
            'medium': [],    # Expires in 4-7 days
            'low': []        # Expires in 8-30 days
        }
        
        for product in products:
            days = product.days_until_expiry()
            
            if days < 0:
                categories['expired'].append(product)
            elif days <= 1:
                categories['critical'].append(product)
            elif days <= 3:
                categories['high'].append(product)
            elif days <= self.warning_days:
                categories['medium'].append(product)
            elif days <= 30:
                categories['low'].append(product)
        
        return categories
    
    def get_medicine_expiry_priority(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Prioritize medicines by expiry and importance
        
        Args:
            medicines: List of medicines
            
        Returns:
            Sorted list of medicines by priority
        """
        def priority_score(medicine: Medicine) -> tuple:
            # Lower score = higher priority
            days = medicine.days_until_expiry()
            
            # Priority factors:
            # 1. Prescription medicines are more important
            # 2. Closer to expiry = higher priority
            prescription_priority = 0 if medicine.prescription_required else 1
            
            return (prescription_priority, days)
        
        return sorted(medicines, key=priority_score)
    
    def calculate_usage_recommendation(
        self,
        product: Product,
        daily_usage: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Calculate usage recommendations based on expiry
        
        Args:
            product: Product to analyze
            daily_usage: Average daily usage amount
            
        Returns:
            Dictionary with usage recommendations
        """
        days_until_expiry = product.days_until_expiry()
        
        recommendation = {
            'barcode': product.barcode,
            'name': product.name,
            'days_until_expiry': days_until_expiry,
            'should_use': False,
            'recommended_daily_usage': None,
            'action': 'none',
            'message': ''
        }
        
        if days_until_expiry < 0:
            recommendation['action'] = 'discard'
            recommendation['message'] = 'Product has expired. Please discard safely.'
        elif days_until_expiry == 0:
            recommendation['should_use'] = True
            recommendation['action'] = 'use_immediately'
            recommendation['message'] = 'Product expires today! Use immediately.'
        elif days_until_expiry <= 3:
            recommendation['should_use'] = True
            recommendation['action'] = 'prioritize'
            recommendation['message'] = f'Product expires in {days_until_expiry} days. Prioritize usage.'
        elif days_until_expiry <= self.warning_days:
            recommendation['should_use'] = True
            recommendation['action'] = 'plan_usage'
            recommendation['message'] = f'Product expires in {days_until_expiry} days. Plan usage accordingly.'
        
        if daily_usage and days_until_expiry > 0:
            # Calculate if current usage rate will finish before expiry
            # Assuming some quantity metrics (simplified)
            recommendation['recommended_daily_usage'] = daily_usage
        
        return recommendation
    
    def get_expiry_summary(self, products: List[Product]) -> Dict[str, any]:
        """
        Get summary of expiry status across all products
        
        Args:
            products: List of products
            
        Returns:
            Summary dictionary
        """
        categories = self.categorize_by_expiry(products)
        
        return {
            'total_products': len(products),
            'expired_count': len(categories['expired']),
            'critical_count': len(categories['critical']),
            'high_priority_count': len(categories['high']),
            'medium_priority_count': len(categories['medium']),
            'low_priority_count': len(categories['low']),
            'medicines_expiring_count': sum(
                1 for p in products 
                if isinstance(p, Medicine) and 0 <= p.days_until_expiry() <= self.warning_days
            ),
            'perishables_expiring_count': sum(
                1 for p in products 
                if isinstance(p, PerishableItem) and 0 <= p.days_until_expiry() <= self.warning_days
            )
        }
