from sys import argv

import json

def create_table(line, tables):
    splitted_line = line.split()
    table_name = splitted_line[1]
    rows = splitted_line[2].split(",")

    tables[table_name] = {}
    for row in rows:
        tables[table_name][row] = [] # Each column initially contains an empty list.

    print("#" * 22 + " CREATE " + "#" * 25)
    print(f"Table '{table_name}' created with columns: {rows}")
    print("#" * 55 + "\n")

def table_structure(columns): # This is a helper function that creates the general prototype of this table.
    table_border_prototype = "+"
    for key, values in columns.items():
        key_length = len(key)
        max_value_length = 0
        for value in values:
            if len(value) > max_value_length:
                max_value_length = len(value)
        table_border_prototype += "-" * (max(key_length, max_value_length) + 2) + "+"
    table_border = table_border_prototype

    # Create a list of column widths to help align headers and data.
    column_widths = []
    splitted_table_border = table_border.split("+")
    for width in splitted_table_border[1:-1]:
        column_widths.append(len(width))

    value_list = list(columns.values())[0]
    number_of_rows = len(value_list)

    columns_elements = "|"
    index = 0
    for key in columns.keys():
        columns_elements += f"{' ' + key:{column_widths[index]}}|"
        index += 1

    # Generate all the rows for the table.
    row_count = 0
    other_rows = ""
    while row_count < number_of_rows:
        row = "|"
        index = 0
        for value in columns.values():
            row += f"{' ' + value[row_count]:{column_widths[index]}}|"
            index += 1
        other_rows += row + "\n"
        row_count += 1

    # Combine all parts to build the full table structure.
    table = ""
    table += table_border + "\n"
    table += columns_elements + "\n"
    table += table_border + "\n"
    table += other_rows
    table += table_border

    return table

def insert(line, tables):
    splitted_line = line.split(" ", 2)
    table_name = splitted_line[1]
    column_elements = splitted_line[2].split(",")

    try:
        columns = tables[table_name]
    except KeyError:
        print("#" * 22 + " INSERT " + "#" *25)
        print(f"Table {table_name} not found")
        print(f"Inserted into '{table_name}': {tuple(column_elements)}")
        print("#" * 55 + "\n")
        return

    index = 0
    for key in columns.keys():
        columns[key].append(column_elements[index])
        index += 1

    table = table_structure(columns)
    print("#" * 22 + " INSERT " + "#" * 25)
    print(f"Inserted into '{table_name}': {tuple(column_elements)}\n")
    print(f"Table: {table_name}")
    print(table)
    print("#" * 55 + "\n")

def select(line, tables):
    list_of_selects = []
    splitted_line = line.split(" WHERE ")
    table_name = splitted_line[0].split()[1]
    requested_datas = splitted_line[0].split()[2].split(",")
    condition = splitted_line[1]
    condition_dictionary = json.loads(condition)

    try:
        columns = tables[table_name]
    except KeyError:
        print("#" * 22 + " SELECT " + "#" *25)
        print(f"Table {table_name} not found")
        print(f"Condition: {condition_dictionary}")
        print(f"Select result from '{table_name}': None")
        print("#" * 55 + "\n")
        return

    for requested_data in requested_datas:
        try:
            if requested_data != "*":
                column_validation = columns[requested_data]
        except KeyError:
            print("#" * 22 + " SELECT " + "#" * 25)
            print(f"Column {requested_data} does not exist")
            print(f"Condition: {condition_dictionary}")
            print(f"Select result from '{table_name}': None")
            print("#" * 55 + "\n")
            return

    for condition_key in condition_dictionary.keys():
        try:
            column_validation = columns[condition_key]
        except KeyError:
            print("#" * 22 + " SELECT " + "#" * 25)
            print(f"Column {condition_key} does not exist")
            print(f"Condition: {condition_dictionary}")
            print(f"Select result from '{table_name}': None")
            print("#" * 55 + "\n")
            return

    # If "*" is requested, select all columns in the table.
    if requested_datas == ["*"]:
        requested_datas = list(columns.keys())

    # Iterate through the rows of the table to filter based on the condition.
    index = 0
    while index < len(columns[requested_datas[0]]):
        equality = 1
        for key in condition_dictionary.keys():
            if columns[key][index] == str(condition_dictionary[key]):
                continue
            else:
                equality = 0
                index += 1
                break
        if equality == 1:
            temporary_tuple = []
            for requested_data in requested_datas:
                temporary_tuple.append((columns[requested_data][index]))
            list_of_selects.append((tuple(temporary_tuple)))
            index += 1

    standardized_condition = str(condition_dictionary).replace('"', "'")
    print("#" * 22 + " SELECT " + "#" * 25)
    print(f"Condition: {standardized_condition}")
    print(f"Select result from '{table_name}': {list_of_selects}")
    print("#" * 55 + "\n")

