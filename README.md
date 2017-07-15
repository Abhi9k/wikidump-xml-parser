# wikidump-xml-parser
Python module to parse xml wikidump of type pages-meta-history and return page which is edited maximum time within any give time range
## Dependency
 1. Python
## Usage
1. Clone this repository
2. Edit the config file
  2.1 First line should be the complete  path to the wikidump xml file
  2.2 Second and third line should be start and end date respectively to define the range in which revisions should be considered
  2.3 All dates should be in YYYY-mm-yy fomat
3. Run the module
  3.1 To parse the first 2 Kb of the dump file type: python wikiparse.py config 0 2048
  3.2 To parse the entire dump file type: python wikiparse.py config 0 -1
