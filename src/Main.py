import tkinter as tk
import random

# ----CONSTANTES----
TITLE_FRAME = "Controle de Temperatura"
SIMULATION_BUTTON_NAME = "Simulador"

GREY_COLOR = "grey31"
WHITE_COLOR = "white"
RED_COLOR = "red"
GREEN_COLOR = "green"
YELLOW_COLOR = "yellow"

VALUE_TO_CONNECT = "Ligar"
VALUE_TURN_OFF = "Desligar"

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE_FRAME)
        self.root.geometry("1100x500")
        self.root.resizable(False, False)

        self.dynamic_rooms = {}
        self.simulating = False

        self.create_rooms()
        self.create_simulation_popup_button()

        self.root.mainloop()

    def create_rooms(self):
        self.create_room(0.090, 0.150, "Sala1", 20, 2)
        self.create_room(0.550, 0.150, "Sala2", 20, 2)
        self.create_room(0.090, 0.440, "Sala3", 20, 2)
        self.create_room(0.550, 0.440, "Sala4", 20, 2)

    def create_room(self, x, y, name, ideal, variation):
        frame = tk.Frame(self.root, bg=GREY_COLOR, highlightbackground=GREY_COLOR, highlightthickness=1)
        frame.place(relx=x, rely=y, relwidth=0.347, relheight=0.2)

        tk.Label(frame, text=f"Nome: {name}", bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10, pady=2)
        tk.Label(frame, text=f"Temperatura desejada: {ideal}", bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10)
        tk.Label(frame, text=f"Variação: {variation}", bg=GREY_COLOR, fg=WHITE_COLOR).pack(anchor='w', padx=10)

        temp_var = tk.DoubleVar(value=0.0)
        temp_label = tk.Label(self.root, textvariable=temp_var, bg=GREY_COLOR, fg=WHITE_COLOR)
        temp_label.place(relx=x + 0.140, rely=y + 0.209, relwidth=0.050, relheight=0.050)

        canvas = tk.Canvas(frame, width=40, height=40, bg=GREY_COLOR, highlightthickness=0)
        canvas.place(relx=0.86, rely=0.33)
        led_id = canvas.create_oval(4, 4, 30, 30, fill=GREEN_COLOR, outline=GREEN_COLOR)

        self.dynamic_rooms[name] = {
            "temp_var": temp_var,
            "ideal": ideal,
            "variation": variation,
            "canvas": canvas,
            "led_id": led_id
        }

    def create_simulation_popup_button(self):
        btn = tk.Button(self.root, text=SIMULATION_BUTTON_NAME, width=12,
                        command=self.open_simulation_popup, bg=GREY_COLOR,
                        fg=WHITE_COLOR, font=("Arial", 12))
        btn.place(relx=0.87, rely=0.85)

    def open_simulation_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Simulador de Temperatura")
        popup.geometry("400x300")
        popup.resizable(False, False)

        self.sim_button = tk.Button(popup, text=VALUE_TO_CONNECT, width=12,
                                    command=self.toggle_simulation, bg=GREEN_COLOR,
                                    fg=WHITE_COLOR, font=("Arial", 12))
        self.sim_button.place(relx=0.5, rely=0.5, anchor='center')

    def toggle_simulation(self):
        self.simulating = not self.simulating
        if self.simulating:
            self.sim_button.config(text=VALUE_TURN_OFF, bg=RED_COLOR)
            self.generate_temperatures()
        else:
            self.sim_button.config(text=VALUE_TO_CONNECT, bg=GREEN_COLOR)

    def generate_temperatures(self):
        if not self.simulating:
            return

        for sala in self.dynamic_rooms.values():
            temp = round(random.uniform(10.0, 30.0), 1)
            sala["temp_var"].set(temp)
            color = self.get_led_color(temp, sala["ideal"], sala["variation"])
            sala["canvas"].itemconfig(sala["led_id"], fill=color, outline=color)

        self.root.after(5000, self.generate_temperatures)

    def get_led_color(self, temp, ideal, variation):
        if temp > ideal + 2 * variation or temp < ideal - 2 * variation:
            return RED_COLOR
        elif temp > ideal + variation or temp < ideal - variation:
            return YELLOW_COLOR
        else:
            return GREEN_COLOR

# Executar programa
Main()
