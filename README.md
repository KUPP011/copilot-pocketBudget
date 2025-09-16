# PocketBudget

PocketBudget is a personal finance and budgeting application designed to help users track expenses, manage income, and visualize financial health.

## Features
- Track transactions (income and expenses)
- Dashboard with charts and summaries
- SQLite database for data storage
- Streamlit-based web interface

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Running the App
```bash
streamlit run app.py
```

## Project Structure
```
app.py                # Main Streamlit app
models.py             # Database models
repository.py         # Data access layer
pages/                # Streamlit multipage scripts
  1_Transactions.py   # Transactions page
  2_Dashboard.py      # Dashboard page
data/pocket.db        # SQLite database file
requirements.txt      # Python dependencies
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License
This project is licensed under the MIT License.

## Contact
For questions, open an issue or contact the maintainer.
