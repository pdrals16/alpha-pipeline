# Alpha Vantage Financial Data Pipeline

A complete ETL pipeline that extracts financial data from Alpha Vantage API, transforms it using Python, and loads it into a PostgreSQL database. The system is orchestrated using Apache Airflow and containerized with Docker.

## Project Overview

This pipeline extracts two main types of financial data:
- Daily stock time series (open, high, low, close, volume)
- Company overview information (fundamentals, metrics, ratings)

The system follows a modular architecture with clear separation of concerns:
- API interaction
- Data transformation
- Database operations

## Core Components

### Data Extraction
- `AlphaVantage` class handles API requests with proper error handling and logging
- Supports both daily time series and company overview data
- Flexible configuration via environment variables

### Data Transformation
- JSON parsing into structured formats
- Column standardization with a consistent naming convention
- Storage in intermediate CSV format

### Data Loading
- PostgreSQL database with tables for daily stock data and company overviews
- Upsert operations with configurable unique keys
- Automatic table creation if needed

### Orchestration
- Airflow DAGs for regular and full historical data loads
- Task groups organized by stock symbol
- Configurable stock symbols via YAML configuration

## Project Structure

```
.
├── .github/workflows      # CI/CD pipeline for deployment
├── .infra                 # Infrastructure configuration
│   ├── airflow           # Airflow Docker configuration
│   ├── docker-compose.yml # Container orchestration
│   ├── init-scripts      # Database initialization scripts
│   └── Makefile          # Utility commands
└── airflow               # Airflow DAGs and application code
    ├── dags              # Airflow DAG definitions
    │   └── alpha         # Alpha Vantage specific DAGs
    │       ├── src       # Source code for ETL operations
    │       └── symbols.yaml # Stock symbols configuration
    ├── data              # Data storage (raw, bronze)
    └── logs              # Airflow logs
```

## Environment Configuration

Create a `.env` file in the `.infra` directory with the following variables:

```
ALPHA_API=your_api_key
ALPHA_URL=https://www.alphavantage.co/query
POSTGRES_HOST=your_host
POSTGRES_PORT=5432
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=your_airflow_user
_AIRFLOW_WWW_USER_PASSWORD=your_airflow_password
```

## Deployment

The project uses GitHub Actions for CI/CD, automatically deploying to a VPS on pushes to the main branch. The deployment workflow:
1. Checks out the code
2. Sets up SSH access to the VPS from Github Secrets
3. Set up the environment file from Github Secrets
4. Pulls the latest code and restarts the services

## Local Development

### Prerequisites
- Docker and Docker Compose
- Make

### Starting the Services

```bash
cd .infra
make up
```

### Additional Commands

- `make up-logs`: Start with logs
- `make down`: Stop services
- `make restart`: Restart services
- `make logs`: View PostgreSQL logs
- `make ps`: List containers
- `make psql`: Connect to PostgreSQL
- `make clean`: Remove containers, volumes, and images

## Airflow Interface

Access the Airflow web interface at `http://localhost:8080` with the credentials specified in your `.env` file.

Available DAGs:
- `alpha_daily_stocks`: Daily updates of stock prices
- `alpha_daily_stocks_full_load`: Full historical load of stock prices
- `alpha_company_overview`: Company information updates
