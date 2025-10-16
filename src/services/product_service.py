"""Product service for managing products"""

import json
import os
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pathlib import Path

from ..models.product import Product, Medicine, PerishableItem, ProductCategory


class ProductService:
    """Service for managing products"""
    
    def __init__(self, storage_path: str = "./data/products"):
        """
        Initialize product service
        
        Args:
            storage_path: Path to product storage directory
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.products: Dict[str, Product] = {}
        self._load_products()
    
    def _load_products(self):
        """Load products from storage"""
        products_file = self.storage_path / "products.json"
        if products_file.exists():
            try:
                with open(products_file, 'r') as f:
                    data = json.load(f)
                    for product_data in data:
                        product = self._dict_to_product(product_data)
                        if product:
                            self.products[product.barcode] = product
            except Exception as e:
                print(f"Error loading products: {e}")
    
    def _save_products(self):
        """Save products to storage"""
        products_file = self.storage_path / "products.json"
        try:
            data = [product.to_dict() for product in self.products.values()]
            with open(products_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving products: {e}")
    
    def _dict_to_product(self, data: Dict[str, Any]) -> Optional[Product]:
        """Convert dictionary to product object"""
        try:
            category = ProductCategory(data['category'])
            
            base_args = {
                'barcode': data['barcode'],
                'name': data['name'],
                'manufacturer': data['manufacturer'],
                'category': category,
                'manufacturing_date': date.fromisoformat(data['manufacturing_date']),
                'expiry_date': date.fromisoformat(data['expiry_date']),
                'batch_number': data['batch_number'],
                'description': data.get('description'),
                'is_verified': data.get('is_verified', False),
                'is_counterfeit': data.get('is_counterfeit', False)
            }
            
            if category == ProductCategory.MEDICINE:
                from ..models.product import MedicineType
                return Medicine(
                    **base_args,
                    medicine_type=MedicineType(data.get('medicine_type', 'other')),
                    dosage=data.get('dosage'),
                    active_ingredients=data.get('active_ingredients', []),
                    side_effects=data.get('side_effects', []),
                    contraindications=data.get('contraindications', []),
                    drug_interactions=data.get('drug_interactions', []),
                    storage_instructions=data.get('storage_instructions'),
                    prescription_required=data.get('prescription_required', False),
                    generic_name=data.get('generic_name'),
                    therapeutic_class=data.get('therapeutic_class')
                )
            elif category in [ProductCategory.FOOD, ProductCategory.BEVERAGE]:
                return PerishableItem(
                    **base_args,
                    storage_temperature=data.get('storage_temperature'),
                    nutritional_info=data.get('nutritional_info', {}),
                    allergens=data.get('allergens', []),
                    ingredients=data.get('ingredients', []),
                    serving_size=data.get('serving_size'),
                    storage_instructions=data.get('storage_instructions'),
                    opened_shelf_life_days=data.get('opened_shelf_life_days')
                )
            else:
                return Product(**base_args)
        except Exception as e:
            print(f"Error converting dict to product: {e}")
            return None
    
    def add_product(self, product: Product) -> bool:
        """
        Add or update product
        
        Args:
            product: Product to add
            
        Returns:
            True if successful
        """
        try:
            product.updated_at = datetime.now()
            self.products[product.barcode] = product
            self._save_products()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def get_product(self, barcode: str) -> Optional[Product]:
        """
        Get product by barcode
        
        Args:
            barcode: Product barcode
            
        Returns:
            Product or None if not found
        """
        return self.products.get(barcode)
    
    def delete_product(self, barcode: str) -> bool:
        """
        Delete product
        
        Args:
            barcode: Product barcode
            
        Returns:
            True if deleted
        """
        if barcode in self.products:
            del self.products[barcode]
            self._save_products()
            return True
        return False
    
    def list_products(
        self,
        category: Optional[ProductCategory] = None,
        expired: Optional[bool] = None,
        verified: Optional[bool] = None
    ) -> List[Product]:
        """
        List products with filters
        
        Args:
            category: Filter by category
            expired: Filter by expiry status
            verified: Filter by verification status
            
        Returns:
            List of products
        """
        products = list(self.products.values())
        
        if category:
            products = [p for p in products if p.category == category]
        
        if expired is not None:
            products = [p for p in products if p.is_expired() == expired]
        
        if verified is not None:
            products = [p for p in products if p.is_verified == verified]
        
        return products
    
    def get_expiring_soon(self, days: int = 7) -> List[Product]:
        """
        Get products expiring soon
        
        Args:
            days: Number of days threshold
            
        Returns:
            List of products expiring within days
        """
        return [
            p for p in self.products.values()
            if 0 <= p.days_until_expiry() <= days
        ]
    
    def get_medicines(self) -> List[Medicine]:
        """Get all medicines"""
        return [
            p for p in self.products.values()
            if isinstance(p, Medicine)
        ]
    
    def get_perishable_items(self) -> List[PerishableItem]:
        """Get all perishable items"""
        return [
            p for p in self.products.values()
            if isinstance(p, PerishableItem)
        ]
    
    def search_products(self, query: str) -> List[Product]:
        """
        Search products by name or manufacturer
        
        Args:
            query: Search query
            
        Returns:
            List of matching products
        """
        query_lower = query.lower()
        return [
            p for p in self.products.values()
            if query_lower in p.name.lower() or query_lower in p.manufacturer.lower()
        ]
