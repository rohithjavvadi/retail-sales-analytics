from snowflake_connection import run_query

query = """
SELECT *
FROM VW_MASTER_SALES
LIMIT 5;
"""

df = run_query(query)

print(df)