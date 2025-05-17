import tkinter as tk

# ----CONSTANTES----

TITLE_FRAME = "Controle de Temperatura"     # Título do painel
VALUE_TO_CONNECT = "Ligar"                  # Texto que fica no botão quando ele está desligado.
VALUE_TURN_OFF = "Desligar"                 # Texto que fica no botão quando ele está Ligado.

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

        self.create_frame(0.090, 0.150, "Sala1", 20, 2, 23)
        self.create_frame(0.550, 0.150, "Sala2", 20, 2, 15)
        self.create_frame(0.090, 0.440, "Sala3", 20, 2, 18)
        self.create_frame(0.550, 0.440, "Sala4", 20, 2, 25)
        self.create_button()
        self.root.mainloop()

    # Cria a tela principal e define algumas configurações a ela.
    def create_main_frame(self):
        self.root = tk.Tk()
        self.root.title(TITLE_FRAME)
        self.root.geometry("1100x500")
        self.root.resizable(False, False)

    # Cria os Componentes que serão exibidos na tela principal
    def create_frame(self, x, y, name, ideal_temperature, variation, temperature):
        self.frame = tk.Frame(self.root, background=GREY_COLOR, highlightbackground="black", highlightthickness=1)
        self.frame.place(relx=x, rely=y, relwidth=0.347, relheight=0.2)

        tk.Label(self.frame, text="Nome: " + name, bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Temperatura desejada: " + str(ideal_temperature), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(self.frame, text="Variação: " + str(variation), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)

        temperarure = tk.Label(self.root, text=temperature, bg=GREY_COLOR, fg=WHITE_COLOR, font=("Arial", 10))
        temperarure.place(relx=x+0.140, rely=y+0.209, relwidth=0.050, relheight=0.050)

        color = GREEN_COLOR

        # Verifica se a variação da temperatura está dentro da variação configurada.
        if temperature > ideal_temperature + variation or temperature < ideal_temperature - variation:
            color = "yellow"
        # Verifica se a variação da temperatura excedeu variação configurada.
        if temperature > ideal_temperature + (2*variation) or temperature < ideal_temperature - (2*variation):
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

# Chama a classe principal
Main()
