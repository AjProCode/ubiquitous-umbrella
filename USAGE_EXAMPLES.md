# MediScan Usage Examples

This document provides practical examples of using MediScan for various scenarios.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Scanning Products](#scanning-products)
3. [Managing Medicines](#managing-medicines)
4. [Tracking Expiry Dates](#tracking-expiry-dates)
5. [Recipe Generation](#recipe-generation)
6. [Counterfeit Detection](#counterfeit-detection)
7. [Advanced Usage](#advanced-usage)

## Getting Started

### First Time Setup

```bash
# Install the application
pip install -r requirements.txt

# Initialize with sample data
python app.py init

# View the dashboard
python app.py dashboard
```

Expected output:
```
═══════════════════════════════════════════════════
        MediScan - Product Management Dashboard      
═══════════════════════════════════════════════════

Total Products: 3
  • Medicines: 2
  • Perishable Items: 1

Expiry Status:
  • Expired: 0
  • Critical (≤1 day): 0
  • High Priority (2-3 days): 0
  • Medium Priority (4-7 days): 1
```

## Scanning Products

### Example 1: Scan a Medicine

```bash
python app.py scan --barcode 8901234567890
```

This scans Paracetamol 500mg and displays:
- Product details (name, manufacturer, batch)
- Verification status
- Counterfeit analysis
- Expiry information
- Medicine-specific details (dosage, active ingredients)

### Example 2: Scan a Perishable Item

```bash
python app.py scan --barcode 8901234567891
```

Scans Organic Milk and shows:
- Product information
- Storage requirements
- Allergen warnings
- Nutritional information
- Days until expiry

## Managing Medicines

### Example 3: Check Drug Interactions

```bash
python app.py interactions
```

This checks all medicines in your inventory for:
- Drug-drug interactions
- Known contraindications
- Severity levels (high, medium, low)

Sample output:
```
⚠️ Found 1 potential interaction(s):

┌─────────────────────────────────────────────┐
│ Paracetamol 500mg ↔ Ibuprofen 400mg        │
│ Severity: MEDIUM                            │
│ Description: Both are pain relievers        │
│ Recommendation: Monitor usage and consult   │
│ healthcare provider if taking together      │
└─────────────────────────────────────────────┘
```

### Example 4: Medicine Safety Analysis

```python
from src.services.product_service import ProductService
from src.ai.medicine_analyzer import MedicineAnalyzer

# Get a medicine
product_service = ProductService()
medicine = product_service.get_product('8901234567890')

# Analyze safety
analyzer = MedicineAnalyzer()
safety = analyzer.analyze_medicine_safety(medicine)

print(f"Safety Score: {safety['safety_score']}/100")
print(f"Safety Level: {safety['safety_level']}")
print(f"Warnings: {safety['warnings']}")
```

## Tracking Expiry Dates

### Example 5: List Products Expiring Soon

```bash
# Products expiring in next 7 days
python app.py expiring

# Products expiring in next 30 days
python app.py expiring --days 30
```

Output shows a table with:
- Product name
- Category
- Days until expiry
- Urgency level

### Example 6: Get Expiry Summary

```python
from src.services.product_service import ProductService
from src.services.expiry_tracker import ExpiryTracker

product_service = ProductService()
expiry_tracker = ExpiryTracker()

products = product_service.list_products()
summary = expiry_tracker.get_expiry_summary(products)

print(f"Total Products: {summary['total_products']}")
print(f"Expired: {summary['expired_count']}")
print(f"Critical: {summary['critical_count']}")
```

### Example 7: Categorize by Expiry Urgency

```python
from src.services.expiry_tracker import ExpiryTracker

expiry_tracker = ExpiryTracker()
categories = expiry_tracker.categorize_by_expiry(products)

print(f"Expired: {len(categories['expired'])}")
print(f"Critical (≤1 day): {len(categories['critical'])}")
print(f"High (2-3 days): {len(categories['high'])}")
print(f"Medium (4-7 days): {len(categories['medium'])}")
print(f"Low (8-30 days): {len(categories['low'])}")
```

## Recipe Generation

### Example 8: Generate Recipes for Expiring Items

```bash
python app.py recipes
```

This generates recipes using ingredients that are expiring soon.

Sample output:
```
┌──────────────────────────────────────────────┐
│ Stir-Fry with Fresh Ingredients              │
│ A quick and healthy stir-fry using your      │
│ expiring ingredients                          │
│                                               │
│ Prep Time: 15 minutes                        │
│ Cook Time: 15 minutes                        │
│ Servings: 4                                  │
│                                               │
│ Priority Ingredients: Organic Milk           │
└──────────────────────────────────────────────┘
```

### Example 9: Get Usage Priority

```python
from src.ai.recipe_generator import RecipeGenerator

recipe_gen = RecipeGenerator()
perishables = product_service.get_perishable_items()

priority_list = recipe_gen.get_usage_priority(perishables)

for item in priority_list:
    print(f"{item['item']}: {item['priority']} - {item['recommended_action']}")
```

Output:
```
Organic Milk: urgent - Use within 2 days
Fresh Vegetables: high - Use this week
Canned Goods: normal - Plan usage
```

## Counterfeit Detection

### Example 10: Analyze Product for Counterfeits

```python
from src.ai.counterfeit_detector import CounterfeitDetector
from src.services.verification_service import VerificationService

detector = CounterfeitDetector()
verification_service = VerificationService()

# Get product and its log
product = product_service.get_product('8901234567890')
log = verification_service.get_log(product.barcode, product.batch_number)

# Analyze
analysis = detector.analyze_product(product, log)

print(f"Risk Score: {analysis['risk_score']}/100")
print(f"Assessment: {analysis['assessment']}")
print(f"Is Counterfeit: {analysis['is_counterfeit']}")
print(f"Recommendation: {analysis['recommendation']}")
```

### Example 11: Batch Counterfeit Analysis

```python
detector = CounterfeitDetector()
products = product_service.list_products()

# Get all logs
verification_service = VerificationService()
logs = {}
for p in products:
    key = f"{p.barcode}_{p.batch_number}"
    log = verification_service.get_log(p.barcode, p.batch_number)
    if log:
        logs[key] = log

# Analyze all products
batch_results = detector.batch_analyze(products, logs)

print(f"Total Products: {batch_results['total_products']}")
print(f"Counterfeit: {batch_results['counterfeit_count']}")
print(f"Suspicious: {batch_results['suspicious_count']}")
print(f"Genuine: {batch_results['genuine_count']}")
```

### Example 12: Get Verification Checklist

```python
checklist = detector.get_verification_checklist(product)

for item in checklist:
    critical = "⚠️" if item['critical'] else "ℹ️"
    print(f"{critical} {item['item']}")
    print(f"   {item['description']}")
```

## Advanced Usage

### Example 13: Create Custom Product

```python
from datetime import date, timedelta
from src.models.product import Medicine, MedicineType

# Create a new medicine
medicine = Medicine(
    barcode='1234567890123',
    name='Custom Medicine',
    manufacturer='PharmaCo',
    manufacturing_date=date.today() - timedelta(days=30),
    expiry_date=date.today() + timedelta(days=700),
    batch_number='BATCH001',
    medicine_type=MedicineType.TABLET,
    dosage='250mg twice daily',
    active_ingredients=['Custom Ingredient'],
    prescription_required=True
)

# Add to database
product_service.add_product(medicine)
```

### Example 14: Track Medicine Adherence

```python
from src.ai.medicine_analyzer import MedicineAnalyzer

analyzer = MedicineAnalyzer()

# Track when medicine was taken
taken_dates = [
    '2024-10-01',
    '2024-10-02',
    '2024-10-03',
    '2024-10-05',
    '2024-10-07'
]

adherence = analyzer.track_medicine_adherence(
    medicine,
    taken_dates,
    prescribed_frequency='daily'
)

print(f"Adherence Rate: {adherence['adherence_rate']}%")
print(f"Status: {adherence['status']}")
print(f"Missed Doses: {adherence['missed_doses']}")
```

### Example 15: Set Up Medicine Reminders

```python
analyzer = MedicineAnalyzer()
medicines = product_service.get_medicines()

# Set up schedule (time in 24h format)
schedule = {
    '8901234567890': '08:00,20:00',  # Morning and evening
    '8901234567892': '09:00,21:00'   # Different times
}

reminders = analyzer.get_medicine_reminders(medicines, schedule)

for reminder in reminders:
    print(f"{reminder['time']}: Take {reminder['medicine']}")
    print(f"  Dosage: {reminder['dosage']}")
    print(f"  Expires in: {reminder['days_until_expiry']} days")
```

### Example 16: Custom Notification

```python
from src.services.notification_service import NotificationService
from src.models.notification import NotificationType, NotificationPriority

notification_service = NotificationService()

# Create custom expiry warning
notification = notification_service.create_expiry_warning(
    product=product,
    days_until_expiry=3,
    schedule_days_before=0
)

# Create counterfeit alert
alert = notification_service.create_counterfeit_alert(
    product=suspicious_product,
    details="Product failed verification checks"
)

# Get all unread notifications
unread = notification_service.get_unread_notifications()
for notif in unread:
    print(f"[{notif.priority.value}] {notif.title}")
    print(f"  {notif.message}")
```

### Example 17: Import Manufacturing Logs

```python
from src.models.manufacturing_log import ManufacturingLog, LogStatus
from datetime import date

# Create a new log entry
log = ManufacturingLog(
    batch_number='BATCH002',
    barcode='1234567890123',
    product_name='Custom Medicine',
    manufacturer='PharmaCo',
    manufacturing_date=date(2024, 1, 1),
    expiry_date=date(2026, 1, 1),
    facility_id='FAC-001',
    quality_check_passed=True,
    status=LogStatus.VALID,
    certification_number='CERT-2024-001'
)

# Add to verification service
verification_service.add_log(log)
```

### Example 18: Search Products

```python
# Search by name or manufacturer
results = product_service.search_products('paracetamol')

for product in results:
    print(f"{product.name} - {product.manufacturer}")
    print(f"  Expires: {product.expiry_date}")
```

### Example 19: Filter Products by Category

```python
from src.models.product import ProductCategory

# Get only medicines
medicines = product_service.list_products(
    category=ProductCategory.MEDICINE,
    verified=True
)

# Get expired products
expired = product_service.list_products(
    expired=True
)

# Get unverified products
unverified = product_service.list_products(
    verified=False
)
```

### Example 20: Generate Barcode Image

```python
from src.services.barcode_scanner import BarcodeScanner

scanner = BarcodeScanner()

# Generate barcode
barcode_image = scanner.generate_barcode(
    barcode_data='1234567890123',
    barcode_type='EAN13',
    output_path='./barcode.png'
)

print("Barcode image saved to barcode.png")
```

## Integration Examples

### Example 21: Scheduled Expiry Check

```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

def check_expiring_daily():
    """Daily check for expiring products"""
    products = product_service.list_products()
    expiring = expiry_tracker.get_expiring_products(products, days_threshold=7)
    
    for item in expiring:
        # Create notification
        product = product_service.get_product(item['barcode'])
        notification_service.create_expiry_warning(
            product,
            item['days_until_expiry']
        )

# Schedule daily at 9 AM
scheduler.add_job(check_expiring_daily, 'cron', hour=9)
scheduler.start()
```

### Example 22: API Integration (Flask)

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/scan/<barcode>', methods=['GET'])
def scan_product(barcode):
    product = product_service.get_product(barcode)
    if product:
        return jsonify(product.to_dict())
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/expiring', methods=['GET'])
def get_expiring():
    days = request.args.get('days', default=7, type=int)
    products = product_service.list_products()
    expiring = expiry_tracker.get_expiring_products(products, days)
    return jsonify(expiring)

if __name__ == '__main__':
    app.run(debug=True)
```

## Tips and Best Practices

1. **Regular Updates**: Run expiry checks daily
2. **Verify Sources**: Always verify manufacturing logs
3. **Report Counterfeits**: Report suspicious products immediately
4. **Follow Dosage**: Use medicine analyzer for accurate dosing
5. **Check Interactions**: Always check for drug interactions
6. **Store Properly**: Follow storage instructions
7. **Use Recipes**: Reduce waste with AI recipe suggestions
8. **Keep Records**: Maintain adherence tracking for medicines
9. **Update Data**: Keep product database current
10. **Backup**: Regularly backup your product database

## Troubleshooting

### Issue: Product not found
- Solution: Check barcode format, ensure product is added to database

### Issue: No manufacturing log
- Solution: Import logs using DataLoader or manually add logs

### Issue: AI features not working
- Solution: Set OPENAI_API_KEY in .env file

### Issue: Camera scanning fails
- Solution: Ensure camera permissions, check camera connectivity

For more help, see README.md or open an issue on GitHub.
