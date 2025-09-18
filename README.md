# Pocket Budget 💰

A tiny personal finance tracker built with **Streamlit + SQLite (SQLModel)**.
Add income/expenses, filter by date/category/type, see dashboards, and export/import CSV.

## 🤖 For Copilot & AI Coding Assistants

This repository is configured to work effectively with GitHub Copilot and other AI coding assistants. Here's everything you need to know:

### 📁 Repository Structure
```
copilot-pocketBudget/
├── app.py                  # Main Streamlit app (homepage)
├── pages/                  # Streamlit multi-page app
│   ├── 1_Transactions.py   # Transaction management page
│   └── 2_Dashboard.py      # Charts and analytics page
├── models.py               # SQLModel database models (Transaction, Category)
├── db.py                   # Database engine and session management
├── repository.py           # Business logic and database operations
├── tests/                  # Test suite
│   ├── conftest.py         # Pytest fixtures and test database setup
│   ├── test_balance.py     # Balance calculation tests
│   ├── test_categories.py  # Category management tests
│   └── test_ordering.py    # Transaction ordering tests
├── data/                   # SQLite database storage (auto-created)
├── requirements.txt        # Python dependencies
└── .github/workflows/ci.yml # CI/CD pipeline
```

### 🛠 Tech Stack
- **Backend**: Python 3.11+, SQLModel (SQLAlchemy + Pydantic), SQLite
- **Frontend**: Streamlit for web UI
- **Data**: Pandas for data manipulation, Plotly for charts
- **Testing**: Pytest with fixtures for isolated database testing
- **CI/CD**: GitHub Actions for automated testing

### 🏗 Architecture Patterns
- **Models**: `models.py` defines `Transaction` and `Category` SQLModel classes
- **Repository Pattern**: `repository.py` contains all database operations
- **Database**: SQLite with lazy engine creation, test isolation via `POCKET_DB_PATH`
- **Multi-page App**: Streamlit pages in `pages/` directory with number prefixes
- **Separation of Concerns**: DB layer, business logic, and UI are clearly separated

### ⚡ Quick Start

```bash
# Setup environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run tests
export PYTHONPATH=.  # or set PYTHONPATH=. on Windows
pytest

# Run specific test file
pytest tests/test_balance.py -v
```

### 🧪 Testing Guidelines
- **Test Database**: Each test gets an isolated SQLite database via `test_db` fixture
- **Test Structure**: Tests are organized by feature (balance, categories, ordering)
- **Running Tests**: Use `pytest` from project root with `PYTHONPATH=.`
- **CI Pipeline**: Tests run automatically on push/PR via GitHub Actions

### 🎯 Key Functions to Know
- `add_transaction()`: Create income/expense transactions
- `totals()`: Calculate income, expenses, and balance
- `fetch_transactions()`: Retrieve transactions with filtering
- `get_or_create_category()`: Handle category management
- `init_db()`: Initialize database tables

### 🔧 Development Conventions
- **Code Style**: UTF-8 encoding headers on Python files
- **Imports**: Standard library first, then third-party, then local imports  
- **Database**: Use context managers (`with get_session() as db:`)
- **Error Handling**: Validate inputs (e.g., non-empty category names)
- **Enums**: Use `TxKind.income` / `TxKind.expense` for transaction types

### 🗄 Database Schema
```python
# Transaction model
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    date: date
    description: str
    amount: float  # Always positive, type determined by 'kind'
    kind: TxKind   # "income" or "expense"
    category_id: Optional[int] = Field(foreign_key="category.id")

# Category model  
class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
```

### 🌐 Environment Variables
- `POCKET_DB_PATH`: Override default database location (useful for testing)

### 📦 Dependencies
Core dependencies in `requirements.txt`:
- `streamlit`: Web framework
- `sqlmodel`: Database ORM
- `pandas`: Data manipulation  
- `plotly`: Interactive charts
- `python-dotenv`: Environment variables

### 🚀 Deployment Notes
- Database auto-creates in `data/pocket.db`
- Streamlit runs on port 8501 by default
- No external database required - SQLite is embedded

This setup ensures AI assistants can understand the codebase structure, testing patterns, and development workflow for effective code generation and modifications.
