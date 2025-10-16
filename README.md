# MediScan - AI-Powered Barcode Scanner

An intelligent barcode scanning application focused on medicines and perishable items, featuring AI-powered counterfeit detection, expiry tracking, medicine interaction analysis, and recipe suggestions.

## 🎯 Features

### Core Features
- **📱 Barcode Scanning**: Scan product barcodes using camera or manual input
- **✅ Product Verification**: Verify products against manufacturing logs to detect counterfeits
- **📊 Product Management**: Store and manage detailed product information
- **📅 Expiry Tracking**: Track expiration dates with smart notifications
- **🔔 Reminder System**: Get timely reminders before products expire

### Medicine-Specific Features
- **💊 Medicine Management**: Specialized tracking for pharmaceutical products
- **⚕️ Drug Interaction Checking**: AI-powered detection of dangerous medicine interactions
- **📋 Dosage Tracking**: Monitor medication adherence and usage
- **🔬 Safety Analysis**: Comprehensive safety profile analysis for medicines
- **⚠️ Contraindication Alerts**: Warnings about contraindications and side effects

### Perishable Items Features
- **🥗 Perishable Tracking**: Focus on food and beverage expiry management
- **👨‍🍳 AI Recipe Suggestions**: Generate recipes based on expiring ingredients
- **📊 Usage Prioritization**: Smart recommendations for using items before expiry
- **❄️ Storage Instructions**: Track proper storage requirements

### AI-Powered Features
- **🤖 Counterfeit Detection**: AI-based analysis to identify fake products
- **🧠 Smart Recommendations**: Intelligent suggestions for product usage
- **📖 Recipe Generation**: AI-generated recipes using expiring ingredients
- **🔍 Pattern Recognition**: Detect suspicious patterns in product data

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Camera/webcam for barcode scanning

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/AjProCode/ubiquitous-umbrella.git
cd ubiquitous-umbrella
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Initialize sample data** (optional)
```bash
python app.py init
```

## 📖 Usage

### Command Line Interface

The application provides a simple CLI for various operations:

#### Scan a Product
```bash
# Scan by barcode
python app.py scan --barcode 8901234567890

# This will:
# - Look up the product in the database
# - Verify against manufacturing logs
# - Check for counterfeits
# - Show expiry status
# - Display detailed product information
```

#### View Dashboard
```bash
python app.py dashboard

# Shows:
# - Total products count
# - Expiry statistics
# - Notification summary
```

#### List Expiring Products
```bash
# List products expiring in next 7 days (default)
python app.py expiring

# List products expiring in next 14 days
python app.py expiring --days 14
```

#### Check Medicine Interactions
```bash
python app.py interactions

# Analyzes all medicines in the database for:
# - Drug-drug interactions
# - Contraindications
# - Potential safety issues
```

#### Generate Recipe Suggestions
```bash
python app.py recipes

# Generates recipes using:
# - Perishable items expiring soon
# - AI-powered recipe generation
# - Prioritization of urgent items
```

## 🏗️ Project Structure

```
ubiquitous-umbrella/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── models/                # Data models
│   │   ├── product.py         # Product, Medicine, PerishableItem
│   │   ├── manufacturing_log.py
│   │   └── notification.py
│   ├── services/              # Business logic
│   │   ├── barcode_scanner.py
│   │   ├── product_service.py
│   │   ├── verification_service.py
│   │   ├── expiry_tracker.py
│   │   └── notification_service.py
│   ├── ai/                    # AI-powered features
│   │   ├── recipe_generator.py
│   │   ├── medicine_analyzer.py
│   │   └── counterfeit_detector.py
│   └── utils/                 # Utilities
│       ├── config.py
│       └── data_loader.py
├── data/                      # Data storage
│   ├── products/             # Product database
│   ├── manufacturing_logs/   # Manufacturing verification logs
│   └── temp/                 # Temporary files
└── tests/                    # Test files
```

## 🔧 Configuration

Edit `.env` file to configure the application:

