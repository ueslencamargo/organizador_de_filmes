import mysql.connector #Peguei todo só pra garantir.
from mysql.connector import connect # o connect vai conectar ao banco de dados e executar os comandos necessários.
import subprocess # Vai chamar os scripts que fiz separado para me organizar melhor
import PySimpleGUI as sg # a interface do login e cadastro toda em PySimpleGUI
import random # Para gerar o código de recuperação.

sg.theme("LightBlue") # Tema do PySimpleGUI
sg.set_options(font=('Calibri', 16)) #Tamnho padrão da fonte.

def menu_opcao():# Menu inicial, com as opções.

    layout_opcao = [

        [sg.Text('\nOrganizador de Filmes Pessoais', text_color='Black')],
        [sg.Text('Pegue sua pipoca e aproveite!\n', font=('Calibri', 12), text_color='Black')],
        [sg.Button('Fazer Login',size=(25, 2))],
        [sg.Button('Novo Cadastro',size=(25, 2))],
        [sg.Button('Recuperar/Atualizar Senha',size=(25, 2))],
        [sg.Button('Recuperar/Atualizar Usuário',size=(25, 2))],
        [sg.Frame('Desenvolvido por:', [[sg.Column([[sg.Text('Aluno: Ueslen Camargo\nProfessor: Alcemar Pothin\nSENAC Cachoeira do Sul\nMaio de 2023', font=('Calibri', 10))]],justification='center'),sg.Image('movie.png')]], size=(280, 100))]
    ]  

    janela_op = sg.Window('Tela Login Cadastro', layout_opcao,element_justification='center',size=(335,525))

    while True:

        event, values = janela_op.read()

        if event == sg.WINDOW_CLOSED:
            break

        match event: # Usei o match pra interpretar os eventos ao invés de if,elif,else

            case 'Fazer Login' :
                janela_op.close()
                command = login() # Chama a função para realizar o login.

            case 'Novo Cadastro' :
                janela_op.close()
                command = cadastro() # Chama a função para realizar o cadastro.

            case 'Recuperar/Atualizar Senha' :
                janela_op.close()
                command = recuperar() # Chama a função para recuperar a senha.
            
            case 'Recuperar/Atualizar Usuário':
                janela_op.close()
                command = atualizar() # Chama a função para alterar o login.

def login():# Realizar o login.

    layout_login = [

        [sg.Text('\nOrganizador de Filmes Pessoais', font=('Calibri', 16), text_color='Black')],
        [sg.Text('Pegue sua pipoca e aproveite!\n', font=('Calibri', 12), text_color='Black')],
        [sg.Text('Nome de Usuário:'),sg.Text('                      ')],
        [sg.Input(size=(25),key='user')],
        [sg.Text('Senha:'),sg.Text('                                          ')],
        [sg.Input(size=(25),password_char='*',key='pass')],
        [sg.Text('')],
        [sg.Button('Entrar',size=(25, 2))],
        [sg.Text('')],
        [sg.Frame('Desenvolvido por:', [[sg.Column([[sg.Text('Aluno: Ueslen Camargo\nProfessor: Alcemar Pothin\nSENAC Cachoeira do Sul\nMaio de 2023', font=('Calibri', 10))]],justification='center'),sg.Image('movie.png')]], size=(280, 100))]
    ]  


    janela_login = sg.Window('Tela Login Cadastro', layout_login,element_justification='center',size=(335,525))

    tentativas = 4 # Quando o usuário errar a senha ele terá mais algumas tentativas.

    conn = connect(host='localhost',user='root',password='sucata',database='cadastro') # Conectando com o banco de dados.
    cursor = conn.cursor()# Abrindo cursor ou Query para receber o comando mysql.

    while True: # Iniciando a leitura da janela e os eventos.
    
        event, values = janela_login.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Entrar': # Quando o usuário clicar em entrar:

            nome_digitado = values['user'] # A que variável recebe o nome de usuário
            senha_digitada = values['pass'] # A que variável recebe a senha.

            cursor.execute("SELECT usuario FROM usuarios where usuario = '{}'".format(nome_digitado))# Verifica se o nome existe no BD
                
            usuario = cursor.fetchone() # A variável recebe a verificação.

        if usuario is not None and nome_digitado == usuario[0]: # Se a verificação não estiver vazia e o nome digitado for correto.
            janela_login.refresh()# Apenas executa um refresh.                                     
                                                                      
        else: # Aqui se o nome digitado não estiver no BD>
            sg.popup_no_titlebar('Usuário não encontrado')# Exibindo a mensagem de que o nome não foi encontrado.

        cursor.execute("select senha from usuarios where usuario = '{}'".format(nome_digitado))# Vai buscar a senha do usuário no banco de dados.

        senha = cursor.fetchone() # A variável recebe a senha que foi buscada.

        if senha is not None and senha_digitada == senha[0]: # Se a busca não estiver vazia e a senha digitada corresponder com a busca.

            cursor.close() # Encerra o cursor pois não vai ser mais usado.
            conn.close() # Fecha a conexão com o banco de dados.
            janela_login.close() # Fecha a janela.
            subprocess.run(["python", "03_tela_inicial.py", str(nome_digitado)])# Abre a tela inicial.
            break  # Sai do loop principal após chamar a função 04_tela_inicial.py

        else: # Aqui se a senha não corresponder.
            tentativas = tentativas -1 # Vai diminuir as tentativas.

            sg.popup_no_titlebar('Senha errada\ntentativas restantes:', tentativas) # Exibir a mensagem de erro e continuar a pedir senha pois ainda tem tentativas.
            
        if tentativas == 0 : # Quando terminar as tentativas.
                    
                sg.popup_no_titlebar('\nLimite de tentativas atingido!\nO software será encerrado!')

                quit()# Fecha o programa.

