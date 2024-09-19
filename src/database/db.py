import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sqlite', 'anuncios.db')

def cria_tabelas():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Imovel (
        id INTEGER PRIMARY KEY,
        descricao TEXT,
        url TEXT,
        endereco TEXT,
        preco REAL,
        valor_total REAL,
        custos_adicionais TEXT ,
        imagem TEXT,
        caracteristicas TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        notificado INTEGER NOT NULL DEFAULT 0
    );
    """)

    conn.commit()

    conn.close()
    print("DB: Tabelas OK!")


def insere_anuncio(id, desc, url, end, preco, total, custos, img, caracteristicas):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sucesso = False
    try:
        cursor.execute("""
        INSERT INTO Imovel (
            id, descricao, url, endereco, preco, valor_total, custos_adicionais, imagem, caracteristicas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, desc, url, end, preco, total, custos, img, caracteristicas))
        conn.commit()
        print("DB: Novo Anuncio inserido com sucesso!")
        sucesso = True
    except sqlite3.IntegrityError:
        #print("DB: Anuncio ja existe na base")
        pass
    except Exception as e:
        print("Um erro ocorreu:", e)
        print("Tipo de erro:", type(e).__name__)
        print("DB: Erro")
        
    conn.close()

    return sucesso

 
def busca_anuncios_nao_notificados():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Imovel WHERE notificado = 0")

    registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return registros


def marca_anuncio_notificado(anuncio_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"UPDATE Imovel SET notificado = 1 WHERE id = {anuncio_id}")

    conn.commit()
    cursor.close()
    conn.close()
