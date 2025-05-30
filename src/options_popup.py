from tkinter import *
from constants import *
from tkinter import messagebox

# ----POP-UP----
# Pop-up de edição de valores
def open_options_popup(self):
    options_popup = Toplevel(self.root)
    options_popup.title("Edição de Valores")
    options_popup.geometry("300x170")
    options_popup.resizable(False, False)
    options_popup.grab_set()

    Label(options_popup, text="Digite a temperatura ideal desejada:").pack(pady=5)
    temp_ideal_entry = Entry(options_popup)
    temp_ideal_entry.pack(pady=5)

    Label(options_popup, text="Digite a variação desejada:").pack(pady=5)
    variation_entry = Entry(options_popup)
    variation_entry.pack(pady=5)

    def confirm_options():
        if not temp_ideal_entry.get().strip or not variation_entry.get().strip():
            messagebox.showwarning("Atenção", "É preciso preencher ambos os campos antes de confirmar.")
            return

        if not temp_ideal_entry.get().isdigit() or not variation_entry.get().isdigit():
            messagebox.showwarning("Atenção", "Digite apenas números.")
            return

        self.ideal_temperature = int(temp_ideal_entry.get())
        self.variation = int(variation_entry.get())

        with open("../options.txt", "w") as options_file:
            options_file.write(f"{self.ideal_temperature}\n")
            options_file.write(f"{self.variation}\n")

        self.reset_frames()
        options_popup.destroy()

    Button(options_popup, text="Confirmar", command=confirm_options, bg=GREEN_COLOR, fg=WHITE_COLOR).pack(pady=5)