def cadastro(): # Realizar novo cadastro.

    sg.popup_no_titlebar('\nLembre-se é importante que o seu e-mail seja válido!\n\n Caso contrário não irá conseguir recuperar a senha.')# Alerta.

    layout_cadastro = [

            [sg.Text('\nOrganizador de Filmes Pessoais', font=('Calibri', 16), text_color='Black')],
            [sg.Text('Pegue seu refri vamos cadastrar!\n', font=('Calibri', 12), text_color='Black')],
            [sg.Text('Nome de Usuário:'),sg.Text('                      ')],
            [sg.Input(size=(25),key='user')],
            [sg.Text('Senha:'),sg.Text('                                          ')],
            [sg.Input(size=(25),password_char='*',key='pass')],
            [sg.Text('E-mail:'),sg.Text('                                        ')],
            [sg.Input(size=(25),key='email')],
            [sg.Button('Cadastrar',size=(25, 2))],
            [sg.Frame('Desenvolvido por:', [[sg.Column([[sg.Text('Aluno: Ueslen Camargo\nProfessor: Alcemar Pothin\nSENAC Cachoeira do Sul\nMaio de 2023', font=('Calibri', 10))]],justification='center'),sg.Image('movie.png')]], size=(280, 100))]
        ]  

    janela_cadastro = sg.Window('Tela Login Cadastro', layout_cadastro,element_justification='center',size=(335,525))

    conn = connect(host='localhost',user='root',password='sucata',database='cadastro')# Conecta ao banco de dados.
    cursor = conn.cursor()# Abre um cursor ou Query.

    while True: # Inicia a leitura da tela de cadastro.
        
        event, values = janela_cadastro.read()

        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Cadastrar':
            
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = '{}'".format(values['user']))# Verifica se o usuário já está cadastrado
            usuario = cursor.fetchone() # armazena a busca

            if usuario is not None: # se a busca não for vazia o usuário já existe.

                sg.popup_no_titlebar(values['user'],'já está cadastrado.',text_color='black')# Aviso

            else:
                
                cursor.execute("SELECT email FROM usuarios WHERE email = '{}'".format(values['email']))# Verifica se o e-mail já está cadastrado

                email = cursor.fetchone()# Armazena o resultado.

                if email is not None: # se o e-mail não for vazio já existe.

                    sg.popup_no_titlebar(values['email'],'já está cadastrado.', text_color='black') # Avisa.

                else:# Se não existe o e-mail.

                    senhacon = sg.popup_get_text('Confirme a senha',password_char='*',no_titlebar=True)# Pede a confirmação de senha.

                    if senhacon == values['pass']: # Se a senha confirmada for igual a digitada anteriormente.

                        sg.popup_no_titlebar('Cadastro realizado com sucesso!')# Avisa
                        janela_cadastro.close()# Fecha a Janela

                        # Grava no banco de dados.
                        cursor.execute("INSERT INTO usuarios (usuario, senha, email) VALUES ('{}', '{}', '{}')".format(values['user'],values['pass'],values['email']))
                        conn.commit()# Confirma a execução.
                        cursor.close() # Encerra o cursor pois não vai ser mais usado.
                        conn.close() # Fecha a conexão com o banco de dados.

                        subprocess.run(["python", "02_bd_usuario.py",str(values['user'])])# Chama a função para criar um BD para o usuário.

                        command = menu_opcao()# Reabre o menu inicial.

                    else: # Aqui se a confirmação da senha não for igual a senha digitada.
                        sg.popup_no_titlebar('A senha não confere!', text_color='black')

