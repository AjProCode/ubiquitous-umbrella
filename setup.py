"""Setup script for MediScan"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mediscan",
    version="1.0.0",
    author="MediScan Team",
    author_email="mediscan@example.com",
    description="AI-Powered Barcode Scanner for Medicines and Perishable Items",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AjProCode/ubiquitous-umbrella",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
        "rich>=13.5.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "full": [
            "opencv-python>=4.8.0,<5.0.0",
            "pyzbar>=0.1.9",
            "python-barcode>=0.15.1",
            "pillow>=10.0.0,<11.0.0",
            "openai>=1.0.0,<2.0.0",
            "transformers>=4.30.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "scikit-learn>=1.3.0,<2.0.0",
            "numpy>=1.24.0,<2.0.0",
            "pandas>=2.0.0,<3.0.0",
            "APScheduler>=3.10.0,<4.0.0",
            "plyer>=2.1.0,<3.0.0",
            "flask>=3.0.0,<4.0.0",
            "flask-cors>=4.0.0,<5.0.0",
            "requests>=2.31.0,<3.0.0",
            "sqlalchemy>=2.0.0,<3.0.0",
            "alembic>=1.12.0,<2.0.0",
        ],
        "barcode": [
            "opencv-python>=4.8.0",
            "pyzbar>=0.1.9",
            "python-barcode>=0.15.1",
            "pillow>=10.0.0",
        ],
        "ai": [
            "openai>=1.0.0,<2.0.0",
            "transformers>=4.30.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "scikit-learn>=1.3.0,<2.0.0",
            "numpy>=1.24.0,<2.0.0",
            "pandas>=2.0.0,<3.0.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Entry point references app.py at root level
            # Use: python app.py <command> or mediscan <command> after install
            "mediscan=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
