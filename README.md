# Configuration and use
This file contains the information to sep up and use the ***eltjr.py*** tool in the CLI tool - ELT directory.
## Dependencies
- This tool was implemented using Python3.9.
- request and pandas must be installed before using the tool.

### requests
To install using PyPI:
> python -m pip install requests

### pandas
Install it with:
> pip install pandas

Pandas uses NumPy. The command should install it if it is absent, otherwise use:
> pip install numpy

## Using the tool
Use the tool is easy, just use the next command in a command-line interface, for example Command Prompt in Windows:
> python eltjr.py *day*

Where day must have the format: YYYY-MM-DD. day argument is required, otherwise, the tool notifies the user.

The tool always produces a result. It can show an error message from the API like:

*Error: httphandler: only data in range [2021-01-01 - 2021-03-31] is available*

or a load status message:

*Loaded songs: 10*

*Failed inserts (integrity): 0*