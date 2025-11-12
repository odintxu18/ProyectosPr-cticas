import tkinter as tk

from rich_toolkit import button

root = tk.Tk()

root.geometry("300x300")
root.title("TicTacToe")
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(
    0,
    weight=1,
)
buttonframe.columnconfigure(1, weight=1)
button1 = tk.Button(buttonframe, text="Iniciar Sesión", font=("Arial", 20))
button2 = tk.Button(buttonframe, text="Registrase", font=("Arial", 20))
button1.grid(row=0, column=0, sticky=tk.W + tk.E)
button2.grid(row=0, column=1, sticky=tk.W + tk.E)
buttonframe.pack(fill="x")


def ajustar_padding(event=None):
    altura = root.winfo_height()
    padding_y = int(altura * 0.3)  # 30% del alto
    buttonframe.pack_configure(fill="x", pady=padding_y)


buttonframe.pack(fill="x", pady=int(root.winfo_height() * 0.3))
root.bind("<Configure>", ajustar_padding)


root.mainloop()
