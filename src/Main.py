import tkinter as tk
import random

# ----CONSTANTES----

TITLE_FRAME = "Controle de Temperatura"     # Título do painel
VALUE_TO_CONNECT = "Ligar"                  # Texto que fica no botão quando ele está desligado.
VALUE_TURN_OFF = "Desligar"                 # Texto que fica no botão quando ele está Ligado.
SIMULATION_BUTTON_NAME = "Simulador"        # Texto do botão que abre o popup do simulador.

GREY_COLOR = "grey31"                       # Cor cinza escuro
WHITE_COLOR = "white"                       # Cor branca
RED_COLOR = "red"                           # Cor vermelha
GREEN_COLOR = "green"                       # Cor verde

# ----CLASSE PRINCIPAL----
class Main:
    def __init__(self):
        self.create_main_frame()

        # Status do botão de ligar/desligar monitoramento de temperatura.
        self.status = tk.StringVar(value=VALUE_TO_CONNECT)

        self.popup_status = tk.StringVar(value=VALUE_TO_CONNECT)

        self.is_generating = False

        self.create_frame(0.090, 0.150, "Sala1", 20, 2, 23)
        self.create_frame(0.550, 0.150, "Sala2", 20, 2, 15)
        self.create_frame(0.090, 0.440, "Sala3", 20, 2, 18)
        self.create_frame(0.550, 0.440, "Sala4", 20, 2, 25)
        self.create_button()
        self.create_simulation_button()

        self.root.mainloop()

    # Cria a tela principal e define algumas configurações a ela.
    def create_main_frame(self):
        self.root = tk.Tk()
        self.root.title(TITLE_FRAME)
        self.root.geometry("1100x500")
        self.root.resizable(False, False)

    # Cria os Componentes que serão exibidos na tela principal
    def create_frame(self, x, y, name, ideal_temperature, variation, temperatue):
        self.frame = tk.Frame(self.root, background=GREY_COLOR, highlightbackground="black", highlightthickness=1)
        self.frame.place(relx=x, rely=y, relwidth=0.347, relheight=0.2)

        tk.Label(self.frame, text="Nome: " + name, bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Temperatura desejada: " + str(ideal_temperature), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Variação: " + str(variation), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)

        temperarure = tk.Label(self.root, text=temperatue, bg=GREY_COLOR, fg=WHITE_COLOR, font=("Arial", 10))
        temperarure.place(relx=x+0.140, rely=y+0.209, relwidth=0.050, relheight=0.050)

        color = GREEN_COLOR

        # Verifica se a variação da temperatura está dentro da variação configurada.
        if temperatue > ideal_temperature + variation or temperatue < ideal_temperature - variation:
            color = "yellow"
        # Verifica se a variação da temperatura excedeu variação configurada.
        if temperatue > ideal_temperature + (2*variation) or temperatue < ideal_temperature - (2*variation):
            color = RED_COLOR

        led_example = tk.Canvas(self.frame, width=40, height=40, background=GREY_COLOR, highlightthickness=0)
        led_example.place(relx=0.86, rely=0.33)
        led_example.create_oval(4, 4, 30, 30, fill=color, outline=color)

    # Cria botão de ligar/desligar monitoramento de temperatura
    def create_button(self):
        self.button = tk.Button(self.root, textvariable=self.status, width=20, command=self.toggle, bg=GREEN_COLOR,
                                fg=WHITE_COLOR, font=("Arial", 12))
        self.button.place(relx=0.43, rely=0.85)

    # Cria botão que abre o popup simulador
    def create_simulation_button(self):
        self.button_popup = tk.Button(self.root, text=SIMULATION_BUTTON_NAME, width=9, command=self.create_popup,
                                      bg=GREY_COLOR, fg=WHITE_COLOR, font=("Arial", 12))
        self.button_popup.place(relx=0.90, rely=0.85)

    # Cria o popup do simulador
    def create_popup(self):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Alerta")
        self.popup.geometry("400x300")
        self.popup.resizable(False, False)

        self.teste = tk.Button(self.popup, textvariable=self.popup_status, width=9,
                               command=self.toggle_popup, bg=GREEN_COLOR, fg=WHITE_COLOR, font=("Arial", 12))

        self.teste.place(relx=0.5, rely=0.5, anchor='center')

    # Verifica estado do botão e altera quando o botão é clicado.
    def toggle(self):
        if self.status.get() == VALUE_TURN_OFF:
            self.status.set(VALUE_TO_CONNECT)
            self.button.configure(bg=GREEN_COLOR)
        else:
            self.status.set(VALUE_TURN_OFF)
            self.button.configure(bg=RED_COLOR)

    # Verifica estado do botão do popup do simulador e altera quando o botão é clicado.
    def toggle_popup(self):
        if self.popup_status.get() == VALUE_TURN_OFF:
            self.popup_status.set(VALUE_TO_CONNECT)
            self.teste.configure(bg=GREEN_COLOR)
            self.is_generating = False
        else:
            self.popup_status.set(VALUE_TURN_OFF)
            self.teste.configure(bg=RED_COLOR)
            self.is_generating = True
            self.start_generating_random_values()

    # Inicia o simulador de dados de temperatura
    def start_generating_random_values(self):
        if self.is_generating:
            value = round(random.uniform(10, 30), 2)
            print(f"Valor gerado: {value}")
            self.root.after(5000, self.start_generating_random_values)

# Executa o programa
Main()