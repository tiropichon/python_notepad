# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from io import open
import time
import tempfile
import win32api
import win32print

class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master=None)
		self.master=master
		self.master.title("Mi editor de texto en python")
		self.scrollbar = Scrollbar(self.master)
		self.scrollbar.pack(side="right", fill="y")
		self.master.iconbitmap("notepad.ico")
		self.create_widgets()
		# Declaramos la variable ruta
		self.ruta=""

	########################
	#       Funciones      #
	########################

	def nuevo(self):
		global ruta
		self.mensaje.set("Nuevo fichero")
		self.ruta=""
		self.texto.delete(1.0,END) # En flotante, el primer carácter es un salto
		self.master.title("Mi editor de texto en python")

	def abrir(self):
		self.mensaje.set("Abrir fichero")
		self.ruta = filedialog.askopenfilename(initialdir=".", 
			filetypes=(("Ficheros de texto",".txt"),), 
			title="Abrir un fichero de texto")
		if self.ruta == "":
			self.mensaje.set("Abrir archivo cancelado")
			self.ruta=""
		else:
			fichero = open(self.ruta, "r")
			contenido = fichero.read()
			fichero.close()
			self.texto.insert(INSERT,contenido)
	
	def guardar(self):
		self.mensaje.set("Guardar fichero")
		if self.ruta != "":
			contenido = self.texto.get(1.0,"end-1c")
			fichero = open(self.ruta, "w+")
			fichero.write(contenido)
			fichero.close()
			self.mensaje.set("Fichero guardado correctamente")
		else:
			self.guardar_como()

	def guardar_como(self):
		self.mensaje.set(self.mensaje.get() + "Guardar fichero como")
		#fichero = filedialog.asksaveasfile(title="Guardar fichero", mode="w", defaultextension=".txt")
		fichero = filedialog.asksaveasfile(initialdir=".",
			filetypes=(("Ficheros de texto",".txt"),),
			mode ="w", title="Guardar como...")

		if fichero is None:
			self.mensaje.set("Guardado cancelado")
			self.ruta=""
		else:
			self.ruta = fichero.name
			contenido = self.texto.get(1.0,"end-1c")
			fichero = open(self.ruta,"w+")
			fichero.write(contenido)
			fichero.close()
			self.mensaje.set("Fichero guardado correctamente")

	def imprimir(self):
		archivo = tempfile.mktemp(".txt")
		print(archivo)
		open(archivo, "w").write(self.texto.get(1.0,"end-1c"))
		win32api.ShellExecute (
			0,
			"printto",
			archivo,
			'"%s"' % win32print.GetDefaultPrinter (),
			".",
			0
			)

	def cut(self, event=None):
		self.copy()
		self.texto.delete("sel.first","sel.last")

	def copy(self, event=None):
		self.master.clipboard_clear()
		text = self.texto.selection_get()
		self.master.clipboard_append(text)


	def paste(self, event=None):
		text = self.texto.selection_get(selection="CLIPBOARD")
		self.texto.insert("insert", text)

	def select_all(self, event=None):
		self.texto.after(50, lambda:event.widget.tag_add("sel","1.0","end"))

	def delete(self, event=None):
		self.texto.delete("sel.first","sel.last")

	def acercade(self):
		messagebox.showinfo("Acerca de...","App desarrollada por Mario Ruiz en el Curso de Python")

	def times(self):
		current_time = time.strftime("%H:%M:%S %d/%m/%Y")
		self.clock.config(text=current_time)
		self.clock.after(200,self.times)

	########################
	#  Ventana principal   #
	########################

	def create_widgets(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar, width=600, height=500)

		filemenu = Menu(self.menubar, tearoff=0)
		editmenu = Menu(self.menubar, tearoff=0)
		formatmenu = Menu(self.menubar, tearoff=0)
		vermenu = Menu(self.menubar, tearoff=0)
		helpmenu = Menu(self.menubar, tearoff=0)

		self.menubar.add_cascade(label="Archivo", menu=filemenu)
		self.menubar.add_cascade(label="Edición", menu=editmenu)
		self.menubar.add_cascade(label="Formato", menu=formatmenu)
		self.menubar.add_cascade(label="Ayuda", menu=helpmenu)

		filemenu.add_command(label="Nuevo", command=self.nuevo)
		filemenu.add_command(label="Abrir...", command=self.abrir)
		filemenu.add_command(label="Guardar", command=self.guardar)
		filemenu.add_command(label="Guardar como...", command=self.guardar_como)
		filemenu.add_separator()
		filemenu.add_command(label="Imprimir", command=self.imprimir)
		filemenu.add_separator()
		filemenu.add_command(label="Salir", command=self.master.quit)

		editmenu.add_command(label="Cortar", command=self.cut)
		editmenu.add_command(label="Copiar", command=self.copy)
		editmenu.add_command(label="Pegar", command=self.paste)
		editmenu.add_command(label="Eliminar", command=self.delete)
		editmenu.add_separator()
		editmenu.add_command(label="Seleccionar todo", command=lambda:self.texto.tag_add("sel","1.0","end"))
		editmenu.add_separator()
		editmenu.add_command(label="Buscar...")
		editmenu.add_command(label="Buscar siguiente")
		editmenu.add_command(label="Reemplazar...")
		editmenu.add_command(label="Ir a...")
		editmenu.add_separator()
		editmenu.add_command(label="Seleccionar todo")

		formatmenu.add_command(label="Fuente...")

		helpmenu.add_command(label="Ver la ayuda")
		helpmenu.add_command(label="Acerca de mi editor de texto", command=self.acercade)

		#Cuadro de texto central
		self.texto = Text(self.master)
		self.texto.pack(fill="both", expand=1)
		self.texto.config(padx=6, pady=4, bd=0, font=("Tahoma",12), undo=True, autoseparators=True, 
			maxundo=-1, yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.texto.yview)
		self.texto.bind_class("Text","<Control-c>",self.copy)
		self.texto.bind_class("Text","<Control-v>",self.paste)
		self.texto.bind_class("Text","<Control-x>",self.cut)
		self.texto.bind_class("Text","<Control-a>",self.select_all)
		self.texto.focus_set()

		#Barra de estado
		self.mensaje = StringVar()
		self.mensaje.set("Bienvenido a tu editor en python")
		self.monitor = Label(self.master,textvar=self.mensaje, justify="left")
		self.monitor.pack(side="left")
		self.clock = Label(self.master, justify="right")
		self.clock.pack(side="right")
		self.times()

def test():
	root = Tk()
	app = Application(root)
	app.mainloop()

if __name__  == "__main__":
	test()