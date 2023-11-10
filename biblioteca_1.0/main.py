#importando todas as bibliotecas que serão necessárias
import tkinter as tk  # comando para fazer a interface grafica
from tkinter import simpledialog, messagebox  # bibliotecas caixas de diálogo interativas
import mysql.connector  # biblioteca para "conversar" com o banco

#conexao com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',  #endereco do servidor (local)
    user='root',  # nome do usuario
    password='',  # senha do SQL (sem senha)
    database='BIBLIOTECA',  # nome do banco
)
cursor = conexao.cursor()  # cursor para executar consultas no SQL

# funcao para cadastrar livro
def cadastrar_livro():
    editora = simpledialog.askstring("Cadastrar Livro", "Editora:")  # solicita ao usuario a editora
    nome = simpledialog.askstring("Cadastrar Livro", "Nome do Livro:")  # solicita ao usuario o nome do livro
    autor = simpledialog.askstring("Cadastrar Livro", "Autor:")  # solicita ao usuario o autor do livro
    faixa_etaria = simpledialog.askinteger("Cadastrar Livro", "Faixa Etária:")  # solicita ao usuario a faixa etária

    # Obtém o código máximo da tabela "cadastrar_livro" e gera um novo código
    cursor.execute("SELECT MAX(codigo) FROM cadastrar_livro")# faz uma consulta para obter o maximo codigo da tabela
    max_codigo = cursor.fetchone()[0]# pega o resultado da consulta e armazena em "max_codigo"
    codigo = max_codigo + 1 if max_codigo else 1 #gera um novo codigo colocando cod max em 1, ou define como 1 se estiver vazia

    # comando sql para inserir dados na tabela "cadastrar_livro"
    comando = "INSERT INTO cadastrar_livro (codigo, editora, nome, autor, faixa_etaria) VALUES (%s, %s, %s, %s, %s)" #comando para inserir dados do livro (%s serve para valores que sao acrescentados posteriormente)
    valores = (codigo, editora, nome, autor, faixa_etaria) #valores a serem inseridos
    
    cursor.execute(comando, valores)  # executa o comando com os valores
    conexao.commit()  # confirma as alterações no banco

    messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")  # exibe uma caixa de dialogo

# funcao para registar "alugar livro"
def alugar_livro():
    nome = simpledialog.askstring("Alugar Livro", "Quem alugou:")  # solicita ao usuario quem esta alugando
    data_que_alugou = simpledialog.askstring("Alugar Livro", "Data que alugou (AAAA-MM-DD):")  # solicita a data de aluguel
    data_de_devolucao = simpledialog.askstring("Alugar Livro", "Data de devolução (AAAA-MM-DD):")  # Solicita a data de devolução

    #inserir dados na tabela "alugar_livro"
    comando = "INSERT INTO alugar_livro (nome, data_que_alugou, data_de_devolucao) VALUES (%s, %s, %s)"#comando para inserir dados do livro (%s serve para valores que sao acrescentados posteriormente)
    valores = (nome, data_que_alugou, data_de_devolucao) #valores a serem inseridos
    
    try:
        cursor.execute(comando, valores)  # Executa o comando com os valores
        conexao.commit()  # Confirma as alterações no banco
        messagebox.showinfo("Sucesso", "Livro alugado com sucesso!")  # Exibe uma caixa de diálogo de sucesso
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Ocorreu um erro ao alugar o livro: {err}")  #Caso de erro exibe uma mensagem de erro

# Criando a janela principal
root = tk.Tk()  # Cria a janela principal
root.title("Sistema de Biblioteca")  # título da janela
root.geometry("300x150")  #tamanho da janela

# Adicionando o botão de cadastro de livros
btn_cadastrar_livro = tk.Button(root, text="Cadastrar Livro", command=cadastrar_livro)  # Cria um botão para cadastrar livros
btn_cadastrar_livro.pack(pady=10)  # Define a posição e o espaçamento do botão

# Adicionando o botão de aluguel de livros
btn_alugar_livro = tk.Button(root, text="Alugar Livro", command=alugar_livro)  # Cria um botão para alugar livros
btn_alugar_livro.pack(pady=10)  # Define a posição e o espaçamento do botão

# loop principal da interface gráfica
root.mainloop()  # Inicia o loop principal da interface gráfica

conexao.commit()  # Confirma as alterações pendentes no banco de dados antes de encerrar o programa
