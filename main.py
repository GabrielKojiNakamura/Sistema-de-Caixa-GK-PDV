from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import customtkinter as ctk
import datetime
from pymongo import MongoClient

# Criar conexão com o MongoDB
uri = "mongodb+srv://Gabriel:wzw5brC7z7Hyn6o9@cluster0.brk82ev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client['Cluster0']  
collection = db['produtos']  
collection_atendente = db['atendente']

# Criar tela principal
root = ctk.CTk()
root.title("GK PDV")
root._set_appearance_mode("light")
root.geometry(f"{int(root.winfo_screenwidth())+int(root.winfo_screenheight())}")
root.state('zoomed')

#Cores
azul = "#172635"    # Hexadecimal para um tom escuro de azul
preto= "#1B1816"    # Hexadecimal para um tom escuro de preto
cinza= "#202124"    # Hexadecimal para um tom escuro de cinza
ciano= "#0DCBEF"    # Hexadecimal para um tom escuro de ciano
vermelho= "#F23F42" # Hexadecimal para um tom escuro de vermelho
verde= "#1ABC9C"# Hexadecimal para um tom escuro de verde

def login():
    # Criar a janela de login
    login_window = ctk.CTkToplevel(root, fg_color=azul)
    login_window.geometry("800x700")
    login_window.maxsize(width=800, height=700)
    login_window.minsize(width=800, height=700)
    login_window.resizable(width=False, height=False)
    login_window.title("Login")

#Frame
    frame_login=ctk.CTkFrame(master=login_window, width=500, height=480,fg_color=preto,border_width=3,corner_radius=20,border_color=ciano)
    frame_login.pack(pady=100)

    #Logo
    logo_image = Image.open("./simbolo.png")
    logo = ImageTk.PhotoImage(logo_image.resize((200, 100)))
    ctk.CTkLabel(frame_login, text=None, image=logo, bg_color=preto).place(x=160, y=60)
        
    # Campos de entrada para nome de usuário e senha

    username_entry = ctk.CTkEntry(master=frame_login, width=300,placeholder_text="nome do usuário",fg_color=cinza,height=50)
    username_entry.place(x=100,y=200)


    password_entry = ctk.CTkEntry(master=frame_login, width=300, placeholder_text="sua senha",show="*",fg_color=cinza,height=50 )  # Show="*" oculta a senha
    password_entry.place(x=100,y=280)

    # Função de verificação de login
    def verificar_login():
            username = username_entry.get()
            password = password_entry.get()

            usuarios = [
                {"username": "admin", "password": "admin"}
            ]

            if username == "" or password == "":
                messagebox.showerror("Erro", "Por favor, preencha todos os campos")
                return

            atendente = collection_atendente.find_one({"username": username, "password": password})

            if atendente:
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                login_window.destroy()  # Fechar a janela de login
                root.deiconify()  # Restaurar a janela principal
            else:
                messagebox.showerror("Erro", "Nome de usuário ou senha incorretos")
                # Limpar os campos de entrada
                username_entry.delete(0, END)
                password_entry.delete(0, END)

    # Botão de login
    login_button = ctk.CTkButton(master=frame_login, text="ENTRAR", command=verificar_login, fg_color=azul, width=300, height=50,font=("Arial Bold",20))
    login_button.place(x=100,y=360)


# Função para abrir a tela de login
def abrir_login():   
    root.iconify()  # Minimizar a janela principal
    login()  # Chamar a função de login

# Chamar a função para abrir a tela de login
abrir_login()

# Função para atualizar a hora
def atualizar_horario():
    agora = datetime.datetime.now()
    hora_formatada = agora.strftime("%H:%M:%S")
    label_horario.config(text=hora_formatada)
    label_horario.after(1000, atualizar_horario)  # Atualiza a cada 1000ms (1 segundo)

# Criar o rótulo para exibir a hora
label_horario = Label(root, font=("Arial", 18),fg="grey")
label_horario.place(x=1600, y=170)

