###########################################################################
#
# USDA Food Database Parser for JavaScript
#
# Author: Kent McKinney
# Created: 1/19/2020
# Modified: 1/20/2020
#
# Parses the USDA food nutrient database files
# Creates a tailored set of data for use in JavaScript applications
#
# Requires: MacOS and Python 3.8
#
# https://github.com/kentpmckinney/project-usda-food-database-parser
#
###########################################################################

import csv
import os
import sys
import datetime
import re

optionFileInventoryCheck = True
optionKeepBrandedFoods = False

# region Data Structures
###########################################################################

class Nutrients:
    'manages a list of nutrients'

    nutrients = []

    def add(self, id, name, unit):
        self.nutrients.append(Nutrient(id, name, unit))

    def exclude(self, id):
        for nutrient in self.nutrients:
            if nutrient.id == id:
                nutrient.include = False

    def isIncluded(self, id):
        for nutrient in self.nutrients:
            if nutrient.id == id and nutrient.include == True:
                return True
        return False


class Nutrient:
    'information about an individual nutrient'

    id = 0
    name = ""
    unit = ""
    include = True

    def __init__(self, id, name, unit):
        self.id = id
        self.name = name
        self.unit = unit
        self.include = True

###########################################################################
# endregion


# region Pre-Parse
###########################################################################
srcPath = "/Volumes/Data/Projects/Diet/data/src/"
dstPath = "/Volumes/Data/Projects/Diet/data/dst/"

print("\nUSDA Food Database Parser for JavaScript v0.1")
print("Source Path: " + srcPath)
print("Destination Path: " + dstPath)
print("Start: " + str(datetime.datetime.now()))

# Calculate the combined size of original set of data files
size = 0
for filename in os.listdir(srcPath):
    if filename.endswith(".csv"):
        size += os.path.getsize(srcPath + filename)/1000/1000

print("Source USDA data file size: " + str(size) + " MB")
print("Loading source data files...")

# File inventory check
if optionFileInventoryCheck == True:
    TODO = True

# Read and sort data from nutrient.csv (list of nutrients)
with open(srcPath + "nutrient.csv", "r") as srcNutrientList:
    null = srcNutrientList.readline()  # discard header
    nutrientListReader = csv.reader(
        srcNutrientList.read().splitlines(), delimiter=',', quotechar='"')
    nutrientList = sorted(nutrientListReader,
                          key=lambda row: row[0], reverse=False)
    del nutrientListReader

# Read and sort data from food.csv (list of foods)
with open(srcPath + "food.csv", "r") as srcFoods:
    null = srcFoods.readline()  # discard header
    foodReader = csv.reader(srcFoods.read().splitlines(),
                            delimiter=',', quotechar='"')
    foodList = sorted(foodReader, key=lambda row: row[0], reverse=False)
    del foodReader
    numFoods = sum(1 for line in foodList)

# Read and sort data from food_nutrient.csv (nutrient content of foods)
with open(srcPath + "food_nutrient.csv", "r") as srcNutrients:
    null = srcNutrients.readline()  # discard header
    foodNutrientReader = csv.reader(
        srcNutrients.read().splitlines(), delimiter=',', quotechar='"')
    foodNutrientList = sorted(
        foodNutrientReader, key=lambda row: row[1], reverse=False)
    del foodNutrientReader

# Import list of nutrients
r = re.compile(r'\(.*?\)|cis-|,\s.*?(?=~)|\(.*?(?=~)|\/.*?(?=~)')
nutrients = Nutrients()
for nutrient in nutrientList:
    id = nutrient[0]
    name = r.sub('', nutrient[1])  # Filter nutrient names
    unit = nutrient[2]
    nutrients.add(id, name, unit)