def recuperar():# Inicia a recuperação da senha

    layout_recuperar = [

            [sg.Text('\nOrganizador de Filmes Pessoais', font=('Calibri', 16), text_color='Black')],
            [sg.Text('Vamos recuperar sua senha!\n', font=('Calibri', 12), text_color='Black')],
            [sg.Text('Nome de Usuário:'),sg.Text('                      ')],
            [sg.Input(size=(25),key='user')],
            [sg.Text('E-mail:'),sg.Text('                                        ')],
            [sg.Input(size=(25),key='email')],
            [sg.Text('')],
            [sg.Button('Recuperar',size=(25, 2))],
            [sg.Text('')],
            [sg.Frame('Desenvolvido por:', [[sg.Column([[sg.Text('Aluno: Ueslen Camargo\nProfessor: Alcemar Pothin\nSENAC Cachoeira do Sul\nMaio de 2023', font=('Calibri', 10))]],justification='center'),sg.Image('movie.png')]], size=(280, 100))]
        ]  

    janela_recuperar = sg.Window('Tela Login Cadastro', layout_recuperar,element_justification='center',size=(335,525))

    conn = connect(host='localhost',user='root',password='sucata',database='cadastro')# Conecta ao banco de dados.
    cursor = conn.cursor()# Abre um cursor ou Query.
    
    while True:# Inicia a leitura da recuperação de senha.

        event, values = janela_recuperar.read()

        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Recuperar': # Quando clicar em recuperar

            cursor.execute("SELECT email FROM usuarios where email = '{}'".format(values['email']))# Verifica se o e-mail está cadastrado.

            email_bd = cursor.fetchone()# Armazena a verificação.

            cursor.execute("SELECT usuario FROM usuarios where email = '{}'".format(values['email']))# Verifica se o usuario confere com o email.

            usuario_bd = cursor.fetchone()# Armazena a verificação.

            if  email_bd is not None and values['email'] == email_bd[0] and usuario_bd is not None and values['user'] == usuario_bd[0]:# Se o e-mail já estiver cadastrado com o nome de usuário.
                
                cursor.close() # Encerra o cursor pois não vai ser mais usado aqui.
                conn.close() # Fecha a conexão com o banco de dados.

                command = codigo_email(values['user'],values['email'],janela_recuperar)# Executa a função codigo e mail, passando o nome de usuário e email.
            
            else: # Se o e-mail e usuário não for encontrado no BD.
                sg.popup_no_titlebar('Dados incorretos, confira e tente novamente!')