# Iniciar a função para atualizar o horário
atualizar_horario()

def finalizar_compra():
    finalizar_compra_window = ctk.CTkToplevel(root, fg_color="white")
    finalizar_compra_window.geometry("1200x700")
    finalizar_compra_window.grab_set() 
        
    #Frame Cadastro de Produto
    frame_finalizar= ctk.CTkFrame(master=finalizar_compra_window, width=2000, height=100, fg_color=azul, bg_color=azul)
    frame_finalizar.place(x=0, y=0)

    #Botão para voltar
    def voltar_pagina_anterior(finalizar_compra_window):
        finalizar_compra_window.destroy()  # Fecha a janela de fechar caixa
        root.deiconify()  # Restaura a janela principal

    btn_voltar = ctk.CTkButton(master=frame_finalizar, text="Voltar à página anterior", command=lambda: voltar_pagina_anterior(finalizar_compra_window),width=100, height=70, fg_color=azul, text_color="white",font=("Arial Bold",18),corner_radius=20)
    btn_voltar.place(x=100, y=20)

    #Label
    ctk.CTkLabel(finalizar_compra_window, text="R$ SUB TOTAL",font=("Arial Bold",18),bg_color="white",text_color="grey").place(x=100, y=150)
    ctk.CTkLabel(finalizar_compra_window, text="R$ SUB TOTAL",font=("Arial Bold",18),bg_color="white",text_color="grey").place(x=100, y=150)
    ctk.CTkLabel(finalizar_compra_window, text="R$ TOTAL A PAGAR",font=("Arial Bold",18),bg_color="white",text_color="grey").place(x=870, y=150)

    #Label Valor
    valor_da_compra=ctk.CTkLabel(finalizar_compra_window, text=f"R$ {total_geral:.2f}",font=("Arial Bold",40),bg_color="white",text_color=cinza).place(x=920, y=250)
    
    def pagamento_dinheiro_window():
        pagamento_dinheiro_window = ctk.CTkToplevel(root, fg_color=azul)
        pagamento_dinheiro_window.geometry("800x700")
        pagamento_dinheiro_window.grab_set()

        #Frame Central
        frame_dinheiro = ctk.CTkFrame(master=pagamento_dinheiro_window, width=400, height=500, fg_color="white", bg_color="white", corner_radius=50)
        frame_dinheiro.place(x=210, y=100)   
        
        #Total a Pagar
        ctk.CTkLabel(frame_dinheiro, text="TOTAL A PAGAR:", font=("Arial Bold",25), text_color="black", bg_color="white").place(x=50, y=50)
        ctk.CTkLabel(frame_dinheiro, text=f"R${total_geral:.2f}", font=("Arial Bold",25), text_color="black", bg_color="white").place(x=50, y=90)
    
        #Valor Recebido
        ctk.CTkLabel(frame_dinheiro, text="VALOR RECEBIDO:", font=("Arial Bold",25), text_color="black", bg_color="white").place(x=50, y=180)
        entry_valor_recebido = ctk.CTkEntry(frame_dinheiro, placeholder_text="Digite o Valor", font=("Arial Bold",25), bg_color="white", fg_color=azul, width=300, height=20, corner_radius=20)
        entry_valor_recebido.place(x=50, y=220)
        
        # Função para calcular o troco
        def calcular_troco():
            try:
                # Obter o valor recebido do usuário
                valor_recebido = float(entry_valor_recebido.get())

                if valor_recebido < total_geral:
                    messagebox.showerror("Erro", "O valor recebido é menor que o total.")
                    return

                # Calcular o troco
                troco = valor_recebido - total_geral

                # Exibir o troco
                label_troco = ctk.CTkLabel(frame_dinheiro, text=f"R$ {troco:.2f}", font=("Arial Bold", 25), bg_color="white", text_color=vermelho)
                label_troco.place(x=250, y=320)

            except ValueError:
                # Lidar com a entrada inválida
                messagebox.showerror("Erro", "Por favor, insira um valor válido.")

            
        # Botão para calcular o troco
        btn_calcular_troco = ctk.CTkButton(master=frame_dinheiro, text="Calcular Troco", command=calcular_troco, font=("Arial Bold",18), text_color="black", fg_color=azul, width=200, height=20, corner_radius=20)
        btn_calcular_troco.place(x=50, y=270)
        
        #Troco a Dar
        ctk.CTkLabel(frame_dinheiro, text="TROCO A DAR: ", font=("Arial Bold",25), text_color="black", bg_color="white").place(x=50, y=320)

        #Voltar para área de pagamento
        def voltar_pagamento():
            pagamento_dinheiro_window.destroy()
        
        #Tela de Compra Finalizada em Dinheiro
        def dinheiro_finalizada():
            pagamento_dinheiro_window.destroy()
            messagebox.showinfo("Sucesso", "Compra Finalizada em Dinheiro")

        #Botões Cancelar/Confirmar
        btn_cancelar_dinheiro=ctk.CTkButton(master=frame_dinheiro, text="CANCELAR",command=voltar_pagamento, font=("Arial Bold",18),text_color="black",fg_color=vermelho,width=100,height=20,corner_radius=20,)
        btn_cancelar_dinheiro.place(x=50, y=450)

        btn_confirmar_dinheiro=ctk.CTkButton(master=frame_dinheiro, text="CONFIRMAR",command=dinheiro_finalizada,font=("Arial Bold",18),text_color="black",fg_color=verde,width=100,height=20,corner_radius=20)
        btn_confirmar_dinheiro.place(x=220, y=450)

    #Pagamento em Dinheiro
    btn_dinheiro = ctk.CTkButton(master=finalizar_compra_window, command=pagamento_dinheiro_window,text="DINHEIRO", width=250, height=70, fg_color=azul,corner_radius=20, bg_color=azul,text_color="white",font=("Arial Bold",18))
    btn_dinheiro.place(x=100, y=350)

    #Pagamento em Máquininha
    def debito_finalizado():
        messagebox.showinfo("Sucesso", "Compra Finalizada em Débito")
        finalizar_compra_window.destroy()
        resetar_frame_right()

    def credito_finalizado():
        messagebox.showinfo("Sucesso", "Compra Finalizada em Crédito")
        finalizar_compra_window.destroy()
        resetar_frame_right()

    btn_debito = ctk.CTkButton(master=finalizar_compra_window,command=debito_finalizado,text="DEBITO", width=250, height=70, fg_color=azul,corner_radius=20, bg_color=azul,text_color="white",font=("Arial Bold",18))
    btn_debito.place(x=450, y=350)

    btn_credito = ctk.CTkButton(master=finalizar_compra_window,command=credito_finalizado, text="CRÉDITO", width=250, height=70, fg_color=azul,corner_radius=20, bg_color=azul,text_color="white",font=("Arial Bold",18))
    btn_credito.place(x=800, y=350)

