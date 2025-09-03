"""Transaction management utilities for database operations."""

from contextlib import contextmanager
from typing import Generator, Any, Callable
from sqlmodel import Session
from backend.app.core.database import engine
import logging

logger = logging.getLogger(__name__)


@contextmanager
def transaction() -> Generator[Session, None, None]:
    """Context manager for database transactions with automatic rollback on error."""
    session = Session(engine)
    try:
        yield session
        session.commit()
        logger.debug("Transaction committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        session.close()


@contextmanager
def read_only_transaction() -> Generator[Session, None, None]:
    """Context manager for read-only database operations."""
    session = Session(engine)
    try:
        yield session
        # No commit for read-only operations
        logger.debug("Read-only transaction completed")
    except Exception as e:
        logger.error(f"Read-only transaction error: {e}")
        raise
    finally:
        session.close()


def transactional(func: Callable) -> Callable:
    """Decorator to wrap a function in a database transaction."""
    def wrapper(*args, **kwargs) -> Any:
        with transaction() as session:
            # Inject session as first argument if function expects it
            import inspect
            sig = inspect.signature(func)
            if 'session' in sig.parameters:
                return func(session, *args, **kwargs)
            else:
                return func(*args, **kwargs)
    return wrapper


class TransactionManager:
    """Advanced transaction management with nested transaction support."""
    
    def __init__(self):
        self._session = None
        self._transaction_depth = 0
    
    def begin(self) -> Session:
        """Begin a new transaction or create a savepoint for nested transactions."""
        if self._session is None:
            self._session = Session(engine)
            self._transaction_depth = 1
            logger.debug("Started new transaction")
        else:
            # Create savepoint for nested transaction
            savepoint_name = f"sp_{self._transaction_depth}"
            self._session.execute(f"SAVEPOINT {savepoint_name}")
            self._transaction_depth += 1
            logger.debug(f"Created savepoint: {savepoint_name}")
        
        return self._session
    
    def commit(self):
        """Commit the current transaction or release savepoint."""
        if self._session is None:
            raise RuntimeError("No active transaction to commit")
        
        if self._transaction_depth == 1:
            self._session.commit()
            logger.debug("Transaction committed")
        else:
            # Release savepoint
            savepoint_name = f"sp_{self._transaction_depth - 1}"
            self._session.execute(f"RELEASE SAVEPOINT {savepoint_name}")
            logger.debug(f"Released savepoint: {savepoint_name}")
        
        self._transaction_depth -= 1
        
        if self._transaction_depth == 0:
            self._session.close()
            self._session = None
    
    def rollback(self):
        """Rollback the current transaction or to savepoint."""
        if self._session is None:
            raise RuntimeError("No active transaction to rollback")
        
        if self._transaction_depth == 1:
            self._session.rollback()
            logger.debug("Transaction rolled back")
        else:
            # Rollback to savepoint
            savepoint_name = f"sp_{self._transaction_depth - 1}"
            self._session.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            logger.debug(f"Rolled back to savepoint: {savepoint_name}")
        
        self._transaction_depth -= 1
        
        if self._transaction_depth == 0:
            self._session.close()
            self._session = None
    
    @contextmanager
    def transaction_scope(self) -> Generator[Session, None, None]:
        """Context manager for transaction scope with automatic cleanup."""
        session = self.begin()
        try:
            yield session
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"Transaction scope error: {e}")
            raise


# Global transaction manager instance
transaction_manager = TransactionManager()


def bulk_insert(session: Session, objects: list, batch_size: int = 1000):
    """Efficiently insert multiple objects in batches."""
    for i in range(0, len(objects), batch_size):
        batch = objects[i:i + batch_size]
        session.add_all(batch)
        session.flush()  # Flush but don't commit
        logger.debug(f"Inserted batch of {len(batch)} objects")


def bulk_update(session: Session, model_class, updates: list, batch_size: int = 1000):
    """Efficiently update multiple objects in batches."""
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]
        session.bulk_update_mappings(model_class, batch)
        session.flush()  # Flush but don't commit
        logger.debug(f"Updated batch of {len(batch)} objects")
