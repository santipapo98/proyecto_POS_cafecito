from tkinter import *
from tkinter import font
import psycopg2
from fpdf import FPDF
from datetime import datetime
import os

root = Tk()

root.geometry("1360x720")

cafe = "Cafe________________________________________700"
aromatica = "Aromatica____________________________________700"
poker = "Poker_______________________________________3.000"
brandy = "Brandy_____________________________________40.000"
brandy_media = "Brandy 1/2____________________________________20.000"
aguardiente_light = "Aguardiente Light____________________________35.000"
aguardiente_light_media = "Aguardiente Light 1/2_______________________17.500"
aguardiente = "Aguardiente____________________________________30.000"
aguardiente_media = "Aguardiente 1/2_______________________________15.000"
ron = "Ron________________________________________50.000"
ron_media = "Ron 1/2__________________________________25.000"
cola_pola = "Cola y Pola___________________________________3.000"
club = "Club________________________________________4.000"
club_negra = "Club Negra_____________________________________5.000"
aguila_light = "Aguila Light____________________________________3.000"
pony_grande = "Pony Malta Grande_____________________________3.000"
pony_peque = "Pony Malta Peque_____________________________1.500"
gaseosa = "Gaseosa____________________________________3.000"
agua_peque = "Agua Peque__________________________________1.000"


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

dic_productos = {"Brandy" : 0, "Brandy 1/2" : 0, "Aguardiente Light" : 0, "Aguardiente Light 1/2" : 0, "Aguardiente" : 0, "Aguardiente 1/2" : 0, "Ron" : 0, "Ron 1/2" : 0, "Poker" : 0,
                "Cola y Pola" : 0, "Club" : 0, "Club Negra" : 0, "Aguila Light" : 0, "Pony Malta Grande" : 0, "Pony Malta Peque" : 0, "Gaseosa" :0, "Cafe" : 0, "Aromatica" : 0, "Agua Peque" : 0}

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

def actualizar_inventario_actual():
    i = 0
    conexion, cursor = base_datos.conectar_bd()
    cursor.execute('insert into historico_ventas (producto, cantidad) select * from venta_dia;')
    cursor.execute('select * from venta_dia')
    ventas = cursor.fetchall()
    for item in dic_productos.keys():
        cursor.execute('update inventario set cantidad_actual = (cantidad_actual - %s) where producto = %s', (int((ventas[i])[1]), item))
        i +=1
    base_datos.cerrar_conexion(conexion, cursor)

def terminar_dia():
    top =Toplevel()
    top.geometry("300x100")
    top.config(bg= "#EBA152")
    label = Label(top, text="Desea terminar la jornada ?", font=("Helvetica", 12), bg= "#EBA152").pack()
    boton1 = Button(top, width=10, text = "Si", command = lambda: [actualizar_inventario_actual(), reiniciar_valores_venta_dia(),root.destroy(),
    os.system('C:/Users/Santiago/Desktop/proyecto_POS_cafecito/Ventas_Dia_' + datetime.today().strftime('%Y-%m-%d') + '.pdf')])
    boton2 = Button(top, width=10, text= "No", command= top.destroy)
    boton1.place(x=20, y=30)
    boton2.place(x=200, y=30)
    
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
        base_datos.cerrar_conexion(conexion,cursor)
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
        pdf.output('Ventas_Dia_' + datetime.today().strftime('%Y-%m-%d') + '.pdf','F')
        

titulo = Label(root, text="Cafe el Cafecito", font = ("Arial", 24), bg= "#EBA152", width=1360).pack()

frame_objetos = Frame()
frame_objetos.pack()
frame_objetos.place(x=860, y=42)
frame_objetos.config(relief= SUNKEN, width= 500, height=720, bg= "#E86346")

scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = BOTH)


lista_objetos = Listbox(frame_objetos)
lista_objetos.config(width=50, height=30, bg="#FFC559", font=('TkMenuFont, 12'), yscrollcommand=scrollbar.set)
lista_objetos.place(x =25, y=10)
scrollbar.config(command=lista_objetos.yview)

boton_cafe = Button(root, text = "Cafe", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, cafe), aumentar_producto("Cafe"), gestionar_botones()])
boton_cafe.place(x=50, y=60)

boton_aromatica = Button(root, text = "Aromatica", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aromatica), aumentar_producto("Aromatica"), gestionar_botones()])
boton_aromatica.place(x=50, y=170)

boton_poker = Button(root, text = "Poker", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, poker), aumentar_producto("Poker"), gestionar_botones()])
boton_poker.place(x=50, y=280)

boton_brandy = Button(root, text = "Brandy", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, brandy), aumentar_producto("Brandy"), gestionar_botones()])
boton_brandy.place(x=50, y=390)

