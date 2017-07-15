# wikidump-xml-parser
Python module to parse xml wikidump of type pages-meta-history and return page which is edited maximum time within any give time range
## Dependency
 1. Python
## Usage
1. Clone this repository
2. Edit the config file
    1. First line should be the complete  path to the wikidump xml file
    2. Second and third line should be start and end date respectively to define the range in which revisions should be considered
    3. All dates should be in YYYY-mm-yy fomat
3. Run the module
    1. To parse the first 2 Kb of the dump file type: ```python wikiparse.py config 0 2048```
    2. To parse the entire dump file type: ```python wikiparse.py config 0 -1```
## Response
The module prints following information on the console
```Page ID Page Title Total number of revisions```
