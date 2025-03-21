# Data Pipeline Automation System - Alpha Vantage

This project is an end-to-end ETL pipeline that scrapes financial data from public APIs, transforms it using pandas, loads it into a SQL database, and visualizes insights through a dashboard. The entire system will be containerized using Docker.

## Project Kanban 

You can see all tasks that I executed to develop this project on this [link](https://github.com/users/pdrals16/projects/1)

## How the project works

The project leverages Alpha Vantage's financial APIs to collect stock market data and company information. The core functionality is implemented in the AlphaVantage class which handles API requests with proper error handling and logging.

### Core Files

#### api.py

This file contains the AlphaVantage class which is responsible for interfacing with the Alpha Vantage API. It provides methods to:

* Initialize with a stock symbol
* Make API requests with proper error handling
* Fetch daily stock time series data
* Retrieve company overview information

The class uses environment variables for configuration and implements comprehensive logging to track API interactions.

#### transform.py

This file contains functions responsible for transforming the data from raw JSON to structured formats:

* read_daily_stock_json: Parses daily stock time series JSON and converts it into a list of dictionaries with standardized fields (date, open, high, low, close, volume)
* read_company_overview_json: Extracts company overview information from JSON files
* read_columns: Renames dataframe columns based on a JSON mapping file reference
* save_as_csv: Exports processed data to CSV files with specified mode (append/overwrite)

These transformation functions work in conjunction with the API data fetching to create a clean, structured dataset ready for analysis and storage.


## Database Setup

The project uses PostgreSQL as its database, containerized with Docker for easy deployment and consistency across environments.

### PostgreSQL Database

The database is configured with the following credentials:
- **Username**: postgres
- **Password**: postgres
- **Database Name**: postgres
- **Port**: 5432

### Starting the Database

You can start the PostgreSQL database using Docker Compose:

```bash
make up
```

This command will start the PostgreSQL container in detached mode. Other useful commands include:

- `make up-logs`: Start containers and follow logs
- `make down`: Stop and remove containers
- `make restart`: Restart all containers
- `make logs`: View PostgreSQL container logs
- `make ps`: List running containers
- `make psql`: Connect to PostgreSQL with psql
- `make clean`: Remove containers, volumes, and images

### Connecting to the Database

To connect to the PostgreSQL instance:

```bash
make psql
```

This will open a psql session with the correct credentials already provided.

## Deliverables

This is a list of all deliverables from the project:

1. Complete source code in a GitHub repository
2. Docker containers for easy deployment
3. Documentation and setup instructions
4. Demo dashboard with sample insights
