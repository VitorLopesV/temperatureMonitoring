from tkinter import *
import tkinter as tk
import os

# ----CONSTANTES----

TITLE_FRAME = "Controle de Temperatura"     # Título do painel
VALUE_TO_CONNECT = "Ligar"                  # Texto que fica no botão quando ele está desligado.
VALUE_TURN_OFF = "Desligar"                 # Texto que fica no botão quando ele está Ligado.

GREY_COLOR = "grey31"                       # Cor cinza-escuro
WHITE_COLOR = "white"                       # Cor branca
RED_COLOR = "red"                           # Cor vermelha
GREEN_COLOR = "green"                       # Cor verde

# ----CLASSE PRINCIPAL----
class Main:
    def __init__(self):
        self.create_main_frame()

        # Status do botão de ligar/desligar monitoramento de temperatura.
        self.status = tk.StringVar(value=VALUE_TO_CONNECT)

        self.save_options()

        self.create_frame(0.090, 0.150, "Sala 1", 23)
        self.create_frame(0.550, 0.150, "Sala 2", 18)
        self.create_frame(0.090, 0.440, "Sala 3", 20)
        self.create_frame(0.550, 0.440, "Sala 4", 25)
        self.create_button()
        self.options()
        self.root.mainloop()

    # Salva os dados de temperatura ideal e variação
    def save_options(self):
        if os.path.exists("options.txt"):
            with open("options.txt", "r") as options_file:
                lines = options_file.readlines()
                self.ideal_temperature = int(lines[0])
                self.variation = int(lines[1])
        else:
            self.ideal_temperature = 20
            self.variation = 2

    # Cria a tela principal e define algumas configurações a ela
    def create_main_frame(self):
        self.root = tk.Tk()
        self.root.title(TITLE_FRAME)
        self.root.geometry("1100x500")
        self.root.resizable(False, False)

    # Cria os Componentes que serão exibidos na tela principal
    def create_frame(self, x, y, name, temperature):
        self.frame = tk.Frame(self.root, background=GREY_COLOR, highlightbackground="black", highlightthickness=1)
        self.frame.place(relx=x, rely=y, relwidth=0.347, relheight=0.2)

        tk.Label(self.frame, text="Nome: " + name, bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Temperatura ideal: " + str(self.ideal_temperature), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Variação: " + str(self.variation), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)

        temperarure = tk.Label(self.root, text=temperature, bg=GREY_COLOR, fg=WHITE_COLOR, font=("Arial", 10))
        temperarure.place(relx=x+0.140, rely=y+0.209, relwidth=0.050, relheight=0.050)

        color = GREEN_COLOR

        # Verifica se a variação da temperatura está dentro da variação configurada.
        if temperature > self.ideal_temperature + self.variation or temperature < self.ideal_temperature - self.variation:
            color = "yellow"
        # Verifica se a variação da temperatura excedeu variação configurada.
        if temperature > self.ideal_temperature + (2*self.variation) or temperature < self.ideal_temperature - (2*self.variation):
            color = RED_COLOR

        led_example = tk.Canvas(self.frame, width=40, height=40, background=GREY_COLOR, highlightthickness=0)
        led_example.place(relx=0.86, rely=0.33)
        led_example.create_oval(4, 4, 30, 30, fill=color, outline=color)

    # Cria botão de ligar/desligar monitoramento de temperatura
    def create_button(self):
        self.button = tk.Button(self.root, textvariable=self.status, width=20, command=self.toggle, bg=GREEN_COLOR,
                                fg=WHITE_COLOR, font=("Arial", 12))
        self.button.place(relx=0.43, rely=0.85)

    # Verifica estado do botão e altera quando o botão é clicado.
    def toggle(self):
        if self.status.get() == VALUE_TURN_OFF:
            self.status.set(VALUE_TO_CONNECT)
            self.button.configure(bg=GREEN_COLOR)
        else:
            self.status.set(VALUE_TURN_OFF)
            self.button.configure(bg=RED_COLOR)

    # Barra de opções
    def options(self):
        optionsbar=Menu(self.root)
        self.root.config(menu=optionsbar)

        filemenu=Menu(optionsbar, tearoff=0)
        optionsbar.add_cascade(label="Opções", menu=filemenu)

        filemenu.add_command(label="Editar", command=self.open_options_popup)
        filemenu.add_command(label="Sair", command=self.root.destroy)

# ----POP-UP----
    # Pop-up de edição de valores
    def open_options_popup(self):
        options_popup = Toplevel(self.root)
        options_popup.title("Edição de Valores")
        options_popup.geometry("300x170")
        options_popup.resizable(False, False)
        options_popup.grab_set()

        tk.Label(options_popup, text="Digite a temperatura ideal desejada:").pack(pady=5)
        temp_ideal_entry = tk.Entry(options_popup)
        temp_ideal_entry.pack(pady=5)

        tk.Label(options_popup, text="Digite a variação desejada:").pack(pady=5)
        variation_entry = tk.Entry(options_popup)
        variation_entry.pack(pady=5)

        def confirm_options():
            self.ideal_temperature = int(temp_ideal_entry.get())
            self.variation = int(variation_entry.get())

            with open("options.txt", "w") as options_file:
                options_file.write(f"{self.ideal_temperature}\n")
                options_file.write(f"{self.variation}\n")

            self.reset_frames()
            options_popup.destroy()

        tk.Button(options_popup, text="Confirmar", command=confirm_options, bg=GREEN_COLOR, fg=WHITE_COLOR).pack(pady=5)

    # Reseta os frames
    def reset_frames(self):
        # Remove todos os frames e tudo que tem dentro
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label) or isinstance(widget, tk.Canvas):
                widget.destroy()

        # Recria todos os frames com a nova temperatura ideal e variação
        self.create_frame(0.090, 0.150, "Sala 1", 23)
        self.create_frame(0.550, 0.150, "Sala 2", 15)
        self.create_frame(0.090, 0.440, "Sala 3", 18)
        self.create_frame(0.550, 0.440, "Sala 4", 25)
        self.create_button()

# Chama a classe principal
Main()