boton_brandy_media = Button(root, text = "Brandy 1/2", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, brandy_media), aumentar_producto("Brandy 1/2"), gestionar_botones()])
boton_brandy_media.place(x=50, y=500)

boton_aguardiente_light = Button(root, text = "Aguardiente \nLight", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aguardiente_light), aumentar_producto("Aguardiente Light"), gestionar_botones()])
boton_aguardiente_light.place(x=50, y=610)

boton_aguardiente_light_media = Button(root, text = "Aguardiente \nLight 1/2", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aguardiente_light_media), aumentar_producto("Aguardiente Light 1/2"), gestionar_botones()])
boton_aguardiente_light_media.place(x=200, y=60)

boton_aguardiente = Button(root, text = "Aguardiente", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aguardiente), aumentar_producto("Aguardiente"), gestionar_botones()])
boton_aguardiente.place(x=200, y=170)

boton_aguardiente_media = Button(root, text = "Aguardiente \n1/2", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aguardiente_media), aumentar_producto("Aguardiente 1/2"), gestionar_botones()])
boton_aguardiente_media.place(x=200, y=280)

boton_ron = Button(root, text = "Ron", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, ron), aumentar_producto("Ron"), gestionar_botones()])
boton_ron.place(x=200, y=390)

boton_ron_media = Button(root, text = "Ron 1/2", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, ron_media), aumentar_producto("Ron 1/2"), gestionar_botones()])
boton_ron_media.place(x=200, y=500)

boton_cola_pola = Button(root, text = "Cola y Pola", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, cola_pola), aumentar_producto("Cola y Pola"), gestionar_botones()])
boton_cola_pola.place(x=200, y=610)

boton_club = Button(root, text = "Club", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, club), aumentar_producto("Club"), gestionar_botones()])
boton_club.place(x=350, y=60)

boton_club_negra = Button(root, text = "Club Negra", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, club_negra), aumentar_producto("Club Negra"), gestionar_botones()])
boton_club_negra.place(x=350, y=170)

boton_aguila_light = Button(root, text = "Aguila Light", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, aguila_light), aumentar_producto("Aguila Light"), gestionar_botones()])
boton_aguila_light.place(x=350, y=280)

boton_pony_malta_grande = Button(root, text = "Pony Malta \nGrande", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, pony_grande), aumentar_producto("Pony Malta Grande"), gestionar_botones()])
boton_pony_malta_grande.place(x=350, y=390)

boton_pony_malta_peque = Button(root, text = "Pony Malta \nPeque", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, pony_peque), aumentar_producto("Pony Malta Peque"), gestionar_botones()])
boton_pony_malta_peque.place(x=350, y=500)

boton_gaseosa = Button(root, text = "Gaseosa", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, gaseosa), aumentar_producto("Gaseosa"), gestionar_botones()])
boton_gaseosa.place(x=350, y=610)

boton_agua_peque = Button(root, text = "Agua Peque", font = ("Arial", 12), width= 10, height=5, command=lambda:[lista_objetos.insert(END, agua_peque), aumentar_producto("Agua Peque"), gestionar_botones()])
boton_agua_peque.place(x=500, y=60)

boton_borrar_item = Button(frame_objetos, text = "Borrar Seleccion", font = ("Arial", 12), command=lambda: [disminuir_productos((lista_objetos.get(ANCHOR).split("_")[0])), lista_objetos.delete(ANCHOR), gestionar_botones()])
boton_borrar_item.place(x=50, y=600)
boton_borrar_item["state"] = DISABLED

boton_anadir = Button(frame_objetos, text = "Anadir Objetos", font = ("Arial", 12), command=lambda: [ingresar_productos_bd(), reiniciar_valores_diccionario(), lista_objetos.delete(0, END), gestionar_botones()])
boton_anadir.place(x = 200, y=600)
boton_anadir["state"]= DISABLED

def gestionar_botones():
    if lista_objetos.size() == 0:
        boton_anadir["state"] = DISABLED
        boton_borrar_item["state"] = DISABLED
    elif lista_objetos.size() > 0:
        boton_anadir["state"] = ACTIVE
        boton_borrar_item["state"] = ACTIVE

boton_borrar_lista = Button(frame_objetos, text = "Borrar Lista", font = ("Arial", 12), command= lambda: [lista_objetos.delete(0, END), reiniciar_valores_diccionario(), gestionar_botones()])
boton_borrar_lista.place(x = 350, y=600)

boton_terminar_dia = Button(frame_objetos, text = "TERMINAR DIA", font = ("Arial", 12), command= lambda: [PDF.generar_reporte(), terminar_dia()])
boton_terminar_dia.place(x = 200, y=640)

mainloop()