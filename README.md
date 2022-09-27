# CSV to IPAC Table Format

This repository provides a simple script that converts a *Comma-Separated Values* file (csv) to an [IPAC Table file](https://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html).

Also useful for pretty-printing of csv files.

# Usage

Download the repository and use the provided script on the command line.

```
$ python csv_to_table.py --help
usage: csv_to_table.py [-h] [--header HEADER] [--units UNITS] [--null NULL] csvfile

Converts a CSV file to IPAC Table file.

positional arguments:
  csvfile          file to convert

options:
  -h, --help       show this help message and exit
  --header HEADER  comma-separated column names
  --units UNITS    units of the column values
  --null NULL      null value specifiers
```

The `header`, `units` and `null` arguments are optional.
Unless the `header` is specified, the script uses the first line of the csv file as the header.
If no `units` and/or `null` values are used then these will be omitted from the table file (they are optional).

The format for providing the `header`, `units` and `null` arguments is by comma-separated values, e.g.:

```
python csv_to_table.py --header "column1,column2,column3" my_file.csv >save_table.txt
```


The `types` required by the IPAC standard are automatically determined.
Right now, this supports only:

* char
* int
* double

If you need a different type just edit it manually after running the script.
The script does **not** do any type conversion on the data, values are copied from the CSV file as strings.

Commas inside quoted values are not supported.

The script does not check the requirements of the IPAC standard.



