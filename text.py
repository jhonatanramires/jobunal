import os
import glob
import pdfplumber

directorio= os.path.dirname(os.path.abspath(__file__))
archivos_pdf= glob.glob(os.path.join(directorio, "*.pdf"))

if not archivos_pdf:
    print("No se encontraron archivos en el directorio.")
    exit()
for archivo_pdf in archivos_pdf:
    
print("Archivos Encontrados:")
for i, archivo in enumerate(archivos_pdf, 1):
    print(f"{i}. {os.path.basename(archivo)}")

ruta= archivos_pdf[0]
texto=[]
with pdfplumber.open(ruta) as pdf:
    for pagina in pdf.pages:
        tablas=pagina.extract_tables()
        for tabla in tablas:
            texto.append(tabla)
print('Información de la Convocatoria')
datos={}
tabla1= texto[0]
datos["Número de convocatoria"]= tabla1[0][1]
datos["Fecha"]= f"{tabla1[0][7]}/{tabla1[0][8]}/{tabla1[0][10]}"
datos["Nombre de la convocatoria"]= tabla1[1][1]
datos["Nombre de la dependencia"]= tabla1[2][1]
datos["Área"]= tabla1[3][1]
tipo_estudiante= tabla1[4]
datos["Tipo de Estudiante"]=[]
if "⛝" in tipo_estudiante[1]:
    datos["Tipo de Estudiante"].append("Pregrado")
if "⛝" in tipo_estudiante[5]:
    datos["Tipo de Estudiante"].append("Posgrado")
tipo_convocatoria=[
    ("Apoyo Académico", tabla1[5][1]),
    ("Apoyo a Proyectos de Investigación o Extensión", tabla1[5][2]),
    ("Gestión Administrativa", tabla1[5][4]),
    ("Bienestar Universitario", tabla1[5][6]),
    ("Otro", tabla1[5][9])
]
datos["Tipo de Convocatoria"] = [nombre for nombre, valor in tipo_convocatoria
                                 if valor and "⛝" in valor]
datos["Requisitos"]= tabla1[6][1]

tabla2=texto[1]
datos["Estudiantes a Vincular"]= tabla2[0][1]
datos["Perfil"]= [tabla2[1][1],tabla2[2][1], tabla2[3][1]]
datos["Actividades a Desarrollar"]= [tabla2[4][1], tabla2[5][1], tabla2[6][1]]
modalidades=[
    ("Presencial", tabla2[7][1]),
    ("Virtual", tabla2[7][2]),
    ("Mixta", tabla2[7][3])
]
datos["Modalidad"]= [nombre for nombre, valor in modalidades 
                     if valor and "⛝" in valor]
datos["Disponibilidad"]= tabla2[8][1]
datos["Estímulo"]= tabla2[9][1]
datos["Duración"]= tabla2[10][1]

tabla3=texto[3] if len(texto)>3 else texto[2]
datos["Criterios Evaluatorios"]= []
for fila in tabla3:
    if fila[1]:
        datos["Criterios Evaluatorios"].append(fila[1])
datos["Responsable"]= tabla3[6][1]
for clave, valor in datos.items():
    print(f"{clave}: {valor}\n")