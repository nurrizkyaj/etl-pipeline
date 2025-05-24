import psycopg2
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

DB_CONFIG = {
    "dbname": "fashionstudiodb",
    "user": "nurrizkyaj",
    "password": "fsdb",
    "host": "localhost",
    "port": "5432"
}

def establish_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        logging.info("Successfully connected to the database.")
        return connection, cursor
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

def create_table_if_not_exists(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        title TEXT UNIQUE,
        price FLOAT,
        rating FLOAT,
        colors INT,
        size TEXT,
        gender TEXT,
        timestamp TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    logging.info(f"Table {table_name} ready for use.")

def insert_or_update_data(cursor, table_name, df):
    insert_query = f"""
    INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (title) DO UPDATE 
    SET price = EXCLUDED.price,
        rating = EXCLUDED.rating,
        colors = EXCLUDED.colors,
        size = EXCLUDED.size,
        gender = EXCLUDED.gender,
        timestamp = EXCLUDED.timestamp;
    """
    
    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))
    logging.info(f"Successfully enter or update {len(df)} data into a table {table_name}.")

def load_to_postgres(df, table_name="products"):
    if df.empty:
        logging.warning("There is no data to insert into PostgreSQL.")
        return
    
    try:
        connection, cursor = establish_connection()
        create_table_if_not_exists(cursor, table_name)
        insert_or_update_data(cursor, table_name, df)

        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Data is successfully inserted or updated in the PostgreSQL table: {table_name}.")
    
    except Exception as e:
        logging.error(f"An error occurred while saving data to PostgreSQL: {e}")