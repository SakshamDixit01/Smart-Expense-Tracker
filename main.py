from expense_tracker import (
    add_expense,
    view_expenses,
    delete_expense,
    monthly_summary
)

from splitwise import (
    create_group,
    view_groups,
    add_group_expenses,
    view_balances,
    settle_balance

)


def display_menu():
    print("\n" + "=" * 45)
    print("      SMART EXPENSE TRACKER MENU       ")
    print("=" * 45)
    print("1. Add Personal Expense")
    print("2. View Personal Expenses")
    print("3. Delete Personal Expense")
    print("4. Monthly Expense Summary")
    print("=" * 45)
    print("5. Create Splitwise Group")
    print("6. View Splitwise Groups")
    print("7. Add Splitwise Group Expense")
    print("8. View Splitwise Balances")
    print("9. Settle Splitwise Balance")
    print("=" * 45)
    print("0. Exit")
    print("=" * 45)

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()


        if choice =='1':
            add_expense()

        elif choice == '2':
            view_expenses()

        elif choice == '3':
            delete_expense()

        elif choice == '4':
            monthly_summary()

        elif choice == '5':
            create_group()

        elif choice == '6':
            view_groups()

        elif choice == '7':
            add_group_expenses()
        elif choice == '8':
            view_balances()

        elif choice == '9':
            settle_balance()

        elif choice == '0':
            print("Exiting the Smart Expense Tracker. Goodbye!")
            print("\n Your Expenses and group are saved")
            break

        else:
            print("Invalid Choice , Please try Again")



if __name__ == "__main__":
    main()