# TSV Reader
This program will get the user's input and loop until the user enters quit. The load_records function reads in data from the hard-coded minor5.tsv file using the csv.DictReader function and assembles two dictionaries from that data. If the user inputted only numbers, then the code will treat the input as a zip code. Otherwise, the input is handled as a city's name. Then, the user's input is used as a key in the assembled dictionaries to identify and print the associated cities.