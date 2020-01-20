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

import csv
import sys
import os

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

# Open source data files
srcFoods = open(srcPath + "food.csv", "r") # food.csv | list of foods
srcNutrients = open(srcPath + "food_nutrient.csv", "r") # food_nutrient.csv | nutrient content of foods
srcNutrientList = open(srcPath + "nutrient.csv", "r") # nutrient.csv | list of nutrients

# Create/Open destination data file
dstData = open(dstPath + "data.txt", "w")

# Import list of nutrients
nutrients = Nutrients()
csvNutrientList = csv.reader(srcNutrientList, delimiter=',')
srcNutrientList.seek(0)
null = srcNutrientList.readline()
for nutrient in csvNutrientList:
    id = nutrient[0]
    name = nutrient[1]
    unit = nutrient[2]
    nutrients.add(id, name, unit)

# Create a header row for the destination data file
dstHeader = ""
for nutrient in nutrients.nutrients:
    if nutrient.include == True:
        dstHeader += nutrient.name + "~"

###########################################################################
#endregion





#region Parse
###########################################################################

# Create CSV readers for source data files
csvSrcFoods = csv.reader(srcFoods, delimiter=',')
csvSrcNutrients = csv.reader(srcNutrients, delimiter=',')
numFoods = sum(1 for line in csvSrcFoods)

# Add the dstHeader to the destination data file
dstData.write(dstHeader)

# Iterate through each food in the source data file "food.csv"
# Limit to 10 items for development/testing purposes
index = 0
progress = 0
srcFoods.seek(0)
null = srcFoods.readline()
for food in csvSrcFoods:
    progress += 1
    sys.stdout.write("\rProessing " + str(progress) + " of " + str(numFoods))
    dataType = food[1]

    if optionKeepBrandedFoods == False:
        if dataType == "branded_food": continue

    # discard food items of type "sample_food"
    if dataType == "sample_food": continue
    if dataType == "sub_sample_food": continue
    if dataType == "market_acquisition": continue

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

    # Add the nutrient contents of the current food to the data string
    srcNutrients.seek(0)
    null = srcNutrients.readline()
    for nutrient in csvSrcNutrients:
        nutFdcId = nutrient[1]
        nutId = nutrient[2]
        if nutFdcId == fdcId and nutrients.isIncluded(nutId) == True:
            amount = nutrient[3]
            dataString += amount
            dataString += "~"
    
    # Add a newline character to the end of the data string
    dataString += "\n"

    # Append the data string to the destination file
    dstData.write('\n')
    dstData.write(dataString)

###########################################################################
#endregion





#region Post-Parse
###########################################################################

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