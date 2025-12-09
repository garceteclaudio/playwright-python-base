# Playwright Python Base

## 📌 Project Details

**Technologies:** Python, Behave, Playwright

## 🚀 Quick Start

### Prerequisites

-   Python 3.12+
-   Playwright
-   Behave
-   Docker (optional)
-   Docker Compose (optional)

------------------------------------------------------------------------

## 🔧 Installation (Local)

### 1. Clone the repository

    git clone https://github.com/tu-repo/playwright-python-base.git
    cd playwright-python-base

### 2. Create virtual environment

#### Linux/Mac:

    python3 -m venv .venv
    source .venv/bin/activate

#### Windows:

    python -m venv .venv
    .venv\Scripts\activate

### 3. Install dependencies

    pip install -r requirements.txt
    playwright install

------------------------------------------------------------------------

## 📁 Project Structure

    PLAYWRIGHT-PYTHON-BASE/
    ├── features/
    │   ├── steps/
    │   │   ├── test_login_steps.py
    │   ├── login.feature
    │   ├── login2.feature
    │   ├── login3.feature
    │   ├── environment.py
    ├── tests/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── runner.py
    ├── runner-1hilo.py
    ├── merge_allure_and_generate.py
    └── README.md

------------------------------------------------------------------------

## 🐳 Running with Docker Compose

### Run with build (first time or when the Dockerfile changes)

    docker-compose up --build

This will: - Build the container\
- Run Playwright + Behave\
- Generate Allure results automatically

### Run without build (faster)

    docker-compose up

------------------------------------------------------------------------

## 🏃 Running Tests (Local)

### Run all tests:

    python runner.py

### Run with tags:

    behave -t @login

------------------------------------------------------------------------

## 📊 Allure Report

### Generate report:

    allure generate --single-file reports -o allure_report_output --report-name "Reporte de Pruebas" --lang es --clean

### Open report:

    allure open allure_report_output

------------------------------------------------------------------------

## 📧 Contact

LinkedIn: https://www.linkedin.com/in/cgarcete/
