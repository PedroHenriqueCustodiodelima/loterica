import streamlit as st
from datetime import datetime


if 'usuarios' not in st.session_state:
    st.session_state.usuarios = [
        {'id': 1, 'nome': 'Admin', 'email': 'admin@example.com', 'senha': '123', 'perfil': 'admin'}
    ]
if 'clientes' not in st.session_state:
    st.session_state.clientes = []
if 'concursos' not in st.session_state:
    st.session_state.concursos = []
if 'boloes' not in st.session_state:
    st.session_state.boloes = []
if 'apostas' not in st.session_state:
    st.session_state.apostas = []
if 'inscricoes' not in st.session_state:
    st.session_state.inscricoes = []
if 'logado' not in st.session_state:
    st.session_state.logado = None


def login():
    st.title("Login")
    escolha = st.radio("Você é:", ["Admin", "Cliente"])
   
    if escolha == "Admin":
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuario_encontrado = next((u for u in st.session_state.usuarios if u['email'] == email and u['senha'] == senha), None)
            if usuario_encontrado:
                st.session_state.logado = usuario_encontrado
                st.success(f"Bem-vindo, {usuario_encontrado['nome']}!")
            else:
                st.error("Email ou senha incorretos!")


    elif escolha == "Cliente":
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            cliente_encontrado = next((c for c in st.session_state.clientes if c['email'] == email and c['senha'] == senha), None)
            if cliente_encontrado:
                st.session_state.logado = cliente_encontrado
                st.success(f"Bem-vindo, {cliente_encontrado['nome']}!")
            else:
                st.error("Email ou senha incorretos!")


def cadastro_cliente():
    st.title("Cadastro de Cliente")
    nome_cliente = st.text_input("Nome")
    email_cliente = st.text_input("Email")
    senha_cliente = st.text_input("Senha", type="password")


    if st.button("Cadastrar"):
        cliente = {
            "id": len(st.session_state.clientes) + 1,
            "nome": nome_cliente,
            "email": email_cliente,
            "senha": senha_cliente
        }
        st.session_state.clientes.append(cliente)
        st.success("Cliente cadastrado com sucesso!")


def cadastro_concurso():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'admin':
        st.error("Apenas administradores podem acessar essa página!")
        return


    st.title("Cadastro de Concurso")
    nome_concurso = st.text_input("Nome do Concurso")
    data_concurso = st.date_input("Data do Concurso", min_value=datetime.now())


    if st.button("Salvar Concurso"):
        concurso = {
            "id": len(st.session_state.concursos) + 1,
            "numero": len(st.session_state.concursos) + 1,
            "data": data_concurso,
            "resultado": ""
        }
        st.session_state.concursos.append(concurso)
        st.success("Concurso cadastrado com sucesso!")


    st.write("Concursos Cadastrados:")
    for concurso in st.session_state.concursos:
        st.write(f"{concurso['numero']} - {concurso['data']}")


def manutencao_bolao():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'admin':
        st.error("Apenas administradores podem acessar essa página!")
        return


    st.title("Manutenção de Bolão")
   
    if len(st.session_state.concursos) == 0:
        st.warning("Cadastre um concurso antes de cadastrar um bolão.")
    else:
        id_concurso = st.selectbox("Selecionar Concurso", [c['numero'] for c in st.session_state.concursos])
        data_bolao = st.date_input("Data do Bolão", min_value=datetime.now())
        num_participantes = st.number_input("Número de Participantes", min_value=6, max_value=15)


        if st.button("Salvar Bolão"):
            bolao = {
                "id": len(st.session_state.boloes) + 1,
                "id_concurso": id_concurso,
                "data": data_bolao,
                "num_participante": num_participantes,
                "ganhou": False
            }
            st.session_state.boloes.append(bolao)
            st.success("Bolão cadastrado com sucesso!")


