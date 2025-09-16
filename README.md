# Pocket Budget 💰

A simple yet powerful personal finance tracker built with **Streamlit** and **SQLite**. Track your income and expenses, organize transactions by categories, visualize your financial data with interactive charts, and manage your budget with ease.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## ✨ Features

- **📊 Financial Tracking**: Record income and expenses with detailed descriptions
- **🏷️ Category Management**: Organize transactions by custom categories
- **📈 Interactive Dashboard**: Visualize your financial data with charts and graphs
- **📅 Date Filtering**: Filter transactions by date ranges
- **💾 Data Export/Import**: Export your data to CSV or import existing financial data
- **🖥️ Web Interface**: Clean, intuitive web-based user interface
- **💾 Local Storage**: All data stored locally in SQLite database - your privacy is protected

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KUPP011/copilot-pocketBudget.git
   cd copilot-pocketBudget
   ```

2. **Create and activate a virtual environment**
   
   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   The application will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Adding Transactions

1. Navigate to the **Transactions** page using the sidebar
2. Fill in the transaction details:
   - **Date**: Select the transaction date
   - **Description**: Add a meaningful description (e.g., "Groceries at Walmart")
   - **Type**: Choose between "Income" or "Expense"
   - **Amount**: Enter the transaction amount
   - **Category**: Select an existing category or create a new one
3. Click **Submit** to save the transaction

### Viewing Dashboard

1. Go to the **Dashboard** page
2. View your financial summary with:
   - **Total Income**: Sum of all income transactions
   - **Total Expenses**: Sum of all expense transactions
   - **Current Balance**: Income minus expenses
   - **Category Breakdown**: Visual charts showing spending by category
   - **Monthly Trends**: Track your financial patterns over time

### Data Management

- **Export Data**: Download your transactions as a CSV file from the Dashboard
- **Import Data**: Upload a CSV file with columns: `date`, `description`, `kind`, `amount`, `category`

## 🏗️ Project Structure

```
copilot-pocketBudget/
├── app.py              # Main application entry point
├── db.py               # Database configuration and connection
├── models.py           # SQLModel data models (Transaction, Category)
├── repository.py       # Database operations and queries
├── requirements.txt    # Python dependencies
├── data/              # SQLite database storage
└── pages/             # Streamlit pages
    ├── 1_Transactions.py  # Transaction management page
    └── 2_Dashboard.py     # Analytics and visualization page
```

## 🛠️ Technical Details

### Built With

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: SQL database operations with Python type hints
- **[SQLite](https://sqlite.org/)**: Lightweight database engine
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[Plotly](https://plotly.com/)**: Interactive data visualization
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)**: Environment variable management

### Database Schema

The application uses two main tables:

- **Categories**: Store transaction categories (id, name)
- **Transactions**: Store financial transactions (id, date, description, amount, kind, category_id, created_at)

## 🔧 Development

### Setting up Development Environment

1. Follow the installation steps above
2. The application will automatically create the SQLite database on first run
3. Make changes to the code - Streamlit will hot-reload automatically

### Running Tests

Currently, the project focuses on simplicity and doesn't include automated tests. Manual testing can be done by:

1. Adding sample transactions
2. Verifying data persistence
3. Testing CSV export/import functionality
4. Checking dashboard visualizations

## 📝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Application won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the virtual environment is activated

**Database errors:**
- The `data/` directory and SQLite database are created automatically
- If you encounter database issues, try deleting the `data/` folder and restarting

**Port already in use:**
- Use a different port: `streamlit run app.py --server.port 8502`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/KUPP011/copilot-pocketBudget/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, operating system, and error messages

---

**Made with ❤️ using Streamlit** - Start tracking your finances today!
