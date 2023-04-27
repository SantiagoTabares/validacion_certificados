import PyPDF2
import re
from datetime import datetime

# # Abrir el archivo PDF en modo lectura binaria
# archivo_pdf = open("..\ejemUClaro.pdf", 'rb')  

# iden_ssff = ('Hace constar que' and 'ha completado el curso')
# iden_carso = ('para acreditar que' and 'completó y aprobó los estudios de')
# iden_uclaro = ('UNIVERSIDAD CLARO certifica que' and 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso' ) 
# iden_coursera = 'ofrecido a través de Courseracompletó con éxito' and ' Coursera confirmó la identidad de esta persona'

# cursos_obligatorios = ['Protección de datos personales', 'Código de Conducta', 'Curso UCC', 'Curso Habilidades UCC',
#                        'Ransomware', 'Incapacidades','Lavado de Dinero', 'Convivencia Saludable', 'Curso UCC','Curso Habilidades UCC',
#                        'Introducción a la Seguridad de la Información 2022 - Carso', 'Agilidad', 'Igualdad y Equidad de Género', 'Curso UCC','Curso ET',
#                        'Programa SSTA 2022', 'CURSOS UCC', 'Curso ET', 
#                        'Reinducción 2023', 'Código de Conducta Local - Comcel', 'Experiencia al Colaborador ', 'Plan Maestro',
#                        'Agilidad 2.0', 'Decálogo del Líder Ágil' , 'Comunicar es la Onda']                     


def buscar_en_pdf(texto_pag, inicio, final):
    if isinstance(inicio, int) :
        index_inicio = inicio
    else:
        index_inicio = texto_pag.find(inicio) + len(inicio)

    if isinstance(final, int) :
        index_final = final
    else:
        index_final = texto_pag.find(final) 

    return texto_pag[index_inicio:index_final]


def SSFF(texto_pag):
    #Nombre certificado
    inicio_nombre = 'constar que'
    final_nombre = 'ha completado'
    nombre_certificado = buscar_en_pdf(texto_pag, inicio_nombre, final_nombre)

    #Fecha
    inicio_fecha = -10
    final_fecha = -1
    fecha_certificado = buscar_en_pdf(texto_pag, inicio_fecha, final_fecha)
    #Certificado

    inicio_certificado = 'el curso'
    index_final_certificado  = inicio_fecha
    certificado = buscar_en_pdf(texto_pag, inicio_certificado,index_final_certificado )

    return nombre_certificado, certificado,  fecha_certificado 

def CARSO(texto_pag):
    #Nombre certificado
    inicio_nombre = 'acreditar que'
    final_nombre = 'completó y '

    nombre_certificado = buscar_en_pdf(texto_pag, inicio_nombre, final_nombre)

    #Fecha
    inicio_fecha = 'México a '
    final_fecha = 'Certificado de '
    fecha_certificado = buscar_en_pdf(texto_pag, inicio_fecha, final_fecha)
    #Certificado

    inicio_certificado = 'estudios de'
    index_final_certificado  = 'presentando a la '
    certificado = buscar_en_pdf(texto_pag, inicio_certificado,index_final_certificado )

    return nombre_certificado, certificado,  fecha_certificado 

def UCLARO(texto_pag):
    #Nombre certificado
    inicio_nombre = 'certifica que'
    final_nombre = 'Ha superado'

    nombre_certificado = buscar_en_pdf(texto_pag, inicio_nombre, final_nombre)

    #Fecha
    inicio_fecha = 'finalización'
    final_fecha = -1
    fecha_certificado = buscar_en_pdf(texto_pag, inicio_fecha, final_fecha)
    #Certificado

    inicio_certificado = 'por el curso'
    index_final_certificado  = 'Fecha'
    certificado = buscar_en_pdf(texto_pag, inicio_certificado,index_final_certificado )

    return nombre_certificado, certificado,  fecha_certificado 

def extraer_informacion(dir_pdf):
    archivo_pdf = open(dir_pdf, 'rb') 
    
    iden_ssff = ('Hace constar que' and 'ha completado el curso')
    iden_carso = ('para acreditar que' and 'completó y aprobó los estudios de')
    iden_uclaro = ('UNIVERSIDAD CLARO certifica que' and 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso' ) 
    iden_coursera = 'ofrecido a través de Courseracompletó con éxito' and ' Coursera confirmó la identidad de esta persona'
    
    pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
    pagina = pdf_reader.getPage(0)
    texto_pag = pagina.extractText()
    #print(pagina.extractText())

    if iden_ssff in texto_pag:
        a, b, c = SSFF(texto_pag)
        return (a, b, c)
    elif iden_carso in texto_pag :
        a, b, c = CARSO(texto_pag)
        return (a, b, c)
    elif iden_uclaro in texto_pag :
        a, b, c = UCLARO(texto_pag)
        return (a, b, c)
    elif iden_coursera in texto_pag :
        return None, None, None
    else:
       return None, None, None
 

if __name__ == '__main__':    
    var1 = "C:\\Users\\Santiago\\Documents\\pdfscertificadosclaro" 
    var2 ="006fedd1-3d70-4f5b-8e4e-cded1e9984c7.pdf"
    x = "{}/{}".format(var1,var2)

    a,b, c = extraer_informacion(x)
    print(c)



    # # Crear un objeto de la clase PdfFileReader 
    # pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
    # # Recorrer todas las páginas del PDF
    # # Obtener la página actual
    # pagina = pdf_reader.getPage(0)
    # # Imprimir el contenido de la página
    # texto_pag = pagina.extractText()
    # print(texto_pag)
    # fecha_encontrada = re.findall(reg_ex, texto_pag)
    # # Si se encuentra una fecha, imprimir en la consola
    # if fecha_encontrada:
    #     print('La fecha es:', fecha_encontrada[0])
    # else:
    #     print("No hay")
    # if iden_ssff in texto_pag:
    #     print("Es SSFF")
    #     a, b, c = SSFF(texto_pag)
    #     print(a, b, c)
    # elif iden_carso in texto_pag :
    #     print("Es CARSO")
    #     a, b, c = CARSO(texto_pag)
    #     print(a, b, c)
    # elif iden_uclaro in texto_pag :
    #     print("Es Universidad Claro")
    #     a, b, c = UCLARO(texto_pag)
    #     print(a, b, c)
    # elif iden_coursera in texto_pag :
    #     print("Es Coursera")
    # else:
    #     print("Es Otro")