def update(line, tables):
    splitted_line = line.split(" WHERE ")
    table_name = splitted_line[0].split()[1]
    the_element_to_be_updated = splitted_line[0].split(" ", 2)[2]
    update_location = splitted_line[1]
    the_element_to_be_updated_dictionary = json.loads(the_element_to_be_updated)
    update_location_dictionary = json.loads(update_location)

    updated_rows = 0

    try:
        columns = tables[table_name]
    except KeyError:
        standardized_the_element_to_be_updated = str(the_element_to_be_updated_dictionary).replace('"', "'")
        standardized_update_location = str(update_location_dictionary).replace('"', "'")
        print("#" *22 + " UPDATE " + "#"*25)
        print(f"Updated '{table_name}' with {standardized_the_element_to_be_updated} where {standardized_update_location}")
        print(f"Table {table_name} not found")
        print(f"{updated_rows} rows updated.")
        print("#" * 55 + "\n")
        return

    for key in the_element_to_be_updated_dictionary.keys():
        try:
            column_validation = columns[key]
        except KeyError:
            standardized_the_element_to_be_updated = str(the_element_to_be_updated_dictionary).replace('"', "'")
            standardized_update_location = str(update_location_dictionary).replace('"', "'")
            table = table_structure(columns)
            print("#" * 22 + " UPDATE " + "#" * 25)
            print(f"Updated '{table_name}' with {standardized_the_element_to_be_updated} where {standardized_update_location}")
            print(f"Column {key} does not exist")
            print(f"{updated_rows} rows updated.\n")
            print(f"Table: {table_name}")
            print(table)
            print("#" * 55 + "\n")
            return

    for key in update_location_dictionary.keys():
        try:
            column_validation = columns[key]
        except KeyError:
            standardized_the_element_to_be_updated = str(the_element_to_be_updated_dictionary).replace('"', "'")
            standardized_update_location = str(update_location_dictionary).replace('"', "'")
            table = table_structure(columns)
            print("#" * 22 + " UPDATE " + "#" * 25)
            print(f"Updated '{table_name}' with {standardized_the_element_to_be_updated} where {standardized_update_location}")
            print(f"Column {key} does not exist")
            print(f"{updated_rows} rows updated.\n")
            print(f"Table: {table_name}")
            print(table)
            print("#" * 55 + "\n")
            return

    # Iterate through the rows and update values where the condition is met.
    number_of_rows = len(list(columns.values())[0])
    for index in range(number_of_rows):
        for key_1, value_1 in update_location_dictionary.items():
            if key_1 in columns:
                if columns[key_1][index] != str(value_1):
                    break
        else:
            updated_rows += 1
            for key_3, value_3 in the_element_to_be_updated_dictionary.items():
                if key_3 in columns:
                    columns[key_3][index] = str(value_3)

    table = table_structure(columns)
    standardized_the_element_to_be_updated = str(the_element_to_be_updated_dictionary).replace('"', "'")
    standardized_update_location = str(update_location_dictionary).replace('"', "'")
    print("#" * 22 + " UPDATE " + "#" * 25)
    print(f"Updated '{table_name}' with {standardized_the_element_to_be_updated} where {standardized_update_location}")
    print(f"{updated_rows} rows updated.\n")
    print(f"Table: {table_name}")
    print(table)
    print("#" * 55 + "\n")


