import os
from dataclasses import dataclass

from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from dbconnections.secrets_manager import get_secret


@dataclass()
class DatabaseConnection:
    """Class for keeping track of a db connection."""
    engine: Engine
    session: Session
    metadata: MetaData
    tables: {Table}


@dataclass()
class DbEngineConfig:
    ECHO: bool = False
    POOL_PRE_PING: bool = True
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 5
    POOL_RECYCLE: int = 3600


class DbConfig:
    db_name: str
    db_driver: str
    dev_port: int  # port used for local port forwarding
    host: str
    user: str
    password: str
    port: int
    secret_name: str
    secret_region: str

    def __init__(self, db_name: str, db_driver: str, dev_port: int,
                 host: str = None, user=None, password=None, port: int = None,
                 secret_name: str = None, secret_region=None):
        self.db_name = db_name
        self.db_driver = db_driver
        self.dev_port = dev_port
        is_dev = "DB_MODE_DEV" in os.environ

        # the db credentials can either be stored inside the DbConfig object or read from the secrets manager
        if secret_name and secret_region:
            secret = get_secret(secret_name, secret_region)
            # if we have a private db and are locally developing we need a port forwarding
            # for production and public databases we can use the host from secrets manager
            self.host = "localhost" if is_dev else secret.get('host')
            self.user = secret.get('username')
            self.password = secret.get('password')
            # we only need a different port for local def
            self.port = dev_port if is_dev else secret.get('port')
        elif host and user and password and (port or dev_port):
            self.host = host
            self.user = user
            self.password = password
            # we only need a different port for local def
            self.port = dev_port if is_dev else port
        self.database = db_name
