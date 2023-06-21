import PySimpleGUI as sg
import mysql.connector
import sys

db = sys.argv[1]

# Conectar ao banco de dados
conn = mysql.connector.connect(host='localhost', user='root', password='', database=db)
cursor = conn.cursor()

# Consultar os filmes cadastrados
query = "SELECT id, titulo, ano, genero FROM filmes"
cursor.execute(query)
filmes = cursor.fetchall()

# Criar uma lista de informações dos filmes
info_filmes = [f"{filme[0]} - {filme[1]}, {filme[2]}, {filme[3]}" for filme in filmes]

# Definir o tema e tamanho de fonte
sg.theme('LightBlue')
sg.set_options(font=('Calibri', 14))


# Definir o layout da janela de lista de filmes
layout_lista_filmes = [
    [sg.Text('              Lista de Filmes           ', font=('Calibri', 20)),sg.Image('movie.png')],
    [sg.Text('          Pesquise por título, gênero, ano, diretor ou atores.', font=('Calibri', 11))],
    [sg.Input(key='pesquisa', size=(30, 2)), sg.Button('Pesquisar')],
    [sg.Listbox(info_filmes, size=(38, 18), key='filmes_list')],
    [sg.Text('                                  Selecione um Filme pra editar.', font=('Calibri', 11))],
    [sg.Button('Editar',size=(12,1),disabled=True),sg.Text(' '*30),sg.Button('Fechar',size=(12,1))]
]

# Criar a janela de lista de filmes
janela_lista_filmes = sg.Window('Lista de Filmes', layout_lista_filmes, finalize=True, no_titlebar=True)

item_index = 2  # Índice do item a ser selecionado
janela_lista_filmes['filmes_list'].update(set_to_index=item_index)
janela_lista_filmes['Pesquisar'].click()

# Loop de evento para capturar interações do usuário
while True:
    event, values = janela_lista_filmes.read()

    # Verificar se o usuário fechou a janela
    if event == sg.WINDOW_CLOSED or event == 'Fechar':
        quit()
    
    # Verificar se o botão "Pesquisar" foi clicado
    if event == 'Pesquisar':
        
        pesquisa = values['pesquisa'].lower()

        # Consultar os filmes de acordo com o critério de pesquisa
        query = "SELECT id, titulo, ano, genero FROM filmes WHERE LOWER(titulo) LIKE %s OR LOWER(ano) LIKE %s OR LOWER(genero) LIKE %s OR LOWER(diretor) LIKE %s"
        params = [f"%{pesquisa}%"] * 4
        cursor.execute(query, params)
        filmes = cursor.fetchall()

        # Atualizar a lista de informações dos filmes exibidos
        info_filmes = [f"{filme[0]} - {filme[1]}, {filme[2]}, {filme[3]}" for filme in filmes]
        janela_lista_filmes['filmes_list'].update(values=info_filmes)

        if values['filmes_list']:
            janela_lista_filmes['Editar'].update(disabled=False)
        else:
            janela_lista_filmes['Editar'].update(disabled=False)
  

    if event == 'Editar' and values['filmes_list']:
        janela_lista_filmes.hide()
        filme_selecionado = values['filmes_list'][0].split(" - ")[0]

        # Consultar as informações do filme selecionado
        query = "SELECT * FROM filmes WHERE id = %s"
        cursor.execute(query, (filme_selecionado,))
        filme = cursor.fetchone()


        # Definir o layout da janela de edição
        layout_edicao_filme = [
            [sg.Text('                 Editar Filme        ', font=('Calibri', 18)),sg.Image('movie.png')],
            [sg.Text('ID:',size=(3, 1)),sg.Text(filme[0])],
            [sg.Text('Título do Filme:', size=(25, 1))], [sg.Input(key='titulo', size=(33, 1), default_text=filme[1])],
            [sg.Text('Ano de Lançamento:', size=(25, 1))], [sg.Input(key='ano', size=(33, 1), default_text=filme[2])],
            [sg.Text('Gênero ou gêneros:', size=(25, 1))], [sg.Input(key='genero', size=(33, 1), default_text=filme[3])],
            [sg.Text('Diretor e atores:', size=(25, 1))], [sg.Input(key='diretor', size=(33, 1), default_text=filme[4])],
            [sg.Text('Link do Trailer:', size=(25, 1))], [sg.Input(key='trailer', size=(33, 1), default_text=filme[5])],
            [sg.Text('Link da Capa:', size=(25, 1))], [sg.Input(key='capa', size=(33, 1), default_text=filme[6])],
            [sg.Text('Link do Arquivo:', size=(25, 1))], [sg.Input(key='arquivo', size=(33, 1), default_text=filme[7])],
            [sg.Text('Link do TMDB:', size=(25, 1))], [sg.Input(key='tmdb', size=(33, 1), default_text=filme[8])],
            [sg.Text(' ')],
            [sg.Button('Salvar',size=(14, 1)),sg.Button(image_filename='delete.png', key='delete', enable_events=True,button_color=()),sg.Button('Cancelar',size=(13, 1))]
        ]

        # Criar a janela de edição
        janela_edicao_filme = sg.Window('Editar Filme', layout_edicao_filme, finalize=True, no_titlebar=True)
        
        while True:
            event_edicao, values_edicao = janela_edicao_filme.read()

            # Verificar se o usuário fechou a janela de edição ou clicou no botão "Cancelar"
            if event_edicao == sg.WINDOW_CLOSED or event_edicao == 'Cancelar':
                janela_lista_filmes['Pesquisar'].click()
                janela_lista_filmes.un_hide()
                janela_edicao_filme.close()
                break

            elif event_edicao == 'delete':
                resposta = sg.popup_ok_cancel('Quer apagar o filme?',filme[1],filme[2],filme[3],no_titlebar=True)
                if resposta == 'OK':
                    # Excluir o filme do banco de dados
                    delete_sql = "DELETE FROM filmes WHERE id = %s"
                    delete_param = (filme[0],)
                    cursor.execute(delete_sql, delete_param)
                    conn.commit()
                    janela_edicao_filme.close()
                    sg.popup_no_titlebar("O filme foi excluído!")
                    janela_lista_filmes.un_hide()

            elif any(values_edicao[key].strip() == '' for key in values_edicao):
                sg.popup_no_titlebar("Por favor, preencha todos os campos.")

            # Verificar se o botão "Salvar" foi clicado
            else:
                    # Atualizar as informações do filme no banco de dados
                    update_sql = "UPDATE filmes SET titulo = %s, ano = %s, genero = %s, diretor = %s, trailer = %s, capa = %s, arquivo = %s, tmdb = %s WHERE id = %s"
                    update_params = (
                        values_edicao['titulo'], values_edicao['ano'], values_edicao['genero'], values_edicao['diretor'],
                        values_edicao['trailer'], values_edicao['capa'], values_edicao['arquivo'], values_edicao['tmdb'],
                        filme[0]
                    )
                    cursor.execute(update_sql, update_params)
                    conn.commit()
                    janela_edicao_filme.close()
                    cursor.close()
                    conn.close()
                    sg.popup("Filme atualizado com sucesso!")
                    janela_lista_filmes.un_hide()

