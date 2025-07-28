# SQL-Project-Retail-Bank-Analysis
This project, "Retail Bank Customer Transaction Analysis," uses Python's Faker to generate realistic bank customer, account, and transaction data. SQL queries are then applied to analyze spending patterns, identify top customers, detect potential fraud, monitor account health, and create insightful reports for bank management.

Features:
---
Data Generation: Python script to create synthetic customer, account, and transaction data.

Database Setup: Uses SQLite for a lightweight, file-based relational database.

Customer Insights: Analyze customer demographics and account distribution.

Transaction Analysis: Understand spending habits, popular categories, and transaction volumes.

Fraud Detection: Identify unusual transaction patterns.

Reporting: Generate summarized reports for bank management.

Database Schema
---
The project uses three main tables:

Customers: Stores customer personal information.

Accounts: Stores bank account details, linked to customers.

Transactions: Records all financial transactions for each account.

Detailed schema with columns and data types is available in the bank_data.py script.

Getting Started:
---

Prerequisites
---
Python 3.x

pip (Python package installer)

VS Code (Visual Studio Code)

VS Code SQLite Extension (by alexcvzz)

Installation
---


Clone the Repository:
---
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
---

Create and Activate Virtual Environment:
---
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

Install Dependencies:
---
pip install faker


How to Run
---
Save the full bank_data.py script in your project root.

Ensure your virtual environment is activated.

Run from your terminal:

python bank_data.py


SQL Analysis
---
After data generation, use the VS Code SQLite extension to explore retail_bank.db.

Connecting in VS Code
Open SQLite Explorer sidebar.

Click "Open Database" and select retail_bank.db.

Right-click on the database and select "New Query" to run SQL.

Example SQL Queries
---
Total Bank Balance:
---
SELECT SUM(current_balance) FROM Accounts;

Top 5 Spending Categories:
---
SELECT category, SUM(amount) AS total_spent
FROM Transactions
WHERE transaction_type = 'Purchase'
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;

Customers with Multiple Accounts:
---
SELECT c.first_name, c.last_name, COUNT(DISTINCT a.account_type) AS num_types
FROM Customers c JOIN Accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id HAVING COUNT(DISTINCT a.account_type) > 1;

Future Enhancements
---
More advanced fraud detection algorithms.

Integration with data visualization tools.

Building a simple web interface for data interaction.

License
---
This project is open-source and available under the MIT License.