def delete(line, tables):
    # Check if the input is for deleting all rows from a table (no condition provided).
    if len(line.split()) == 2:
        table_name = line.split()[1]
        try:
            columns = tables[table_name]
        except KeyError:
            print("#" * 22 + " DELETE " + "#" * 25)
            print(f"Table {table_name} not found")
            print(f"{0} rows deleted.")
            print("#" * 55 + "\n")
            return

        for key in columns.keys():
            columns[key] = []

        print("#" * 22 + " DELETE " + "#" * 25)
        print("All rows deleted.")
        print("#" * 55 + "\n")
        return

    splitted_line = line.split(" WHERE ")
    table_name = splitted_line[0].split()[1]
    the_element_to_be_deleted = splitted_line[1]
    the_element_to_be_deleted_dictionary = json.loads(the_element_to_be_deleted)

    try:
        columns = tables[table_name]
    except KeyError:
        standardized_the_element_to_be_deleted = str(the_element_to_be_deleted_dictionary).replace("'", "'")
        print("#" * 22 + " DELETE " + "#" * 25)
        print(f"Deleted from '{table_name}' where {standardized_the_element_to_be_deleted}")
        print(f"Table {table_name} not found")
        print(f"{0} rows deleted.")
        print("#" * 55 + "\n")
        return

    for key in the_element_to_be_deleted_dictionary.keys():
        try:
            column_validation = columns[key]
        except KeyError:
            standardized_the_element_to_be_deleted = str(the_element_to_be_deleted_dictionary).replace("'", "'")
            table = table_structure(columns)
            print("#" * 22 + " DELETE " + "#" * 25)
            print(f"Deleted from '{table_name}' where {standardized_the_element_to_be_deleted}")
            print(f"Column {key} does not exist")
            print(f"{0} rows deleted.\n")
            print(f"Table: {table_name}")
            print(table)
            print("#" * 55 + "\n")
            return

    # Find rows that match the delete condition.
    list_of_rows_to_be_deleted = []
    number_of_rows = len(list(columns.values())[0])

    for index_of_row in range(number_of_rows):
        # Check if the current row satisfies the delete condition.
        for key_1, value_1 in the_element_to_be_deleted_dictionary.items():
            if key_1 in columns.keys():
                if str(value_1) != columns[key_1][index_of_row]:
                    break
        else:
            list_of_rows_to_be_deleted.append(index_of_row)

    # Delete rows in reverse order to prevent indexing issues during deletion.
    list_of_rows_to_be_deleted.sort(reverse=True)
    for row in list_of_rows_to_be_deleted:
        for key in columns.keys():
            columns[key].pop(row)

    table = table_structure(columns)
    standardized_the_element_to_be_deleted = str(the_element_to_be_deleted_dictionary).replace("'", "'")
    print("#" * 22 + " DELETE " + "#" * 25)
    print(f"Deleted from '{table_name}' where {standardized_the_element_to_be_deleted}")
    print(f"{len(list_of_rows_to_be_deleted)} rows deleted.\n")
    print(f"Table: {table_name}")
    print(table)
    print("#" * 55 + "\n")

