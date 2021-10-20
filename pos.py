from tkinter import *
from tkinter import font

root = Tk()

root.geometry("1360x720")

cafe = "Cafe________________________________________700"
aromatica = "Aromatica____________________________________700"
poker = "Poker______________________________________3000"

#Diccionario con todos los productos

dic_productos = {"Cafe" : 0, "Aromatica" : 0, "Poker" : 0}

def aumentar_producto(nombre_producto):
    dic_productos [nombre_producto] += 1

def disminuir_productos(nombre_producto):
    if dic_productos [nombre_producto] > 0:
        dic_productos [nombre_producto] -= 1
        
def reiniciar_valores_diccionario():
    for producto in list(dic_productos):
        dic_productos[producto] = 0

titulo = Label(root, text="Cafe el Cafecito", font = ("Arial", 24), bg= "#EBA152", width=1360).pack()

frame_objetos = Frame()
frame_objetos.pack()
frame_objetos.place(x=860, y=42)
frame_objetos.config(relief= SUNKEN, width= 500, height=720, bg= "#E86346")

lista_objetos = Listbox(frame_objetos)
lista_objetos.config(width=50, height=30, bg="#FFC559", font=('TkMenuFont, 12'))
lista_objetos.place(x =42, y=10)

boton_cafe = Button(root, text = "Cafe Vendido", font = ("Arial", 12), command=lambda:[lista_objetos.insert(END, cafe), aumentar_producto("Cafe")])
boton_cafe.place(x=100, y=100)

boton_aromatica = Button(root, text = "Aromatica Vendida", font = ("Arial", 12), command=lambda:[lista_objetos.insert(END, aromatica), aumentar_producto("Aromatica")])
boton_aromatica.place(x=100, y=150)

boton_poker = Button(root, text = "Poker Vendida", font = ("Arial", 12), command=lambda:[lista_objetos.insert(END, poker), aumentar_producto("Poker")])
boton_poker.place(x=100, y=200)

boton_borrar_item = Button(frame_objetos, text = "Borrar Seleccion", font = ("Arial", 12), command=lambda: [disminuir_productos((lista_objetos.get(ANCHOR).split("_")[0])), lista_objetos.delete(ANCHOR) ])
boton_borrar_item.place(x=100, y=600)

boton_anadir = Button(frame_objetos, text = "Anadir Objetos", font = ("Arial", 12))
boton_anadir.place(x = 250, y=600)

boton_borrar_lista = Button(frame_objetos, text = "Borrar Lista", font = ("Arial", 12), command= lambda: [lista_objetos.delete(0, END), reiniciar_valores_diccionario()])
boton_borrar_lista.place(x = 400, y=600)

mainloop()