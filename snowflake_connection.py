import snowflake.connector
import pandas as pd
from config import SNOWFLAKE_CONFIG


def get_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        account=SNOWFLAKE_CONFIG["account"],
        warehouse=SNOWFLAKE_CONFIG["warehouse"],
        database=SNOWFLAKE_CONFIG["database"],
        schema=SNOWFLAKE_CONFIG["schema"],
        role=SNOWFLAKE_CONFIG["role"],
    )


def run_query(query):
    conn = get_connection()

    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()