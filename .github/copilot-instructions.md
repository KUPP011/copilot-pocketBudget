# Pocket Budget - Copilot Instructions

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the information here.**

Pocket Budget is a personal finance tracker built with **Streamlit + SQLite (SQLModel)**. Users can add income/expenses, filter by date/category/type, view dashboards with charts, and export/import CSV data.

## Working Effectively

### Bootstrap and Setup
1. **Python Environment**:
   ```bash
   python --version  # Should show Python 3.12.3 or newer
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Linux/macOS: source .venv/bin/activate
   ```

2. **Install Dependencies** (takes ~30 seconds):
   ```bash
   pip install -r requirements.txt
   ```
   **NEVER CANCEL** - Installation typically takes 30 seconds. Set timeout to 60+ seconds.

3. **Run the Application**:
   ```bash
   # Main application
   streamlit run app.py
   
   # Individual pages (for testing)
   streamlit run pages/1_Transactions.py
   streamlit run pages/2_Dashboard.py
   ```
   Applications start in ~5-10 seconds and run on http://localhost:8501 (or 8502, 8503 for additional instances).

### Build and Test
- **No formal build process** - This is a pure Python Streamlit application
- **No unit tests** - Application relies on manual testing through the UI
- **Syntax validation**:
  ```bash
  python -m py_compile app.py models.py db.py repository.py pages/*.py
  ```
- **NEVER use linting tools** - None are configured (no flake8, black, isort, or pylint)

### Database
- **SQLite database** is automatically created at `data/pocket.db` on first run
- Database initialization is handled automatically by `init_db()` calls in each module
- **No migrations needed** - SQLModel handles schema creation automatically

## Validation Scenarios

**ALWAYS test these scenarios after making changes:**

### 1. Application Startup Validation
```bash
streamlit run app.py --server.headless true --server.port 8501
# Should show: "You can now view your Streamlit app in your browser."
# Test accessibility: curl -I http://localhost:8501
# Should return: HTTP/1.1 200 OK
```

### 2. Database Functionality Test
```bash
python -c "
from db import init_db, get_session
from repository import add_transaction, list_categories, fetch_transactions
from models import TxKind
from datetime import date

init_db()
with get_session() as db:
    tx = add_transaction(db, date=date.today(), description='Test', amount=10.0, kind=TxKind.expense, category_name='Test')
    cats = list_categories(db)
    txs = fetch_transactions(db)
    print(f'✓ Added transaction {tx.id}, {len(cats)} categories, {len(txs)} total transactions')
"
```

### 3. Full User Workflow Test
1. Start the application: `streamlit run app.py`
2. Navigate to "Transactions" page (sidebar)
3. Add a test transaction with amount, description, and category
4. Navigate to "Dashboard" page
5. Verify charts display the new transaction
6. Test CSV export functionality
7. Verify data persists after restart

### 4. Pages Accessibility Test
```bash
# Test each page starts independently
streamlit run pages/1_Transactions.py --server.headless true --server.port 8502 &
streamlit run pages/2_Dashboard.py --server.headless true --server.port 8503 &
# Both should be accessible via curl
```

## File Structure and Navigation

### Key Application Files
- **`app.py`** - Main application home page with summary metrics
- **`models.py`** - SQLModel definitions (Transaction, Category, TxKind enum)
- **`db.py`** - Database engine and session management
- **`repository.py`** - Database operations and business logic
- **`pages/1_Transactions.py`** - Transaction entry and management UI
- **`pages/2_Dashboard.py`** - Charts, analytics, and CSV import/export

### Important Directories
- **`data/`** - SQLite database storage (created automatically, gitignored)
- **`.venv/`** - Python virtual environment (gitignored)
- **`pages/`** - Streamlit multi-page application pages
- **`.github/`** - GitHub configuration and issue templates

### Common Development Patterns
- **Always call `init_db()`** before database operations
- **Use `get_session()`** context manager for database transactions
- **SQLModel handles ORM** - no raw SQL needed
- **Streamlit pages are independent** - each can run standalone
- **Categories are auto-created** when adding transactions
- **All amounts stored as positive floats** - type determined by `kind` field

## Troubleshooting

### Database Issues
- **Database locked**: Ensure no other Streamlit instances are running
- **Missing tables**: `init_db()` will recreate them automatically
- **Data loss**: Database is file-based in `data/pocket.db`

### Import/Export Issues
- **CSV format**: Must have columns: date, description, kind, amount, category (optional)
- **Date format**: Should be parseable by pandas (YYYY-MM-DD recommended)
- **Kind values**: Must be "income" or "expense"

### Streamlit Issues
- **Port conflicts**: Use different `--server.port` values for multiple instances
- **Permission errors**: Ensure write permissions to current directory for `data/` folder
- **Module import errors**: Ensure virtual environment is activated

## Performance Notes
- **Startup time**: ~5-10 seconds for Streamlit to initialize
- **Database operations**: Nearly instantaneous with SQLite
- **CSV operations**: Linear with data size, typically under 1 second for <1000 transactions
- **No caching implemented** - Each page load queries database fresh

## Dependencies
Current dependencies from `requirements.txt`:
- `streamlit` - Web framework
- `sqlmodel` - SQL ORM with Pydantic integration  
- `sqlalchemy` - Database toolkit (SQLModel dependency)
- `pandas` - Data manipulation for CSV and analysis
- `plotly` - Interactive charts and visualizations
- `python-dotenv` - Environment variable management (unused currently)

All dependencies install via pip in ~30 seconds on typical systems.