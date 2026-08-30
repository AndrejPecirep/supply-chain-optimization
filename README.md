# Supply Chain Optimization & AI Risk Copilot

A portfolio-grade supply chain analytics and optimization project that combines **demand forecasting, inventory optimization, supplier risk assessment, document parsing, route optimization, dashboards, automated validation, testing, and CI workflows** in one end-to-end solution.

The project demonstrates how data engineering, machine learning, optimization techniques, and operational analytics can be applied to common supply chain challenges such as stockouts, excess inventory, unreliable suppliers, manual document processing, and inefficient transportation planning.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Objectives](#objectives)
- [Solution Architecture](#solution-architecture)
- [Core Capabilities](#core-capabilities)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Flow](#data-flow)
- [Demand Forecasting](#demand-forecasting)
- [Inventory Optimization](#inventory-optimization)
- [Supplier Risk Assessment](#supplier-risk-assessment)
- [Document and Manifest Parsing](#document-and-manifest-parsing)
- [Route Optimization](#route-optimization)
- [Streamlit Application](#streamlit-application)
- [Dashboards and Reporting](#dashboards-and-reporting)
- [Data Validation and Testing](#data-validation-and-testing)
- [CI Automation](#ci-automation)
- [Docker Support](#docker-support)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Generated Outputs](#generated-outputs)
- [Configuration](#configuration)
- [Business KPIs](#business-kpis)
- [Governance and Human-in-the-Loop Controls](#governance-and-human-in-the-loop-controls)
- [Design Decisions](#design-decisions)
- [Possible Future Improvements](#possible-future-improvements)
- [Disclaimer](#disclaimer)

---

## Project Overview

**Supply Chain Optimization & AI Risk Copilot** is an end-to-end demonstration project designed to show how a supply chain organization can make better operational decisions using data, machine learning, mathematical optimization, and automated document analysis.

The solution covers several important supply chain domains:

- SKU-level demand forecasting
- Economic Order Quantity (EOQ) calculation
- Safety stock calculation
- Reorder point recommendations
- Supplier operational and contract risk scoring
- Shipping manifest parsing
- OCR-ready document ingestion
- Transportation route optimization
- Automated data validation
- Automated model execution
- Unit and integrity testing
- Streamlit-based analytical interface
- Power BI and Tableau reporting assets
- Dockerized execution
- GitHub Actions workflows
- Executive and technical documentation

The repository is structured as a portfolio project, but it follows practices commonly found in real software and analytics projects: modular code, configuration files, testing, data validation, CI automation, reproducible execution, documented outputs, and separation between raw, processed, and generated data.

---

## Business Problem

Supply chain teams frequently work with fragmented spreadsheets, manually reviewed supplier contracts, historical inventory reports, shipping documents, and delayed operational information.

This can lead to:

- Excess inventory and unnecessarily high working capital
- Stockouts and reduced customer service levels
- Weak visibility into future demand
- Late identification of supplier problems
- Dependence on single-source suppliers
- Manual review of contracts and logistics documents
- Delayed detection of penalty clauses and SLA risks
- Expedited freight costs
- Inefficient replenishment policies
- Slow management reporting

The purpose of this project is to demonstrate how these processes can be brought together into a single analytical workflow.

---

## Objectives

The main objectives are to:

1. Transform raw supply chain data into structured analytical inputs.
2. Validate important data before running models.
3. Forecast future demand at SKU level.
4. Calculate inventory replenishment recommendations.
5. Combine supplier operational KPIs with contract-related risk indicators.
6. Convert shipping manifest text or OCR output into structured JSON.
7. Demonstrate a simple transportation route optimization technique.
8. Produce reusable CSV, JSON, and Parquet outputs.
9. Present results through an interactive Streamlit application and BI assets.
10. Add automated testing and GitHub Actions workflows.
11. Package the application with Docker for reproducible execution.
12. Document the business case, current state, target state, and AI governance considerations.

---

## Solution Architecture

The project follows a modular workflow:

```text
Raw Supply Chain Data
        |
        v
Data Validation
        |
        +----------------------+
        |                      |
        v                      v
Demand Forecasting      Supplier / Contract Data
        |                      |
        v                      v
Inventory Policies      Supplier Risk Assessment
        |                      |
        +-----------+----------+
                    |
                    v
             Generated Outputs
                    |
          +---------+---------+
          |                   |
          v                   v
   Streamlit App       BI / Executive Reporting

Shipping Documents
        |
        v
Text / OCR Extraction
        |
        v
Manifest Parser
        |
        v
Structured JSON

Location Data
        |
        v
Route Optimization Module
```

The project intentionally separates input data, model logic, orchestration, validation, tests, configuration, documentation, dashboards, and generated outputs.

---

## Core Capabilities

### 1. Demand Forecasting

The forecasting module trains a machine learning model on historical customer demand and generates a forward-looking SKU-level forecast.

Current implementation:

- Uses `RandomForestRegressor`
- Creates time-based features from `order_date`
- Encodes SKU, customer segment, and region
- Preserves chronological order during the train/test split
- Calculates Mean Absolute Percentage Error (MAPE)
- Generates a default 90-day forecast
- Prevents negative demand predictions
- Writes forecast results to CSV

The current model is intended as a strong portfolio baseline rather than a production forecasting system.

---

### 2. Inventory Optimization

The inventory optimization module calculates replenishment policies from historical demand and supplier lead-time information.

Implemented calculations include:

#### Economic Order Quantity

EOQ estimates an order quantity that balances ordering and holding costs:

```text
EOQ = sqrt((2 × Annual Demand × Ordering Cost) / Holding Cost per Unit)
```

The implementation validates that the inputs are positive and rounds the final recommendation upward to a whole unit.

#### Safety Stock

Safety stock is calculated from maximum and average demand together with maximum and average supplier lead time.

The goal is to create a buffer against demand and lead-time variability.

#### Reorder Point

The project combines safety stock with expected demand during average supplier lead time to produce a reorder point recommendation.

Generated inventory policies include:

- SKU
- EOQ
- Safety stock
- Reorder point
- Average daily demand

---

### 3. Supplier Risk Assessment

Supplier risk is evaluated by combining operational supplier metrics with contract-related indicators.

Operational factors include:

- On-time delivery rate
- Quality defect rate
- Financial health score
- Single-source dependency

Contract text is also scanned for risk-related terms such as:

- penalties
- expedited freight
- single-source clauses
- exclusivity
- cure periods
- delivery performance below 90%
- termination clauses

The contract indicators are converted into a contract risk score and combined with supplier master-data KPIs to calculate an overall operational risk score.

Suppliers are then classified as:

- `LOW`
- `MEDIUM`
- `HIGH`

Each risk category receives a recommended action.

Examples:

- Continue standard monitoring
- Create a mitigation plan
- Review alternate suppliers
- Escalate to procurement leadership
- Request legal review

> **Implementation note:** the current supplier scoring engine is intentionally transparent and rule/KPI based. The repository also contains configuration and prompt assets that demonstrate how an LLM-assisted review layer could be integrated, but the current scoring path does not require an external LLM API call.

---

### 4. Document and Manifest Parsing

The project contains a document parsing module for shipping manifests.

For text-based manifests, regular expressions extract:

- Manifest ID
- Supplier
- Delivery date
- Vehicle
- SKU
- Quantity
- Total quantity

For supported image formats, the parser can use:

- `pytesseract`
- `Pillow`

to convert scanned documents into text before parsing.

Supported image extensions include:

```text
.png
.jpg
.jpeg
.tif
.tiff
```

Parsed results are stored as structured JSON, making the information easier to use in analytics or downstream systems.

> OCR requires a working Tesseract installation on the host operating system in addition to the Python package.

---

### 5. Route Optimization

The repository includes a transportation route optimization module.

It contains:

- A reusable `Location` data class
- Haversine distance calculation
- Nearest-neighbor route construction
- Total route distance calculation
- Return-to-depot logic

The Haversine formula is used to estimate geographic distance between latitude/longitude coordinates.

The nearest-neighbor algorithm repeatedly selects the closest unvisited location until every stop has been visited, then returns to the depot.

This is a practical heuristic demonstration rather than an exact Traveling Salesman Problem solver.

The current route module can be run independently and is not yet integrated into the main Streamlit navigation or the end-to-end pipeline.

---

## Technology Stack

### Programming and Data

- Python 3.11
- pandas
- NumPy
- PyArrow
- OpenPyXL

### Machine Learning

- scikit-learn
- Random Forest Regression
- MAPE model evaluation

### AI / Document Processing

- PyPDF
- pytesseract
- Pillow
- Regex-based information extraction
- YAML-based AI configuration
- Prompt templates

The dependency set also includes libraries suitable for future LLM/RAG extensions, such as LangChain, OpenAI integration, and FAISS.

### Visualization and Application

- Streamlit
- Plotly
- Matplotlib
- Power BI
- Tableau

### Quality and Engineering

- pytest
- Ruff
- mypy
- GitHub Actions
- Docker
- Docker Compose
- Makefile

### Output Formats

- CSV
- JSON
- Parquet
- Excel
- Power BI
- Tableau
- PDF
- DOCX
- PPTX

---

## Project Structure

```text
supply-chain-optimization-project/
│
├── .github/
│   └── workflows/
│       ├── ai-model-eval.yml
│       └── data-validation.yml
│
├── config/
│   └── ai_agent_config.yaml
│
├── dashboards/
│   ├── ai_risk_copilot_dashboard.pbix
│   ├── supply_chain_kpi_dashboard.pbix
│   └── tableau_route_analysis.twbx
│
├── data/
│   ├── raw/
│   │   ├── customer_orders_demand.csv
│   │   ├── inventory_levels_historical.csv
│   │   ├── suppliers_master_data.csv
│   │   ├── transport_rates_2025_2026.xlsx
│   │   ├── shipping_manifests_scans/
│   │   └── supplier_contracts_pdf/
│   │
│   ├── processed/
│   │   ├── ai_extracted_contract_terms.json
│   │   ├── cleaned_inventory_data.parquet
│   │   └── demand_forecast_input.csv
│   │
│   └── output/
│       ├── cleaned_inventory_data.csv
│       ├── demand_forecast_90_days.csv
│       ├── inventory_policy_recommendations.csv
│       ├── parsed_shipping_manifests.json
│       ├── supplier_risk_scores.csv
│       └── supplier_risk_scores.json
│
├── docs/
│   ├── ai-integration-architecture.md
│   ├── business-case.md
│   ├── current-state-analysis.md
│   ├── executive-summary.md
│   └── proposed-target-state.md
│
├── models/
│   ├── __init__.py
│   ├── ai_demand_forecasting.py
│   ├── ai_document_parser.py
│   ├── ai_supplier_risk_agent.py
│   ├── inventory_optimization.py
│   └── route_optimization.py
│
├── prompts/
│   ├── anomaly_explanation_prompt.txt
│   └── supplier_audit_prompt.txt
│
├── scripts/
│   ├── __init__.py
│   ├── run_pipeline.py
│   └── validate_data.py
│
├── templates/
│   ├── supplier_sla_template.docx
│   └── warehouse_audit_checklist.pdf
│
├── tests/
│   ├── test_ai_agent_precision.py
│   ├── test_data_integrity.py
│   └── test_inventory_math.py
│
├── utils/
│   ├── __init__.py
│   └── io.py
│
├── .env.example
├── .gitignore
├── app.py
├── Dockerfile
├── docker-compose.yml
├── Executive_Presentation_Supply_Chain.pptx
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

Temporary Python and pytest cache files are intentionally excluded from the documented project structure because they are generated automatically and are not part of the application source code.

---

## Data Flow

### Raw Data

The `data/raw/` directory contains the source datasets used by the project:

- Historical customer demand
- Historical inventory levels
- Supplier master data
- Transportation rates
- Supplier contracts
- Shipping manifest samples

### Processed Data

The `data/processed/` directory contains intermediate analytical datasets such as:

- Cleaned inventory data
- Demand forecasting input
- Extracted contract terms

### Generated Output

The pipeline creates business-facing model and analytical results in `data/output/`.

This raw → processed → output separation makes the project easier to understand, maintain, and extend.

---

## Demand Forecasting

The forecasting workflow is implemented in:

```text
models/ai_demand_forecasting.py
```

### Feature Engineering

The module creates features including:

- Day of week
- Month
- Day of year
- Weekend indicator
- SKU
- Customer segment
- Region
- Price
- Promotion flag

Categorical columns are converted into machine-readable dummy variables.

### Model

The model currently uses:

```python
RandomForestRegressor(
    n_estimators=120,
    random_state=42,
    min_samples_leaf=2
)
```

A chronological 80/20 train/test split is used with `shuffle=False` so future observations are not randomly mixed into the training sample.

### Evaluation

The model calculates:

```text
MAPE — Mean Absolute Percentage Error
```

The evaluation metric is included in generated forecast data as `model_mape`.

### Forecast Horizon

The default forecast horizon is:

```text
90 days
```

For every future date, predictions are produced for each SKU available in the historical dataset.

---

## Inventory Optimization

Inventory logic is located in:

```text
models/inventory_optimization.py
```

The workflow:

1. Converts order dates into datetime values.
2. Aggregates quantity by SKU and day.
3. Calculates demand statistics.
4. Reads supplier lead-time information.
5. Calculates EOQ.
6. Calculates safety stock.
7. Calculates the reorder point.
8. Produces an inventory policy table.

The generated recommendation file is:

```text
data/output/inventory_policy_recommendations.csv
```

---

## Supplier Risk Assessment

Supplier risk logic is implemented in:

```text
models/ai_supplier_risk_agent.py
```

The module reads:

```text
data/raw/suppliers_master_data.csv
data/raw/supplier_contracts_pdf/
```

Contract files can be read from PDF or plain-text representations.

The final risk score combines multiple dimensions instead of relying on a single metric. This demonstrates how procurement teams can combine quantitative operational KPIs with qualitative contract signals.

Generated results:

```text
data/output/supplier_risk_scores.csv
data/output/supplier_risk_scores.json
```

The JSON output can be consumed by other applications or APIs, while the CSV output is convenient for analysts and BI tools.

---

## Document and Manifest Parsing

Manifest parsing is implemented in:

```text
models/ai_document_parser.py
```

A manifest is converted from unstructured text into a structure similar to:

```json
{
  "manifest_id": "M1",
  "supplier": "Example Supplier",
  "delivery_date": "2026-01-01",
  "vehicle": "TRUCK-01",
  "items": [
    {
      "sku": "SKU-A100",
      "quantity": 12
    }
  ],
  "total_quantity": 12
}
```

This demonstrates a typical automation pattern:

```text
Document
   ↓
OCR / text extraction
   ↓
Field extraction
   ↓
Structured JSON
   ↓
Analytics / operational system
```

Generated output:

```text
data/output/parsed_shipping_manifests.json
```

---

## Route Optimization

Route optimization is implemented in:

```text
models/route_optimization.py
```

The sample module demonstrates route planning from a Sarajevo distribution center to locations such as:

- Mostar
- Banja Luka
- Tuzla

The algorithm:

1. Starts at the depot.
2. Calculates geographic distances.
3. Selects the nearest unvisited stop.
4. Repeats the process until all stops are visited.
5. Returns to the depot.
6. Reports the complete route and total estimated distance.

For larger real-world routing problems, this module could later be replaced or extended with OR-Tools, vehicle-capacity constraints, delivery windows, traffic data, and multiple vehicles.

---

## Streamlit Application

The interactive application is defined in:

```text
app.py
```

The application title is:

```text
Supply Chain Optimization & AI Risk Copilot
```

It provides five navigation areas.

### Executive Overview

Displays high-level metrics including:

- Number of suppliers
- Number of SKUs
- Number of historical orders

### Demand Forecast

Trains the forecasting model, generates the 90-day forecast, displays the results, and plots forecast quantity over time.

### Supplier Risk

Displays:

- Supplier name
- Country
- Operational risk score
- Risk level
- Recommended action

A supplier risk bar chart is also provided.

### Inventory Policy

Calculates and displays SKU-level inventory recommendations.

### Manifest Parser

Allows a user to paste manifest or OCR text and converts it into structured output.

---

## Dashboards and Reporting

The repository includes additional reporting assets:

```text
dashboards/ai_risk_copilot_dashboard.pbix
dashboards/supply_chain_kpi_dashboard.pbix
dashboards/tableau_route_analysis.twbx
```

These files demonstrate how model outputs can be consumed by business intelligence tools.

The project also includes:

```text
Executive_Presentation_Supply_Chain.pptx
```

for executive-level communication.

Supporting business documents are available in `docs/`, while reusable operational templates are available in `templates/`.

---

## Data Validation and Testing

Before analytical results are trusted, the project validates expected source data.

Validation logic is located in:

```text
scripts/validate_data.py
```

The test suite is located in:

```text
tests/
```

### Test Areas

#### Data Integrity

Checks that required files exist and supplier data passes validation rules.

#### Inventory Mathematics

Checks that:

- EOQ is positive for valid inputs.
- Safety stock does not become negative.

#### Supplier and Document Logic

Checks that:

- Contract penalty terms are detected.
- Contract risk is calculated.
- Manifest SKUs and quantities are extracted correctly.

Run the tests with:

```bash
pytest -q
```

---

## CI Automation

The project uses GitHub Actions to automate quality checks.

### Data Validation Workflow

File:

```text
.github/workflows/data-validation.yml
```

Triggered on:

- Push
- Pull request

The workflow:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs project dependencies.
4. Runs the data validation script.
5. Runs the pytest test suite.

### AI Model Evaluation Workflow

File:

```text
.github/workflows/ai-model-eval.yml
```

The workflow can be:

- Triggered manually
- Executed automatically every Monday at 04:00 UTC

It runs:

```text
ai_demand_forecasting.py
ai_supplier_risk_agent.py
ai_document_parser.py
```

This demonstrates scheduled model execution and repeatable evaluation within GitHub.

---

## Docker Support

The application can be containerized using the included:

```text
Dockerfile
docker-compose.yml
```

The Docker image:

- Uses Python 3.11 slim
- Installs dependencies from `requirements.txt`
- Copies the project into `/app`
- Exposes Streamlit port `8501`
- Starts the Streamlit application

Docker Compose additionally:

- Maps local port `8501`
- Loads environment variables from `.env`
- Mounts the local `data/` directory into the container

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd supply-chain-optimization-project
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file from the example:

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Do not commit the real `.env` file.

---

## Running the Project

### Validate Source Data

```bash
python scripts/validate_data.py
```

### Run the Complete Pipeline

```bash
python scripts/run_pipeline.py
```

The pipeline:

1. Loads suppliers, demand, and inventory data.
2. Builds inventory policy recommendations.
3. Generates the 90-day demand forecast.
4. Scores supplier risk.
5. Parses shipping manifests.
6. Writes structured outputs to `data/output/`.
7. Writes inventory data as Parquet when the required engine is available, with CSV fallback support.

### Run the Streamlit Application

```bash
streamlit run app.py
```

Then open the local Streamlit address shown in the terminal.

### Run Tests

```bash
pytest -q
```

---

## Running Individual Modules

### Demand Forecast

```bash
python models/ai_demand_forecasting.py
```

### Supplier Risk

```bash
python models/ai_supplier_risk_agent.py
```

### Manifest Parser

```bash
python models/ai_document_parser.py
```

### Inventory Optimization

```bash
python models/inventory_optimization.py
```

### Route Optimization Demo

```bash
python models/route_optimization.py
```

---

## Running with Docker

### Build the Image

```bash
docker build -t supply-chain-ai .
```

### Run the Container

```bash
docker run -p 8501:8501 supply-chain-ai
```

### Or Use Docker Compose

```bash
docker compose up --build
```

The application will be available on port:

```text
8501
```

---

## Generated Outputs

After running the pipeline, the project produces files such as:

```text
data/output/
├── cleaned_inventory_data.csv
├── demand_forecast_90_days.csv
├── inventory_policy_recommendations.csv
├── parsed_shipping_manifests.json
├── supplier_risk_scores.csv
└── supplier_risk_scores.json
```

Depending on the environment and execution path, cleaned inventory data may also be written as Parquet.

### Output Purpose

| Output | Purpose |
|---|---|
| `demand_forecast_90_days.csv` | Future SKU demand predictions |
| `inventory_policy_recommendations.csv` | EOQ, safety stock, and reorder recommendations |
| `supplier_risk_scores.csv` | Analyst-friendly supplier risk results |
| `supplier_risk_scores.json` | Machine-readable supplier risk results |
| `parsed_shipping_manifests.json` | Structured logistics document data |
| `cleaned_inventory_data.*` | Reusable cleaned inventory data |

---

## Configuration

AI and governance-related configuration is stored in:

```text
config/ai_agent_config.yaml
```

Configuration categories include:

- LLM provider and model
- Temperature
- Supplier risk thresholds
- Risk factor weights
- Human-in-the-loop review thresholds
- Forecast horizon
- Forecast validation metric
- OCR language
- OCR confidence threshold

This separates configurable business rules from application source code and provides a foundation for future integration work.

> Not every YAML setting is currently wired into every Python execution path. The configuration file represents both current settings and the intended extension architecture.

---

## Prompt Templates

The repository contains prompt assets in:

```text
prompts/
├── anomaly_explanation_prompt.txt
└── supplier_audit_prompt.txt
```

These files demonstrate how prompt logic can be kept outside application code for easier maintenance and future LLM integration.

The current core pipeline is deterministic and does not require an OpenAI API call to run.

---

## Business KPIs

The project is designed around supply chain KPIs such as:

- Forecast MAPE
- Supplier risk score
- On-time delivery rate
- Quality defect rate
- Financial health score
- Inventory turnover
- Stockout incidents
- Safety stock
- Reorder point
- Expedited freight cost
- Supplier concentration / single-source dependency
- Route distance

These metrics connect the technical implementation to business decisions.

---

## Governance and Human-in-the-Loop Controls

AI and automated scoring should support decision-makers rather than silently replace procurement or legal judgment.

The project documentation defines governance concepts such as:

- AI recommendations are advisory.
- High-risk findings should receive manager review.
- Penalty clauses can require legal review.
- Contract analysis should not replace legal counsel.
- Risk findings should remain explainable and traceable to source data.
- Critical supplier decisions should remain human-controlled.

This is particularly important in supplier management because automated outputs can influence procurement, contractual, financial, and operational decisions.

---

## Design Decisions

### Modular Python Structure

Forecasting, risk scoring, document parsing, inventory optimization, and routing are implemented as separate modules so each capability can be tested and extended independently.

### Raw / Processed / Output Separation

Separating source data from transformed data and generated results improves reproducibility and reduces accidental modification of source datasets.

### Explainable Supplier Scoring

A transparent weighted scoring model was used so the reasoning behind supplier risk can be inspected rather than hidden inside a black-box model.

### Chronological Forecast Validation

The demand model uses a non-shuffled train/test split to better reflect forecasting behavior.

### Multiple Output Formats

CSV and JSON outputs allow the same analytical results to be used by analysts, dashboards, applications, or APIs.

### CI and Tests

Validation and tests are part of the repository rather than being treated as an afterthought.

### Containerization

Docker provides a reproducible runtime for the Streamlit application.

---

## Documentation Included

The `docs/` directory contains:

### Executive Summary

Explains the overall solution and intended business value.

### Current State Analysis

Describes the limitations of spreadsheet-driven planning, manual contract review, and delayed operational reporting.

### Business Case

Connects the technical solution to working capital, service levels, supplier risk, and process automation.

### Proposed Target State

Describes a more automated, data-driven supply chain planning environment.

### AI Integration Architecture

Documents demand forecasting, supplier risk analysis, document parsing, and human-in-the-loop governance.

---

## Possible Future Improvements

The current project provides a strong end-to-end foundation. Potential extensions include:

- Time-series cross-validation
- Hyperparameter optimization
- XGBoost or LightGBM forecasting
- ARIMA / SARIMA / Prophet comparison
- Forecasting by region and customer segment
- Prediction intervals and uncertainty estimates
- Feature importance and SHAP explainability
- Supplier risk history and trend monitoring
- True LLM-assisted contract summarization
- Retrieval-Augmented Generation over supplier contracts
- Vector search with FAISS
- Structured LLM output using Pydantic
- API layer using FastAPI
- Authentication and user roles
- PostgreSQL or cloud data warehouse integration
- Airflow orchestration
- dbt transformation layer
- Cloud object storage
- Automated model registry and monitoring
- OR-Tools vehicle routing
- Vehicle capacity constraints
- Delivery time windows
- Multiple depots
- Real traffic and geospatial APIs
- Automated Power BI dataset refresh
- Centralized logging and observability
- Production-grade secrets management

These improvements would move the portfolio solution toward a larger enterprise architecture.

---

## What This Project Demonstrates

From a software and data perspective, the repository demonstrates experience with:

- Python project organization
- Data ingestion and transformation
- pandas-based analytics
- Machine learning
- Feature engineering
- Forecast evaluation
- Mathematical inventory calculations
- Risk scoring
- PDF and document extraction
- OCR integration
- Regex-based parsing
- JSON and CSV generation
- Geospatial distance calculations
- Optimization heuristics
- Streamlit development
- Power BI and Tableau integration
- Automated testing
- Data quality validation
- GitHub Actions
- Docker
- Configuration management
- Technical documentation
- Business-oriented analytical thinking

---

## Disclaimer

This repository is a **portfolio and educational project** designed to demonstrate supply chain analytics, machine learning, optimization, and software engineering concepts.

The datasets and recommendations should not be treated as production procurement, legal, financial, logistics, or inventory decisions without appropriate validation and domain review.

Supplier contract analysis is not legal advice, and automated risk scores should be reviewed by qualified business stakeholders before any real-world action.

---

## Author

**Andrej Pecirep**

Bachelor of Electrical Engineering — Computing and Informatics  
University of Sarajevo — Faculty of Electrical Engineering

GitHub: `AndrejPecirep`

---

## License

This project is provided for portfolio and educational purposes. Add a dedicated license file if you intend to define explicit reuse, modification, or distribution terms.