# Specify which nutrients to exclude
# These nutrients will not be used by the application being developed
nutrients.exclude("1005")  # Carbohydrate, by difference
nutrients.exclude("1007")  # Ash
nutrients.exclude("1024")  # Specific Gravity
nutrients.exclude("1259")  # 4:00
nutrients.exclude("1260")  # 6:00
nutrients.exclude("1261")  # 8:00
nutrients.exclude("1262")  # 10:00
nutrients.exclude("1263")  # 12:00
nutrients.exclude("1264")  # 14:00
nutrients.exclude("1265")  # 16:00
nutrients.exclude("1266")  # 18:00
nutrients.exclude("1267")  # 20:00
nutrients.exclude("1268")  # 18:01
nutrients.exclude("1269")  # 18:02
nutrients.exclude("1270")  # 18:03
nutrients.exclude("1271")  # 20:04
nutrients.exclude("1272")  # 22:6 n-3 (DHA)
nutrients.exclude("1273")  # 22:00
nutrients.exclude("1274")  # 14:01
nutrients.exclude("1275")  # 16:01
nutrients.exclude("1276")  # 18:04
nutrients.exclude("1277")  # 20:01
nutrients.exclude("1278")  # 20:5 n-3 (EPA)
nutrients.exclude("1279")  # 22:01
nutrients.exclude("1280")  # 22:5 n-3 (DPA)
nutrients.exclude("1281")  # 14:1 t
nutrients.exclude("1299")  # 15:00
nutrients.exclude("1300")  # 17:00
nutrients.exclude("1301")  # 24:00:00
nutrients.exclude("1303")  # 16:1 t
nutrients.exclude("1304")  # 18:1 t
nutrients.exclude("1305")  # 22:1 t
nutrients.exclude("1306")  # 18:2 t not further defined
nutrients.exclude("1307")  # 18:2 i
nutrients.exclude("1310")  # 18:2 t,t
nutrients.exclude("1311")  # 18:2 CLAs
nutrients.exclude("1312")  # 24:1 c
nutrients.exclude("1313")  # 20:2 n-6 c,c
nutrients.exclude("1314")  # 16:1 c
nutrients.exclude("1315")  # 18:1 c
nutrients.exclude("1316")  # 18:2 n-6 c,c
nutrients.exclude("1317")  # 22:1 c
nutrients.exclude("1321")  # 18:3 n-6 c,c,c
nutrients.exclude("1323")  # 17:01
nutrients.exclude("1325")  # 20:03
nutrients.exclude("1332")  # 13:00
nutrients.exclude("1333")  # 15:01
nutrients.exclude("1334")  # 22:02
nutrients.exclude("1335")  # 11:00
nutrients.exclude("1404")  # 18:3 n-3 c,c,c (ALA)
nutrients.exclude("1405")  # 20:3 n-3
nutrients.exclude("1406")  # 20:3 n-6
nutrients.exclude("1408")  # 20:4 n-6
nutrients.exclude("1409")  # 18:3i
nutrients.exclude("1410")  # 21:05
nutrients.exclude("1411")  # 22:04
nutrients.exclude("1412")  # 18:1-11 t (18:1t n-7)
nutrients.exclude("1414")  # 20:3 n-9
nutrients.exclude("2003")  # 5:00
nutrients.exclude("2004")  # 7:00
nutrients.exclude("2005")  # 9:00
nutrients.exclude("2006")  # 21:00
nutrients.exclude("2007")  # 23:00
nutrients.exclude("2008")  # 12:01
nutrients.exclude("2009")  # 14:1 c
nutrients.exclude("2010")  # 17:1 c
nutrients.exclude("2012")  # 20:1 c
nutrients.exclude("2013")  # 20:1 t
nutrients.exclude("2014")  # 22:1 n-9
nutrients.exclude("2015")  # 22:1 n-11
nutrients.exclude("2016")  # 18:2 c
nutrients.exclude("2018")  # 18:3 c
nutrients.exclude("2019")  # 18:3 t
nutrients.exclude("2020")  # 20:3 c
nutrients.exclude("2021")  # 22:3 c
nutrients.exclude("2022")  # 20:4 c
nutrients.exclude("2023")  # 20:5 c
nutrients.exclude("2024")  # 22:5 c
nutrients.exclude("2025")  # 22:6 c
nutrients.exclude("2026")  # 20:2 c

# Create a header row for the destination data file
dstHeader = "Description~Data Type~"
for nutrient in nutrients.nutrients:
    if nutrient.include == True:
        dstHeader += nutrient.name + "~"

# Remove the extra trailing ~ character from the header
if dstHeader.endswith('~'):
    dstHeader = dstHeader[:-1]

# Hide the mouse cursor so that it does not display on the terminal
if os.name == 'posix':
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

###########################################################################
# endregion


# region Parse
###########################################################################

# Create/Open destination data file for the food.txt output file
with open(dstPath + "food.txt", "w") as dstData:
    dataString = ""
    for food in foodList:
        dataType = food[1]
        if optionKeepBrandedFoods == False:
            if dataType == "branded_food":
                continue
        description = food[2]
        dataString += description + "\n"

    # Append the data string to the destination file
    dstData.write(dataString)

quit()

# Create/Open destination data file for nut.txt output file
with open(dstPath + "nut.txt", "w") as dstData:

    # Add the dstHeader to the destination data file
    dstData.write(dstHeader)

    # Iterate through each food in the source data file "food.csv"
    progress = 0
    for food in foodList:
        # Update progress indicator in the terminal
        progress += 1
        sys.stdout.write("\rProessing " + str(progress) +
                         " of " + str(numFoods))

        dataType = food[1]

        if optionKeepBrandedFoods == False:
            if dataType == "branded_food":
                continue

        fdcId = food[0]
        description = food[2]

        # Add the food description to the data string
        dataString = description
        dataString += "~"
        dataString += dataType
        dataString += "~"

        # Get a list of the nutrient content for this food
        # Break out of the loop once the relevant data has been parsed
        # Remove items once processed to improve parsing speed
        append = False
        nutrientContent = []
        for item in foodNutrientList:
            itemFdcId = item[1]
            if itemFdcId == fdcId:
                nutrientContent.append(item)
                foodNutrientList.remove(item)  # Improve parsing speed
                append = True
            elif append == True:  # Improve parsing speed
                break  # Improve parsing speed

        # Iterate through all nutrients and add amounts for this food's nutrients
        for nutrient in nutrients.nutrients:
            nutId = nutrient.id
            if nutrient.include == True:
                addedAmount = False
                for item in nutrientContent:
                    itemId = item[2]
                    if itemId == nutId:
                        amount = item[3]
                        dataString += amount + "~"
                        addedAmount = True
                if addedAmount == False:  # No data for this nutrient in this food
                    dataString += "~"

        # Remove the extra trailing ~ character from the data string
        if dataString.endswith('~'):
            dataString = dataString[:-1]

        # Add a newline character to the end of the data string
        dataString += "\n"

        # Append the data string to the destination file
        dstData.write(dataString)

###########################################################################
# endregion


# region Post-Parse
###########################################################################

print("\nEnd: " + str(datetime.datetime.now()))

# Calculate the combined size of modified set of data files
size = 0
for filename in os.listdir(dstPath):
    if filename.endswith(".txt"):
        size += os.path.getsize(dstPath + filename)/1000/1000

print("Destination USDA data file size: " + str(size) + " MB\n")

###########################################################################
# endregion