# Código e Descrição
entry_barra_codigo = ctk.CTkEntry(root, width=1370, height=50, placeholder_text="Código/Descrição",fg_color="white",text_color=cinza,font=("Arial Bold",18),border_color=azul)
entry_barra_codigo.place(x=199, y=200)

# Quantidade
entry_quantidade = ctk.CTkEntry(root, width=150, height=50, placeholder_text="Quantidade",fg_color="white", text_color=cinza,border_color=azul,font=("Arial Bold",18))
entry_quantidade.place(x=199, y=400)

# Definir uma variável global para o contador de itens
contador_itens = 1
# Definir uma variável global para o total geral
total_geral = 0

def pesquisar_produto():
    global contador_itens, total_geral  # Usar as variáveis globais contador_itens e total_geral

    codigo_produto = entry_barra_codigo.get()

    # Consultar o MongoDB para encontrar o produto pelo código
    produto_encontrado = collection.find_one({"codigo_produto": codigo_produto})

    if produto_encontrado:
        quantidade = int(entry_quantidade.get())  # Obtém a quantidade inserida na entry

        # Exibir os detalhes do produto no frame
        ctk.CTkLabel(master=frame_right, text="Item", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=80, y=30)
        ctk.CTkLabel(master=frame_right, text="ID", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=200, y=30)
        ctk.CTkLabel(master=frame_right, text="Descrição", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=320, y=30)
        ctk.CTkLabel(master=frame_right, text="Quantidade", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=580, y=30)
        ctk.CTkLabel(master=frame_right, text="Valor Unitário", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=780, y=30)
        ctk.CTkLabel(master=frame_right, text="Imposto(%)", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=970, y=30)
        ctk.CTkLabel(master=frame_right, text="Valor Total", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=1070, y=30)

        y_coordinate = 0 + contador_itens * 50  # Definir a coordenada y baseada no número de itens já exibidos

        # Formatar o número do item para exibição
        numero_item_formatado = f"{contador_itens:03d}"
        contador_itens += 1  # Incrementar o contador de itens

        #Item
        ctk.CTkLabel(master=frame_right, text=numero_item_formatado, font=("Arial", 18), bg_color="white", text_color=cinza).place(x=80, y=y_coordinate)

        #ID
        ctk.CTkLabel(master=frame_right, text=f"{produto_encontrado['codigo_produto']}", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=200, y=y_coordinate)

        #Descrição
        ctk.CTkLabel(master=frame_right, text=f"{produto_encontrado['nome_produto']}", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=320, y=y_coordinate)

        #Quantidade
        ctk.CTkLabel(master=frame_right, text=f"{quantidade}", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=580, y=y_coordinate)

        #Valor Unitário
        ctk.CTkLabel(master=frame_right, text=f"{float(produto_encontrado['valor_unitario'])}", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=780, y=y_coordinate)

        # Imposto
        imposto_por_item = float(produto_encontrado['imposto']) * quantidade
        ctk.CTkLabel(master=frame_right, text=f"{imposto_por_item:.2f}", font=("Arial", 18), bg_color="white", text_color=cinza).place(x=970, y=y_coordinate)

        # Valor Total com Imposto
        valor_total_sem_imposto = float(produto_encontrado['valor_unitario']) * quantidade
        
        imposto_total = (imposto_por_item/100) * valor_total_sem_imposto
        valor_total_com_imposto = valor_total_sem_imposto + imposto_total
        ctk.CTkLabel(master=frame_right, text=f"{valor_total_com_imposto:.2f}", font=("Arial", 18), bg_color=azul, text_color="white").place(x=1070, y=y_coordinate)

        # Adicionar o valor total ao total geral
        total_geral += valor_total_com_imposto

        # Limpar o rótulo do total geral antes de exibir
        for widget in frame_rightdown.winfo_children():
            widget.destroy()

        # Exibir o total geral
        total_label = ctk.CTkLabel(master=frame_rightdown, text=f"R$ {total_geral:.2f}", font=("Arial Bold",50), bg_color="white", text_color=cinza)
        total_label.place(x=400, y=40)
        ctk.CTkLabel(master=frame_rightdown, text="SUB TOTAL", font=("Arial Bold", 30), bg_color="white", text_color=cinza).place(x=60, y=50)

    else:
        # Exibir uma mensagem se nenhum produto for encontrado
        messagebox.showerror("Erro", "Produto não encontrado")
        
