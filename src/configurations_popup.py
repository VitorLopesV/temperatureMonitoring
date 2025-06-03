from tkinter import *
from constants import *
from tkinter import messagebox

# ----POP-UP----
# Pop-up de edição de valores
def open_configurations_popup(self):
    configurations_popup = Toplevel(self.root)
    configurations_popup.title("Edição de Valores")
    configurations_popup.geometry("300x170")
    configurations_popup.resizable(False, False)
    configurations_popup.grab_set()

    Label(configurations_popup, text="Digite a temperatura ideal desejada:").pack(pady=5)
    temp_ideal_entry = Entry(configurations_popup)
    temp_ideal_entry.pack(pady=5)

    Label(configurations_popup, text="Digite a variação desejada:").pack(pady=5)
    variation_entry = Entry(configurations_popup)
    variation_entry.pack(pady=5)

    def confirm_configurations():
        if not temp_ideal_entry.get().strip or not variation_entry.get().strip():
            messagebox.showwarning("Atenção", "É preciso preencher ambos os campos antes de confirmar.")
            return

        if not temp_ideal_entry.get().isdigit() or not variation_entry.get().isdigit():
            messagebox.showwarning("Atenção", "Digite apenas números.")
            return

        self.ideal_temperature = int(temp_ideal_entry.get())
        self.variation = int(variation_entry.get())

        with open("../configurations.txt", "w") as configurations_file:
            configurations_file.write(f"{self.ideal_temperature}\n")
            configurations_file.write(f"{self.variation}\n")

        self.reset_frames()
        configurations_popup.destroy()

    Button(configurations_popup, text="Confirmar", command=confirm_configurations, bg=GREEN_COLOR, fg=WHITE_COLOR).pack(pady=5)
