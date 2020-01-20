###########################################################################
#
# USDA Food Database Parser for JavaScript
#
# Author: Kent McKinney
# License: GPLv3
# Created: 1/19/2020
#
# Parses the USDA food nutrient database CSV files
# Creates an optimzed set of data for use in JavaScript applications
#
# Requires: MacOS and Python 3.5+
#
###########################################################################

# import pandas as pd
import csv
import os
import sys
import datetime

optionFileInventoryCheck = True
optionKeepBrandedFoods = False





#region Data Structures
###########################################################################

class Nutrients:
    'encapsulates a nutrient list and methods to manipulate nutrient data'

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
   'encapsulates information about an individual nutrient'

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
#endregion





#region Pre-Parse
###########################################################################

srcPath = "/Volumes/Data/Projects/Diet/data/src/"
dstPath  = "/Volumes/Data/Projects/Diet/data/dst/"

print("USDA Food Database Parser for JavaScript v0.0")
print("Source Path: " + srcPath)
print("Destination Path: " + dstPath)
print("Start: " + str(datetime.datetime.now()))

# Report the combined size of original set of data files
size = 0
for filename in os.listdir(srcPath):
    if filename.endswith(".csv"): 
        size += os.path.getsize(srcPath + filename)
        continue
    else:
        continue
size = size/1000/1000
print("Source USDA data file size: " + str(size) + " MB")

# Create/Open destination data file
dstData = open(dstPath + "data.txt", "w")

print("Loading source data files nutrient.csv, food.csv, and food_nutrient.csv...")

# Read and sort data from nutrient.csv (list of nutrients)
srcNutrientList = open(srcPath + "nutrient.csv", "r")
null = srcNutrientList.readline() # discard header
srcNutrientListInMemory = srcNutrientList.read().splitlines()
nutrientListReader = csv.reader(srcNutrientListInMemory, delimiter=',', quotechar='"')
nutrientList = sorted(nutrientListReader, key=lambda row: row[0], reverse=False)

# Read and sort data from food.csv (list of foods)
srcFoods = open(srcPath + "food.csv", "r")
null = srcFoods.readline() # discard header
srcFoodsInMemory = srcFoods.read().splitlines()
FoodReader = csv.reader(srcFoodsInMemory, delimiter=',', quotechar='"')
FoodList = sorted(FoodReader, key=lambda row: row[0], reverse=False)
numFoods = sum(1 for line in FoodList)

# Read and sort data from food_nutrient.csv (nutrient content of foods)
srcNutrients = open(srcPath + "food_nutrient.csv", "r")
null = srcNutrients.readline() # discard header
srcNutrientsInMemory = srcNutrients.read().splitlines()
FoodNutrientReader = csv.reader(srcNutrientsInMemory, delimiter=',', quotechar='"')
FoodNutrientList = sorted(FoodNutrientReader, key=lambda row: row[1], reverse=False)

# Import list of nutrients
nutrients = Nutrients()
for nutrient in nutrientList:
    id = nutrient[0]
    name = nutrient[1]
    unit = nutrient[2]
    nutrients.add(id, name, unit)

