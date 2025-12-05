

## 📌 Project Details

**Technologies**: Python, behave and playwright

## 🚀 Quick Start

## Prerequisites

- Python 3.8+
- Behave

## Installation

1. Clone the repository
2. Set up virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Estructura del proyecto

```text
PLAYWRIGHT-PYTHON-BASE/
├── config/
│   ├── device-config.json
├── features/
│   ├── steps/
│   ├── environment.py
├── pages/
├── behave.ini
└── README.md
└── requirements.txt
└── runner-1hilo.py
└── runner.py
```

## ⚙ Configuration

##### Report settings:

- See behave.ini

## 🏃 Running Tests

Run runner.py and use tags to execute specific scenarios.

## 📊 Generating Reports

### Gerate Allure HTML report

    allure generate --single-file reports -o allure_report_output --report-name "Mi Reporte de Pruebas" --lang es --clean

## 📧 Contact

#### For questions or issues, please contact:

https://www.linkedin.com/in/cgarcete/
