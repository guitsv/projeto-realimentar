import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        if conn.is_connected():
            print("Conexão ao banco de dados realizada com sucesso.")
            return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    return None

def consultar_alimentos():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alimentos")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

def consultar_alimentos_disponiveis():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alimentos WHERE status = 'disponível'")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

def inserir_alimento(nome, descricao, categoria, data_validade, quantidade):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alimentos (nome, descricao, categoria, data_validade, quantidade, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, descricao, categoria, data_validade, quantidade, 'disponível'))
            conn.commit()
            print("Alimento inserido com sucesso!")
        finally:
            cursor.close()
            conn.close()

def alterar_status_alimento(id_alimento, novo_status):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE alimentos
                SET status = %s
                WHERE id = %s
            """, (novo_status, id_alimento))
            conn.commit()
            print(f"Status do alimento {id_alimento} alterado para {novo_status}.")
        finally:
            cursor.close()
            conn.close()
