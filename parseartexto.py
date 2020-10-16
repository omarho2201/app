import re

#1.- Abrir archivo y extraer texto
_textoaparsear=open('TextoParaParseo.txt', 'r')  
_contenido=_textoaparsear.read()

#2.- Buscar patrones. --- Definir un Patron de busqueda
_patron = (r"ID CURSO:\n"
	r"\d{3} NOMBRE\n"
	r"\s\n"
	r"CURSO:\n"
	r"\w+ \w+ \w+ FECHA:\d{2}\/\d{2}\/\d{4}\n"
	r"\s\n"
	r"CURSANTES\n"
	r"\s\n"
	r"C\n"
	r"LAVE\n"
	r":\n"
	r"\w+\n"
	r"\s\n"
	r"NOMBRE:\n"
	r"(\w+)\n"
	r"\s\n"
	r"\s\n"
	r"APELLIDOS:\n"
	r"(\w+ \w+)\n"
	r"\s\n"
	r"\s\n"
	r"CORREO:\n"
	r"(^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO:\n"
	r"(\d+)\n"
	r"\s\n"
	r"CLAVE: (\w+)\n"
	r"\s\n"
	r"NOMBRE: (\w+)\n"
	r"\s\n"
	r"APELLIDOS: (\w+ \w+)\n"
	r"\s\n"
	r"CORREO: ([a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO: (\d+)\n"
	r"\s\n"
	r"CLAVE: (\w+)\n"
	r"\s\n"
	r"NOMBRE: (\w+)\n"
	r"\s\n"
	r"APELLIDOS: (\w+ \w+) \n"
	r"\s\n"
	r"CORREO: ([a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO: (\d+)")

#3.- Listado de resultados encontrados
_todos=re.findall(_patron, _contenido, re.MULTILINE)
print(_todos)

#4.- Mostrar
for _registro in _todos:
    print(_registro)
