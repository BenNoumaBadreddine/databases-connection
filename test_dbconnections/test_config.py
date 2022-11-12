from dbconnections.databases_dataclasses import DbConfig


MLFLOW_DB_CONFIG = DbConfig(db_name="mlflow_db",
                            db_driver="postgresql+psycopg2",
                            dev_port=5432,  # port used for local port forwarding
                            host="localhost",
                            user="ml_user",
                            password="1234",
                            port=5432,
                            secret_name=None,
                            secret_region=None)

APPLICATION_NAME = "pytest db connections module"