```env
# AI API Configuration
OPENAI_API_KEY=your_api_key_here  # For AI features

# Notification Settings
ENABLE_NOTIFICATIONS=true
NOTIFICATION_LEAD_TIME_DAYS=7     # Days before expiry to notify

# Verification Settings
VERIFICATION_STRICT_MODE=true     # Reject unverified products

# Medicine Safety
MEDICINE_INTERACTION_CHECK=true   # Check drug interactions
DOSAGE_TRACKING=true             # Track medication adherence

# Recipe Generation
ENABLE_RECIPE_SUGGESTIONS=true
RECIPE_COMPLEXITY=medium         # easy, medium, hard
```

## 📊 Data Models

### Product
Base class for all products with:
- Barcode, name, manufacturer
- Manufacturing and expiry dates
- Batch number
- Verification status

### Medicine (extends Product)
Specialized for pharmaceutical products:
- Medicine type (tablet, syrup, injection, etc.)
- Active ingredients
- Dosage information
- Side effects and contraindications
- Drug interactions
- Prescription requirements

### PerishableItem (extends Product)
For food and beverages:
- Storage temperature requirements
- Nutritional information
- Allergen information
- Shelf life after opening

### ManufacturingLog
Verification data from manufacturers:
- Batch details
- Quality check results
- Certification numbers
- Recall status

## 🤖 AI Features

### Counterfeit Detection
The AI analyzes multiple factors to detect fake products:
- Manufacturing log verification
- Date consistency checks
- Batch number validation
- Pattern recognition
- Risk scoring (0-100)

### Medicine Interaction Analysis
Checks for dangerous drug combinations:
- Active ingredient interactions
- Known drug-drug interactions
- Contraindication warnings
- Safety scoring

### Recipe Generation
AI-powered recipe suggestions:
- Uses expiring ingredients
- Considers dietary preferences
- Adjustable difficulty levels
- Multiple cuisine options

## 🔒 Security & Privacy

- Product data stored locally
- No automatic data transmission
- API keys encrypted in environment variables
- Manufacturing log verification for authenticity
- Counterfeit alert system

## 🚨 Important Warnings

1. **Medicine Use**: This app provides information only. Always consult healthcare professionals for medical advice.

2. **Counterfeit Detection**: While our AI is sophisticated, it's not 100% accurate. When in doubt, consult the manufacturer.

3. **Expiry Dates**: Do not use expired medicines. Dispose of them properly.

4. **Drug Interactions**: The interaction checker is informational. Consult your doctor or pharmacist.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review sample data for examples

## 🔮 Future Enhancements

- [ ] Mobile app integration
- [ ] OCR for label scanning
- [ ] Multi-language support
- [ ] Cloud sync capabilities
- [ ] Advanced AI models
- [ ] Pharmacy integration
- [ ] Nutrition tracking
- [ ] Smart shopping lists

## 📚 Sample Data

The application includes sample data for testing:
- 3 sample products (medicines and food items)
- Manufacturing logs for verification
- Run `python app.py init` to load sample data

## ⚙️ API Reference

### BarcodeScanner
- `scan_from_camera()`: Scan using camera
- `scan_from_image()`: Scan from image file
- `validate_barcode()`: Validate barcode format

### ProductService
- `add_product()`: Add/update product
- `get_product()`: Retrieve product by barcode
- `list_products()`: List with filters
- `get_expiring_soon()`: Get products expiring soon

### VerificationService
- `verify_product()`: Verify against logs
- `check_for_recalls()`: Check recall status
- `flag_as_counterfeit()`: Flag suspicious products

### ExpiryTracker
- `check_expiry_status()`: Check product expiry
- `get_expiring_products()`: List expiring items
- `categorize_by_expiry()`: Categorize by urgency

### MedicineAnalyzer
- `check_interactions()`: Check drug interactions
- `analyze_medicine_safety()`: Safety analysis
- `track_medicine_adherence()`: Track medication usage

### RecipeGenerator
- `generate_recipe()`: Create recipes
- `suggest_recipes_for_expiring_items()`: Smart suggestions
- `get_usage_priority()`: Prioritize ingredient usage

### CounterfeitDetector
- `analyze_product()`: Detect counterfeits
- `batch_analyze()`: Analyze multiple products
- `report_counterfeit()`: Report fake products

---

**Built with ❤️ for safer medicine management and reduced food waste**