def manutencao_aposta():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'admin':
        st.error("Apenas administradores podem acessar essa página!")
        return


    st.title("Manutenção de Aposta")


    if len(st.session_state.boloes) == 0:
        st.warning("Cadastre um bolão antes de cadastrar uma aposta.")
    else:
        id_bolao = st.selectbox("Selecionar Bolão", [b['id'] for b in st.session_state.boloes])
        qtd_numeros = st.slider("Quantidade de Números Apostados", min_value=6, max_value=15)
        numeros = st.text_input(f"Digite {qtd_numeros} números separados por vírgula")


        if st.button("Salvar Aposta"):
            aposta = {
                "id": len(st.session_state.apostas) + 1,
                "id_bolao": id_bolao,
                "qtd_numeros": qtd_numeros,
                "numeros": numeros,
                "acertos": 0
            }
            st.session_state.apostas.append(aposta)
            st.success("Aposta cadastrada com sucesso!")


def informar_resultado():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'admin':
        st.error("Apenas administradores podem acessar essa página!")
        return


    st.title("Informar Resultado do Concurso")


    if len(st.session_state.concursos) == 0:
        st.warning("Cadastre um concurso antes de informar o resultado.")
    else:
        id_concurso = st.selectbox("Selecionar Concurso", [c['numero'] for c in st.session_state.concursos])
        resultado = st.text_input("Resultado (Números sorteados separados por vírgula)")


        if st.button("Salvar Resultado"):
            for bolao in [b for b in st.session_state.boloes if b['id_concurso'] == id_concurso]:
                bolao['resultado'] = resultado
                bolao['ganhou'] = True  
            st.success("Resultado informado com sucesso!")


def inscrever_bolao():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'cliente':
        st.error("Apenas clientes podem acessar essa página!")
        return


    st.title("Inscrição em Bolão")
   
    if len(st.session_state.boloes) == 0:
        st.warning("Cadastre um concurso e um bolão antes de inscrever-se.")
    else:
        id_bolao = st.selectbox("Selecionar Bolão", [b['id'] for b in st.session_state.boloes])
        data_inscricao = st.date_input("Data da Inscrição", min_value=datetime.now())


        if st.button("Inscrever"):
            inscricao = {
                "id": len(st.session_state.inscricoes) + 1,
                "id_bolao": id_bolao,
                "id_cliente": st.session_state.logado['id'],
                "data": data_inscricao
            }
            st.session_state.inscricoes.append(inscricao)
            st.success("Inscrição realizada com sucesso!")


def visualizar_boloes():
    if not st.session_state.logado or st.session_state.logado.get('perfil') != 'cliente':
        st.error("Apenas clientes podem acessar essa página!")
        return


    st.title("Visualização de Bolões")
       
    if len(st.session_state.boloes) == 0:
        st.warning("Cadastre um concurso e um bolão antes de visualizar.")
    else:
        for bolao in st.session_state.boloes:
            inscricoes_bolao = [i for i in st.session_state.inscricoes if i['id_bolao'] == bolao['id']]
            if inscricoes_bolao:
                st.write(f"Bolão #{bolao['id']} - {bolao['data']}")
                st.write(f"Resultado: {bolao['resultado']}")
                st.write(f"Ganhou: {bolao['ganhou']}")


menu = st.sidebar.radio("Menu", ["Login", "Cadastro de Concurso", "Manutenção de Bolão", "Manutenção de Aposta", "Informar Resultado", "Inscrição em Bolão", "Visualização de Bolões", "Cadastro Cliente"])


if menu == "Login":
    login()
elif menu == "Cadastro de Concurso":
    cadastro_concurso()
elif menu == "Manutenção de Bolão":
    manutencao_bolao()
elif menu == "Manutenção de Aposta":
    manutencao_aposta()
elif menu == "Informar Resultado":
    informar_resultado()
elif menu == "Inscrição em Bolão":
    inscrever_bolao()
elif menu == "Visualização de Bolões":
    visualizar_boloes()
elif menu == "Cadastro Cliente":
    cadastro_cliente()
