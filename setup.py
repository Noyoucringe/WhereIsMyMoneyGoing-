from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="1.0.0",
    description="A comprehensive expense tracking application with OCR, categorization, anomaly detection, and visualizations",
    author="Noyoucringe",
    packages=find_packages(),
    install_requires=[
        "pytesseract>=0.3.10",
        "Pillow>=10.1.0",
        "pandas>=2.1.4",
        "numpy>=1.26.2",
        "scikit-learn>=1.3.2",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        "opencv-python>=4.8.1.78",
        "pdf2image>=1.16.3",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "expense-tracker=expense_tracker.cli:main",
        ],
    },
)