# Botão de pesquisa
btn_pesquisar = ctk.CTkButton(master=root, text="Pesquisar", command=pesquisar_produto, width=100, height=50, fg_color=azul,corner_radius=20, bg_color=azul,text_color="white",font=("Arial Bold",18))
btn_pesquisar.place(x=1570, y=200)

# Frames
frame_top= ctk.CTkFrame(master=root, width=2000, height=100, fg_color=azul)
frame_top.place(x=0, y=0)

frame_rightdown = ctk.CTkFrame(master=root, width=1000, height=330, fg_color="white",border_color=azul,border_width=2)
frame_rightdown.place(x=1000, y=920)

frame_right = ctk.CTkFrame(master=root, width=5000, height=400, fg_color="white",border_color=azul,border_width=2)
frame_right.place(x=500, y=400)

# Logo
logo_image = Image.open("./Logo 2.png")
logo = ImageTk.PhotoImage(logo_image.resize((192, 100)))
ctk.CTkLabel(master=frame_top, text=None, image=logo, bg_color=azul).place(x=40, y=0)

# Labels Root Principal
#Informações
ctk.CTkLabel(master=frame_top, text="Suporte (11) 99999-9999", font=("Arial", 18), bg_color=azul, text_color="white").place(x=1600, y=40)
ctk.CTkLabel(root, text="Você está sendo atendido por: xxxxxxx", font=("Arial", 22), bg_color="white", text_color="gray").place(x=199, y=260)
ctk.CTkLabel(master=frame_rightdown, text="SUB TOTAL", font=("Arial Bold", 30), bg_color="white", text_color="grey").place(x=60, y=50) 

