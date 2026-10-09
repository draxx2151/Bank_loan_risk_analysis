"""
Database Manager Module
Handles SQLite connection lifecycle, schema initialization, bulk loading, and query execution.
Provides deferred, pluggable interface for MySQL support.
"""

import sqlite3
from pathlib import Path
from typing import Union, Tuple, Optional, Any
import pandas as pd
from src.config import DEFAULT_DB_PATH, SCHEMA_SQL_PATH

class DatabaseError(Exception):
    """Custom exception for database operation failures."""
    pass

class DatabaseManager:
    """Manages SQLite database connections, schema execution, and bulk data operations."""

    def __init__(self, db_path: Union[str, Path] = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        # Ensure parent directory exists if using file DB
        if str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Creates and returns a SQLite connection."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to SQLite database at {self.db_path}: {e}")

    def initialize_schema(self, schema_file: Union[str, Path] = SCHEMA_SQL_PATH) -> bool:
        """Executes DDL schema file to create tables and indexes."""
        schema_path = Path(schema_file)
        if not schema_path.exists():
            raise DatabaseError(f"Schema file not found at {schema_path}")

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            with self.get_connection() as conn:
                conn.executescript(sql_script)
                conn.commit()
            return True
        except (sqlite3.Error, OSError) as e:
            raise DatabaseError(f"Error initializing schema from {schema_path}: {e}")

    def initialize_views(self, views_file: Union[str, Path] = None) -> bool:
        """Executes views SQL script to create analytical database views."""
        if views_file is None:
            views_file = self.db_path.parent.parent.parent / "sql" / "views.sql"
        views_path = Path(views_file)
        if not views_path.exists():
            raise DatabaseError(f"Views file not found at {views_path}")

        try:
            with open(views_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            with self.get_connection() as conn:
                conn.executescript(sql_script)
                conn.commit()
            return True
        except (sqlite3.Error, OSError) as e:
            raise DatabaseError(f"Error initializing views from {views_path}: {e}")

    def load_cleaned_data(
        self, 
        df: pd.DataFrame, 
        table_name: str = "bank_loans", 
        if_exists: str = "replace"
    ) -> int:
        """Bulk loads cleaned Pandas DataFrame into SQLite database table."""
        if df is None or df.empty:
            raise DatabaseError("Cannot load empty or None DataFrame into database.")

        # Drop temporary date object columns before DB insertion if present
        export_df = df.copy()
        dt_cols = [c for c in export_df.columns if c.endswith("_dt")]
        if dt_cols:
            export_df = export_df.drop(columns=dt_cols)

        try:
            with self.get_connection() as conn:
                export_df.to_sql(
                    name=table_name, 
                    con=conn, 
                    if_exists=if_exists, 
                    index=False,
                    chunksize=5000
                )
                conn.commit()

            inserted_count = self.get_record_count(table_name)
            return inserted_count
        except Exception as e:
            raise DatabaseError(f"Error loading data into table '{table_name}': {e}")

    def execute_query(self, query: str, params: Union[Tuple, dict] = ()) -> pd.DataFrame:
        """Executes a SQL query and returns results as a Pandas DataFrame."""
        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn, params=params)
                return df
        except Exception as e:
            raise DatabaseError(f"Error executing query: {e}\nQuery: {query}")

    def get_record_count(self, table_name: str = "bank_loans") -> int:
        """Returns total row count for specified table."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                return count
        except sqlite3.Error as e:
            raise DatabaseError(f"Error getting row count for table '{table_name}': {e}")

    def connect_mysql(self, host: str, user: str, password: str, database: str):
        """
        Pluggable MySQL connection adapter (Deferred until SQLite implementation is fully tested).
        """
        try:
            import mysql.connector
            return mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
        except ImportError:
            raise DatabaseError("mysql-connector-python package is not installed. Install via requirements.txt.")
        except Exception as e:
            raise DatabaseError(f"MySQL connection error: {e}")
