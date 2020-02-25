import csv, json, re

CSV_PATH = "countries.csv"
JSON_PATH = "countries.json"

def ListToString(l):
    str1 = " "
    return (str1.join(l))

data = []
with open(CSV_PATH, "r", encoding="utf-8-sig") as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=";")
    for csvRow in csvReader:

        # Removes any brackets from the country name
        # Puts information from brackets into 'preceding'
        if (match := re.search(r'\(.*\)', csvRow["country"].lower())) is not None:
            string = match.group()
            csvRow["country"] = csvRow["country"].lower().replace(string, '').strip()
            csvRow.update({"preceding": string[1:-1]})
        

        # Removes any commas within the Country name
        if (match:= re.search(',', csvRow["country"].lower())) is not None:
            string = match.group()
            csvRow["country"] = csvRow["country"].lower().replace(string, ' ,').strip()
            lst = []
            prec = []
            lst = csvRow["country"].split()
            i = 0
            while i<len(lst):
                if lst[i] == ',':
                    comma = i+1
                    while comma<len(lst):
                        prec.append(lst[comma])
                        comma+=1
                i+=1
            result = ListToString(prec)

            csvRow["country"] = csvRow["country"].lower().replace(string, '').strip()
            csvRow["country"] = csvRow["country"].lower().replace(result, '').strip()

            csvRow.update({"preceding": result})


        # Finds country name with word 'and' or 'of' and splits it into a list
        # Then stores countries with multiple names as two/three 'akas'
        if (re.search(' and ', csvRow["country"].lower())) or (re.search(' of ', csvRow["country"].lower())) is not None:
              
            # Splits all words in country names
            akas = []          
            akas = csvRow["country"].split()

            # Lists to store indevidual country names
            name_one = []
            name_two = []  
            name_three = [] 

            # List to store all akas         
            result = []

            # Is after first and/or
            is_after = False

            # Is after second and/or
            is_after_again = False

            # Is a third aka used
            used_three = False

            for i in range(len(akas)):

                # If the current word in the list is 'and' or 'of' set booleans
                if akas[i] == "and" or akas[i] == "of":
                    if is_after == True:
                        is_after_again = True
                    is_after = True

                # Checks if the current word is not 'and' or 'of' or a space
                if akas[i] != "and" or akas[i] != "of" or akas[i] == " ":
                    if is_after_again == True:
                        if akas[i] == "and" or akas[i] == "of":
                            continue
                        # appends akas[i] to name_three 
                        name_three.append(akas[i])
                        used_three = True
                    if is_after == True and is_after_again == False:
                        if akas[i] == "and" or akas[i] == "of":
                            continue
                        # appends akas[i] to name two
                        name_two.append(akas[i])
                    if is_after == False:
                        # appends akas[i] to name three
                        name_one.append(akas[i])

            # Converts the indevidual lists to strings
            str1 = ListToString(name_one).lower()
            str2 = ListToString(name_two).lower()

            # If third aka is used, convert to string and append it to result
            if used_three == True:
                str3 = ListToString(name_three).lower()
                print(str2)
                result.append(str3)

            # Append first and second aka to result
            result.append(str1)
            result.append(str2)

            # Append aka as new CSV row
            csvRow.update({"aka": result})


        # All following makes sure everything is lower case
        else:
            csvRow["country"] = csvRow["country"].lower()

        csvRow["country"] = csvRow["country"].lower()
        csvRow["state"] = csvRow["state"].lower()
        csvRow["m49"] = csvRow["m49"].zfill(3)

        # Appends all data to the csv row
        data.append(csvRow)

# write the data to a json file
with open(JSON_PATH, "w") as jsonFile:
    jsonFile.write(json.dumps(data, indent=4, ensure_ascii=False))


# have another regex(?) for akas
#  some countries have "and" in them - split by first "and" and save the first one as an aka AS A LIST