"""Product verification service using manufacturing logs"""

import csv
import json
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pathlib import Path

from ..models.manufacturing_log import ManufacturingLog, LogStatus
from ..models.product import Product


class VerificationService:
    """Service for verifying products against manufacturing logs"""
    
    def __init__(self, log_path: str = "./data/manufacturing_logs"):
        """
        Initialize verification service
        
        Args:
            log_path: Path to manufacturing logs directory
        """
        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.logs: Dict[str, ManufacturingLog] = {}
        self._load_logs()
    
    def _load_logs(self):
        """Load manufacturing logs from storage"""
        # Load CSV logs
        for csv_file in self.log_path.glob("*.csv"):
            self._load_csv_log(csv_file)
        
        # Load JSON logs
        for json_file in self.log_path.glob("*.json"):
            self._load_json_log(json_file)
    
    def _load_csv_log(self, file_path: Path):
        """Load manufacturing log from CSV file"""
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    log = self._dict_to_log(row)
                    if log:
                        key = f"{log.barcode}_{log.batch_number}"
                        self.logs[key] = log
        except Exception as e:
            print(f"Error loading CSV log {file_path}: {e}")
    
    def _load_json_log(self, file_path: Path):
        """Load manufacturing log from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for entry in data if isinstance(data, list) else [data]:
                    log = self._dict_to_log(entry)
                    if log:
                        key = f"{log.barcode}_{log.batch_number}"
                        self.logs[key] = log
        except Exception as e:
            print(f"Error loading JSON log {file_path}: {e}")
    
    def _dict_to_log(self, data: Dict[str, Any]) -> Optional[ManufacturingLog]:
        """Convert dictionary to manufacturing log"""
        try:
            return ManufacturingLog(
                batch_number=data['batch_number'],
                barcode=data['barcode'],
                product_name=data['product_name'],
                manufacturer=data['manufacturer'],
                manufacturing_date=date.fromisoformat(data['manufacturing_date']),
                expiry_date=date.fromisoformat(data['expiry_date']),
                facility_id=data['facility_id'],
                quality_check_passed=bool(data.get('quality_check_passed', True)),
                status=LogStatus(data.get('status', 'valid')),
                certification_number=data.get('certification_number'),
                inspected_by=data.get('inspected_by'),
                inspection_date=date.fromisoformat(data['inspection_date']) 
                    if data.get('inspection_date') else None,
                notes=data.get('notes')
            )
        except Exception as e:
            print(f"Error converting dict to log: {e}")
            return None
    
    def verify_product(self, product: Product) -> tuple[bool, str]:
        """
        Verify product against manufacturing logs
        
        Args:
            product: Product to verify
            
        Returns:
            Tuple of (is_verified, message)
        """
        key = f"{product.barcode}_{product.batch_number}"
        
        if key not in self.logs:
            return False, "Product not found in manufacturing logs"
        
        log = self.logs[key]
        
        # Check if log is valid
        if not log.is_valid():
            if log.status == LogStatus.RECALLED:
                return False, "Product has been recalled by manufacturer"
            elif log.status == LogStatus.COUNTERFEIT:
                return False, "Product flagged as counterfeit"
            elif log.status == LogStatus.SUSPICIOUS:
                return False, "Product flagged as suspicious"
            elif not log.quality_check_passed:
                return False, "Product failed quality checks"
        
        # Verify details match
        if log.manufacturer.lower() != product.manufacturer.lower():
            return False, "Manufacturer mismatch"
        
        if log.manufacturing_date != product.manufacturing_date:
            return False, "Manufacturing date mismatch"
        
        if log.expiry_date != product.expiry_date:
            return False, "Expiry date mismatch"
        
        return True, "Product verified successfully"
    
    def add_log(self, log: ManufacturingLog) -> bool:
        """
        Add manufacturing log
        
        Args:
            log: Manufacturing log to add
            
        Returns:
            True if successful
        """
        try:
            key = f"{log.barcode}_{log.batch_number}"
            self.logs[key] = log
            
            # Save to JSON file
            log_file = self.log_path / "manufacturing_logs.json"
            logs_data = [log.to_dict() for log in self.logs.values()]
            
            with open(log_file, 'w') as f:
                json.dump(logs_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error adding log: {e}")
            return False
    
    def get_log(self, barcode: str, batch_number: str) -> Optional[ManufacturingLog]:
        """
        Get manufacturing log
        
        Args:
            barcode: Product barcode
            batch_number: Batch number
            
        Returns:
            Manufacturing log or None
        """
        key = f"{barcode}_{batch_number}"
        return self.logs.get(key)
    
    def check_for_recalls(self, barcode: str) -> List[ManufacturingLog]:
        """
        Check if product has any recalls
        
        Args:
            barcode: Product barcode
            
        Returns:
            List of recalled logs for the product
        """
        return [
            log for log in self.logs.values()
            if log.barcode == barcode and log.status == LogStatus.RECALLED
        ]
    
    def get_counterfeit_alerts(self) -> List[ManufacturingLog]:
        """
        Get all counterfeit alerts
        
        Returns:
            List of counterfeit logs
        """
        return [
            log for log in self.logs.values()
            if log.status == LogStatus.COUNTERFEIT
        ]
    
    def flag_as_counterfeit(self, barcode: str, batch_number: str, notes: str = "") -> bool:
        """
        Flag product as counterfeit
        
        Args:
            barcode: Product barcode
            batch_number: Batch number
            notes: Additional notes
            
        Returns:
            True if successful
        """
        key = f"{barcode}_{batch_number}"
        if key in self.logs:
            self.logs[key].status = LogStatus.COUNTERFEIT
            self.logs[key].notes = notes
            return True
        return False
