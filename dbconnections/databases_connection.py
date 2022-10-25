import logging
import os
import timeit
from dataclasses import dataclass
from threading import Thread
from urllib.parse import quote

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from databases_dataclasses import DbConfig, DbEngineConfig

logger = logging.getLogger(__name__)

_DATABASES = {}
_DB_ENGINE_CONFIG = DbEngineConfig()
_IS_DEV = "DB_MODE_DEV" in os.environ


@dataclass()
class DatabaseConnection:
    """Class for keeping track of a db connection."""
    engine: Engine
    session: Session
    metadata: MetaData
    tables: {Table}

    def __init__(self, db_config: DbConfig, application_name: str = None):
        _connection_string = f"{db_config.db_driver}://{db_config.user}:{quote(db_config.password)}@{db_config.host}:{db_config.port}/{db_config.database}"
        if application_name:
            if _IS_DEV:
                application_name += " - <local-debugging>"
            _connection_string += f"?application_name={application_name}"
        self.engine = create_engine(_connection_string,
                                    echo=_DB_ENGINE_CONFIG.ECHO,
                                    pool_pre_ping=_DB_ENGINE_CONFIG.POOL_PRE_PING,
                                    pool_size=_DB_ENGINE_CONFIG.POOL_SIZE,
                                    max_overflow=_DB_ENGINE_CONFIG.MAX_OVERFLOW,
                                    pool_recycle=_DB_ENGINE_CONFIG.POOL_RECYCLE)
        self.session_class = sessionmaker(bind=self.engine)
        self.session = Session(self.engine, future=True)


def init_all_databases(db_configs: [DbConfig],
                       db_engine_config: DbEngineConfig = None,
                       use_threading=True,
                       application_name=None):
    start = timeit.default_timer()
    logger.info(f"Start init all databases")

    # if specific configurations are passed use them instead of the default one
    if db_engine_config:
        global _DB_ENGINE_CONFIG
        _DB_ENGINE_CONFIG = DbEngineConfig()

    if use_threading:
        threads = []
        for db_config in db_configs:
            thread = Thread(target=get_db_connection, args=[db_config, application_name])
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        for db_config in db_configs:
            _ = get_db_connection(db_config, application_name)

    logger.info(f"Init of all dbs took {timeit.default_timer() - start}s")


def get_db_connection(db_config: DbConfig, application_name: str = None) -> DatabaseConnection:
    """
    Returns a db connection object depending on whether we are in a production or local environment and
    also depending on the wanted database.
    If the db connection was already initialized, reuse it.
    The environment variable DB_MODE_DEV is used to determine if we are locally testing or not.

    :return: Database connection object
    """
    global _DATABASES
    if _DATABASES.get(db_config.db_name) is None:
        # the requested db is not available in the dict. Therefore we must create a new connection
        logger.debug(f'No database connection to reuse for {db_config.db_name}')
        _DATABASES[db_config.db_name] = DatabaseConnection(db_config, application_name)
    else:
        logger.debug(f'Reusing database connection for {db_config.db_name}')
    return _DATABASES.get(db_config.db_name)
