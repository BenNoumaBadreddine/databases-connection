# Databases connection

This repository can be used as a toolbox (python packages) that will be installed and
imported in any python project. 

## Usage

To use this database toolbox in any python project, we need to use the following command:

    pip install git+https://github.com/BenNoumaBadreddine/databases-connection.git@0.0.1#egg=dbconnections

After you complete the installation of the tool, you can import any function, for example:

```python
from dbconnections.databases_connection import get_db_connection
```

### Important

If you make changes you have to increase the version number in the 'setup.py' file.

Therefore, a new git tag needs to be released.

Otherwise, your project will not recognise that a new
version was published and think that everything is up-to-date.

## Pytests

In order to check if the project is working please execute the pytests inside the 'test_dbconnections' folder.

