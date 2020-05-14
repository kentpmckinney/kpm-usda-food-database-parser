<!-- Category: Original;Python -->
# USDA Food Database Parser

This is a Python script to experiment with tailoring and optimizing United States Department of Agriculture (USDA) food database files for use in a JavaScript application.

The United States Department of Agriculture (USDA) publishes a food database with the nutrient contents of many foods commonly found in the United States.

There are currently two ways to access USDA food data:

* Statically include the data files within an application
* Use a web API to pull the data from a server

Either of these methods can be used exlusively, or they can be combined.

The size of the USDA database files is currently greater than 400MB, which is a substantial footprint. Using a web API would minimize the footprint, but it would create a dependency on a network service and consume network resources.

One question worth exploring is: how much of the source data will the target application actually need, and can the rest be stripped away? It also follows to wonder whether there's a more compact way to store the data and whether the data can be formatted to load more quickly and to use computing resources more efficiently.

This project explores these questions in depth.

https://github.com/kentpmckinney/kpm-usda-food-database-parser

## Previewing this Project

This project is hosted at: https://kentpmckinney.github.io/kpm-usda-food-database-parser

## Working with the Source Code

The following instructions explain how to set up a development environment for this project on MacOS. Steps will differ depending on the operating system.

### Prerequisites

The following software must be installed and properly configured on the target machine. 

```
Python 3
```
```
Git (optional but recommended)
```

### Setting up a Development Environment

1. Download a copy of this `usda2js.py` to a local folder.
2. Download a copy of the April 2019 version of the [USDA Food Database](https://fdc.nal.usda.gov/download-datasets.html).
3. Extract the files in the food database to a folder.
4. Edit the script `usda2js.py` and modify the variable srcPath to point to the location of the extracted original USDA Food Database files. Set dstPath to point to the folder where you would like the parsed files to be written to.
5. Run the script with the following command:

```
python3 ./usda2js.py
```

## Deployment

Run the script against the USDA dataset and then deploy the resulting text files

## Technologies Used

* Python

## Authors

Kent McKinney - [GitHub](https://github.com/kentpmckinney) - [LinkedIn](https://www.linkedin.com/in/kentpmckinney/)

### Copyright &copy; 2020 Kent P. McKinney

## Acknowledgments

https://fdc.nal.usda.gov/download-datasets.html