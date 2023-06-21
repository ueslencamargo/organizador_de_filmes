import tkinter as tk  # Importa a biblioteca Tkinter para criar a interface gráfica
from urllib.request import urlopen  # Importa a função urlopen para abrir URLs
from mysql.connector import connect  # Importa a função connect para conectar ao banco de dados MySQL
from PIL import Image, ImageTk
from io import BytesIO
import subprocess
import sys
from tkinter import messagebox

bd = sys.argv[1]

comando = 'SELECT capa FROM filmes ORDER BY id desc LIMIT 10'

comando = 'SELECT capa FROM filmes ORDER BY id desc LIMIT 10'

# Conectar ao banco de dados MySQL
conn = connect(
    host='localhost',  # Endereço do banco de dados
    user='root',  # Nome de usuário do banco de dados
    password='',  # Senha do banco de dados
    database=bd  # Nome do banco de dados
    )

    # Selecionar URLs das capas dos filmes
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados
cursor.execute('{}'.format(comando))# Executa uma consulta SQL para selecionar as URLs das capas dos filmes

url_capas = [url[0].strip() for url in cursor.fetchall()]  # Armazena as URLs das capas dos filmes em uma lista
cursor.close()  # Fecha o cursor

cursor = conn.cursor() 
cursor.execute("SELECT titulo FROM filmes")
cursor.fetchall()
nfilmes = cursor.rowcount
cursor.close()  # Fecha o cursor
conn.close()  # Fecha a conexão com o banco de dados

