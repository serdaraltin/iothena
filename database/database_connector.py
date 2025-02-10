from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

class Connector:
    engine = None

    def __init__(self) -> None:
        """
        Initialize the database connection and session maker.
        """
        self.engine = create_engine(database_config.remote_url())
        self.Session = sessionmaker(bind=self.engine)


    def check_connection(self):
        """
        Check if the database connection is valid.
        """
        try:
            with self.engine.connect() as connection:
                return True
        except SQLAlchemyError as e:
            return str(e)

    @contextmanager
    def get_session(self):
        """
        Context manager for safely handling database sessions.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
