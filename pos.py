from tkinter import *
from tkinter import font
import psycopg2
from fpdf import FPDF
from datetime import datetime

root = Tk()

root.geometry("1360x720")

cafe = "Cafe________________________________________700"
aromatica = "Aromatica____________________________________700"
poker = "Poker______________________________________3000"

#funciones para la base de datos
class base_datos:
    
    def conectar_bd():
        con = psycopg2.connect(
            host = 'localhost',
            database = 'proyecto_cafecito',
            user = 'postgres',
            password = 'santipapo98'
            )
        cur= con.cursor()
        return con, cur

    def cerrar_conexion(conexion, cursor):
        conexion.commit()
        conexion.close()
        cursor.close()

#Diccionario con todos los productos

dic_productos = {"Cafe" : 0, "Aromatica" : 0, "Poker" : 0}

#funcion que actualiza los valores vendidos durante el dia
def ingresar_productos_bd():
    conexion, cursor = base_datos.conectar_bd()
    for item in dic_productos:
        cursor.execute('update venta_dia set cantidad = (cantidad+ %s) where producto = %s', (dic_productos[item], item))
    base_datos.cerrar_conexion(conexion,cursor)

#Reiniciar Valores de la venta del dia

def reiniciar_valores_venta_dia():
    conexion, cursor = base_datos.conectar_bd()
    cursor.execute('update venta_dia set cantidad = 0')
    base_datos.cerrar_conexion(conexion, cursor)

def terminar_dia():
    conexion, cursor = base_datos.conectar_bd()
    cursor.execute('insert into historico_ventas (id, producto, cantidad) select id, producto, cantidad from venta_dia')
    #generar_reporte()
    base_datos.cerrar_conexion(conexion, cursor)

def aumentar_producto(nombre_producto):
    dic_productos [nombre_producto] += 1

def disminuir_productos(nombre_producto):
    if dic_productos [nombre_producto] > 0:
        dic_productos [nombre_producto] -= 1
        
def reiniciar_valores_diccionario():
    for producto in list(dic_productos):
        dic_productos[producto] = 0

#generacion de datos mediante PDF

class PDF(FPDF):
    def generar_reporte():
        conexion, cursor = base_datos.conectar_bd()
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 16)
        pdf.cell(0, 10, 'Ventas Cafe el Cafecito', 0, 1, 'C')
        pdf.cell(0, 10, 'Reporte generado el dia: ' + datetime.today().strftime('%Y-%m-%d'), 'B', 2, 'C')
        cursor.execute('select producto, precio_producto, cantidad_actual from inventario')
        record = cursor.fetchall()
        cursor.execute('select cantidad from venta_dia')
        ventas = cursor.fetchall()
        pdf.cell(70, 10, 'Articulo', 'B')
        pdf.cell(30, 10, 'Precio', 'B')
        pdf.cell(30, 10, 'Entrada', 'B')
        pdf.cell(30, 10, 'Ventas', 'B')
        pdf.cell(30, 10, 'Actual', 'B', ln=True)
        for item in range(len(record)):
            pdf.cell(70, 10, str((record[item])[0]))
            pdf.cell(30, 10, str((record[item])[1]))
            pdf.cell(30, 10, str((record[item])[2]))
            pdf.cell(30, 10, str((ventas[item])[0]))
            pdf.cell(30, 10, str(int((record[item])[2])-int((ventas[item])[0])) , ln=True)
        base_datos.cerrar_conexion(conexion,cursor)
        pdf.output('Ventas_Dia_' + datetime.today().strftime('%Y-%m-%d') + '.pdf','F')
        

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

boton_anadir = Button(frame_objetos, text = "Anadir Objetos", font = ("Arial", 12), command=lambda: [ingresar_productos_bd(), lista_objetos.delete(0, END)])
boton_anadir.place(x = 250, y=600)

if lista_objetos.size() == 0:
    boton_anadir["state"] = DISABLED
    boton_borrar_item["state"] = DISABLED
elif lista_objetos.size() > 0:
    boton_anadir["state"] = NORMAL
    boton_borrar_item["state"] = ACTIVE

boton_borrar_lista = Button(frame_objetos, text = "Borrar Lista", font = ("Arial", 12), command= lambda: [lista_objetos.delete(0, END), reiniciar_valores_diccionario()])
boton_borrar_lista.place(x = 400, y=600)

boton_borrar_lista = Button(frame_objetos, text = "TERMINAR DIA", font = ("Arial", 12), command= lambda: [PDF.generar_reporte(), reiniciar_valores_venta_dia()])
boton_borrar_lista.place(x = 250, y=650)

mainloop()