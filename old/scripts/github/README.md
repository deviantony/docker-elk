## Description

These are scripts for collecting and analyzing HydroShare github issues. 

## Usage

`./gitstats.py`

## Files

gitstats.py: main script for collecting and summarizing issue status.

creds.py: python file containing github credentials in the form:
```
username="MyUsername"
password="MySuperSecretPassword"
```

collectdata.py: script for downloading github issues and saving it to a csv file.

issue.py: class definition for storing github json text

plot.py: functions for creating plots using the github issues csv file. 
