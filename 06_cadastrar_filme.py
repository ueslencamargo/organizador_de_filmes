import PySimpleGUI as sg
import sys
import mysql.connector

#db = sys.argv[1]

db='ueslen'

# Definir o tema e tamanho de fonte
sg.theme('LightBlue')
sg.set_options(font=('Calibri', 14))

# Definir o layout da janela
layout_cadastro = [
    [sg.Text('        Cadastrar Filme    ', font=('Calibri', 20)),sg.Image('movie.png')],
    [sg.Text('É muito importante as informações estarem corretas!',font=('Calibri', 11))],
    [sg.Text('Título do Filme:', size=(25, 1))], [sg.Input(key='titulo', size=(33, 1))],
    [sg.Text('Ano de Lançamento:', size=(25, 1))], [sg.Input(key='ano', size=(33, 1))],
    [sg.Text('Gênero ou gêneros:', size=(25, 1))], [sg.Input(key='genero', size=(33, 1))],
    [sg.Text('Diretor e atores:', size=(25, 1))], [sg.Input(key='diretor_atores', size=(33, 1))],
    [sg.Text('Link do Trailer:', size=(14, 1)),sg.Text('use o link embed',font=('Calibri', 11,'italic'))], [sg.Input(key='link_trailer', size=(33, 1))],
    [sg.Text('Link da Capa:', size=(11, 1)),sg.Text('use o url direto para a imagem',font=('Calibri', 11,'italic'))], [sg.Input(key='link_capa', size=(33, 1))],
    [sg.Text('Link do Arquivo:', size=(13, 1)),sg.Text('use o link direto para o vídeo',font=('Calibri', 11,'italic'))], [sg.Input(key='link_arquivo', size=(33, 1))],
    [sg.Text('Link do TMDB:', size=(25, 1))], [sg.Input(key='tmdb', size=(33, 1))],
    [sg.Text('     É recomendável usar um encurtador de link.   \n                      Para urls muito longas.',font=('Calibri', 12))],
    [sg.Button('Inserir', size=(12, 1)),sg.Text(' '*15),sg.Button('Cancelar', size=(12, 1))]
]

def check_existing_record(cursor, titulo):
    query = "SELECT COUNT(*) FROM filmes WHERE titulo = %s"
    cursor.execute(query, (titulo,))
    result = cursor.fetchone()
    count = result[0]
    return count > 0

# Criar a janela
janela_cadastrof = sg.Window('Cadastro de Filme', layout_cadastro, element_justification='left', finalize=True, no_titlebar=True)

# Conectar ao banco de dados
conn = mysql.connector.connect(host='localhost', user='root', password='', database=db)
cursor = conn.cursor()

# Loop de evento para capturar interações do usuário
while True:
    event, values = janela_cadastrof.read()

    # Verificar se o usuário fechou a janela ou clicou no botão de Cadastrar
    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break

    elif event == 'Inserir':
        titulo = values['titulo']
        if check_existing_record(cursor, titulo):
            janela_cadastrof.hide()
            sg.popup_no_titlebar("Já temos cadastrado um filme chamado:",titulo,"Procure atualizar as informações.")
            janela_cadastrof.un_hide()
        
        else:
            # Verificar se há algum valor em branco
            if any(value.strip() == '' for value in values.values()):
                sg.popup_no_titlebar("Por favor, preencha todos os campos.")
            else:
                # Inserir um novo registro
                insert_sql = "INSERT INTO filmes (titulo, ano, genero, diretor, trailer, capa, arquivo, tmdb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                insert_params = (
                    values['titulo'], values['ano'], values['genero'], values['diretor_atores'], values['link_trailer'],
                    values['link_capa'], values['link_arquivo'], values['tmdb'])
                cursor.execute(insert_sql, insert_params)
                conn.commit()
                sg.popup_no_titlebar("Filme cadastrado com sucesso!")


# Fechar a janela
janela_cadastrof.close()
cursor.close()
conn.close()
