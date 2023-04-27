import PyPDF2
import re
from datetime import datetime

# Abrir el archivo PDF en modo lectura binaria
archivo_pdf = open("..\ejemSSFF.pdf", 'rb')  

iden_ssff = ('Hace constar que' and 'ha completado el curso')
iden_carso = ('para acreditar que' and 'completó y aprobó los estudios de')
iden_uclaro = ('UNIVERSIDAD CLARO certifica que' and 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso' ) 
iden_coursera = 'ofrecido a través de Courseracompletó con éxito' and ' Coursera confirmó la identidad de esta persona'

cursos_obligatorios = ['Protección de datos personales', 'Código de Conducta', 'Curso UCC', 'Curso Habilidades UCC',
                       'Ransomware', 'Incapacidades','Lavado de Dinero', 'Convivencia Saludable', 'Curso UCC','Curso Habilidades UCC',
                       'Introducción a la Seguridad de la Información 2022 - Carso', 'Agilidad', 'Igualdad y Equidad de Género', 'Curso UCC','Curso ET',
                       'Programa SSTA 2022', 'CURSOS UCC', 'Curso ET', 
                       'Reinducción 2023', 'Código de Conducta Local - Comcel', 'Experiencia al Colaborador ', 'Plan Maestro',
                       'Agilidad 2.0', 'Decálogo del Líder Ágil' , 'Comunicar es la Onda']                     

# Crear un objeto de la clase PdfFileReader 
pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
# Recorrer todas las páginas del PDF
# Obtener la página actual
pagina = pdf_reader.getPage(0)
# Imprimir el contenido de la página
texto_pag = pagina.extractText()
print(texto_pag)

# fecha_encontrada = re.findall(reg_ex, texto_pag)
# # Si se encuentra una fecha, imprimir en la consola
# if fecha_encontrada:
#     print('La fecha es:', fecha_encontrada[0])
# else:
#     print("No hay")

if iden_ssff in texto_pag:
    print("Es SSFF")

    #Nombre certificado
    inicio_nombre = 'constar que'
    final_nombre = 'ha completado'
    index_inicio_nombre = texto_pag.find(inicio_nombre) + len(inicio_nombre)
    index_final_nombre = texto_pag.find(final_nombre)
    nombre_certificado = texto_pag[index_inicio_nombre:index_final_nombre]
    print(nombre_certificado)

    #Fecha
    inicio_fecha = -10
    fecha_certificado =texto_pag[inicio_fecha:-1]
    print(fecha_certificado)


    #Certificado

    inicio_certificado = 'el curso'
    index_inicio_certificado = texto_pag.find(inicio_certificado) +len(inicio_certificado)

    index_final_certificado  = inicio_fecha

    certificado = texto_pag[index_inicio_certificado:index_final_certificado] 
    print(certificado)
   
elif iden_carso in texto_pag :
    print("Es CARSO")
elif iden_uclaro in texto_pag :
    print("Es Universidad Claro")
elif iden_coursera in texto_pag :
    print("Es Coursera")
else:
    print("Es Otro")