# USDA Food Database Parser

This is a Python script to experiment with tailoring and optimizing United States Department of Agriculture (USDA) food database files for use in a JavaScript application.

## About this Project

The United States Department of Agriculture (USDA) publishes a food database with the nutrient contents of many foods commonly found in the United States.

There are currently two ways to access USDA food data:

* Statically include the data files within an application
* Use a web API to pull the data from a server

Either of these methods can be used exlusively, or they can be combined.

The size of the USDA database files is currently greater than 400MB, which is a substantial footprint. Using a web API would minimize the footprint, but it would create a dependency on a network service and consume network resources.

One question worth exploring is: how much of the source data will the target application actually need, and can the rest be stripped away? It also follows to wonder whether there's a more compact way to store the data and whether the data can be formatted to load more quickly and to use computing resources more efficiently.

This project explores these questions in depth.

## Getting Started

1. Download a copy of this `usda2js.py` to a local folder.
2. Download a copy of the April 2019 version of the [USDA Food Database](https://fdc.nal.usda.gov/download-datasets.html).
3. Extract the files in the food database to a folder.
4. Edit the script `usda2js.py` and modify the variable srcPath to point to the location of the extracted original USDA Food Database files. Set dstPath to point to the folder where you would like the parsed files to be written to.
5. Run the script with the following command:

```
python3 ./usda2js.py
```

### Prerequisites

This script was developed on MacOS running Python 3.8 using the April 2019 version of the USDA Food Database. Use on other platforms or with other versions of Python or the food database may require changes to the source.

```
MacOS
500MB+ available memory
Ability to run a script for up to 24 hours
Python 3.8
USDA Food Database (April 2019)
```

## Authors

**Kent McKinney** - [GitHub](https://github.com/kentpmckinney)

## License

This project is licensed under the GPlv3 License - see the [LICENSE.md](LICENSE.md) file for details