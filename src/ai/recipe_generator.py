"""AI-powered recipe generator based on expiring items"""

import os
from typing import List, Dict, Any, Optional
from datetime import date

from ..models.product import PerishableItem


class RecipeGenerator:
    """Generate recipes using AI based on available items and expiry dates"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize recipe generator
        
        Args:
            api_key: OpenAI API key (uses env variable if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_ai = bool(self.api_key)
    
    def generate_recipe(
        self,
        items: List[PerishableItem],
        dietary_preferences: Optional[List[str]] = None,
        cuisine_type: Optional[str] = None,
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Generate recipe using available items
        
        Args:
            items: List of perishable items to use
            dietary_preferences: List of dietary preferences (e.g., vegetarian, vegan)
            cuisine_type: Type of cuisine (e.g., Italian, Asian)
            difficulty: Recipe difficulty (easy, medium, hard)
            
        Returns:
            Dictionary with recipe details
        """
        if not items:
            return {
                'success': False,
                'error': 'No items provided'
            }
        
        # Sort items by expiry urgency
        items_sorted = sorted(items, key=lambda x: x.days_until_expiry())
        
        if self.use_ai:
            return self._generate_with_ai(items_sorted, dietary_preferences, cuisine_type, difficulty)
        else:
            return self._generate_fallback_recipe(items_sorted, dietary_preferences, cuisine_type, difficulty)
    
    def _generate_with_ai(
        self,
        items: List[PerishableItem],
        dietary_preferences: Optional[List[str]],
        cuisine_type: Optional[str],
        difficulty: str
    ) -> Dict[str, Any]:
        """Generate recipe using OpenAI API"""
        try:
            # Note: Actual OpenAI integration would require the openai package
            # This is a placeholder implementation
            
            ingredients = [item.name for item in items]
            expiring_items = [
                item.name for item in items 
                if 0 <= item.days_until_expiry() <= 3
            ]
            
            prompt = self._build_prompt(
                ingredients, expiring_items, dietary_preferences, cuisine_type, difficulty
            )
            
            # Placeholder for AI response
            # In production, you would call OpenAI API here:
            # response = openai.ChatCompletion.create(...)
            
            return self._generate_fallback_recipe(items, dietary_preferences, cuisine_type, difficulty)
            
        except Exception as e:
            print(f"Error generating recipe with AI: {e}")
            return self._generate_fallback_recipe(items, dietary_preferences, cuisine_type, difficulty)
    
    def _build_prompt(
        self,
        ingredients: List[str],
        expiring_items: List[str],
        dietary_preferences: Optional[List[str]],
        cuisine_type: Optional[str],
        difficulty: str
    ) -> str:
        """Build prompt for AI recipe generation"""
        prompt = f"Create a {difficulty} difficulty recipe using these ingredients: {', '.join(ingredients)}.\n"
        
        if expiring_items:
            prompt += f"Priority ingredients (expiring soon): {', '.join(expiring_items)}.\n"
        
        if dietary_preferences:
            prompt += f"Dietary requirements: {', '.join(dietary_preferences)}.\n"
        
        if cuisine_type:
            prompt += f"Cuisine type: {cuisine_type}.\n"
        
        prompt += "Provide the recipe with title, description, ingredients with measurements, step-by-step instructions, cooking time, and servings."
        
        return prompt
    
    def _generate_fallback_recipe(
        self,
        items: List[PerishableItem],
        dietary_preferences: Optional[List[str]],
        cuisine_type: Optional[str],
        difficulty: str
    ) -> Dict[str, Any]:
        """Generate simple fallback recipe without AI"""
        
        # Categorize items
        vegetables = []
        proteins = []
        grains = []
        other = []
        
        for item in items:
            name_lower = item.name.lower()
            if any(veg in name_lower for veg in ['tomato', 'lettuce', 'carrot', 'pepper', 'onion', 'spinach', 'broccoli']):
                vegetables.append(item.name)
            elif any(prot in name_lower for prot in ['chicken', 'beef', 'pork', 'fish', 'tofu', 'egg']):
                proteins.append(item.name)
            elif any(grain in name_lower for grain in ['rice', 'pasta', 'bread', 'quinoa']):
                grains.append(item.name)
            else:
                other.append(item.name)
        
        # Generate simple recipe based on available items
        recipes = []
        
        if vegetables and proteins:
            recipes.append({
                'title': 'Stir-Fry with Fresh Ingredients',
                'description': 'A quick and healthy stir-fry using your expiring ingredients',
                'cuisine': cuisine_type or 'Asian',
                'difficulty': difficulty,
                'prep_time': '15 minutes',
                'cook_time': '15 minutes',
                'servings': 4,
                'ingredients': [
                    f"{item} (as available)" for item in vegetables + proteins
                ] + ['2 tbsp cooking oil', '2 tbsp soy sauce', 'Salt and pepper to taste'],
                'instructions': [
                    'Prepare and chop all ingredients',
                    'Heat oil in a large pan or wok over high heat',
                    'Add protein and cook until done',
                    'Add vegetables and stir-fry for 5-7 minutes',
                    'Season with soy sauce, salt, and pepper',
                    'Serve hot'
                ],
                'priority_items': [item.name for item in items if 0 <= item.days_until_expiry() <= 3],
                'dietary_info': dietary_preferences or []
            })
        
        if vegetables:
            recipes.append({
                'title': 'Fresh Vegetable Soup',
                'description': 'Nutritious soup using vegetables that need to be used soon',
                'cuisine': cuisine_type or 'Universal',
                'difficulty': difficulty,
                'prep_time': '10 minutes',
                'cook_time': '25 minutes',
                'servings': 4,
                'ingredients': [
                    f"{veg} (chopped)" for veg in vegetables
                ] + ['4 cups vegetable broth', 'Herbs and spices to taste'],
                'instructions': [
                    'Chop all vegetables',
                    'Bring broth to boil in a large pot',
                    'Add vegetables and reduce to simmer',
                    'Cook for 20-25 minutes until vegetables are tender',
                    'Season to taste and serve'
                ],
                'priority_items': [item.name for item in items if 0 <= item.days_until_expiry() <= 3],
                'dietary_info': dietary_preferences or []
            })
        
        if not recipes:
            # Generic recipe template
            recipes.append({
                'title': 'Creative Meal with Available Ingredients',
                'description': 'Use your creativity with these ingredients',
                'cuisine': cuisine_type or 'Fusion',
                'difficulty': difficulty,
                'prep_time': '20 minutes',
                'cook_time': '30 minutes',
                'servings': 4,
                'ingredients': [item.name for item in items],
                'instructions': [
                    'Prepare and season ingredients',
                    'Cook according to ingredient requirements',
                    'Combine ingredients creatively',
                    'Adjust seasoning and serve'
                ],
                'priority_items': [item.name for item in items if 0 <= item.days_until_expiry() <= 3],
                'dietary_info': dietary_preferences or []
            })
        
        return {
            'success': True,
            'recipes': recipes,
            'items_used': [item.name for item in items],
            'expiring_soon': [item.name for item in items if 0 <= item.days_until_expiry() <= 3]
        }
    
    def suggest_recipes_for_expiring_items(
        self,
        items: List[PerishableItem],
        max_recipes: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Suggest multiple recipes for expiring items
        
        Args:
            items: List of perishable items
            max_recipes: Maximum number of recipes to suggest
            
        Returns:
            List of recipe suggestions
        """
        if not items:
            return []
        
        # Filter items expiring within 7 days
        expiring_items = [item for item in items if 0 <= item.days_until_expiry() <= 7]
        
        if not expiring_items:
            return []
        
        suggestions = []
        
        # Generate recipes with different combinations
        result = self.generate_recipe(expiring_items, difficulty="easy")
        if result.get('success') and result.get('recipes'):
            suggestions.extend(result['recipes'][:max_recipes])
        
        return suggestions
    
    def get_usage_priority(self, items: List[PerishableItem]) -> List[Dict[str, Any]]:
        """
        Get prioritized list of items for usage
        
        Args:
            items: List of perishable items
            
        Returns:
            Prioritized list with recommendations
        """
        prioritized = []
        
        for item in sorted(items, key=lambda x: x.days_until_expiry()):
            days = item.days_until_expiry()
            
            if days < 0:
                priority = "expired"
                action = "Discard immediately"
            elif days == 0:
                priority = "critical"
                action = "Use today"
            elif days <= 2:
                priority = "urgent"
                action = "Use within 2 days"
            elif days <= 5:
                priority = "high"
                action = "Use this week"
            else:
                priority = "normal"
                action = "Plan usage"
            
            prioritized.append({
                'item': item.name,
                'barcode': item.barcode,
                'days_until_expiry': days,
                'expiry_date': item.expiry_date.isoformat(),
                'priority': priority,
                'recommended_action': action
            })
        
        return prioritized
