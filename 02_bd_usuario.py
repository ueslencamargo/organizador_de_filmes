import mysql.connector #Peguei todo só pra garantir.
from mysql.connector import connect
import sys

nome_usuario = sys.argv[1]

try:
    # Conectar ao banco de dados MySQL
    conn = connect(
        host='localhost',  # Endereço do banco de dados
        user='root',  # Nome de usuário do banco de dados
        password='',  # Senha do banco de dados
        database='cadastro'  # Nome do banco de dados
    )

    # Criar o novo banco de dados
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} default charset utf8".format(nome_usuario))
    conn.commit()
    cursor.close()
    conn.close()

    print("Banco de dados {} criado com sucesso.".format(nome_usuario))

    # Conectar ao banco de dados criado
    conn = connect(
        host='localhost',  # Endereço do banco de dados
        user='root',  # Nome de usuário do banco de dados
        password='',  # Senha do banco de dados
        database=nome_usuario  # Nome do banco de dados do usuário
    )

    # Criar a tabela "filmes"
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(50),
            ano VARCHAR(8),
            genero VARCHAR(50),
            diretor VARCHAR(50),
            trailer VARCHAR(200),
            capa VARCHAR(200),
            arquivo VARCHAR(200),
            tmdb VARCHAR(200)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    print("Tabela filmes criada com sucesso.")

except Exception as e:
    print("Ocorreu um erro ao criar o banco de dados ou a tabela:", str(e))
