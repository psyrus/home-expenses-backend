from sqlalchemy import create_engine
import logging

# https://docs.sqlalchemy.org/en/20/core/connections.html#module-sqlalchemy.engine
# https://gameprogrammingpatterns.com/singleton.html
# https://gameprogrammingpatterns.com/service-locator.html

class DatabaseSingleton:
    _engine = None

    def __new__(cls):
        if cls._engine is None:
            cls._engine = super(DatabaseSingleton, cls).__new__(cls)
            cls._engine = create_engine(
                "postgresql+psycopg://postgres:postgres@localhost:5432/backend")
            logging.info("Creating new engine instance")
        else:
            logging.info("No new engine instance needed to be created")
        return cls._engine