# Specify which nutrients to exclude
# These nutrients will not be used by the application being developed
nutrients.exclude("1005")
nutrients.exclude("1007")
nutrients.exclude("1024")
nutrients.exclude("1259")
nutrients.exclude("1260")
nutrients.exclude("1261")
nutrients.exclude("1262")
nutrients.exclude("1263")
nutrients.exclude("1264")
nutrients.exclude("1265")
nutrients.exclude("1266")
nutrients.exclude("1267")
nutrients.exclude("1268")
nutrients.exclude("1269")
nutrients.exclude("1270")
nutrients.exclude("1271")
nutrients.exclude("1272")
nutrients.exclude("1273")
nutrients.exclude("1274")
nutrients.exclude("1275")
nutrients.exclude("1276")
nutrients.exclude("1277")
nutrients.exclude("1278")
nutrients.exclude("1279")
nutrients.exclude("1280")
nutrients.exclude("1281")
nutrients.exclude("1299")
nutrients.exclude("1300")
nutrients.exclude("1301")
nutrients.exclude("1303")
nutrients.exclude("1304")
nutrients.exclude("1305")
nutrients.exclude("1306")
nutrients.exclude("1307")
nutrients.exclude("1310")
nutrients.exclude("1311")
nutrients.exclude("1312")
nutrients.exclude("1313")
nutrients.exclude("1314")
nutrients.exclude("1315")
nutrients.exclude("1316")
nutrients.exclude("1317")
nutrients.exclude("1321")
nutrients.exclude("1323")
nutrients.exclude("1325")
nutrients.exclude("1332")
nutrients.exclude("1333")
nutrients.exclude("1334")
nutrients.exclude("1335")
nutrients.exclude("1404")
nutrients.exclude("1405")
nutrients.exclude("1406")
nutrients.exclude("1408")
nutrients.exclude("1409")
nutrients.exclude("1410")
nutrients.exclude("1411")
nutrients.exclude("1412")
nutrients.exclude("1414")
nutrients.exclude("2003")
nutrients.exclude("2004")
nutrients.exclude("2005")
nutrients.exclude("2006")
nutrients.exclude("2007")
nutrients.exclude("2008")
nutrients.exclude("2009")
nutrients.exclude("2010")
nutrients.exclude("2012")
nutrients.exclude("2013")
nutrients.exclude("2014")
nutrients.exclude("2015")
nutrients.exclude("2016")
nutrients.exclude("2018")
nutrients.exclude("2019")
nutrients.exclude("2020")
nutrients.exclude("2021")
nutrients.exclude("2022")
nutrients.exclude("2023")
nutrients.exclude("2024")
nutrients.exclude("2025")
nutrients.exclude("2026")

# Create a header row for the destination data file
dstHeader = ""
for nutrient in nutrients.nutrients:
    if nutrient.include == True:
        dstHeader += nutrient.name + "~"

# Remove the extra trailing ~ character from the header
    dstHeader = dstHeader.rstrip('~')

###########################################################################
#endregion





#region Parse
###########################################################################

# Add the dstHeader to the destination data file
dstData.write(dstHeader)

# Iterate through each food in the source data file "food.csv"
# Limit to 10 items for development/testing purposes
index = 0
progress = 0
for food in FoodList:
    progress += 1
    sys.stdout.write("\rProessing " + str(progress) + " of " + str(numFoods))
    fdcId = food[0]
    dataType = food[1]

    if optionKeepBrandedFoods == False:
        if dataType == "branded_food": continue

    index = index + 1
    if index >= 10:
        break

    fdcId = food[0]
    description = food[2]

    # Add the food description to the data string
    dataString = description
    dataString += "~"
    dataString += dataType
    dataString += "~"

    # Get a list of the nutrient content for this food
    # The list is sorted so if appends stop then no further need to loop
    append = False
    nutrientContent = []
    for item in FoodNutrientList:
        itemFdcId = item[1]
        if itemFdcId == fdcId:
            nutrientContent.append(item)
            append = True
        elif append == True:
                break

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
            if addedAmount == False:
                dataString += "~"

    # Remove the extra trailing ~ character from the data string
    dataString = dataString.rstrip('~')

    # Add a newline character to the end of the data string
    dataString += "\n"

    # Append the data string to the destination file
    dstData.write('\n')
    dstData.write(dataString)

###########################################################################
#endregion





#region Post-Parse
###########################################################################

print("\nEnd: " + str(datetime.datetime.now()))

# Report the combined size of modified set of data files
size = 0
for filename in os.listdir(dstPath):
    if filename.endswith(".txt"): 
        size += os.path.getsize(dstPath + filename)
        continue
    else:
        continue
size = size/1000/1000
print("Destination USDA data file size: " + str(size) + " MB")

# Close files
dstData.close()

###########################################################################
#endregion