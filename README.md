# In-Memory Database Engine (Python)

A command-driven in-memory relational database engine written in Python using only the standard library (`sys`, `json`). It reads table and query instructions line by line from an input text file, validates table/column names, and prints formatted ASCII tables to standard output.

## Supported Operations

- `CREATE_TABLE <table_name> <col1,col2,...>`
  Creates a new in-memory table with the given columns.
- `INSERT <table_name> <val1,val2,...>`
  Appends a row to the table and prints the updated ASCII table.
- `SELECT <table_name> <col1,col2|*> WHERE {"col": "value"}`
  Filters rows matching the JSON condition and returns the selected columns as tuples.
- `UPDATE <table_name> {"col": "new_value"} WHERE {"col": "value"}`
  Updates matching rows and prints the updated table along with the affected row count.
- `DELETE <table_name>` or `DELETE <table_name> WHERE {"col": "value"}`
  Clears all rows or deletes rows matching the JSON filter.
- `COUNT <table_name> WHERE *` or `COUNT <table_name> WHERE {"col": "value"}`
  Prints total row count or count of rows matching a condition.
- `JOIN <table1,table2> ON <column>`
  Performs an inner join across two tables on a shared column and renders the combined ASCII table.

## Usage

Requires Python 3.x (no third-party packages).

1. Create an input file (for example `commands.txt`):
   ```text
   CREATE_TABLE users id,name,department
   INSERT users 1,Emre,Engineering
   INSERT users 2,Deniz,Operations
   SELECT users name,department WHERE {"id": "1"}
   UPDATE users {"department": "Security"} WHERE {"name": "Emre"}
   COUNT users WHERE *
   ```

2. Run the script:
   ```bash
   python database/database.py commands.txt
   ```

## Project Structure

```text
database/
└── database.py    # Command parser, CRUD/JOIN handlers, and dynamic ASCII table formatter
```
