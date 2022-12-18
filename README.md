# csvplus
> Create, Read, Update, Delete, and Move Rows in a CSV File

## install
```sh
pip install csvplus
```

## usage
```py
import csvplus

filepath = "./folder/cars.csv"

# create csv with the given column names 
csvplus.create(filepath, ["make","model","year"])

# append a new row to the end of the csv file
csvplus.add(filepath, { "make": "Kia", "model": "Soul", "year": 2023 })

# delete all rows matching the where conditions
csvplus.delete(filepath, where={ "make": "Tesla" })

# find all rows matching the where conditions
csvplus.read("countries.csv", where={ "year": 1776 })
[{ "name": "United States of Ameriac", "abbreviation": "USA", "year": 1776 }]

# move rows
move(filepath, from_row, to_row, debug_level=0, quoting=csv.QUOTE_ALL):
csvplus.move("example.csv", 0, 20) # move the first row to the 20th line
```