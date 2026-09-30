import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


class Expense:
    """Represents a single expense."""

    def __init__(self, amount, category, date, description, expense_id=None):
        self.id = expense_id or self._generate_id()
        self.amount = float(amount)
        self.category = category.strip().title()
        self.date = date
        self.description = description.strip()

    @staticmethod
    def _generate_id():
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["amount"],
            data["category"],
            data["date"],
            data["description"],
            data.get("id")
        )


class ExpenseTracker:
    """Handles expense management and JSON storage."""

    def __init__(self, filename=DATA_FILE):
        self.filename = Path(filename)
        self.expenses = []
        self.load()

    def load(self):
        try:
            if self.filename.exists():
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.expenses = [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("Warning: Could not load saved data. Starting with an empty list.")
            self.expenses = []

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([expense.to_dict() for expense in self.expenses], file, indent=4)
        except OSError as error:
            print(f"Error saving data: {error}")

    def add_expense(self, amount, category, date, description):
        expense = Expense(amount, category, date, description)
        self.expenses.append(expense)
        self.save()
        return expense

    def view_expenses(self, expenses=None):
        items = self.expenses if expenses is None else expenses
        if not items:
            print("\nNo expenses found.")
            return

        print("\n" + "=" * 78)
        print(f"{'ID':<16} {'Date':<12} {'Category':<15} {'Amount':>10}  Description")
        print("-" * 78)
        for expense in items:
            short_id = expense.id[-8:]
            print(
                f"{short_id:<16} {expense.date:<12} {expense.category:<15} "
                f"{expense.amount:>10.2f}  {expense.description}"
            )
        print("=" * 78)

    def find_by_id(self, expense_id):
        if not expense_id:
            return None
        for expense in self.expenses:
            if expense.id.endswith(expense_id) or expense.id == expense_id:
                return expense
        return None

    def search(self, category=None, date=None):
        results = self.expenses
        if category:
            results = [e for e in results if e.category.lower() == category.lower()]
        if date:
            results = [e for e in results if e.date == date]
        return results

    def update_expense(self, expense_id, amount, category, date, description):
        expense = self.find_by_id(expense_id)
        if not expense:
            return False
        expense.amount = float(amount)
        expense.category = category.strip().title()
        expense.date = date
        expense.description = description.strip()
        self.save()
        return True

    def delete_expense(self, expense_id):
        expense = self.find_by_id(expense_id)
        if not expense:
            return False
        self.expenses.remove(expense)
        self.save()
        return True

    def total(self, expenses=None):
        items = self.expenses if expenses is None else expenses
        return sum(e.amount for e in items)

    def category_totals(self):
        totals = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount
        return totals


def get_amount(prompt="Amount: "):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Amount must be greater than 0.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_date(prompt="Date (YYYY-MM-DD): "):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Please use the format YYYY-MM-DD.")


def get_text(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty.")


def add_expense(tracker):
    print("\n--- Add Expense ---")
    amount = get_amount()
    category = get_text("Category: ", "Category")
    date = get_date()
    description = get_text("Description: ", "Description")
    expense = tracker.add_expense(amount, category, date, description)
    print(f"Expense added successfully. ID: {expense.id[-8:]}")


def search_expenses(tracker):
    print("\n--- Search / Filter ---")
    category = input("Category (press Enter to skip): ").strip()
    date = input("Date YYYY-MM-DD (press Enter to skip): ").strip()

    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date.")
            return

    results = tracker.search(category or None, date or None)
    tracker.view_expenses(results)
    print(f"Filtered total: {tracker.total(results):.2f}")


def update_expense(tracker):
    print("\n--- Update Expense ---")
    tracker.view_expenses()
    expense_id = input("Enter expense ID: ").strip()
    expense = tracker.find_by_id(expense_id)

    if not expense:
        print("Expense not found.")
        return

    print("Enter new values:")
    amount = get_amount(f"Amount [{expense.amount}]: ")
    category = get_text(f"Category [{expense.category}]: ", "Category")
    date = get_date(f"Date [{expense.date}]: ")
    description = get_text(f"Description [{expense.description}]: ", "Description")

    tracker.update_expense(expense_id, amount, category, date, description)
    print("Expense updated successfully.")


def delete_expense(tracker):
    print("\n--- Delete Expense ---")
    tracker.view_expenses()
    expense_id = input("Enter expense ID: ").strip()

    if tracker.delete_expense(expense_id):
        print("Expense deleted successfully.")
    else:
        print("Expense not found.")


def show_totals(tracker):
    print("\n--- Spending Summary ---")
    print(f"Total expenses: {tracker.total():.2f}")
    print("\nCategory-wise totals:")
    totals = tracker.category_totals()
    if not totals:
        print("No expenses available.")
        return
    for category, amount in sorted(totals.items()):
        print(f"- {category}: {amount:.2f}")


def main():
    tracker = ExpenseTracker()

    while True:
        print("""
================ EXPENSE TRACKER ================
1. Add expense
2. View all expenses
3. Search / filter
4. Show total & category-wise totals
5. Update expense
6. Delete expense
7. Save data
0. Exit
==================================================
""")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_expense(tracker)
            elif choice == "2":
                tracker.view_expenses()
            elif choice == "3":
                search_expenses(tracker)
            elif choice == "4":
                show_totals(tracker)
            elif choice == "5":
                update_expense(tracker)
            elif choice == "6":
                delete_expense(tracker)
            elif choice == "7":
                tracker.save()
                print("Data saved successfully.")
            elif choice == "0":
                tracker.save()
                print("Data saved. Goodbye!")
                break
            else:
                print("Please choose a valid option.")
        except (KeyboardInterrupt, EOFError):
            tracker.save()
            print("\nData saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
