import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE_NAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category", "Amount"])


def add_transaction():
    date = date_entry.get()
    transaction_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, transaction_type, category, amount])

    messagebox.showinfo("Success", "Transaction added successfully!")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


def view_transactions():
    window = tk.Toplevel(root)
    window.title("All Transactions")
    window.geometry("700x400")

    tree = ttk.Treeview(window)
    tree["columns"] = ("Date", "Type", "Category", "Amount")

    tree.column("#0", width=0, stretch=False)
    tree.column("Date", anchor="center", width=150)
    tree.column("Type", anchor="center", width=120)
    tree.column("Category", anchor="center", width=180)
    tree.column("Amount", anchor="center", width=120)

    tree.heading("#0", text="")
    tree.heading("Date", text="Date")
    tree.heading("Type", text="Type")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")

    tree.pack(fill="both", expand=True)

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)


def check_balance():
    income = 0
    expenses = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            amount = float(row["Amount"])
            if row["Type"] == "Income":
                income += amount
            else:
                expenses += amount

    balance = income - expenses

    messagebox.showinfo(
        "Balance Summary",
        f"Total Income: ₹{income:.2f}\n"
        f"Total Expenses: ₹{expenses:.2f}\n"
        f"Current Balance: ₹{balance:.2f}"
    )


def exit_program():
    root.destroy()


initialize_file()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x450")
root.resizable(False, False)

# Title
heading = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"))
heading.pack(pady=15)

# Form Frame
frame = tk.Frame(root)
frame.pack(pady=10)

# Date
tk.Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
date_entry = tk.Entry(frame, width=30)
date_entry.grid(row=0, column=1)

# Type
tk.Label(frame, text="Transaction Type:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
type_var = tk.StringVar(value="Expense")
type_menu = ttk.Combobox(frame, textvariable=type_var,
                         values=["Income", "Expense"], state="readonly", width=27)
type_menu.grid(row=1, column=1)

# Category
tk.Label(frame, text="Category:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
category_entry = tk.Entry(frame, width=30)
category_entry.grid(row=2, column=1)

# Amount
tk.Label(frame, text="Amount:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
amount_entry = tk.Entry(frame, width=30)
amount_entry.grid(row=3, column=1)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=25)

btn1 = tk.Button(button_frame, text="Add Transaction", command=add_transaction,
                 width=18, bg="green", fg="white")
btn1.grid(row=0, column=0, padx=10, pady=10)

btn2 = tk.Button(button_frame, text="View Transactions", command=view_transactions,
                 width=18, bg="blue", fg="white")
btn2.grid(row=0, column=1, padx=10, pady=10)

btn3 = tk.Button(button_frame, text="Check Balance", command=check_balance,
                 width=18, bg="orange", fg="white")
btn3.grid(row=1, column=0, padx=10, pady=10)

btn4 = tk.Button(button_frame, text="Exit", command=exit_program,
                 width=18, bg="red", fg="white")
btn4.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
