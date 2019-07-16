# ak-luna-pipeline

## Installation

All package dependencies are maintained in the requirements.txt file. Use pip to install:

```
pip install -r requirements.txt
```

## Usage

Scripts can be run in any order.

1. Source in Luna snippets from a target environment using the Property Manager Snippets CLI.
2. Run compareProject.py, providing both the location of the Luna snippets above and the location of the Pipeline snippets.
3. Run versionSync.py to reconcile the state of the pipeline stages with the actual state in Luna.

## Script Execution

All scripts must be invoked using the python3 interpreter directly.

**Example**

```
python3 <script> <arguments>
```

The arguments supported by each script will be defined below, and can be identified by calling the script with a '--help' or no argument:

```
python3 <script> --help
```

### versionSync.py

Synchronizes the state of all pipeline stages with their complementary Luna state (latest version, etag, activation status).

```
usage: versionSync.py [-h] [--config CONFIG] [--section SECTION] property

positional arguments:
  property           The location of the Akamai pipeline CLI project.

optional arguments:
  -h, --help         show this help message and exit
  --config CONFIG    Full or relative path to .edgerc file (default:
                     /Users/dmcallis/.edgerc)
  --section SECTION  The section of the edgerc file with the proper {OPEN} API
                     credentials. (default: default)
```

### compareProject.py

Reconciles the snippets from the target

```

usage: compareProject.py [-h] pipeline snippets

positional arguments:
  pipeline    The location of the Akamai pipeline CLI project.
  snippets    The location of the property snippets to compare.

optional arguments:
  -h, --help  show this help message and exit
