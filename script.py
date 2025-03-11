import time
import csv
import json
import psycopg2
import pymongo
from pymongo import MongoClient

#Configurazione connessioni ai DB
SQL_DB = {
    "host": "localhost",
    "user": "postgres",
    "password": "password",
    "database": "benchmark"
}

MONGO_DB = {
    "host": "localhost",
    "port": 27017,
    "username": None,  # Imposta a None se non è richiesto
    "password": None,  # Imposta a None se non è richiesto
    "authSource": "admin",  # Il database di autenticazione, di solito "admin"
    "database": "benchmark_db"
}

#Funzioni per connetterci ai Db
def connect_sql():
    conn = psycopg2.connect(**SQL_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_benchmark_id ON benchmark(id)")  # Indice su PostgreSQL
    conn.commit()
    return conn

def connect_mongo():
    client = MongoClient(
        MONGO_DB["host"],
        MONGO_DB["port"],
        username=MONGO_DB.get("username"),
        password=MONGO_DB.get("password"),
        authSource=MONGO_DB.get("authSource", "admin")
    )
    db = client[MONGO_DB["database"]]
    db.users.create_index("id")
    return db

#Funzioni per leggere i file CSV e JSON
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames
        if "nome" in header and "email" in header:
            return [
                {"id": int(row['id']), "nome": row['nome'], "email": row['email'], "indirizzo": row['indirizzo']}
                for row in reader
            ]
        else:  # File di update
            return [
                {"id": int(row['id']), "indirizzo": row['indirizzo']}
                for row in reader
            ]

def read_json(file_path):
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
        if "nome" in data[0] and "email" in data[0]:  
            return [
                {"id": int(row['id']), "nome": row['nome'], "email": row['email'], "indirizzo": row['indirizzo']}
                for row in data
            ]
        else:  # File di update
            return [
                {"id": int(row['id']), "indirizzo": row['indirizzo']}
                for row in data
            ]

#Elimionazione dati dai FB
def clear_sql():
    conn = connect_sql()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE benchmark RESTART IDENTITY CASCADE")  
    conn.commit()
    cursor.close()
    conn.close()

def clear_mongo():
    db = connect_mongo()
    db.users.delete_many({})

# FunzionI per i benchmark
def benchmark_sql(operation, data):
    conn = connect_sql()
    cursor = conn.cursor()
    start_time = time.time()
    
    if operation == "INSERT":
        clear_sql()
        query = "INSERT INTO benchmark (id, nome, email, indirizzo) VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, [(row['id'], row['nome'], row['email'], row['indirizzo']) for row in data])
    elif operation == "SELECT":
        for row in data:
            cursor.execute("SELECT * FROM benchmark WHERE id = %s", (row['id'],))
            cursor.fetchone()
    elif operation == "SELECT_ALL":
        cursor.execute("SELECT * FROM benchmark")
        cursor.fetchall()
    elif operation == "UPDATE":
        query = "UPDATE benchmark SET indirizzo = %s WHERE id = %s"
        cursor.executemany(query, [(row['indirizzo'], row['id']) for row in data])
    elif operation == "DELETE":
        cursor.execute("DELETE FROM benchmark")
    
    conn.commit()
    cursor.close()
    conn.close()
    return time.time() - start_time

def benchmark_mongo(operation, data):
    db = connect_mongo()
    collection = db.users
    start_time = time.time()
    
    if operation == "INSERT":
        clear_mongo()
        collection.insert_many(data)
    elif operation == "SELECT":
        for row in data:
            collection.find_one({"id": row['id']})
    elif operation == "SELECT_ALL":
        list(collection.find())
    elif operation == "UPDATE":
        for row in data:
            collection.update_one({"id": row['id']}, {"$set": {"indirizzo": row['indirizzo']}})
    elif operation == "DELETE":
        collection.delete_many({})
    
    return time.time() - start_time

# Esegui il benchmark
if __name__ == "__main__":
    insert_data_csv = read_csv("insert_data.csv")
    update_data_csv = read_csv("update_data.csv")
    insert_data_json = read_json("insert_data.json")
    update_data_json = read_json("update_data.json")
    
    clear_sql()
    clear_mongo()
    
    # Esegui prima tutto per CSV
    for op in ["INSERT", "SELECT", "SELECT_ALL", "UPDATE", "DELETE"]:
        print(f"CSV - {op}: POSTGRES = {benchmark_sql(op, insert_data_csv if op != 'UPDATE' else update_data_csv):.4f}s, MongoDB = {benchmark_mongo(op, insert_data_csv if op != 'UPDATE' else update_data_csv):.4f}s")
    
    # Poi esegui tutto per JSON
    for op in ["INSERT", "SELECT", "SELECT_ALL", "UPDATE", "DELETE"]:
        print(f"JSON - {op}: POSTGRES = {benchmark_sql(op, insert_data_json if op != 'UPDATE' else update_data_json):.4f}s, MongoDB = {benchmark_mongo(op, insert_data_json if op != 'UPDATE' else update_data_json):.4f}s")