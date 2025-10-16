"""AI-powered counterfeit detection system"""

import os
from typing import Dict, Any, Optional, List
from datetime import date, datetime

from ..models.product import Product, Medicine
from ..models.manufacturing_log import ManufacturingLog, LogStatus


class CounterfeitDetector:
    """Detect counterfeit products using AI and manufacturing logs"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize counterfeit detector
        
        Args:
            api_key: OpenAI API key (uses env variable if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_ai = bool(self.api_key)
        self.suspicious_patterns = []
    
    def analyze_product(
        self,
        product: Product,
        manufacturing_log: Optional[ManufacturingLog] = None
    ) -> Dict[str, Any]:
        """
        Analyze product for counterfeit indicators
        
        Args:
            product: Product to analyze
            manufacturing_log: Optional manufacturing log for verification
            
        Returns:
            Analysis results dictionary
        """
        risk_score = 0
        risk_factors = []
        confidence_level = 'low'
        
        # Check if log exists
        if not manufacturing_log:
            risk_score += 30
            risk_factors.append('No manufacturing log found')
            confidence_level = 'medium'
        else:
            # Verify log status
            if manufacturing_log.status == LogStatus.COUNTERFEIT:
                risk_score += 100
                risk_factors.append('CRITICAL: Flagged as counterfeit in manufacturing log')
                confidence_level = 'high'
            elif manufacturing_log.status == LogStatus.SUSPICIOUS:
                risk_score += 50
                risk_factors.append('Flagged as suspicious in manufacturing log')
                confidence_level = 'high'
            elif manufacturing_log.status == LogStatus.RECALLED:
                risk_score += 80
                risk_factors.append('Product has been recalled')
                confidence_level = 'high'
            
            # Verify quality check
            if not manufacturing_log.quality_check_passed:
                risk_score += 40
                risk_factors.append('Failed quality checks')
            
            # Check for data mismatches
            if manufacturing_log.manufacturer.lower() != product.manufacturer.lower():
                risk_score += 50
                risk_factors.append('Manufacturer name mismatch')
                confidence_level = 'high'
            
            if manufacturing_log.manufacturing_date != product.manufacturing_date:
                risk_score += 30
                risk_factors.append('Manufacturing date mismatch')
            
            if manufacturing_log.expiry_date != product.expiry_date:
                risk_score += 30
                risk_factors.append('Expiry date mismatch')
        
        # Check product-specific indicators
        if isinstance(product, Medicine):
            medicine_risks = self._check_medicine_indicators(product)
            risk_score += medicine_risks['score']
            risk_factors.extend(medicine_risks['factors'])
        
        # Check for suspicious patterns
        pattern_risks = self._check_suspicious_patterns(product)
        risk_score += pattern_risks['score']
        risk_factors.extend(pattern_risks['factors'])
        
        # Determine overall assessment
        is_counterfeit = risk_score >= 80
        is_suspicious = risk_score >= 40
        
        assessment = 'genuine' if risk_score < 20 else \
                    'low_risk' if risk_score < 40 else \
                    'suspicious' if risk_score < 80 else \
                    'counterfeit'
        
        recommendation = self._get_recommendation(assessment, risk_factors)
        
        return {
            'product': product.name,
            'barcode': product.barcode,
            'batch_number': product.batch_number,
            'risk_score': min(100, risk_score),
            'assessment': assessment,
            'is_counterfeit': is_counterfeit,
            'is_suspicious': is_suspicious,
            'confidence_level': confidence_level,
            'risk_factors': risk_factors,
            'recommendation': recommendation,
            'checked_at': datetime.now().isoformat()
        }
    
    def _check_medicine_indicators(self, medicine: Medicine) -> Dict[str, Any]:
        """Check medicine-specific counterfeit indicators"""
        score = 0
        factors = []
        
        # Check for missing critical information
        if not medicine.active_ingredients:
            score += 20
            factors.append('Missing active ingredient information')
        
        if medicine.prescription_required and not medicine.dosage:
            score += 15
            factors.append('Prescription medicine missing dosage information')
        
        if not medicine.batch_number or len(medicine.batch_number) < 4:
            score += 25
            factors.append('Invalid or missing batch number')
        
        # Check for suspicious pricing or naming (would require additional data)
        # This is a placeholder for more sophisticated checks
        
        return {'score': score, 'factors': factors}
    
    def _check_suspicious_patterns(self, product: Product) -> Dict[str, Any]:
        """Check for suspicious patterns in product data"""
        score = 0
        factors = []
        
        # Check date validity
        today = date.today()
        
        if product.manufacturing_date > today:
            score += 50
            factors.append('Manufacturing date is in the future')
        
        if product.expiry_date <= product.manufacturing_date:
            score += 60
            factors.append('Expiry date is before manufacturing date')
        
        # Check manufacturing-expiry date span
        date_span = (product.expiry_date - product.manufacturing_date).days
        
        if isinstance(product, Medicine):
            # Medicines typically have 1-5 years shelf life
            if date_span < 180:  # Less than 6 months
                score += 15
                factors.append('Unusually short shelf life for medicine')
            elif date_span > 3650:  # More than 10 years
                score += 20
                factors.append('Unusually long shelf life for medicine')
        
        # Check barcode format (basic validation)
        if not product.barcode or len(product.barcode) < 8:
            score += 30
            factors.append('Invalid barcode format')
        
        # Check manufacturer name
        if not product.manufacturer or len(product.manufacturer) < 2:
            score += 25
            factors.append('Invalid or missing manufacturer name')
        
        return {'score': score, 'factors': factors}
    
    def _get_recommendation(
        self,
        assessment: str,
        risk_factors: List[str]
    ) -> str:
        """Get recommendation based on assessment"""
        
        if assessment == 'counterfeit':
            return (
                "⚠️ CRITICAL WARNING: This product appears to be counterfeit. "
                "DO NOT USE. Report to authorities and dispose safely. "
                "Contact the manufacturer if you believe this is an error."
            )
        elif assessment == 'suspicious':
            return (
                "⚠️ WARNING: This product shows suspicious indicators. "
                "Exercise extreme caution. Verify with manufacturer before use. "
                "Consider getting it tested or report to authorities."
            )
        elif assessment == 'low_risk':
            return (
                "ℹ️ NOTICE: Some minor concerns detected. "
                "Verify product authenticity with manufacturer if possible. "
                "Ensure you purchased from authorized retailers."
            )
        else:
            return (
                "✓ Product appears genuine based on available data. "
                "Continue following standard safety practices."
            )
    
    def batch_analyze(
        self,
        products: List[Product],
        manufacturing_logs: Dict[str, ManufacturingLog]
    ) -> Dict[str, Any]:
        """
        Analyze multiple products for counterfeits
        
        Args:
            products: List of products to analyze
            manufacturing_logs: Dictionary of manufacturing logs (keyed by barcode_batchnumber)
            
        Returns:
            Batch analysis results
        """
        results = []
        counterfeit_count = 0
        suspicious_count = 0
        
        for product in products:
            key = f"{product.barcode}_{product.batch_number}"
            log = manufacturing_logs.get(key)
            
            analysis = self.analyze_product(product, log)
            results.append(analysis)
            
            if analysis['is_counterfeit']:
                counterfeit_count += 1
            elif analysis['is_suspicious']:
                suspicious_count += 1
        
        return {
            'total_products': len(products),
            'counterfeit_count': counterfeit_count,
            'suspicious_count': suspicious_count,
            'genuine_count': len(products) - counterfeit_count - suspicious_count,
            'results': results,
            'high_risk_products': [
                r for r in results if r['assessment'] in ['counterfeit', 'suspicious']
            ]
        }
    
    def report_counterfeit(
        self,
        product: Product,
        evidence: str,
        reporter_info: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Report a counterfeit product
        
        Args:
            product: Product to report
            evidence: Evidence description
            reporter_info: Optional reporter information
            
        Returns:
            Report details
        """
        report = {
            'report_id': f"CF-{datetime.now().strftime('%Y%m%d%H%M%S')}-{product.barcode}",
            'product_name': product.name,
            'barcode': product.barcode,
            'batch_number': product.batch_number,
            'manufacturer': product.manufacturer,
            'evidence': evidence,
            'reported_at': datetime.now().isoformat(),
            'status': 'pending_investigation'
        }
        
        if reporter_info:
            report['reporter'] = reporter_info
        
        # In a production system, this would send to authorities/manufacturer
        print(f"Counterfeit report filed: {report['report_id']}")
        
        return report
    
    def get_verification_checklist(self, product: Product) -> List[Dict[str, Any]]:
        """
        Get verification checklist for manual inspection
        
        Args:
            product: Product to verify
            
        Returns:
            List of verification items
        """
        checklist = [
            {
                'item': 'Barcode scan',
                'description': 'Verify barcode scans correctly and matches printed number',
                'critical': True
            },
            {
                'item': 'Packaging quality',
                'description': 'Check for misspellings, poor print quality, or damaged packaging',
                'critical': True
            },
            {
                'item': 'Batch number',
                'description': f'Verify batch number {product.batch_number} is clearly printed and legitimate',
                'critical': True
            },
            {
                'item': 'Expiry date',
                'description': f'Confirm expiry date {product.expiry_date.isoformat()} is properly printed',
                'critical': True
            },
            {
                'item': 'Manufacturer information',
                'description': f'Verify manufacturer {product.manufacturer} details and contact information',
                'critical': True
            },
            {
                'item': 'Seal/tamper evidence',
                'description': 'Check that product has proper seals and shows no signs of tampering',
                'critical': True
            }
        ]
        
        if isinstance(product, Medicine):
            checklist.extend([
                {
                    'item': 'Prescription label',
                    'description': 'Verify prescription information if applicable',
                    'critical': True
                },
                {
                    'item': 'Active ingredients',
                    'description': 'Check that active ingredients match documentation',
                    'critical': True
                },
                {
                    'item': 'Dosage information',
                    'description': 'Verify dosage information is clear and correct',
                    'critical': True
                }
            ])
        
        return checklist
