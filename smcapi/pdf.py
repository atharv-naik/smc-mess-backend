import pdfkit
from tabulate import tabulate
from smc.models import MenuItem, Student

# Dummy transactions data
transactions = [
    {
        "transaction_id": "3HYaLLRNETS",
        "transaction_type": "Debit",
        "amount": "0.0",
        "timestamp": "2023-07-06T12:46:37.661266Z",
        "student": 1,
        "items": []
    },
    {
        "transaction_id": "cGvxKNfuSur",
        "transaction_type": "Debit",
        "amount": "25.0",
        "timestamp": "2023-07-06T12:46:41.743818Z",
        "student": 1,
        "items": [
            "3CjJ7dZoLwK",
            "hk6c9qXQARX"
        ]
    },
    {
        "transaction_id": "3E8pU66nRLr",
        "transaction_type": "Deposit",
        "amount": "50.0",
        "timestamp": "2023-07-09T10:15:02.449484Z",
        "student": 1,
        "items": []
    },
    {
        "transaction_id": "3PWeoBiZ2bj",
        "transaction_type": "Debit",
        "amount": "25.0",
        "timestamp": "2023-07-09T16:40:12.512999Z",
        "student": 1,
        "items": [
            "4eFcUyTLRa2",
            "EY8pBHtVfMc",
            "Ro3d8EmKGkC"
        ]
    },
    {
        "transaction_id": "FBA6mEYAXpg",
        "transaction_type": "Purchase",
        "amount": "-272.0",
        "timestamp": "2023-07-09T16:46:58.614062Z",
        "student": 1,
        "items": [
            "4Nefj8PPhUf",
            "hk6c9qXQARX"
        ]
    }
]

def make_pdf(transactions, path="statement.pdf"):
    # convert transations model object into a json
    transformed_transactions = []
    for transaction in transactions:
        transformed_transaction = {
            "transaction_id": transaction.transaction_id,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "balance": transaction.balance,
            "timestamp": transaction.timestamp,
            "student_id": transaction.student.id,
            "items": [item.name for item in transaction.items.all()]
        }
        transformed_transactions.append(transformed_transaction)

    transactions = transformed_transactions


    # Define the column names for the table
    headers = ["Transaction ID", "Transaction Type", "Amount", "Balance", "Timestamp", "Student", "Items"]

    # Prepare the data for the table
    table_data = []
    for transaction in transactions:
        row = [
            transaction["transaction_id"],
            transaction["transaction_type"],
            transaction["amount"],
            transaction["balance"],
            transaction["timestamp"],
            Student.objects.get(id=transaction["student_id"]).roll,
            ", ".join(transaction["items"])
        ]
        table_data.append(row)

    # Generate the tabulated data as HTML
    html_table = tabulate(table_data, headers, tablefmt="html")

    # Define the CSS styles for the table
    css = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #dddddd;
        }
    </style>
    """

    # Combine the HTML table and CSS styles
    html = f"<html><head>{css}</head><body>{html_table}</body></html>"

    # Generate the PDF from HTML using pdfkit
    pdfkit.from_string(html, path)
    
    return path
