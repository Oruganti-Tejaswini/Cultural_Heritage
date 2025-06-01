import snowflake.connector
import os

def connect_snowflake():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="CULTUREFLOW",
        schema="RAW_DATA"
    )
    return conn

def insert_ar_metadata(monument_name, image_name):
    conn = connect_snowflake()
    cs = conn.cursor()
    cs.execute("""
        INSERT INTO AR_IMAGE_METADATA (monument_name, image_name)
        VALUES (%s, %s)
    """, (monument_name, image_name))
    cs.close()
    conn.close()
