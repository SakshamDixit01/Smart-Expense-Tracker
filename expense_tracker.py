from datetime import datetime
from storage import load_expenses, save_expenses


CATEGORIES = [
    "Food",
    "Travel",
    "shopping",
    "Educatrion",
    "Bills",
    "Entertainment",
    "Health",
    "Other"
]  



def get_positive_amount(prompt):
    """ Accept only positive numeric amounts. """

    while True:
        try:
            amount = float(input(prompt).strip())


            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if not amount < float("inf"):
                print("Please Enter a Valid amount.")
                continue
            return round(amount , 2)

        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_date():
    """ Get an expense date from the user in YYYY-MM-DD format. """

    while True:
        date_next = input("Enter the date (YYYY-MM-DD) or press Enter for today: ").strip()

        if not date_next:
            return datetime.today().strftime("%Y-%m-%d") 

        try:
            return datetime.strptime(date_next, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def choose_category():
    """ Display Categories and return the selected category."""

    print("\nExpense Categories:")

    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input("Choose a category : "))

            if 1 <= choice <= len(CATEGORIES):

                return CATEGORIES[choice - 1]
            print("Invalid choice. Please select a valid category number.")

        except ValueError:
            print("Invalid input. Please enter a number ")


def add_expense():
    """ Add a new personal expense. """

    print("\n --- Add personal expense ---")


    amount = get_positive_amount("Enter the amount: ")

    category = choose_category()
    description = input("Enter a description (optional): ").strip()


    if not description:
        description = category

    date = get_date()

    expenses = load_expenses()


    expense_id = max((expense.get("id", 0) for expense in expenses), default=0
    ) + 1

    expense = {
        "id" : expense_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)


    if save_expenses(expenses):
        print("\nExpense added successfully")
        print(f"Expense ID: {expense_id}")
        print(f"Amount: {amount :.2f}")
    else:
        print("Could not save the expense.")


def view_expenses():
    """ Display all saved personal expenses. """

    print("\n --- All Personal Expenses ---")


    expenses = load_expenses()


    if not expenses:
        print("No Expenses found")
        return 

    expenses.sort(
        key = lambda expense: (
            expense.get("date", ""),
            expense.get("id", 0)

        ),
        reverse = True
    )

    total = 0 

    print("-" * 75)
    print(
        f"{'ID':<5}{'Category':<17}{'Date':<13}" f"{'amount':>12} Description"

    )
    print("-" * 75)

    for expense in expenses:
        amount = expense.get("amount", 0)

        total += amount

        print(
            
            f"{expense.get('id', ''):<5}"
            f"{expense.get('category', ''):<17}"
            f"{expense.get('date', ''):<13}"
            f"{amount:>12.2f} {expense.get('description', '')}"
        )

    print("-" * 75)
    print(f"Total personal expenses: {total:.2f}")

def delete_expense():
    """ Delete a personal expense using this ID """

    print("\n --- Delete personal Expense ---")

    expenses = load_expenses()

    if not expenses:
        print("No expenses available to delete. ")
        return
        
    view_expenses()

    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    updated_expenses = [expense for expense in expenses if expense.get("id") != expense_id]

    if len(updated_expenses) == len(expenses):
        print("Expense ID not found. No expense deleted.")
        return

    if save_expenses(updated_expenses):
        print(f"Expense with ID {expense_id} deleted successfully.")
    else:
        print("Could not delete the expense. Please try again.")

def monthly_summary():
    """ Show total expenses for a selected month """

    print("\n --- Monthly Expense Summary ---")

    month = input("Enter the month (YYYY-MM): ").strip()

    if not month:
        month = datetime.today().strftime("%Y-%m")


    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")
        return

    expenses = load_expenses()

    monthly_expenses = [
    
        expense for expense in expenses if expense.get("date", "").startswith(month)
    ]


    if not monthly_expenses:
        print(f"No expenses found for {month}.")
        return

    total = sum(
        expense.get("amount", 0)
        for expense in monthly_expenses 
    )

    category_totals = {}

    for expense in monthly_expenses:
        category = expense.get("category", "Other")

        category_totals[category] = (
category_totals.get(category, 0) + expense.get("amount", 0)
        )

    print("\nMonth: {month}")
    print(f"Numer of Expenses: {len(monthly_expenses)}")
    print(f"Total spending: {total:.2}")


    print("\nCategory-wise spending: ")

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item :item[1],
        reverse = True
    ):
        percentage = amount/total * 100 if total else 0

        print(
            f"{category:<18}{amount:>9.2f}"f"({percentage:.1f}%)"
        )