def atualizar():# Inicia a atualização de nome de usuário.

    layout_atualizar = [

            [sg.Text('\nOrganizador de Filmes Pessoais', font=('Calibri', 16), text_color='Black')],
            [sg.Text('\nAtualizar/recuperar o seu nome de usuário!\n', font=('Calibri', 12), text_color='Black')],
            [sg.Text('E-mail de recuperação'),sg.Text('              ')],
            [sg.Input(size=(25),key='email')],
            [sg.Text('Senha:'),sg.Text('                                         ')],
            [sg.Input(size=(25),password_char='*',key='pass')],
            [sg.Text('')],
            [sg.Button('Recuperar/Atualizar',size=(25, 2))],
            [sg.Text('')],
            [sg.Frame('Desenvolvido por:', [[sg.Column([[sg.Text('Aluno: Ueslen Camargo\nProfessor: Alcemar Pothin\nSENAC Cachoeira do Sul\nMaio de 2023', font=('Calibri', 10))]],justification='center'),sg.Image('movie.png')]], size=(280, 100))]
        ]  

    janela_atualizar = sg.Window('Tela Login Cadastro', layout_atualizar,element_justification='center',size=(335,525))

    conn = connect(host='localhost',user='root',password='sucata',database='cadastro')# Conecta ao banco de dados.
    cursor = conn.cursor()# Abre um cursor ou Query.
    
    while True:

        event, values = janela_atualizar.read()

        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Recuperar/Atualizar':

            cursor.execute("SELECT email FROM usuarios where email = '{}'".format(values['email']))# Verifica se o e-mail está cadastrado.

            email_bd = cursor.fetchone()# Armazena a verificação.

            cursor.execute("SELECT usuario FROM usuarios where email = '{}'".format(values['email']))# Verifica se o usuario confere com o email.

            usuario_bd = cursor.fetchone()# Armazena a verificação.

            cursor.execute("SELECT senha FROM usuarios where email = '{}'".format(values['email']))# Verifica a senha 

            senha_bd = cursor.fetchone() # Armazena a senha.

            if  email_bd is not None and values['email'] == email_bd[0] and values['pass'] == senha_bd[0]:# Se o e-mail já estiver cadastrado.

                sg.popup_no_titlebar('O seu nome de usuário é:',usuario_bd[0])# exibe o nome de usuário.

                novo_nome = sg.popup_get_text('Insira um novo nome de usuário para atualizar.\n\nCaso não queira atualizar deixe em branco.',no_titlebar=True)# Pede o nome novo de usuário caso ele queira atualizar.
                    
                if novo_nome != '': # Se não for deixado em branco.
                    
                    conn = connect(host='localhost',user='root',password='sucata',database='cadastro')# Conecta ao banco de dados.
                    cursor = conn.cursor()# Abre um cursor ou Query.
                    cursor.execute("update usuarios set usuario = '{}' where email = '{}'".format(novo_nome,email_bd[0]))# Atualiza o nome com o nome digitado.

                    conn.commit()
                    cursor.close() # Encerra o cursor pois não vai ser mais usado aqui.
                    conn.close() # Fecha a conexão com o banco de dados.
                
                    sg.popup_no_titlebar('O seu novo nome de usuário é:',novo_nome)
                    janela_atualizar.close()
                    command = menu_opcao()

                else:
                    sg.popup_no_titlebar('O seu nome de usuário continua:',usuario_bd[0])
                    janela_atualizar.close()
                    command = menu_opcao()
            
            else:
                sg.popup_no_titlebar('Dados incorretos, confira e tente novamente!')

def codigo_email(usuario,emailrec,janela_recuperar):# Recebe o e-mail de recuperação e gera o código.

    codigo = random.randint(000000,900000)# Código gerado aleátoriamente de 6 digitos.

    command = enviando_email(codigo,emailrec)# Chama a função para enviar o código, passando o código e o email.

    janela_recuperar.close() # Fecha a janela recuperar.

    while True: # inicia o loop para pedir o código de confirmação.

        codigo_digitado = sg.popup_get_text('Foi enviado um código para o seu e-mail insira-o aqui:',no_titlebar=True)# Pede o código.

        if codigo_digitado is None: # Aqui se nada for digitado.
            command = menu_opcao() # Volta para o menu.
            break

        if codigo_digitado != '': # Se o código não for vazio.
            try:
                codigo_digitado = int(codigo_digitado)# Converte para inteiro.
            except ValueError:# Se ocorrer algum erro.
                sg.popup_no_titlebar('Código incorreto!')# Aviso.
                continue

            if codigo == codigo_digitado:# Se o codigo digitado for correto.

                while True: # Inicia o loop para pedir a senha.

                    senha_nova = sg.popup_get_text('Insira sua nova senha:', password_char='*', no_titlebar=True)

                    if senha_nova == '':# se o campo senha estiver vazio.

                        sg.popup_no_titlebar('Por favor, digite uma senha.')

                    else:# Depois de digitar a senha, inicia a gravação no banco:

                        conn = connect(host='localhost', user='root', password='sucata', database='cadastro')
                        cursor = conn.cursor()
                        cursor.execute("update usuarios set senha = '{}' where email = '{}'".format(senha_nova, emailrec))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        sg.popup_no_titlebar('Senha atualizada com sucesso!')
                        command = menu_opcao()
                        break  # Sai do loop interno ao atualizar a senha
            else:
                sg.popup_no_titlebar('Código incorreto!')# Se digitar o código errado.
        else:
            sg.popup_no_titlebar('Código incorreto!')
        break

def enviando_email(codigo,emailrec):# Código para enviar e-mail do google peguei do hastagtreinamentos.
    import smtplib
    import email.message
 
    corpo_email = f"""
    <p>Seu código de recuperação é: {codigo}</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "Código de Recuperação"
    msg['From'] = 'ueslenzx@gmail.com'
    msg['To'] = emailrec
    password = 'uoklotofdfovdiyl' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

command = menu_opcao()