import tkinter as tk

def saludar():
    print("¡Hola desde Tkinter!")

root = tk.Tk()
root.title("Mi Aplicación")
button = tk.Button(root, text="Saludar", command=saludar)
button.pack()

if __name__ == '__main__':
    root.mainloop()
