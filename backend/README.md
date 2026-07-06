# QuantFlow

A comprehensive financial data pipeline application for ingesting, processing, and analyzing financial market data. QuantFlow automates the collection of market data from providers like Yahoo Finance, applies data quality transformations, and prepares it for analysis and forecasting.

## 🎯 Project Overview

QuantFlow is a production-ready data pipeline system designed to:

- **Ingest** historical market data from multiple data sources (Yahoo Finance, Alpha Vantage, etc.)
- **Validate** and **process** raw market data using sophisticated validation and transformation rules
- **Store** data in organized layers (raw, processed, curated) for different use cases
- **Orchestrate** complex data workflows through configurable pipelines
- **Monitor** pipeline execution with comprehensive logging and status tracking
- **Forecast** market trends using preprocessed data (future feature)

## 🏗️ Architecture

QuantFlow follows a modular, layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         FastAPI (REST API)              │
│      Dashboard & Worker Apps            │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Pipeline Orchestration Layer         │
│ (Historical Ingestion, Preprocessing)   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│       Business Logic Services           │
│  (Ingestion, Preprocessing, Analysis)   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│  Storage Layer & Repositories           │
│     (Data Access Abstraction)           │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    File System Storage                  │
│  (Raw, Processed, Curated Layers)       │
└─────────────────────────────────────────┘
```

### Key Design Patterns

- **Provider Pattern**: Abstract data source interfaces for easy extensibility
- **Repository Pattern**: Data access abstraction with file-based persistence
- **Pipeline Pattern**: Modular task orchestration with status tracking
- **Aggregator Pattern**: Batch result collection and error handling
- **Validator Pattern**: Multi-layer data quality enforcement

## ✨ Features

### Data Ingestion
- ✅ Async HTTP client for efficient data fetching
- ✅ Rate limiting and retry logic with exponential backoff
- ✅ Multiple data provider support (Yahoo Finance, Alpha Vantage)
- ✅ Comprehensive data validation
- ✅ Error aggregation and detailed reporting

### Data Processing
- ✅ OHLCV (Open, High, Low, Close, Volume) data normalization
- ✅ Duplicate record detection and removal
- ✅ Timestamp validation and sorting
- ✅ Data quality metrics and validation
- ✅ Metadata extraction and enrichment

### Pipeline Management
- ✅ Async pipeline execution for high concurrency
- ✅ Status tracking (PENDING → RUNNING → SUCCESS/FAILED/PARTIAL_SUCCESS)
- ✅ Graceful error handling and recovery
- ✅ Hierarchical logging with context
- ✅ Configurable batch processing

### Storage
- ✅ Multi-layer storage organization (raw, processed, curated)
- ✅ JSON-based persistence with fast I/O (orjson)
- ✅ Provider-based data partitioning
- ✅ List and query operations on stored data
- ✅ Transaction-like save/load/delete operations

### Testing
- ✅ Comprehensive pytest suite with 150+ tests
- ✅ Async test support with pytest-asyncio
- ✅ Mock-based unit testing
- ✅ Integration test coverage
- ✅ Edge case and error scenario testing

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **pip**: Python package manager
- **Git**: For version control

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/quantflow.git
cd quantflow/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Development Dependencies (Optional)

```bash
pip install pytest pytest-asyncio pytest-cov
```

### 5. Set Up Configuration

Create a `.env` file in the backend directory (or configure environment variables):

```env
# Storage Configuration
DATASET_DIR=./datasets

# Ingestion Configuration
YAHOO_BASE_URL=https://query1.finance.yahoo.com
YAHOO_RANGE=5y
YAHOO_INTERVAL=1d
API_TIMEOUT=10

