import PyPDF2
import re
from datetime import datetime

# Abrir el archivo PDF en modo lectura binaria
archivo_pdf = open("..\ejemCoursera.pdf", 'rb')  

iden_ssff = ('Hace constar que' and 'ha completado el curso')
iden_carso = ('para acreditar que' and 'completó y aprobó los estudios de')
iden_uclaro = ('UNIVERSIDAD CLARO certifica que' and 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso' ) 
iden_coursera = 'ofrecido a través de Courseracompletó con éxito' and ' Coursera confirmó la identidad de esta persona'


# Crear un objeto de la clase PdfFileReader
pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
# Recorrer todas las páginas del PDF
# Obtener la página actual
pagina = pdf_reader.getPage(0)
# Imprimir el contenido de la página
texto_pag = pagina.extractText()
#print(texto_pag)

# fecha_encontrada = re.findall(reg_ex, texto_pag)
# # Si se encuentra una fecha, imprimir en la consola
# if fecha_encontrada:
#     print('La fecha es:', fecha_encontrada[0])
# else:
#     print("No hay")

if iden_ssff in texto_pag:
    print("Es SSFF")
elif iden_carso in texto_pag :
    print("Es CARSO")
elif iden_uclaro in texto_pag :
    print("Es Universidad Claro")
elif iden_coursera in texto_pag :
    print("Es Coursera")
else:
    print("Es Otro")