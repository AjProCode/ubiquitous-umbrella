"""AI-powered medicine analyzer for interactions and recommendations"""

import os
from typing import List, Dict, Any, Optional, Set

from ..models.product import Medicine


class MedicineAnalyzer:
    """Analyze medicines for interactions, safety, and recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize medicine analyzer
        
        Args:
            api_key: OpenAI API key (uses env variable if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_ai = bool(self.api_key)
        
        # Common drug interaction database (simplified)
        self.known_interactions = {
            'warfarin': ['aspirin', 'ibuprofen', 'vitamin k'],
            'aspirin': ['warfarin', 'ibuprofen', 'naproxen'],
            'ibuprofen': ['aspirin', 'warfarin', 'naproxen'],
            'metformin': ['alcohol'],
            'statins': ['grapefruit', 'fibrates'],
        }
    
    def check_interactions(
        self,
        medicines: List[Medicine]
    ) -> Dict[str, Any]:
        """
        Check for drug interactions among medicines
        
        Args:
            medicines: List of medicines to analyze
            
        Returns:
            Dictionary with interaction analysis
        """
        if len(medicines) < 2:
            return {
                'has_interactions': False,
                'interactions': [],
                'message': 'Not enough medicines to check interactions'
            }
        
        interactions = []
        checked_pairs = set()
        
        for i, med1 in enumerate(medicines):
            for med2 in medicines[i+1:]:
                pair_key = tuple(sorted([med1.barcode, med2.barcode]))
                if pair_key in checked_pairs:
                    continue
                
                checked_pairs.add(pair_key)
                
                # Check for known interactions
                interaction = self._check_interaction_pair(med1, med2)
                if interaction:
                    interactions.append(interaction)
                
                # Check contraindications
                if med1.name.lower() in [c.lower() for c in med2.contraindications]:
                    interactions.append({
                        'medicine1': med1.name,
                        'medicine2': med2.name,
                        'severity': 'high',
                        'description': f'{med2.name} is contraindicated with {med1.name}',
                        'recommendation': 'Consult your healthcare provider immediately'
                    })
                
                # Check active ingredients
                for ingredient1 in med1.active_ingredients:
                    for ingredient2 in med2.active_ingredients:
                        if ingredient1.lower() == ingredient2.lower():
                            interactions.append({
                                'medicine1': med1.name,
                                'medicine2': med2.name,
                                'severity': 'medium',
                                'description': f'Both contain {ingredient1}. Risk of overdose.',
                                'recommendation': 'Avoid taking together. Consult healthcare provider.'
                            })
        
        return {
            'has_interactions': len(interactions) > 0,
            'interactions': interactions,
            'medicines_checked': [m.name for m in medicines],
            'message': f'Found {len(interactions)} potential interaction(s)' if interactions else 'No interactions found'
        }
    
    def _check_interaction_pair(
        self,
        med1: Medicine,
        med2: Medicine
    ) -> Optional[Dict[str, Any]]:
        """Check interaction between two medicines"""
        
        # Check known interactions
        for ingredient1 in med1.active_ingredients:
            ing1_lower = ingredient1.lower()
            if ing1_lower in self.known_interactions:
                for ingredient2 in med2.active_ingredients:
                    ing2_lower = ingredient2.lower()
                    if ing2_lower in self.known_interactions[ing1_lower]:
                        return {
                            'medicine1': med1.name,
                            'medicine2': med2.name,
                            'severity': 'high',
                            'description': f'Known interaction between {ingredient1} and {ingredient2}',
                            'recommendation': 'Consult your healthcare provider'
                        }
        
        # Check drug_interactions lists
        for interaction_name in med1.drug_interactions:
            if interaction_name.lower() in med2.name.lower() or \
               any(interaction_name.lower() in ing.lower() for ing in med2.active_ingredients):
                return {
                    'medicine1': med1.name,
                    'medicine2': med2.name,
                    'severity': 'medium',
                    'description': f'{med1.name} has known interaction with {interaction_name}',
                    'recommendation': 'Monitor for adverse effects. Consult healthcare provider.'
                }
        
        return None
    
    def analyze_medicine_safety(
        self,
        medicine: Medicine
    ) -> Dict[str, Any]:
        """
        Analyze medicine safety profile
        
        Args:
            medicine: Medicine to analyze
            
        Returns:
            Safety analysis dictionary
        """
        safety_score = 100
        warnings = []
        recommendations = []
        
        # Check expiry
        days_until_expiry = medicine.days_until_expiry()
        if days_until_expiry < 0:
            safety_score -= 100
            warnings.append('CRITICAL: Medicine has expired. Do not use.')
        elif days_until_expiry <= 7:
            safety_score -= 20
            warnings.append(f'WARNING: Medicine expires in {days_until_expiry} days')
            recommendations.append('Replace with fresh medicine soon')
        
        # Check if prescription required
        if medicine.prescription_required:
            warnings.append('Prescription medicine - use only as directed by healthcare provider')
        
        # Check storage
        if medicine.storage_instructions:
            recommendations.append(f'Storage: {medicine.storage_instructions}')
        
        # Check side effects
        if medicine.side_effects:
            recommendations.append(f'Be aware of {len(medicine.side_effects)} potential side effect(s)')
        
        # Check contraindications
        if medicine.contraindications:
            warnings.append(f'Has {len(medicine.contraindications)} contraindication(s)')
        
        # Check drug interactions
        if medicine.drug_interactions:
            warnings.append(f'Has {len(medicine.drug_interactions)} known drug interaction(s)')
        
        safety_level = 'critical' if safety_score <= 0 else \
                      'low' if safety_score < 50 else \
                      'medium' if safety_score < 80 else 'high'
        
        return {
            'medicine': medicine.name,
            'barcode': medicine.barcode,
            'safety_score': max(0, safety_score),
            'safety_level': safety_level,
            'warnings': warnings,
            'recommendations': recommendations,
            'days_until_expiry': days_until_expiry,
            'is_expired': medicine.is_expired(),
            'requires_prescription': medicine.prescription_required
        }
    
    def get_dosage_recommendations(
        self,
        medicine: Medicine,
        patient_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get dosage recommendations
        
        Args:
            medicine: Medicine to analyze
            patient_info: Optional patient information (age, weight, conditions)
            
        Returns:
            Dosage recommendations
        """
        recommendations = {
            'medicine': medicine.name,
            'standard_dosage': medicine.dosage or 'Not specified',
            'warnings': [],
            'special_instructions': []
        }
        
        if medicine.prescription_required:
            recommendations['warnings'].append(
                'This is a prescription medicine. Follow your doctor\'s instructions exactly.'
            )
        
        if medicine.storage_instructions:
            recommendations['special_instructions'].append(
                f'Storage: {medicine.storage_instructions}'
            )
        
        if patient_info:
            age = patient_info.get('age')
            if age and age < 18:
                recommendations['warnings'].append(
                    'Pediatric dosing may differ. Consult healthcare provider.'
                )
            elif age and age > 65:
                recommendations['warnings'].append(
                    'Geriatric patients may require dosage adjustment.'
                )
        
        # Add therapeutic class info
        if medicine.therapeutic_class:
            recommendations['therapeutic_class'] = medicine.therapeutic_class
        
        return recommendations
    
    def track_medicine_adherence(
        self,
        medicine: Medicine,
        taken_dates: List[str],
        prescribed_frequency: str = "daily"
    ) -> Dict[str, Any]:
        """
        Track medicine adherence
        
        Args:
            medicine: Medicine being tracked
            taken_dates: List of dates when medicine was taken (ISO format)
            prescribed_frequency: How often medicine should be taken
            
        Returns:
            Adherence tracking data
        """
        from datetime import datetime, timedelta
        
        if not taken_dates:
            return {
                'medicine': medicine.name,
                'adherence_rate': 0,
                'status': 'not_started',
                'message': 'No doses recorded'
            }
        
        # Calculate expected doses
        taken_date_objs = [datetime.fromisoformat(d).date() for d in taken_dates]
        first_date = min(taken_date_objs)
        last_date = max(taken_date_objs)
        days_span = (last_date - first_date).days + 1
        
        # Calculate adherence based on frequency
        if prescribed_frequency == "daily":
            expected_doses = days_span
        elif prescribed_frequency == "twice_daily":
            expected_doses = days_span * 2
        elif prescribed_frequency == "weekly":
            expected_doses = max(1, days_span // 7)
        else:
            expected_doses = len(taken_dates)  # Unknown frequency
        
        actual_doses = len(taken_dates)
        adherence_rate = min(100, (actual_doses / expected_doses * 100)) if expected_doses > 0 else 0
        
        # Determine status
        if adherence_rate >= 90:
            status = 'excellent'
        elif adherence_rate >= 75:
            status = 'good'
        elif adherence_rate >= 50:
            status = 'fair'
        else:
            status = 'poor'
        
        return {
            'medicine': medicine.name,
            'barcode': medicine.barcode,
            'adherence_rate': round(adherence_rate, 1),
            'status': status,
            'expected_doses': expected_doses,
            'actual_doses': actual_doses,
            'missed_doses': max(0, expected_doses - actual_doses),
            'tracking_period_days': days_span,
            'message': f'Adherence rate: {round(adherence_rate, 1)}% ({status})'
        }
    
    def get_medicine_reminders(
        self,
        medicines: List[Medicine],
        schedule: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        Generate medicine reminders based on schedule
        
        Args:
            medicines: List of medicines
            schedule: Dictionary mapping barcode to schedule (e.g., "8:00,20:00")
            
        Returns:
            List of reminder configurations
        """
        reminders = []
        
        for medicine in medicines:
            if medicine.barcode in schedule:
                times = schedule[medicine.barcode].split(',')
                for time_str in times:
                    reminders.append({
                        'medicine': medicine.name,
                        'barcode': medicine.barcode,
                        'time': time_str.strip(),
                        'dosage': medicine.dosage or 'As prescribed',
                        'special_instructions': medicine.storage_instructions or 'Follow prescription',
                        'days_until_expiry': medicine.days_until_expiry()
                    })
        
        return sorted(reminders, key=lambda x: x['time'])
