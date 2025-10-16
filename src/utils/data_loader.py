"""Data loading utilities"""

import csv
import json
from typing import List, Dict, Any
from pathlib import Path
from datetime import date


class DataLoader:
    """Utility for loading sample data"""
    
    @staticmethod
    def create_sample_manufacturing_logs(output_path: str = "./data/manufacturing_logs"):
        """Create sample manufacturing logs"""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        sample_logs = [
            {
                'batch_number': 'MED2024001',
                'barcode': '8901234567890',
                'product_name': 'Paracetamol 500mg',
                'manufacturer': 'PharmaCorp',
                'manufacturing_date': '2024-01-15',
                'expiry_date': '2026-01-15',
                'facility_id': 'FAC-001',
                'quality_check_passed': True,
                'status': 'valid',
                'certification_number': 'CERT-2024-001',
                'inspected_by': 'Inspector A',
                'inspection_date': '2024-01-20'
            },
            {
                'batch_number': 'FOOD2024001',
                'barcode': '8901234567891',
                'product_name': 'Organic Milk',
                'manufacturer': 'DairyFresh',
                'manufacturing_date': '2024-10-10',
                'expiry_date': '2024-10-25',
                'facility_id': 'FAC-002',
                'quality_check_passed': True,
                'status': 'valid',
                'certification_number': 'CERT-2024-002',
                'inspected_by': 'Inspector B',
                'inspection_date': '2024-10-11'
            },
            {
                'batch_number': 'MED2024002',
                'barcode': '8901234567892',
                'product_name': 'Ibuprofen 400mg',
                'manufacturer': 'MediCare Ltd',
                'manufacturing_date': '2024-03-01',
                'expiry_date': '2026-03-01',
                'facility_id': 'FAC-003',
                'quality_check_passed': True,
                'status': 'valid',
                'certification_number': 'CERT-2024-003',
                'inspected_by': 'Inspector C',
                'inspection_date': '2024-03-05'
            }
        ]
        
        # Save as JSON
        json_file = output_dir / 'sample_logs.json'
        with open(json_file, 'w') as f:
            json.dump(sample_logs, f, indent=2)
        
        # Save as CSV
        csv_file = output_dir / 'sample_logs.csv'
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sample_logs[0].keys())
            writer.writeheader()
            writer.writerows(sample_logs)
        
        print(f"Sample manufacturing logs created in {output_dir}")
        return sample_logs
    
    @staticmethod
    def create_sample_products(output_path: str = "./data/products"):
        """Create sample products"""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        sample_products = [
            {
                'barcode': '8901234567890',
                'name': 'Paracetamol 500mg',
                'manufacturer': 'PharmaCorp',
                'category': 'medicine',
                'manufacturing_date': '2024-01-15',
                'expiry_date': '2026-01-15',
                'batch_number': 'MED2024001',
                'description': 'Pain reliever and fever reducer',
                'is_verified': True,
                'is_counterfeit': False,
                'medicine_type': 'tablet',
                'dosage': '500mg, 1-2 tablets every 4-6 hours',
                'active_ingredients': ['Paracetamol'],
                'side_effects': ['Nausea', 'Rash', 'Liver damage (overdose)'],
                'contraindications': ['Liver disease', 'Alcohol dependence'],
                'drug_interactions': ['Warfarin', 'Alcohol'],
                'storage_instructions': 'Store below 25°C in a dry place',
                'prescription_required': False,
                'generic_name': 'Acetaminophen',
                'therapeutic_class': 'Analgesic/Antipyretic'
            },
            {
                'barcode': '8901234567891',
                'name': 'Organic Milk',
                'manufacturer': 'DairyFresh',
                'category': 'beverage',
                'manufacturing_date': '2024-10-10',
                'expiry_date': '2024-10-25',
                'batch_number': 'FOOD2024001',
                'description': 'Fresh organic whole milk',
                'is_verified': True,
                'is_counterfeit': False,
                'storage_temperature': '2-4°C',
                'nutritional_info': {
                    'calories': '60 per 100ml',
                    'protein': '3.2g',
                    'fat': '3.5g',
                    'carbohydrates': '4.8g'
                },
                'allergens': ['Milk', 'Lactose'],
                'ingredients': ['Organic Whole Milk'],
                'serving_size': '250ml',
                'storage_instructions': 'Keep refrigerated',
                'opened_shelf_life_days': 3
            },
            {
                'barcode': '8901234567892',
                'name': 'Ibuprofen 400mg',
                'manufacturer': 'MediCare Ltd',
                'category': 'medicine',
                'manufacturing_date': '2024-03-01',
                'expiry_date': '2026-03-01',
                'batch_number': 'MED2024002',
                'description': 'Anti-inflammatory and pain reliever',
                'is_verified': True,
                'is_counterfeit': False,
                'medicine_type': 'tablet',
                'dosage': '400mg, 1 tablet every 6-8 hours',
                'active_ingredients': ['Ibuprofen'],
                'side_effects': ['Stomach upset', 'Dizziness', 'Headache'],
                'contraindications': ['Stomach ulcers', 'Aspirin allergy', 'Severe heart failure'],
                'drug_interactions': ['Aspirin', 'Warfarin', 'Blood pressure medications'],
                'storage_instructions': 'Store below 25°C',
                'prescription_required': False,
                'generic_name': 'Ibuprofen',
                'therapeutic_class': 'NSAID'
            }
        ]
        
        # Save products
        products_file = output_dir / 'products.json'
        with open(products_file, 'w') as f:
            json.dump(sample_products, f, indent=2)
        
        print(f"Sample products created in {output_dir}")
        return sample_products
