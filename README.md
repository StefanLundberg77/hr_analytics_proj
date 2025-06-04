# HiRe™ – HR Analytics Dashboard

_Final Project in Data Engineering 2 @OPA24 (Object-Oriented Programming with AI)_

A proof of concept for an interactive HR analytics platform using **Streamlit**, **dbt**, **DuckDB**, and **Google Gemini**.

---

## 📝 Project Description

HiRe™ is a talent intelligence tool for recruiters, powered by real-time data and AI analysis. It enables you to:

- Browse job openings by sector (Data/IT, Social Work, Security)
- Visualize KPIs and trends in job ads
- Analyze job descriptions using Gemini (LLM) for top hard & soft skills
- Compare role-specific soft skills with field averages via spider charts
- Present insights in an HR-report tone, designed for decision-makers

---

## 🚀 How to Run

#### 1. Clone the repository

```git clone``` https://github.com/StefanLundberg77/hr_analytics_proj.git

Navigate to project root:

```cd hr_analytics_proj```

#### 2. Create a virtual environment

```uv venv .venv```

#### 3. Activate the environment

Windows:

```.venv\Scripts\activate```

macOS/Linux:

```source .venv/bin/activate```

#### 4. Install dependencies

Windows:

```uv pip install -r requirements.txt```

macOS/Linux:

```uv pip install -r requirements.mac.txt```

#### 5. Fetch data from the JobAds API

```python load_api.py```

Or run ```load_api.py``` directly in your IDE.

#### 6. Run the Streamlit dashboard

```streamlit run app.py```

## 🔧 Configuration & DuckDB Profile

Setup your ```profiles.yml``` for DBT:

```yaml
project_HiRe:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ../ads_data_warehouse.duckdb
      threads: 1

    prod:
      type: duckdb
      path: prod.duckdb
      threads: 4

```

DuckDB is file-based and requires no server or setup.

## 📄 DBT Testing & Schema Validation

This project uses DBT ```.sql``` tests and schema ```.yml``` files to ensure data quality and pipeline stability.

#### ✅ Example test types:

- ```not_null```: Ensures required fields are populated

- ```unique```: Prevents duplicate records

- ```accepted_values```: Validates field value ranges

#### 📂 Schema files

- src_schema.yml

- dim_schema.yml

#### 🧪 SQL Tests

- test_mart_duplicate_job_details.sql

- test_mart_no_duplicates.sql

- test_surrogate_key.sql

#### ▶️ Run tests:

#### Full pipeline with models + tests:
- ```dbt build```

#### Or step-by-step:
- ```dbt run```      # Run models

- ```dbt test```     # Run all tests

```check_materialization_models.py```

- Prints a list of all dbt models with their materialization type for quick debugging from the manifest.json file. Run it directly in your IDE.

## 🧠 Gemini API Integration

Get your API key from Google Gemini API Console:

https://ai.google.dev/gemini-api/docs/api-key

1. Create a .env file in your project root:

```.env```

2. In your ```.env```store API key:

```GEMINI_API_KEY=your-api-key-here```

3. The API key is loaded via ```python-dotenv```

Note: Add ```.env``` to ```.gitignore``` to avoid exposing secrets.

## 🖥️ Streamlit UI Features

The project includes a Streamlit dashboard for:

- Visualizing job ads by category and region

- Generating AI-powered skill summaries

- Comparing soft skills with field averages using radar charts

- Delivering insights in a polished HR report tone

### Launch it with:

```streamlit run app.py```

#### 👥 Contributors

Stefan Lundberg – StefanLundberg77

Susanna Rokka – SusannR11

Richard Norrman – richardnorrman

Caroline Helmvee – linehanna


