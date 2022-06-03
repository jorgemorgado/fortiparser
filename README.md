# fortiparser

A Python module to parse a Forinet FortiGate configuration file. It returns a dictionary or a JSON structure.

## Setup

### Virtual Environment

```bash
# create venv
python3 -m venv venv

# activate virtual environment
. venv/bin/activate

# check version
python -V

# install dependencies
#pip install -r requirements.txt
```

## Example

Using the ```parser.py``` script to demonstrate the module:

```bash
# Get help
./parser.py -h

# Provide a configuration file
./parser.py path/to/your_configuration_file.conf

# Provide a configuration file via stdin
./parser.py < path/to/your_configuration_file.conf

# Save the JSON output to a file
./parser.py path/to/your_configuration_file.conf > your_configuration.json

# Different output types
./parser.py --format json sample.conf
./parser.py --format dict sample.conf
./parser.py --format text sample.conf
```