# Logging
LOG_LEVEL=INFO
```

## 📁 Project Structure

```
backend/
├── apps/                           # Application entry points
│   ├── api/                        # FastAPI REST API application
│   ├── dashboard/                  # Web dashboard application
│   └── worker/                     # Background job worker
├── pipelines/                      # Pipeline orchestration
│   ├── historical_ingestion/       # Historical data ingestion pipeline
│   ├── preprocessing/              # Data preprocessing pipeline
│   ├── feature_engineering/        # Feature extraction pipeline
│   ├── orchestration/              # Pipeline coordination
│   └── re_training/                # Model retraining pipeline
├── services/                       # Business logic services
│   ├── ingestion/                  # Data source abstraction
│   │   ├── providers/              # Data providers (Yahoo, AV, etc.)
│   │   ├── validators/             # Data validation
│   │   └── aggregators/            # Result aggregation
│   ├── preprocessing/              # Data transformation
│   │   ├── preprocessors/          # Data normalizers
│   │   ├── validators/             # Quality validation
│   │   └── aggregators/            # Result aggregation
│   ├── transformation/             # Advanced transformations
│   ├── forecasting/                # Forecasting models
│   ├── analytics/                  # Analytics and metrics
│   └── exports/                    # Data export functionality
├── storage/                        # Data persistence layer
│   ├── repositories/               # Data repository patterns
│   ├── models/                     # Database models
│   ├── schemas/                    # Storage schemas
│   ├── migrations/                 # Database migrations
│   └── seed/                       # Initial data
├── datasets/                       # Data storage
│   ├── raw/                        # Raw ingested data
│   ├── processed/                  # Cleaned and normalized data
│   └── curated/                    # Final analysis-ready data
├── shared/                         # Shared utilities
│   ├── config/                     # Configuration management
│   ├── constants/                  # Application constants
│   ├── decorators/                 # Function decorators
│   ├── enums/                      # Enumerated types
│   ├── exceptions/                 # Custom exceptions
│   ├── models/                     # Shared data models
│   └── utils/                      # Utility functions
├── tests/                          # Comprehensive test suite
│   ├── services/                   # Service layer tests
│   ├── pipelines/                  # Pipeline tests
│   ├── storage/                    # Storage layer tests
│   └── app/                        # Application tests
├── infrastructure/                 # Infrastructure code
│   ├── docker/                     # Docker configuration
│   ├── terraform/                  # Infrastructure as Code
│   └── monitoring/                 # Monitoring and alerting
├── logs/                           # Application logs
├── notebook/                       # Jupyter notebooks for exploration
├── compose.yaml                    # Docker Compose configuration
├── Dockerfile                      # Docker image definition
├── pyproject.toml                  # Python project configuration
├── requirements.txt                # Python dependencies
└── pytest.ini                      # Pytest configuration
```

## 🔄 Pipeline Overview

### Historical Ingestion Pipeline

Fetches historical market data from configured data providers and stores it in the raw layer.

**Flow:**
1. Load symbols from configuration
2. Create async tasks for each symbol
3. Fetch data from provider (with retries)
4. Validate response data
5. Aggregate results (successful/failed)
6. Persist raw data to repository
7. Update pipeline status

**Example:**
```python
python -m pipelines.historical_ingestion.main
```

**Configuration:** `pipelines/historical_ingestion/config.py`

### Preprocessing Pipeline

Transforms raw data into clean, normalized datasets ready for analysis.

**Flow:**
1. Load raw data from repository
2. Extract metadata from each record
3. Process OHLCV records:
   - Remove duplicates
   - Validate data quality (OHLC ranges)
   - Sort by timestamp
   - Filter incomplete records
4. Validate complete dataset
5. Aggregate results
6. Persist processed data
7. Update pipeline status

**Example:**
```python
python -m pipelines.preprocessing.main
```

**Configuration:** `pipelines/preprocessing/config.py`

### Feature Engineering Pipeline

Derives additional features from preprocessed data for forecasting models.

**Status:** In development

### Retraining Pipeline

Periodically retrains forecasting models with updated data.

**Status:** In development

## 📊 Data Models

### Core Models

**PriceRecord**
```python
symbol: str
timestamp: datetime
open: float
high: float
low: float
close: float
volume: int
```

**PreprocessedSymbol**
```python
symbol: str
asset_type: AssetType
currency: str
metadata: MetaData
records: list[PriceRecord]
```

**Result**
```python
successful: dict[str, Any]
failed: dict[str, str]
```

**PipelineStatus**
- `PENDING`: Initial state
- `RUNNING`: Currently executing
- `SUCCESS`: All tasks succeeded
- `FAILED`: All tasks failed
- `PARTIAL_SUCCESS`: Some tasks succeeded, some failed

### Data Layers

**RAW Layer**
- Direct API responses from data providers
- Minimal validation
- Storage: `datasets/raw/{provider}/{symbol}.json`

**PROCESSED Layer**
- Cleaned, normalized, validated data
- Duplicates removed
- Timestamps sorted
- Storage: `datasets/processed/{provider}/{symbol}.json`

**CURATED Layer**
- Analysis-ready datasets
- Features engineered
- Ready for modeling
- Storage: `datasets/curated/{provider}/{symbol}.json`

## ⚙️ Configuration

### Storage Configuration

**File:** `shared/config/storage_config.py`

```python
DATASET_DIR: Path = Path(__file__).parent.parent.parent / "datasets"
```

### Ingestion Configuration

**File:** `shared/config/ingestion_config.py`

Key settings:
- `BASE_URL`: Yahoo Finance API endpoint
- `YAHOO_RANGE`: Historical data range (e.g., "5y", "10y", "max")
- `YAHOO_INTERVAL`: Data interval (e.g., "1d", "1h")
- `API_TIMEOUT`: Request timeout in seconds
- `DEFAULT_HEADERS`: HTTP headers for API requests

### Preprocessing Configuration

**File:** `pipelines/preprocessing/config.py`

Key settings:
- Validation thresholds
- Symbol batches to process
- Error tolerance levels

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Module

```bash
pytest tests/services/ingestion/ -v
pytest tests/pipelines/historical_ingestion/ -v
pytest tests/storage/repositories/ -v
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

