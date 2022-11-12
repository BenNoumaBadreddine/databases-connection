from dbconnections.databases_connection import get_db_connection
from test_dbconnections.test_config import APPLICATION_NAME, MLFLOW_DB_CONFIG
from test_dbconnections.test_dbs_schema import Experiment


def test_mlflow_db_connection():
    try:
        mlflow_db_connection = get_db_connection(MLFLOW_DB_CONFIG,
                                                 application_name=APPLICATION_NAME)
        experiment_instance = mlflow_db_connection.session.query(Experiment.experiment_id).first()
        assert experiment_instance is not None
    except Exception as ex:
        assert False, f"test_mlflow_db_connection failed: {ex}"
