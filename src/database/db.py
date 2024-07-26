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
        caracteristicas TEXT
    );
    """)

    conn.commit()

    conn.close()

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
        print("DB: Anuncio ja existe na base")
    except Exception as e:
        print("Um erro ocorreu:", e)
        print("Tipo de erro:", type(e).__name__)
        print("DB: Erro")
        
    conn.close()

    return sucesso


def novo_anuncio():
    id_imovel = 2
    descricao_imovel = "Casa com piscina em São Paulo"
    url_imovel = "http://imoveis.com/casa-com-piscina"
    endereco_imovel = "Av. Paulista, 100"
    preco_imovel = 750_000.00
    custo_total = 1_000_000.00
    custos_adicionais = "IPTU 200, energia 500"
    imagem_imovel = "http://imoveis.com/foto-casa.jpg"
    caracteristicas_imovel = "4 quartos, piscina, garagem para 2 carros"

    result = insere_anuncio(id_imovel, descricao_imovel, url_imovel, endereco_imovel,  preco_imovel, custo_total, custos_adicionais, imagem_imovel, caracteristicas_imovel)
    print(result)





