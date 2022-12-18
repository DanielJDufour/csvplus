import csv


def _validate_fieldnames(data, fieldnames):
    for k in data.keys():
        if k not in fieldnames:
            raise f"key {k} does not appear in the csv fieldnames"


# mutable
def _move_item(lst, from_index, to_index):
    if from_index == to_index:
        return

    item = lst.pop(from_index)

    if from_index < to_index:
        lst.insert(to_index - 1, item)
    else:
        lst.insert(to_index, item)

    return lst


def create(filepath, fieldnames):
    with open(filepath, "w") as f:
        csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL).writeheader()


#####
# PUBLIC METHODS
#####


def add(filepath, entry, debug_level=0):
    if debug_level >= 1:
        print("deleting row from " + filepath)

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if debug_level >= 1:
            print("fieldnames:", fieldnames)

    _validate_fieldnames(entry, fieldnames)

    with open(filepath, "a") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writerow(entry)


def read(filepath, where={}, debug_level=0):
    if debug_level >= 1:
        print("updating rows")

    with open(filepath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if debug_level >= 1:
            print("fieldnames:", fieldnames)

        _validate_fieldnames(where, fieldnames)

        rows = [row for row in reader if where.items() < row.items()]

    return rows


def move(filepath, from_row, to_row, debug_level=0, quoting=csv.QUOTE_ALL):
    if debug_level >= 1:
        print("moving row")

    with open(filepath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if debug_level >= 1:
            print("fieldnames:", fieldnames)
        rows = list(reader)

        _move_item(rows, from_row, to_row)

    # write a new csv with updated rows
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=quoting)
        writer.writeheader()
        writer.writerows(rows)

    return rows


def update(filepath, where={}, data={}, debug_level=0, quoting=csv.QUOTE_ALL):
    if debug_level >= 1:
        print("updating rows")

    with open(filepath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if debug_level >= 1:
            print("fieldnames:", fieldnames)

        _validate_fieldnames(where, fieldnames)

        rows = [
            {**row, **data} if where.items() < row.items() else row for row in reader
        ]

    # write a new csv with updated rows
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=quoting)
        writer.writeheader()
        writer.writerows(rows)


def delete(filepath, where={}, debug_level=0):
    if debug_level >= 1:
        print("deleting row from " + filepath)

    with open(filepath) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if debug_level >= 1:
            print("fieldnames:", fieldnames)
        rows = list(reader)

    if debug_level >= 1:
        print(f"before filtering, there are {len(rows)} rows")

    _validate_fieldnames(where, fieldnames)

    for key, value in where.items():
        rows = [row for row in rows if row[key] != value]

    if debug_level >= 1:
        print(f"after filtering, there are {len(rows)} rows")

    # write a new csv with row filtered out
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    if debug_level >= 1:
        print("finished deleting row from " + filepath)


def exists(filepath, where, debug_level=0):
    if len(where) == 0:
        raise "must pass in where object with at least one key-value pair"
    return len(read(filepath=filepath, where=where, debug_level=debug_level)) > 0
