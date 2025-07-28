from faker import Faker
import sqlite3
from datetime import date, datetime, timedelta
import random

fake = Faker()

# 1. Connect to SQLite database (creates one if it doesn't exist)
conn = sqlite3.connect('retail_bank.db')
cursor = conn.cursor()

# 2. Re-create tables (for demonstration, in a real scenario you might just connect)
cursor.execute('''
    DROP TABLE IF EXISTS Transactions;
''')
cursor.execute('''
    DROP TABLE IF EXISTS Accounts;
''')
cursor.execute('''
    DROP TABLE IF EXISTS Customers;
''')

cursor.execute('''
    CREATE TABLE Customers (
        customer_id INT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        date_of_birth DATE,
        email VARCHAR(100) UNIQUE,
        account_open_date DATE NOT NULL
    );
''')
cursor.execute('''
    CREATE TABLE Accounts (
        account_id INT PRIMARY KEY,
        customer_id INT NOT NULL,
        account_type VARCHAR(50) NOT NULL,
        current_balance DECIMAL(18, 2) NOT NULL,
        currency VARCHAR(3) NOT NULL DEFAULT 'USD',
        status VARCHAR(20) NOT NULL DEFAULT 'Active',
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    );
''')
cursor.execute('''
    CREATE TABLE Transactions (
        transaction_id INT PRIMARY KEY,
        account_id INT NOT NULL,
        transaction_date DATETIME NOT NULL,
        transaction_type VARCHAR(50) NOT NULL,
        amount DECIMAL(18, 2) NOT NULL,
        merchant VARCHAR(255),
        category VARCHAR(100),
        location VARCHAR(255),
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    );
''')
conn.commit()

# 3. Generate and Insert Customers
print("Generating and inserting Customers...")
num_customers = 50
customers_to_insert = []
for i in range(1, num_customers + 1):
    dob = fake.date_of_birth(minimum_age=18, maximum_age=70)
    account_open_date = fake.date_between(start_date='-15y', end_date='-1y')
    customers_to_insert.append((i, fake.first_name(), fake.last_name(), dob, fake.email(), account_open_date))

cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?)", customers_to_insert)
conn.commit()
print(f"Inserted {len(customers_to_insert)} customers.")

# 4. Generate and Insert Accounts
print("Generating and inserting Accounts...")
accounts_to_insert = []
account_id_counter = 1
account_types = ['Checking', 'Savings', 'Credit Card']
customer_ids = [c[0] for c in customers_to_insert] # Get customer IDs

for cust_id in customer_ids:
    num_accounts = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1], k=1)[0]
    for _ in range(num_accounts):
        acc_type = random.choice(account_types)
        balance = round(random.uniform(100, 10000) if acc_type != 'Credit Card' else random.uniform(-5000, 0), 2)
        accounts_to_insert.append((account_id_counter, cust_id, acc_type, balance, 'USD', 'Active'))
        account_id_counter += 1

cursor.executemany("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)", accounts_to_insert)
conn.commit()
print(f"Inserted {len(accounts_to_insert)} accounts.")

# Get all account IDs for transaction generation
all_account_ids = [acc[0] for acc in accounts_to_insert]


# 5. Generate and Insert Transactions
print("Generating and inserting Transactions...")
num_transactions = 1000 # Keep it reasonable for quick demo
transactions_to_insert = []
transaction_id_counter = 1
transaction_types = ['Purchase', 'Deposit', 'Withdrawal', 'Transfer']
merchants = ['Amazon', 'Walmart', 'Starbucks', 'Shell', 'Local Restaurant', 'Online Subscription']
categories = ['Groceries', 'Utilities', 'Entertainment', 'Salary', 'Rent', 'Shopping', 'Transport', 'Healthcare']

for _ in range(num_transactions):
    account_id = random.choice(all_account_ids)
    trans_type = random.choice(transaction_types)
    amount = round(random.uniform(5, 500), 2)
    trans_date = fake.date_time_between(start_date='-2y', end_date='now')

    merchant = random.choice(merchants) if trans_type == 'Purchase' else None
    category = random.choice(categories)
    if trans_type == 'Deposit':
        amount = round(random.uniform(100, 2000), 2)
        category = 'Salary' if random.random() < 0.3 else 'Other Income'
        merchant = None
    elif trans_type == 'Withdrawal':
        category = 'Cash Withdrawal'
        merchant = None
    elif trans_type == 'Transfer':
        category = 'Transfer'
        merchant = None

    location = fake.city() if random.random() < 0.7 else None

    transactions_to_insert.append((transaction_id_counter, account_id, trans_date, trans_type, amount, merchant, category, location))
    transaction_id_counter += 1

# Using executemany for batch insertion
cursor.executemany("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", transactions_to_insert)
conn.commit()
print(f"Inserted {len(transactions_to_insert)} transactions.")

# Optional: Verify data
cursor.execute("SELECT COUNT(*) FROM Customers;")
print(f"Total Customers in DB: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Accounts;")
print(f"Total Accounts in DB: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Transactions;")
print(f"Total Transactions in DB: {cursor.fetchone()[0]}")

# Close connection
conn.close()
print("Data insertion complete and database connection closed.")
