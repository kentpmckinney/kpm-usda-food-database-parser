# USDA Food Database Parser

Python script to parse USDA food database CSV files and convert the data into a format which is optimized for use in a JavaScript application.

The size of the USDA database is curretly greater than 400MB. There is a web API available, but it 

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
Python 3.8
USDA Food Database April 2019
```

## Authors

**Kent McKinney** - [GitHub](https://github.com/kentpmckinney)

## License

This project is licensed under the GPlv3 License - see the [LICENSE.md](LICENSE.md) file for details