#Código
ctk.CTkLabel(root, text="Código/Descrição", font=("Arial", 22), bg_color="white", text_color="grey").place(x=199, y=170)

#Quantidade
ctk.CTkLabel(root, text="Quantidade", font=("Arial", 22), bg_color="white", text_color="gray").place(x=199, y=370)

#Valor da Compra
ctk.CTkLabel(master=frame_rightdown, text="R$", font=("Arial Bold", 50), bg_color="white", text_color=cinza).place(x=400, y=40) 

# Função para fechar a janela de cadastro e restaurar a janela principal
def voltar_pagina_anterior(cadastro_window):
    cadastro_window.destroy()  # Fecha a janela de cadastro
    root.deiconify()  # Restaura a janela principal

# Criando nova janela de cadastro
def cadastro():

    root.iconify()  # Minimiza a janela principal

    cadastro_window = ctk.CTkToplevel(root, fg_color="white")
    cadastro_window.geometry("800x700")
    cadastro_window.state('zoomed')  # Maximiza a nova janela

    def salvar_mongodb():
        codigo_produto = entry_codigoproduto.get()
        nome_produto = entry_nome_produto.get()
        valor_unitario = entry_valor_unitario.get()
        quantidade = entry_quantidade.get()
        imposto = entry_imposto.get()

        if codigo_produto and nome_produto and valor_unitario and quantidade and imposto:
            produto = {
                "codigo_produto": codigo_produto,
                "nome_produto": nome_produto,
                "valor_unitario": valor_unitario,
                "quantidade": quantidade,
                "imposto": imposto
            }

            # Insere o produto na coleção do MongoDB
            collection.insert_one(produto)

            messagebox.showinfo("Sucesso", "Produto salvo no MongoDB!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar!")

    #Frame Cadastro de Produto
    frame_topcadastro= ctk.CTkFrame(master=cadastro_window, width=2000, height=100, fg_color=azul)
    frame_topcadastro.place(x=0, y=0)

    frame_cadastro=ctk.CTkFrame(cadastro_window,width=1400,height=700)
    frame_cadastro.place(x=250,y=230)

    # OptionMenu Categoria
    ctk.CTkLabel(master= cadastro_window, text="Categoria", font=("arial bold", 14), text_color="black").pack()
    categoria = ctk.CTkOptionMenu(master=frame_cadastro, values=["Alimentos", "Bebidas", "Higiene Pessoal", "Hortifruti", "Congelados", "Frios", "Vestuário", "Pets", "Outros..."])
    categoria.pack(pady=20)
    categoria.set("Escolha a categoria")

    #Frame Cadastro de Produto

    frame_topcadastro= ctk.CTkFrame(master=cadastro_window, width=2000, height=100, fg_color=azul)
    frame_topcadastro.place(x=0, y=0)

    frame_cadastro= ctk.CTkFrame(cadastro_window,width=1400,height=700)
    frame_cadastro.place(x=250,y=230)

    btn_salvar = ctk.CTkButton(master=frame_cadastro, text="Salvar",width=450,height=50, command=salvar_mongodb, fg_color=azul,corner_radius=20,text_color="white",font=("Arial Bold",18))
    btn_salvar.place(x=475,y=550)

    # Entry Nome do Produto
    entry_nome_produto = ctk.CTkEntry(master=frame_cadastro, width=450,height=50,placeholder_text="Nome do Produto")
    entry_nome_produto.place(x=475,y=50)

    # Entry Codigo do Produto
    entry_codigoproduto = ctk.CTkEntry(master=frame_cadastro, width=450,height=50, placeholder_text="Codigo do Produto")
    entry_codigoproduto.place(x=475,y=150)

    # Entry Quantidade
    entry_quantidade = ctk.CTkEntry(master=frame_cadastro,width=450,height=50,placeholder_text="Quantidade")
    entry_quantidade.place(x=475,y=250)

    # Entry Valor Unitário
    entry_valor_unitario = ctk.CTkEntry(master=frame_cadastro,width=450,height=50,placeholder_text="Valor Unitário")
    entry_valor_unitario.place(x=475,y=350)

    # Entry Imposto
    entry_imposto= ctk.CTkEntry(master=frame_cadastro,width=450,height=50, placeholder_text="Imposto")
    entry_imposto.place(x=475,y=450)

    # Botão para voltar à página anterior
    btn_voltar = ctk.CTkButton(master=frame_topcadastro, text="Voltar à página anterior", command=lambda: voltar_pagina_anterior(cadastro_window),width=100, height=70, fg_color=azul, text_color="white",font=("Arial Bold",18),corner_radius=20)
    btn_voltar.place(x=475, y=20)

   #Logo dentro do Cadastro
    logo_image = Image.open("./Logo 2.png")
    logo = ImageTk.PhotoImage(logo_image.resize((192, 100)))
    ctk.CTkLabel(frame_topcadastro, text=None, image=logo, bg_color=azul).place(x=40, y=0)

   #Logo dentro do Cadastro
    logo_image = Image.open("./Logo 2.png")
    logo = ImageTk.PhotoImage(logo_image.resize((192, 100)))
    ctk.CTkLabel(frame_topcadastro, text=None, image=logo, bg_color=azul).place(x=40, y=0)

# Botão para abrir a janela de cadastro
btn_cadastro = ctk.CTkButton(master=frame_top, text="Cadastrar Produto", command=cadastro, width=100, height=70, fg_color=azul,corner_radius=20, bg_color=azul,text_color="white",font=("Arial Bold",18))
btn_cadastro.place(x=500, y=20)

def resetar_frame_right():
        global total_geral, contador_itens

        # Limpar todos os widgets dentro do frame_right
        for widget in frame_right.winfo_children():
            widget.destroy()

        # Resetar as variáveis globais
        total_geral = 0
        contador_itens = 1

btn_cancelar = ctk.CTkButton(master=frame_top, text="Cancelar Compra", command=resetar_frame_right, width=100, height=70, fg_color=azul,corner_radius=20,text_color="white",font=("Arial Bold",18))
btn_cancelar.place(x=800, y=20)

btn_fechar = ctk.CTkButton(master=frame_top, text="Fechar Compra", command=finalizar_compra, width=100, height=70, fg_color=azul,corner_radius=20,text_color="white",font=("Arial Bold",18))
btn_fechar.place(x=1100, y=20)

root.mainloop()  # Executa o loop principal