def count(line, tables):
    splitted_line = line.split(" WHERE ")
    table_name = splitted_line[0].split()[1]
    element_to_be_counted = splitted_line[1]

    try:
        columns = tables[table_name]
    except KeyError:
        print("#" * 22 + " COUNT " + "#" * 25)
        print(f"Table {table_name} not found")
        print(f"Total number of entries in '{table_name}' is {0}")
        print("#" * 55 + "\n")
        return

    # If element_to_be_counted is "*", count all rows in the table
    if element_to_be_counted == "*":
        count = len(next(iter(columns.values())))
        print("#" * 22 + " COUNT " + "#" * 25)
        print(f"Count: {count}")
        print(f"Total number of entries in '{table_name}' is {count}")
        print("#" * 55 + "\n")
        return

    # Parse the WHERE condition into a JSON dictionary
    element_to_be_counted_dictionary = json.loads(element_to_be_counted)

    for key in element_to_be_counted_dictionary:
        try:
            column_validation = columns[key]
        except KeyError:
            print("#" * 22 + " COUNT " + "#" * 25)
            print(f"Column {key} does not exist")
            print(f"Total number of entries in '{table_name}' is {0}")
            print("#" * 55 + "\n")
            return

    count = 0
    total_rows = len(next(iter(columns.values())))

    # Iterate through each row in the table to check if it matches the condition.
    for i in range(total_rows):
        for key_1, value_1 in element_to_be_counted_dictionary.items():
            # Check if the condition is not met for the current row.
            if key_1 in columns:
                if columns[key_1][i] != str(value_1):
                    break
        else:
            count += 1

    print("#" * 22 + " COUNT " + "#" * 25)
    print(f"Count: {count}")
    print(f"Total number of entries in '{table_name}' is {count}")
    print("#" * 55 + "\n")

def join(line, tables):
    splitted_line = line.split(" ON ")
    first_table_name = splitted_line[0].split()[1].split(",")[0]
    second_table_name = splitted_line[0].split()[1].split(",")[1]
    condition = splitted_line[1]

    try:
        columns_1 = tables[first_table_name]
    except KeyError:
        print("#" * 23 + " JOIN " + "#" * 26)
        print(f"Join tables {first_table_name} and {second_table_name}")
        print(f"Table {first_table_name} does not exist")
        print("#" * 55 + "\n")
        return

    try:
        columns_2 = tables[second_table_name]
    except KeyError:
        print("#" * 23 + " JOIN " + "#" * 26)
        print(f"Join tables {first_table_name} and {second_table_name}")
        print(f"Table {second_table_name} does not exist")
        print(f"#" * 55 + "\n")
        return

    try:
        column_validation_1 = columns_1[condition]
        column_validation_2 = columns_2[condition]
    except KeyError:
        print("#" * 23 + " JOIN " + "#" * 26)
        print(f"Join tables {first_table_name} and {second_table_name}")
        print(f"Column {condition} does not exist ")
        print("#" * 55 + "\n")
        return

    table_1 = table_structure(columns_1)
    table_2 = table_structure(columns_2)

    # Split the tables into lines for easier manipulation.
    splitted_table_1 = table_1.split("\n")
    splitted_table_2 = table_2.split("\n")

    joined_table = ""

    # Combine the headers and borders of the two tables.
    index = 0
    while index < 3:
        joined_table += splitted_table_1[index] + splitted_table_2[index][1:] + "\n"
        index +=1

    # Perform the join operation based on the condition column.
    row_count = 0
    index_1 = 3
    for element_1 in columns_1[condition]:
        index_2 = 3
        for element_2 in columns_2[condition]:
            if element_1 == element_2:
                joined_table += splitted_table_1[index_1] + splitted_table_2[index_2][1:] + "\n"
                row_count += 1
            index_2 +=1
        index_1 += 1

    joined_table += splitted_table_1[0] + splitted_table_2[0][1:]
    print("#"*23 + " JOIN " + "#"*26)
    print(f"Join tables {first_table_name} and {second_table_name}")
    print(f"Join result ({row_count} rows):" + "\n")
    print("Table: Joined Table")
    print(joined_table)
    print("#"*55 + "\n")

def main():
    tables = {}
    with open(argv[1], "r", encoding="utf-8-sig") as text_file_input:
        for line in text_file_input:
            line = line.strip()
            if line.startswith("CREATE_TABLE"):
                create_table(line, tables)
            elif line.startswith("INSERT"):
                insert(line, tables)
            elif line.startswith("SELECT"):
                select(line, tables)
            elif line.startswith("UPDATE"):
                update(line, tables)
            elif line.startswith("DELETE"):
                delete(line, tables)
            elif line.startswith("COUNT"):
                count(line, tables)
            elif line.startswith("JOIN"):
                join(line, tables)

if __name__ == "__main__":
    main()