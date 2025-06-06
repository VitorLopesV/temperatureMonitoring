import os
import random
import tkinter as tk
import serial
import threading
from tkinter import messagebox
from tkinter import *
from constants import *
from configurations_popup import open_configurations_popup

# ----CLASSE PRINCIPAL----
class TemperatureControlApp:
    def __init__(self):
        self.create_main_frame()

        self.arduino_port = "COM3"
        self.baud_rate = 9600
        self.serial_connection = None

        # Status do botão de ligar/desligar monitoramento de temperatura.
        self.status = tk.StringVar(value=VALUE_TO_CONNECT)

        self.save_configurations()

        self.rooms_data = {}

        self.temperature_update_job = None

        self.create_rooms()
        self.create_button()
        self.configurations()
        self.update_all_room_displays()

        self.start_serial_thread()

        self.root.mainloop()

    # Cria e configura os estoques
    def create_rooms(self):
        self.setup_room("Sala 1", 0.090, 0.150)
        self.setup_room("Sala 2", 0.550, 0.150)
        self.setup_room("Sala 3", 0.090, 0.440)
        self.setup_room("Sala 4", 0.550, 0.440)

    # Salva os dados de temperatura ideal e variação
    def save_configurations(self):
        if os.path.exists("../configurations.txt"):
            with open("../configurations.txt", "r") as configurations_file:
                lines = configurations_file.readlines()
                self.ideal_temperature = int(lines[0])
                self.variation = int(lines[1])
        else:
            self.ideal_temperature = 24
            self.variation = 2

    # Cria a tela principal e define algumas configurações a ela
    def create_main_frame(self):
        self.root = tk.Tk()
        self.root.title(TITLE_FRAME)
        self.root.geometry("1100x500")
        self.root.resizable(False, False)

    # Cria todos os componentes de um estoque
    def setup_room(self, name, x, y):
        frame = tk.Frame(self.root, background=GREY_COLOR, highlightbackground="black", highlightthickness=1)
        frame.place(relx=x, rely=y, relwidth=0.347, relheight=0.2)

        tk.Label(frame, text="Nome: " + name, bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(frame, text="Temperatura ideal: " + str(self.ideal_temperature), bg=GREY_COLOR, fg=WHITE_COLOR).pack(
            anchor='w', padx=10, pady=2)
        tk.Label(frame, text="Variação: " + str(self.variation), bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w',
                                                                                                     padx=10, pady=2)

        temp_var = tk.DoubleVar(value=0.0)
        temperature_label = tk.Label(self.root, textvariable=temp_var, bg=GREY_COLOR, fg=WHITE_COLOR,
                                     font=("Arial", 10))
        temperature_label.place(relx=x + 0.140, rely=y + 0.209, relwidth=0.050, relheight=0.050)

        led_canvas = tk.Canvas(frame, width=40, height=40, background=GREY_COLOR, highlightthickness=0)
        led_canvas.place(relx=0.86, rely=0.33)
        led_oval = led_canvas.create_oval(4, 4, 30, 30, fill=GREEN_COLOR, outline=GREEN_COLOR)

        self.rooms_data[name] = {
            "frame": frame,
            "temp_var": temp_var,
            "temperature_label": temperature_label,
            "led_canvas": led_canvas,
            "led_oval_id": led_oval,
            "x": x,
            "y": y
        }

    # Atualiza a cor do led.
    def update_room_display(self, room_name):
        room_info = self.rooms_data[room_name]
        current_temperature = room_info["temp_var"].get()
        led_canvas = room_info["led_canvas"]
        led_oval_id = room_info["led_oval_id"]

        color = GREEN_COLOR

        if (current_temperature > self.ideal_temperature + self.variation or
                current_temperature < self.ideal_temperature - self.variation):
            color = YELLOW_COLOR
        if (current_temperature > self.ideal_temperature + (2 * self.variation) or
                current_temperature < self.ideal_temperature - (2 * self.variation)):
            color = RED_COLOR
        if current_temperature == 0.0:
            color = WHITE_COLOR

        led_canvas.itemconfig(led_oval_id, fill=color, outline=color)

    # Atualiza a cor de todos os leds de cada estoque.
    def update_all_room_displays(self):
        for room_name in self.rooms_data:
            self.update_room_display(room_name)

    # Simula dos sensores de temperatura.
    def simulate_temperatures(self):
        # Só simula se o monitoramento estiver LIGADO
        if self.status.get() == VALUE_TURN_OFF:
            for room_name, room_info in self.rooms_data.items():
                if room_name == "Sala 1":
                    continue

                new_temp = random.uniform(10.0, 30.0)
                room_info["temp_var"].set(f"{new_temp:.2f}")

            self.update_all_room_displays()

        self.temperature_update_job = self.root.after(3000, self.simulate_temperatures)

    # Cria botão de ligar/desligar monitoramento de temperatura
    def create_button(self):
        self.button = tk.Button(self.root, textvariable=self.status, width=20, command=self.toggle, bg=GREEN_COLOR,
                                fg=WHITE_COLOR, font=("Arial", 12))
        self.button.place(relx=0.41, rely=0.85)

    # Verifica estado do botão e altera quando o botão é clicado.
    def toggle(self):
        if self.status.get() == VALUE_TURN_OFF:
            self.status.set(VALUE_TO_CONNECT)
            self.button.configure(bg=GREEN_COLOR)
            # Para a simulação
            if self.temperature_update_job:
                self.root.after_cancel(self.temperature_update_job)
                self.temperature_update_job = None
            # Zerando as temperaturas das salas quando a simulação for desligada
            for room_name, room_info in self.rooms_data.items():
                room_info["temp_var"].set(0.0)

            self.update_all_room_displays()

        else:
            self.status.set(VALUE_TURN_OFF)
            self.button.configure(bg=RED_COLOR)
            # Inicia a simulação
            self.simulate_temperatures()

    # Barra de configurações
    def configurations(self):
        configurations_bar = Menu(self.root)
        self.root.config(menu=configurations_bar)

        filemenu = Menu(configurations_bar, tearoff=0)
        configurations_bar.add_cascade(label="Configurações", menu=filemenu)

        filemenu.add_command(label="Editar", command=lambda: open_configurations_popup(self))
        filemenu.add_command(label="Sair", command=self.root.destroy)

    # Reseta os frames
    def reset_frames(self):
        # Cancela qualquer atualização de temperatura em andamento antes de destruir widgets
        if self.temperature_update_job:
            self.root.after_cancel(self.temperature_update_job)
            self.temperature_update_job = None

        for room_info in self.rooms_data.values():
            room_info["frame"].destroy()
            room_info["temperature_label"].destroy()
            room_info["led_canvas"].destroy()
        self.rooms_data = {}  # Limpa o dicionário

        self.setup_room("Sala 1", 0.090, 0.150)
        self.setup_room("Sala 2", 0.550, 0.150)
        self.setup_room("Sala 3", 0.090, 0.440)
        self.setup_room("Sala 4", 0.550, 0.440)

        self.update_all_room_displays()

        # Se o monitoramento estava ligado, reinicia-o
        if self.status.get() == VALUE_TURN_OFF:
            self.simulate_temperatures()

    # Inicia a comunicação serial com o Arduino
    def start_serial_thread(self):
        try:
            self.serial_connection = serial.Serial(self.arduino_port, self.baud_rate, timeout=1)
            serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
            serial_thread.start()
        except serial.SerialException:
            messagebox.showerror("Erro no Arduino", "Verifique se a porta COM está correta ou se o Arduino está ativo em algum outro programa.")

    # Lê os dados de temperatura enviados pelo Arduino pela porta serial
    def read_serial_data(self):
        while True:
            if self.serial_connection and self.serial_connection.in_waiting:
                temp_celsius = self.serial_connection.readline().decode('utf-8').strip()
                if self.status.get() == VALUE_TURN_OFF:
                    self.rooms_data["Sala 1"]["temp_var"].set(temp_celsius)
                    self.update_room_display("Sala 1")

# Chama a classe principal
TemperatureControlApp()
