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

## 🔧 Installation (Local)

### 1. Clone the repository
```bash
    git clone https://github.com/tu-repo/playwright-python-base.git
    cd playwright-python-base
```
### 2. Create virtual environment

#### Linux/Mac:
```bash
    python3 -m venv .venv
    source .venv/bin/activate
```
#### Windows:
```bash
    python -m venv .venv
    .venv\Scripts\activate
```
### 3. Install dependencies
```bash
    pip install -r requirements.txt
    playwright install
```
------------------------------------------------------------------------

## 🏃 Run Tests (Local)

### Run all tests with python:
```bash
  python runner.py
```

### Run test using Behave:
#### With a specific tag
```bash
  behave --tags=@test12345 -f allure_behave.formatter:AllureFormatter -o allure-results

```

#### Run all tests
```bash
  behave -f allure_behave.formatter:AllureFormatter -o allure-results
```
     

------------------------------------------------------------------------

## 📊 Allure Report (Local)

### Generate the report (only when using runner.py)
```bash
    python merge_allure_and_generate.py
```
Check the allure-report/ folder and open the generated report.

### Generate a single-file report with Allure
```bash
    allure generate allure-results -o allure-report --clean --single-file
```
Check the allure-report/index.html file and open the generated report.

### Generate and view the report using the Allure server
```bash
    allure serve allure-results
```    

------------------------------------------------------------------------


## 🐳 Running with Docker Compose

### Run with build (first time or when the Dockerfile changes)

    docker-compose up --build

This will: - Build the container\
- Run Playwright + Behave\
- Generate Allure results automatically

### Run without build (faster)

    docker-compose up

### Open report:

    allure-results/

------------------------------------------------------------------------


## 📧 Contact

LinkedIn: https://www.linkedin.com/in/cgarcete/
