#Daniel Moreno
#Brief Description: This program will get the user's input and loop until the user enters quit. The load_records function reads in data from the hard-coded minor5.tsv file using the csv.DictReader function and assembles two dictionaries from that data.
#If the user inputted only numbers, then the code will treat the input as a zip code. Otherwise, the input is handled as a city's name.
#Then, the user's input is used as a key in the assembled dictionaries to identify and print the associated cities.

import csv

#get the next line in the file without advancing the file pointer
def peek_line(file):
    pos = file.tell()
    line = file.readline()
    file.seek(pos)
    return line

#define the function to load the file and assemble two dictionaries from the data
def load_records (filename):
    #created a try-except block to catch OSErrors which could be thrown when opening the file
    try:
        #open the file in r+ mode so that it can be read and altered
        #the with keyword is used to ensure that the file is automatically closed, even if an error occurs
        with open(filename, "r+") as dataFile:
            #check whether the first row contains "State" which indicates a header
            if "State" in peek_line(dataFile):
                pass
            elif "state" in peek_line(dataFile):
                pass
            #if the first row is not a header, insert a header row
            else:
                #get the current line which will be overwritten
                content = dataFile.read()
                dataFile.seek(0,0)
                #insert header row so that the csv.DictReader works properly and reinsert the old line after the new line
                dataFile.write("State\tStreet Address\tCity\tZip Code\n" + content)
                #move the file pointer back to the start of the file
                dataFile.seek(0)
            #read the file as if it was a tab-separated csv file
            tsvReader = csv.DictReader(dataFile, delimiter="\t")
            #initialize the dictionaries and a temp tuple
            zipToLineDict = {}
            cityToZipDict = {}
            #iterate through the rows, assemble the tuples of strings, and assemble the dictionaries
            for row in tsvReader:
                #assemble the line tuple
                line = (row["State"],row["Street Address"],row["City"],row["Zip Code"])
                #create the first dictionary: zip codes mapped to list of line tuples
                #assumes that every zip code in the tsv file is unique such that there will not be multiple cities with the same zip code
                zipToLineDict[row["Zip Code"]] = line
                #create the next dictionary: cities mapped to a set of zip codes
                #if a city already has a mapped tuple, prepend the new zip code
                if row["City"] in cityToZipDict:
                    cityToZipDict[row["City"]] = (row["Zip Code"], ) + cityToZipDict[row["City"]]
                #otherwise, add a tuple of one zip code to the dictionary
                else:
                    cityToZipDict[row["City"]] = (row["Zip Code"], )
            return zipToLineDict, cityToZipDict
    except OSError:
        print("The file could not be opened/read")
    return None, None
    
#get the user's initial input
userAnswer = input("Enter input: ")
#assemble the dictionaries after opening the file
#hardcodes the file name as the sample output does not provide any examples of the user entering a file name
zipToLineDict, cityToZipDict = load_records("locations.tsv")
#keep looping until the user enters "quit"; temporarily lowercases the input to check for quit
while userAnswer.lower() != "quit":
    #check whether the user's input consists only of digits which would indicate a zip code
    if userAnswer.isdigit():
        #check whether zip code exists
        if userAnswer in zipToLineDict:
            #get the tuple mapped to the zip code
            line = zipToLineDict[userAnswer]
            #print out results
            print(line[1])
            print(line[2] + ", " + line[0] + ", " + line [3])
        else:
            print("No records found in this zip code.")
    #when this else executes, it is assumed that a city name was entered
    else:
        #check whether city exists
        if userAnswer in cityToZipDict:
            #get the tuple of zips mapped to the city
            zips = cityToZipDict[userAnswer]
            #loop through all of the retrieved zips
            for zip in zips:
                #get the tuple mapped to the zip code
                line = zipToLineDict[zip]
                #print out results
                print(line[1])
                print(line[2] + ", " + line[0] + ", " + line [3])
        else:
            print("No records found in this town.")
    #get the next round of user input
    userAnswer = input("Enter input: ")