### Run Async Tests

```bash
pytest tests/pipelines/ -v
```

### Test Statistics

- **Total Tests**: 150+
- **Service Tests**: 97
- **Pipeline Tests**: 45
- **Storage Tests**: 35
- **Coverage**: Comprehensive unit and integration coverage

### Test Organization

```
tests/
├── services/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── transformation/
│   └── forecasting/
├── pipelines/
│   ├── historical_ingestion/
│   └── preprocessing/
├── storage/
│   └── repositories/
└── app/
    └── api/
```

## 📝 Usage Examples

### Ingesting Historical Data

```python
import asyncio
from shared.config.storage_config import DATASET_DIR
from shared.models.ingestion_models import YahooConfig
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator
from services.ingestion.aggregators.yahoo_aggregator import YahooAggregator
from storage.repositories.data_repository import DataRepository
from pipelines.historical_ingestion.pipeline import HistoricalIngestion
from shared.enums.datasource import DataSource
from shared.utils.logger import get_logger

async def ingest_data():
    logger = get_logger("Ingestion")
    
    config = YahooConfig(
        base_url="https://query1.finance.yahoo.com",
        range="5y",
        interval="1d",
        timeout=10,
        source=DataSource.YAHOO,
    )
    
    provider = YahooProvider(logger, YahooValidator(), config)
    aggregator = YahooAggregator(logger)
    repository = DataRepository(DATASET_DIR)
    
    symbols = ["AAPL", "MSFT", "GOOGL"]
    from shared.models.ingestion_models import MarketSymbol
    market_symbols = [MarketSymbol(ticker=s) for s in symbols]
    
    pipeline = HistoricalIngestion(
        symbols=market_symbols,
        logger=logger,
        provider=provider,
        aggregator=aggregator,
        repository=repository
    )
    
    result = await pipeline.run()
    print(f"Successful: {len(result.successful)}")
    print(f"Failed: {len(result.failed)}")

asyncio.run(ingest_data())
```

### Processing Data

```python
from pipelines.preprocessing.main import main

# Run preprocessing pipeline
main()
```

### Loading Data

```python
from storage.repositories.data_repository import DataRepository
from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource

repository = DataRepository(root_dir="./datasets")

# Load processed data
data = repository.load(
    layer=DataLayer.PROCESSED,
    provider=DataSource.YAHOO,
    key="AAPL"
)

print(data)
```

## 🔍 Logging

QuantFlow uses Python's built-in logging with hierarchical loggers:

```python
from shared.utils.logger import get_logger

logger = get_logger("HistoricalIngestion")
child_logger = logger.getChild("YahooProvider")
```

**Log Levels:**
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages for potentially problematic situations
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

## 🐳 Docker

### Build Docker Image

```bash
docker build -f Dockerfile -t quantflow:latest .
```

### Run with Docker Compose

```bash
docker-compose up
```

### View Logs

```bash
docker-compose logs -f backend
```

## 📦 Dependencies

**Core Dependencies:**
- `aiohttp==3.13.5`: Async HTTP client for data fetching
- `orjson==3.11.9`: Fast JSON serialization/deserialization
- `pandas==3.0.3`: Data manipulation and analysis
- `tenacity==9.1.4`: Retry logic with exponential backoff

**Development Dependencies:**
- `pytest==9.0.3`: Testing framework
- `pytest-asyncio==0.24.0`: Async test support
- `pytest-cov==5.0.0`: Code coverage
- `mypy`: Static type checking
- `deptry`: Dependency validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 conventions
- Use type hints for all functions
- Write docstrings for public functions
- Add unit tests for new features
- Run pytest before submitting PR

## 🐛 Troubleshooting

### API Rate Limiting

If you encounter rate limiting errors from Yahoo Finance:
- The system implements exponential backoff with retries
- Adjust `API_TIMEOUT` in configuration
- Space out requests by processing fewer symbols per run

### Data Validation Errors

If data validation fails:
- Check the error logs for specific validation failures
- Review the OHLC ranges and timestamp ordering
- Ensure data source is responding correctly

### Import Errors

```bash
# Ensure you're in the backend directory
cd backend

# Verify virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Development Team**: QuantFlow Contributors

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for usage examples

## 🚀 Future Enhancements

- [ ] Multiple data provider support (Alpha Vantage, IEX Cloud, etc.)
- [ ] Machine learning forecasting models
- [ ] Real-time data ingestion
- [ ] WebSocket support for live data
- [ ] GraphQL API alternative
- [ ] Distributed processing (Spark, Dask)
- [ ] Advanced analytics dashboard
- [ ] Model performance tracking
- [ ] A/B testing framework
- [ ] Data quality monitoring

## 📚 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Tenacity Retry Library](https://tenacity.readthedocs.io/)

---

**Last Updated**: June 2026  
**Version**: 0.1.0  
**Status**: Active Development
