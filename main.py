import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


# Variáveis globais
pedacos = 0  # armazena o número de pedaços
forma = ''  # armazena a forma de corte


def corte_pela_forma():
    """Tela para escolher formas de corte."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ttk.Label(main_frame, text="Escolha a forma de corte:", font=("Helvetica", 16), foreground="white", background="#0288D1")
    label.pack(pady=10)

    formas = ["Estrela", "Casa", "Amoeba"]

    for forma in formas:
        button = ttk.Button(main_frame, text=forma, command=lambda f=forma: selecionar_forma(f))
        button.pack(pady=5)

    back_button = ttk.Button(main_frame, text="Voltar", command=main_menu)
    position_back_button(back_button)


def selecionar_forma(formato):
    global forma
    forma = formato
    messagebox.showinfo("Forma Selecionada", f"Você escolheu a forma: {forma}")
    main_menu()


def corte_por_maximizacao():
    """Tela para definir o número máximo de pedaços."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ttk.Label(main_frame, text="Defina o número máximo de pedaços:", font=("Helvetica", 16), foreground="white", background="#0288D1")
    label.pack(pady=10)

    spinbox = ttk.Spinbox(main_frame, from_=1, to=8, width=5)
    spinbox.pack(pady=5)
    spinbox.set(1)

    submit_button = ttk.Button(main_frame, text="Confirmar", command=lambda: confirmar_pedacos(spinbox.get()))
    submit_button.pack(pady=10)

    back_button = ttk.Button(main_frame, text="Voltar", command=main_menu)
    position_back_button(back_button)


def confirmar_pedacos(num_pedacos):
    global pedacos
    pedacos = int(num_pedacos)
    messagebox.showinfo("Pedaços Selecionados", f"Você definiu o máximo de {pedacos} pedaços.")
    main_menu()


def position_back_button(back_button):
    back_button.place(x=main_frame.winfo_width() - 10, y=main_frame.winfo_height() - 15, anchor="se")


def update_gif(label, frames, index):
    """Atualiza os frames do GIF."""
    if not label.winfo_exists(): # Previne erros ao se passar de tela devido ao gif
        return 
    frame = frames[index]
    index = (index + 1) % len(frames)  # Loop pelos frames
    label.configure(image=frame)
    label.image = frame
    root.after(100, update_gif, label, frames, index)  # Atualiza a cada 100ms


def main_menu():
    """Tela inicial com as opções principais."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Container para alinhar o GIF e o texto lado a lado
    title_frame = tk.Frame(main_frame, bg="#0288D1")
    title_frame.pack(pady=20)

    # Carregando e redimensionando os frames do GIF
    gif = Image.open("images/cake.gif")  # Substitua pelo caminho do GIF
    gif_frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        resized_frame = gif.copy().resize((64, 64))  # Redimensiona para 64x64 pixels
        gif_frames.append(ImageTk.PhotoImage(resized_frame))

    gif_label = tk.Label(title_frame, bg="#0288D1")
    gif_label.pack(side="right")
    update_gif(gif_label, gif_frames, 0)

    label = ttk.Label(title_frame, text="Renata Bakery", font=("times", 30), foreground="white", background="#0288D1")
    label.pack(side="right")

    corte_forma_button = ttk.Button(main_frame, text="Corte pela Forma", command=corte_pela_forma)
    maximizacao_button = ttk.Button(main_frame, text="Corte Max. de Pedaços", command=corte_por_maximizacao)

    # Alinhamento dos botões
    def position_buttons():
        main_frame.update_idletasks()
        frame_width = main_frame.winfo_width()
        frame_height = main_frame.winfo_height()

        button_width = 140
        button_height = 30
        spacing = 20

        x1 = (frame_width - (2 * button_width + spacing)) // 2
        x2 = x1 + button_width + spacing
        y = (frame_height - button_height) // 2

        corte_forma_button.place(x=x1, y=y, width=button_width, height=button_height)
        maximizacao_button.place(x=x2, y=y, width=button_width, height=button_height)

    position_buttons()
    main_frame.bind("<Configure>", lambda event: position_buttons())


# Configuração da janela principal
root = tk.Tk()
root.title("Renata Bakery")
root.geometry("400x300")

# Ícone
icon = tk.PhotoImage(file="images/UR.png")
root.iconphoto(False, icon)

# Configuração do frame principal com fundo preto
main_frame = tk.Frame(root, bg="#0288D1")
main_frame.pack(expand=True, fill="both")

main_menu()

root.mainloop()
