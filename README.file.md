# Inovegen Internship — Task 2: Expense Tracker

A command-line Expense Tracker built in Python using object-oriented programming and JSON storage.

## Features
- Add expenses with amount, category, date, and description
- View all expenses
- Search/filter by category or date
- Calculate total spending
- Calculate category-wise totals
- Update expenses
- Delete expenses
- Save/load data using JSON
- Input validation and error handling
- Clear menu and organized functions/classes

## Requirements
- Python 3.8 or newer
- No external libraries are required

## How to Run
1. Open a terminal in this folder.
2. Run:
   `python expense_tracker.py`
3. Use the numbered menu.

## Files
- `expense_tracker.py` — complete Python source code
- `expenses.json` — sample JSON data
- `README.md` — setup, usage, and feature documentation

## JSON Storage
The program automatically saves changes to `expenses.json`. If the file does not exist, it starts with an empty expense list.

## Example Workflow
1. Select `1` to add an expense.
2. Select `2` to view expenses.
3. Select `3` to filter by category/date.
4. Select `4` to view total and category-wise totals.
5. Select `5` or `6` to update/delete an expense.
6. Select `0` to save and exit.

## Validation
- Amount must be a positive number.
- Date must use `YYYY-MM-DD`.
- Category and description cannot be empty.
- Invalid menu choices are handled without crashing.
- Corrupt/unreadable JSON is handled safely.

## Optional Bonus
The current version focuses on all required functionality. Monthly summaries, category spending summaries, and CSV export can be added as extensions.
