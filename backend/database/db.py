import sqlite3
from datetime import datetime, date

def get_db_connection():
    conn = sqlite3.connect('gridstack.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table for packaged products
    cur.execute('''
    CREATE TABLE IF NOT EXISTS packaged_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        brand TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        count INTEGER NOT NULL,
        expired TEXT NOT NULL,
        expected_life_span INTEGER
    )
    ''')
    
    # Create table for fresh produce
    cur.execute('''
    CREATE TABLE IF NOT EXISTS fresh_produce (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        produce TEXT NOT NULL,
        result INTEGER NOT NULL    
    )
    ''')
    
    conn.commit()
    conn.close()

def add_packaged_product(brand, expiry_date, count):
    conn = get_db_connection()
    cur = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    today = date.today()
    
    if expiry_date_obj < today:
        expired = "Yes"
        expected_life_span = 0
    else:
        expired = "No"
        expected_life_span = (expiry_date_obj - today).days
    
    cur.execute('''
    INSERT INTO packaged_products (timestamp, brand, expiry_date, count, expired, expected_life_span)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, brand, expiry_date, count, expired, expected_life_span))
    
    conn.commit()
    conn.close()

def add_fresh_produce(produce, result):
    conn = get_db_connection()
    cur = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cur.execute('''
    INSERT INTO fresh_produce (timestamp, produce, result)
    VALUES (?, ?, ?)
    ''', (timestamp, produce, result))
    
    conn.commit()
    conn.close()

def get_all_packaged_products():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM packaged_products')
    products = cur.fetchall()
    
    conn.close()
    return [dict(product) for product in products]

def get_all_fresh_produce():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM fresh_produce')
    produce = cur.fetchall()
    
    conn.close()
    return [dict(item) for item in produce]

