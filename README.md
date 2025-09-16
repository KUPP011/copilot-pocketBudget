# Pocket Budget 💰

A tiny personal finance tracker built with **Streamlit + SQLite (SQLModel)**.
Add income/expenses, filter by date/category/type, see dashboards, and export/import CSV.

## Quick Start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Configuration for Copilot Coding Agent

This section provides essential information for AI coding assistants working on this repository.

### Project Overview
- **Framework**: Streamlit web application
- **Database**: SQLite with SQLModel ORM
- **Primary Language**: Python 3.7+
- **UI Framework**: Streamlit with Plotly for charts
- **Architecture**: Simple MVC pattern with repository layer

### Project Structure
```
copilot-pocketBudget/
├── app.py                 # Main Streamlit app (home page)
├── db.py                 # Database connection and initialization
├── models.py             # SQLModel data models (Transaction, Category)
├── repository.py         # Data access layer (CRUD operations)
├── requirements.txt      # Python dependencies
├── pages/               # Streamlit multi-page structure
│   ├── 1_Transactions.py # Transaction management page
│   └── 2_Dashboard.py   # Charts and data export/import
└── data/               # SQLite database storage (auto-created)
```

### Key Files and Components

#### Core Files
- **`app.py`**: Main entry point, displays summary metrics
- **`models.py`**: Defines `Transaction` and `Category` SQLModel classes
- **`db.py`**: Database session management and initialization
- **`repository.py`**: Contains all database operations (add_transaction, get_transactions, etc.)

#### Pages
- **`pages/1_Transactions.py`**: CRUD interface for transactions
- **`pages/2_Dashboard.py`**: Analytics, charts, CSV import/export

### Development Guidelines

#### Code Style
- Follow PEP 8 conventions
- Use type hints where possible
- Import SQLModel classes from `models.py`
- Database operations should go through `repository.py` functions
- Use `get_session()` context manager for database access

#### Database Operations
```python
# Always use the repository pattern
from db import get_session
from repository import add_transaction, fetch_transactions, list_categories

with get_session() as db:
    transactions = fetch_transactions(db)
    categories = list_categories(db)
    # Database operations here
```

#### Key Repository Functions
- `add_transaction()`: Create new transaction
- `fetch_transactions()`: Query transactions with filters
- `df_transactions()`: Get transactions as pandas DataFrame
- `category_totals()`: Aggregate spending by category
- `monthly_trend()`: Get monthly income/expense trends
- `delete_transaction()`: Remove transaction by ID
- `get_or_create_category()`: Find or create category
- `list_categories()`: Get all categories

#### Adding New Features
1. Model changes go in `models.py`
2. Database operations go in `repository.py`  
3. UI components go in appropriate page files
4. Use Streamlit's session state for form handling
5. Follow existing patterns for error handling

#### Dependencies
- `streamlit`: Web UI framework
- `sqlmodel`: ORM and database models
- `sqlalchemy`: Database engine (via SQLModel)
- `pandas`: Data manipulation for CSV operations
- `plotly`: Interactive charts
- `python-dotenv`: Environment configuration (if needed)

### Common Tasks

#### Adding a New Transaction Field
1. Update `Transaction` model in `models.py`
2. Add migration logic in `db.py` if needed
3. Update repository functions in `repository.py`
4. Modify forms in `pages/1_Transactions.py`

#### Adding New Charts
1. Create query function in `repository.py`
2. Add chart component in `pages/2_Dashboard.py`
3. Use Plotly Express for consistency

#### Database Schema
```python
# Transaction model structure
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    description: str
    amount: float  # store as positive; type captured by 'kind'
    kind: TxKind = Field(default=TxKind.expense)  # "income" or "expense"
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Category model structure  
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
```

### Testing
Currently no automated tests exist. When adding tests:
- Use pytest for testing framework
- Test database operations with temporary SQLite database
- Mock Streamlit components for UI testing

### Build and Deployment
- No build step required (Python interpreted)
- Run with `streamlit run app.py`
- Database file created automatically in `data/` directory
- All dependencies listed in `requirements.txt`
