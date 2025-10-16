# MediScan Quick Start Guide

Get up and running with MediScan in 5 minutes!

## Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher:
```bash
python --version
```

### Step 2: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/AjProCode/ubiquitous-umbrella.git
cd ubiquitous-umbrella

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Initialize
```bash
# Create sample data
python app.py init
```

## Basic Usage

### View Dashboard
```bash
python app.py dashboard
```

Output:
```
═══════════════════════════════════════════════════
        MediScan - Product Management Dashboard      
═══════════════════════════════════════════════════

Total Products: 3
  • Medicines: 2
  • Perishable Items: 1
```

### Scan a Product
```bash
python app.py scan --barcode 8901234567890
```

Output shows:
- Product name and details
- Manufacturing and expiry dates
- Verification status
- Medicine-specific information

### Check Expiring Items
```bash
python app.py expiring --days 7
```

Shows products expiring in the next 7 days.

### Check Medicine Interactions
```bash
python app.py interactions
```

Analyzes all medicines for potential drug interactions.

### Generate Recipes
```bash
python app.py recipes
```

Creates recipe suggestions using expiring ingredients.

## Common Tasks

### Add a New Product

```python
from datetime import date, timedelta
from src.models.product import Medicine, MedicineType
from src.services.product_service import ProductService

# Create product service
service = ProductService()

# Create medicine
medicine = Medicine(
    barcode='1234567890123',
    name='Aspirin 100mg',
    manufacturer='PharmaCompany',
    manufacturing_date=date.today() - timedelta(days=60),
    expiry_date=date.today() + timedelta(days=730),
    batch_number='BATCH123',
    medicine_type=MedicineType.TABLET,
    dosage='100mg daily',
    active_ingredients=['Aspirin'],
    prescription_required=False
)

# Add to database
service.add_product(medicine)
print("Product added successfully!")
```

### Check Product Safety

```python
from src.services.product_service import ProductService
from src.ai.medicine_analyzer import MedicineAnalyzer

# Get medicine
service = ProductService()
medicine = service.get_product('8901234567890')

# Analyze safety
analyzer = MedicineAnalyzer()
safety = analyzer.analyze_medicine_safety(medicine)

print(f"Safety Score: {safety['safety_score']}/100")
print(f"Warnings: {len(safety['warnings'])}")
```

### Verify Product Authenticity

```python
from src.services.verification_service import VerificationService
from src.ai.counterfeit_detector import CounterfeitDetector

# Get product
product = service.get_product('8901234567890')

# Verify
verification = VerificationService()
is_verified, message = verification.verify_product(product)

print(f"Verified: {is_verified}")
print(f"Message: {message}")

# Check for counterfeits
detector = CounterfeitDetector()
log = verification.get_log(product.barcode, product.batch_number)
analysis = detector.analyze_product(product, log)

print(f"Risk Score: {analysis['risk_score']}/100")
print(f"Assessment: {analysis['assessment']}")
```

## Configuration

### Basic Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Enable/disable features
ENABLE_NOTIFICATIONS=true
NOTIFICATION_LEAD_TIME_DAYS=7

# AI features (optional)
OPENAI_API_KEY=your_key_here

# Medicine safety
MEDICINE_INTERACTION_CHECK=true
DOSAGE_TRACKING=true

# Recipe generation
ENABLE_RECIPE_SUGGESTIONS=true
RECIPE_COMPLEXITY=medium
```

## Sample Workflow

### Typical Day with MediScan

**Morning: Check Dashboard**
```bash
python app.py dashboard
```

**Scan New Products**
```bash
python app.py scan --barcode 8901234567890
python app.py scan --barcode 8901234567891
```

**Check What's Expiring**
```bash
python app.py expiring --days 7
```

**Need Recipe Ideas?**
```bash
python app.py recipes
```

**Taking Multiple Medicines?**
```bash
python app.py interactions
```

## Tips and Tricks

### 1. Quick Barcode Validation
```python
from src.services.barcode_scanner import BarcodeScanner

scanner = BarcodeScanner()
is_valid = scanner.validate_barcode('8901234567890')
print(f"Valid: {is_valid}")
```

### 2. Filter Products
```python
from src.models.product import ProductCategory

service = ProductService()

# Get only medicines
medicines = service.list_products(category=ProductCategory.MEDICINE)

# Get expired products
expired = service.list_products(expired=True)

# Get unverified products
unverified = service.list_products(verified=False)
```

### 3. Search Products
```python
# Search by name
results = service.search_products('paracetamol')
for product in results:
    print(f"{product.name} - {product.expiry_date}")
```

### 4. Get Expiry Summary
```python
from src.services.expiry_tracker import ExpiryTracker

tracker = ExpiryTracker()
products = service.list_products()
summary = tracker.get_expiry_summary(products)

print(f"Total: {summary['total_products']}")
print(f"Expired: {summary['expired_count']}")
print(f"Critical: {summary['critical_count']}")
```

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Install missing dependency
```bash
pip install <missing-module>
```

### Issue: "Product not found"
**Solution**: Initialize sample data or add products
```bash
python app.py init
```

### Issue: "Camera not working"
**Solution**: Camera features require opencv and pyzbar
```bash
pip install opencv-python pyzbar
```

### Issue: "AI features not working"
**Solution**: Set OpenAI API key
```bash
# In .env file
OPENAI_API_KEY=your_key_here
```

## Next Steps

1. **Read Full Documentation**: Check README.md for complete features
2. **Explore Examples**: See USAGE_EXAMPLES.md for detailed examples
3. **Understand Architecture**: Read ARCHITECTURE.md for design details
4. **Contribute**: See CONTRIBUTING.md to help improve MediScan

## Getting Help

- **Documentation**: README.md, USAGE_EXAMPLES.md, ARCHITECTURE.md
- **Issues**: Open an issue on GitHub
- **Questions**: Use GitHub Discussions

## Quick Reference

### Commands
- `init` - Initialize sample data
- `dashboard` - View overview
- `scan` - Scan product
- `expiring` - List expiring items
- `interactions` - Check medicine interactions
- `recipes` - Generate recipes

### Key Directories
- `src/models/` - Data models
- `src/services/` - Business logic
- `src/ai/` - AI features
- `data/` - Data storage

### Configuration Files
- `.env` - Configuration
- `requirements.txt` - Dependencies
- `setup.py` - Installation

## Example Session

```bash
# Start fresh
python app.py init

# Check status
python app.py dashboard

# Scan a medicine
python app.py scan --barcode 8901234567890

# Check interactions
python app.py interactions

# See what's expiring
python app.py expiring

# Get recipe ideas
python app.py recipes
```

## Success Indicators

You're ready when you can:
- ✅ Run `python app.py dashboard` successfully
- ✅ Scan products with barcodes
- ✅ View expiring items
- ✅ Check medicine interactions
- ✅ Generate recipe suggestions

## Stay Updated

Watch the repository for:
- New features
- Bug fixes
- Documentation updates
- Community contributions

---

**Ready to start? Run `python app.py dashboard` now!** 🚀
