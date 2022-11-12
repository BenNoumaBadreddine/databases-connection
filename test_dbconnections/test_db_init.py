import logging

from dbconnections.databases_connection import get_db_connection, init_all_databases
from test_dbconnections.test_config import MLFLOW_DB_CONFIG, APPLICATION_NAME

dbs = [MLFLOW_DB_CONFIG]


def test_db_init_individual_no_exception():
    try:
        for db in dbs:
            logging.getLogger().warning(f"Testing db: {db.db_name}")
            _ = get_db_connection(db)
    except Exception as ex:
        assert False, f"get_db_connection failed: {ex}"


def test_db_init_no_exception():
    try:
        # test initialization with and without threading as well a with and without application name
        init_all_databases(dbs, use_threading=False, application_name=APPLICATION_NAME)
        init_all_databases(dbs, use_threading=False, application_name=None)
        init_all_databases(dbs, use_threading=True, application_name=APPLICATION_NAME)
        init_all_databases(dbs, use_threading=True, application_name=None)
    except Exception as ex:
        assert False, f"init_all_databases failed: {ex}"
