import PyPDF2
import re
import datetime
import locale
from dateutil.parser import parse

# # Abrir el archivo PDF en modo lectura binaria
# archivo_pdf = open("..\ejemUClaro.pdf", 'rb')  

def extraer_informacion(dir_pdf):
    
    archivo_pdf = open(dir_pdf, 'rb') 

    formatos_cursos = {}
    formatos_cursos["ssff"] = {"inicioNombre":'Hace constar que', 
                               "finalNombre":'ha completado el curso',
                               "inicioFecha": -10, 
                               "finalFecha": -1,
                               "inicioCertificado": 'el curso', 
                               "finalCertificado": -10}
    
    formatos_cursos["carso"] = {"inicioNombre": 'para acreditar que' ,
                                "finalNombre": 'completó y aprobó los estudios de',
                                "inicioFecha" : 'México a ',
                                "finalFecha" : 'Certificado de ',
                                "inicioCertificado" : 'estudios de ',
                                "finalCertificado"  : 'presentando a la '}
    
    formatos_cursos["uclaro"] = {"inicioNombre": 'UNIVERSIDAD CLARO certifica que' ,
                                 "finalNombre": 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso',
                                 "inicioFecha" : 'finalización', "finalFecha" : -1,
                                 "inicioCertificado" :'por el curso',
                                 "finalCertificado": 'Fecha'}
    
    formatos_cursos["coursera"] = {"inicioNombre": 'ofrecido a través de Courseracompletó con éxito' ,
                                   "finalNombre": 'Coursera confirmó la identidad de esta persona'}
    
    
    pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
    pagina = pdf_reader.getPage(0)
    texto_pag = pagina.extractText()
    print(texto_pag)
    plataforma = "sin identificar"
    
    ## la clave representa la plataforma donde se hizo el certificado
    for clave, valor in formatos_cursos.items():
        if valor["inicioNombre"] in texto_pag: plataforma = clave
    
    ##una vez se extrae y valida la plataforma, se busca los parametros
    if plataforma == "coursera" or plataforma == "sin identificar" :
        print("este certificado no cumple con los requisitos")
        nombre, certificado, fecha, aprobado, talentos = None,None,None,None,None
    else:
        nombre, certificado, fecha, aprobado, talentos = buscarParametrosDeRegistro(plataforma, texto_pag, formatos_cursos)
    
    return nombre, certificado, fecha, plataforma, aprobado, talentos

def aprobar_pdf(fecha ,fechaLimite , certificado):
    cursos_obligatorios = ['Protección de datos personales', 'Código de Conducta', 'Curso UCC', 'Curso Habilidades UCC',
                        'Ransomware', 'Incapacidades','Lavado de Dinero', 'Convivencia Saludable', 'Curso UCC','Curso Habilidades UCC',
                        'Introducción a la Seguridad de la Información 2022 - Carso', 'Agilidad', 'Igualdad y Equidad de Género', 'Curso UCC','Curso ET',
                        'Programa SSTA 2022', 'CURSOS UCC', 'Curso ET', 
                        'Reinducción 2023', 'Código de Conducta Local - Comcel', 'Experiencia al Colaborador ', 'Plan Maestro',
                        'Agilidad 2.0', 'Decálogo del Líder Ágil' , 'Comunicar es la Onda']
    
    fecha_aceptada = fechaLimite < fecha
    return fecha_aceptada and certificado not in  cursos_obligatorios

    

def buscarParametrosDeRegistro(plataforma, texto_pag, formatos_cursos):
    
    
    nombre = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioNombre"],
                           formatos_cursos[plataforma]["finalNombre"])
    
    certificado = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioCertificado"],
                           formatos_cursos[plataforma]["finalCertificado"])
    
    fechaSinFormato = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioFecha"],
                           formatos_cursos[plataforma]["finalFecha"])
    
    fechaConFormato = formatearFecha(fechaSinFormato, plataforma)

    fechaLimite = parse("01/04/2022", dayfirst=True)
    fechaLimite = fechaLimite.strftime("%d/%m/%Y")

    
    aprobado = aprobar_pdf(fechaConFormato ,fechaLimite , certificado)

    talentos_plataforma = {"ssff":5, "carso": 10, "uclaro": 5, "coursera":20}

    if aprobado: 
        talentos = talentos_plataforma[plataforma]
    else: 
        talentos = 0

    return nombre,certificado, fechaConFormato, aprobado, talentos


def buscar_en_pdf(texto_pag, inicio, final):
    
    if isinstance(inicio, int) : index_inicio = inicio
    else: index_inicio = texto_pag.find(inicio) + len(inicio)

    if isinstance(final, int) :  index_final = final
    else: index_final = texto_pag.find(final) 

    return texto_pag[index_inicio:index_final]

def formatearFecha(fechaSinFormato, plataforma):
    
    try:

        ##en caso de ser carso, convierte texto a fecha
        if(plataforma == "carso"): 
            # Establecer el idioma en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            # Fecha en formato string
            fecha = fechaSinFormato[:-1]
            # Convertir a objeto date
            fechaConFormato = datetime.datetime.strptime(fecha, '%d de %B del %Y').date()
            fechaConFormato = fechaConFormato.strftime("%d/%m/%Y")
            
        else:
            ##en caso de cualquier otra plataforma solo formatea la fecha
            fecha = parse(fechaSinFormato, dayfirst=True)
            fechaConFormato = fecha.strftime("%d/%m/%Y")
        
    except:
        ##en caso de error, es porque la fecha no tiene formato valido
        print("problema formateando la fecha")
        fechaConFormato = fechaSinFormato
    
    return fechaConFormato


if __name__ == '__main__':    
    dir = "C:\\Users\\Santiago\\Documents\\pdfscertificadosclaro"   
    #dir = "C:\\Users\\migue\\OneDrive\\Documentos\\pdfscertificadosclaro" #Miguel

    pdf ="1b441572-b707-41d0-a103-6953f6544b56.pdf"
    nombre, certificado, fecha, plataforma, aprobado, talentos =extraer_informacion("{}/{}".format(dir,pdf))
    print(certificado)




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