def exibir_imagens():

    def ao_clicar_genero(genero):
        global url_capas # Usa a variável url_capas globalmente
        
        url_capas = selecionar_capas(genero)  # Chama a função selecionar_capas para obter as capas dos filmes do gênero selecionado

        # Remover todas as imagens existentes no frame de imagens
        for widget in frame_imagens.winfo_children():
            widget.destroy()

        # Carregar as novas imagens
        carregar_imagens_na_janela(0)

    def carregar_imagens_na_janela(indice):

        if indice >= len(url_capas):
            return

        url = url_capas[indice]
        try:
            with urlopen(url) as resposta:
                dados_imagem = resposta.read()
        except ValueError:
        # Tratamento da exceção (nesse caso, apenas ignorando o erro)
            pass
        try:
            imagem_pil = Image.open(BytesIO(dados_imagem))
            largura_redimensionada = 200
            altura_redimensionada = 275
       
        # Redimensionar a imagem
            imagem_redimensionada = imagem_pil.resize((largura_redimensionada, altura_redimensionada))

        # Converter a imagem redimensionada para o formato do Tkinter
            imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

            imagens.append(imagem_tk)

            label_imagem = tk.Label(frame_imagens, image=imagem_tk, bg="black")


            label_imagem.grid(row=indice // 5, column=indice % 5, padx=17, pady=5)

            label_imagem.bind("<Button-1>", lambda evento, indice=indice: ao_clicar_na_imagem(indice))
        
        except UnboundLocalError:
            pass

        janela.after(20, carregar_imagens_na_janela, indice + 1)

        def ao_clicar_na_imagem(indice):
            base = url_capas[indice].replace('g,','g')

            tmdb, arquivo, trailer = informações(base)

            subprocess.run(["python", "tela_filme.py", str(tmdb), str(arquivo), str(trailer)])
        
    def capturar_texto(event):
        global url_capas  # Usa a variável url_capas globalmente
        texto = caixa_pesquisa.get()  # Obtém o texto digitado na caixa de pesquisa
        
        url_capas = pesquisa(texto)  # Chama a função pesquisa para obter as capas dos filmes correspondentes à pesquisa

        # Remover todas as imagens existentes no frame de imagens
        for widget in frame_imagens.winfo_children():
            widget.destroy()

        # Carregar as novas imagens
        carregar_imagens_na_janela(0)

    def selecionar_capas(genero):
        
        conn = connect(
            host='localhost',  # Endereço do banco de dados
            user='root',  # Nome de usuário do banco de dados
            password='',  # Senha do banco de dados
            database=bd  # Nome do banco de dados
        )

        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados
        cursor.execute("SELECT capa FROM filmes WHERE genero like '%{}%' ORDER BY id DESC LIMIT 10".format(genero))  # Executa uma consulta SQL para selecionar as URLs das capas dos filmes do gênero especificado
    
        url_capas = [url[0].strip() for url in cursor.fetchall()]  # Armazena as URLs das capas dos filmes em uma lista
        cursor.close()  # Fecha o cursor

        cursor = conn.cursor()

        cursor.execute("SELECT capa FROM filmes WHERE genero like '%{}%'".format(genero))  # Executa uma consulta SQL para selecionar as URLs das capas dos filmes do gênero especificado
        cursor.fetchall()

        total = cursor.rowcount
        cursor.close()  # Fecha o cursor
        conn.close()  # Fecha a conexão com o banco de dados


        conn.close()  # Fecha a conexão com o banco de dados

        messagebox.showinfo("Informação", f"{total} filmes de {genero}")

        return url_capas
    
    def recentes():

        global url_capas # Usa a variável url_capas globalmente

        # Remover todas as imagens existentes no frame de imagens
        for widget in frame_imagens.winfo_children():
            widget.destroy()

                # Conectar ao banco de dados MySQL
        conn = connect(
            host='localhost',  # Endereço do banco de dados
            user='root',  # Nome de usuário do banco de dados
            password='',  # Senha do banco de dados
            database=bd  # Nome do banco de dados
        )

        # Selecionar URLs das capas dos filmes
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados
        cursor.execute("SELECT capa FROM filmes ORDER BY id DESC LIMIT 10")# Executa uma consulta SQL para selecionar as URLs das capas dos filmes

        url_capas = [url[0].strip() for url in cursor.fetchall()]  # Armazena as URLs das capas dos filmes em uma lista
        cursor.close()  # Fecha o cursor

        cursor = conn.cursor()

        carregar_imagens_na_janela(0)

        return url_capas
    
    def informações(base):
        
        conn = connect(
            host='localhost',  # Endereço do banco de dados
            user='root',  # Nome de usuário do banco de dados
            password='',  # Senha do banco de dados
            database=bd  # Nome do banco de dados
        )

        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados
        cursor.execute("SELECT tmdb, arquivo, trailer FROM filmes WHERE capa = '{}'".format(base))  # Executa uma consulta SQL para selecionar as URLs das capas dos filmes do gênero especificado

        row = cursor.fetchone()  # Obtém a primeira linha da consulta
        if row:
            tmdb, arquivo, trailer = row  # Desempacota os valores da linha
        else:
            tmdb, arquivo, trailer = None, None, None  # Valores padrão caso não haja resultado

        cursor.close()  # Fecha o cursor
        conn.close()  # Fecha a conexão com o banco de dados

        return tmdb, arquivo, trailer

    def pesquisa(texto):
        
        conn = connect(
            host='localhost',  # Endereço do banco de dados
            user='root',  # Nome de usuário do banco de dados
            password='',  # Senha do banco de dados
            database=bd  # Nome do banco de dados
        )

        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL no banco de dados
        cursor.execute("SELECT capa FROM filmes WHERE titulo LIKE '%{}%' OR ano LIKE '%{}%' OR diretor LIKE '%{}%' ORDER BY id DESC LIMIT 10".format(texto, texto, texto))

        url_capas = [url[0].strip() for url in cursor.fetchall()]  # Armazena as URLs das capas dos filmes em uma lista
        cursor.close()  # Fecha o cursor
        conn.close()  # Fecha a conexão com o banco de dados

        return url_capas

    janela = tk.Tk()  # Cria uma janela Tkinter
    janela.title("Organizador de Filmes Pessoais - Senac - Cachoeira do Sul- RS - Professor Alcemar Pothin - Aluno Ueslen Camargo")
    largura_janela = 1250
    altura_janela = 720
    largura_tela = janela.winfo_screenwidth()  # Obtém a largura da tela
    altura_tela = janela.winfo_screenheight()  # Obtém a altura da tela
    pos_x = (largura_tela - largura_janela) // 2  # Calcula a posição x da janela para centralizá-la na tela
    pos_y = (altura_tela - altura_janela) // 2  # Calcula a posição y da janela para centralizá-la na tela
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")  # Define a geometria da janela
    janela.configure(bg="#50336F")  # Define a cor de fundo da janela como preto
    janela.overrideredirect(False)  # Remove a barra de título da janela

    frame_principal = tk.Frame(janela, bg="#50336F")  # Cria um frame na janela principal
    frame_principal.pack(pady=10)  # Define o espaçamento do frame

    frame_botoes = tk.Frame(frame_principal, bg="#50336F")  # Cria um frame para os botões
    frame_botoes.pack(padx=10, pady=10)  # Define o espaçamento do frame de botões

    generos = ["Ação", "Terror", "Drama", "Ficção", "Suspense", "Romance", "Fantasia", "Animação", "Faroeste", "Aventura", "Comédia"]  # Lista de gêneros de filmes

    botao_width = 10  # Largura dos botões

    botao_recentes = tk.Button(frame_botoes, text="Recentes",width = 10,command=recentes)
    botao_recentes.pack(side="left", padx=5, pady=3)  # Posiciona os botões no frame de botões

    for genero in generos:
        botao_genero = tk.Button(frame_botoes, text=genero, width=botao_width, command=lambda genero=genero: ao_clicar_genero(genero))  # Cria um botão para cada gênero e associa a função ao_clicar_genero a cada botão
        botao_genero.pack(side="left", padx=5, pady=3)  # Posiciona os botões no frame de botões

    frame_imagens = tk.Frame(frame_principal, bg="#50336F")  # Cria um frame para exibir as imagens
    frame_imagens.pack(padx=15, pady=12)  # Define o espaçamento do frame de imagens

    imagens = []  # Lista para armazenar as imagens

    carregar_imagens_na_janela(0)  # Chama a função para carregar as imagens na janela
    
    mundo = Image.open("J:\My Drive\SEGUNDA TENTATIVA\compartilhar.png")
    mundo = mundo.resize((30, 30))  # Ajuste o tamanho da imagem conforme necessário
    mundo = ImageTk.PhotoImage(mundo)

    frame_botoes_inferiores = tk.Frame(janela, bg="#50336F")  # Cria um frame para os botões inferiores
    frame_botoes_inferiores.pack(side="top", pady=(0,10))  # Define o espaçamento do frame de botões inferiores

    #botao_adicionar = tk.Button(frame_botoes_inferiores, text="Adicionar Filme", width=13,command=lambda: subprocess.run(["python", "cadastrar_filme.py", str(bd)]))  # Cria um botão para adicionar filmes
    #botao_adicionar.pack(side="left", padx=60)  # Posiciona o botão na parte esquerda do frame

    texto_lateral = tk.Label(frame_botoes_inferiores, text=bd, fg="white", bg="#50336F", font=("Calibri", 12, "italic"))
    texto_lateral.pack(side="left")

    caixa_pesquisa = tk.Entry(frame_botoes_inferiores, bg="dark grey", fg="black", width=45, font=18)  # Cria uma caixa de texto para a pesquisa
    caixa_pesquisa.insert(0, "Pesquisar por título, ano, diretor ou atores...")  # Insere um texto padrão na caixa de pesquisa
    caixa_pesquisa.bind("<FocusIn>", lambda event: caixa_pesquisa.delete(0, "end"))  # Remove o texto padrão quando a caixa de pesquisa recebe foco
    caixa_pesquisa.pack(side="left", padx=60)  # Posiciona a caixa de pesquisa no frame
    caixa_pesquisa.bind("<Return>", capturar_texto)  # Captura o texto quando a tecla Enter é pressionada

    texto_lateral = tk.Label(frame_botoes_inferiores, text=f"{nfilmes} filmes cadastrados", fg="white", bg="#50336F", font=("Calibri", 12, "italic"))
    texto_lateral.pack(side="left",padx=60)

    botao_redondo = tk.Button(frame_botoes_inferiores, image=mundo, borderwidth=0, highlightthickness=0, bg="#50336F", activebackground="#50336F", command=lambda: exibir_imagens())
    botao_redondo.pack(side="left")

    comando ='SELECT capa FROM filmes WHERE id > 12 ORDER BY id DESC LIMIT 10'

    janela.mainloop()  # Inicia o loop principal do Tkinter
    

exibir_imagens()  # Chama a função para exibir as imagens
