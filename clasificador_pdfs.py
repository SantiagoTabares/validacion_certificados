import PyPDF2
import re
import datetime
import locale
import lectorImagenes
from dateutil.parser import parse

# # Abrir el archivo PDF en modo lectura binaria
# archivo_pdf = open("..\ejemUClaro.pdf", 'rb')  

def extraer_informacion(dir_pdf):
    
    archivo_pdf = open(dir_pdf, 'rb') 

    formatos_cursos = {}
    formatos_cursos = {}
    formatos_cursos["ssff"] = { "palabraClave": 'Hace constar que',
                                "inicioNombre":'Hace constar que', 
                                "finalNombre":'ha completado el curso',
                                "inicioFecha": -10, 
                                "finalFecha": -1,
                                "inicioCertificado": 'el curso', 
                                "finalCertificado": -10}
    
    formatos_cursos["carso"] = {"palabraClave": 'para acreditar que',
                                "inicioNombre": 'para acreditar que' ,
                                "finalNombre": 'completó y aprobó los estudios de',
                                "inicioFecha" : 'México a ',
                                "finalFecha" : 'Certificado de ',
                                "inicioCertificado" : 'estudios de ',
                                "finalCertificado"  : 'presentando a la '}
    
    formatos_cursos["uclaro"] = {"palabraClave": 'UNIVERSIDAD CLARO certifica que',
                                "inicioNombre": 'UNIVERSIDAD CLARO certifica que' ,
                                "finalNombre": 'Ha superado cumpliendo con los requisitos académicos exigidos por el curso',
                                "inicioFecha" : 'finalización', "finalFecha" : -1,
                                "inicioCertificado" :'por el curso',
                                "finalCertificado": 'Fecha'}
    
    formatos_cursos["coursera"] = { "palabraClave": 'coursera',
                                    "inicioNombre": 'ofrecido a través de Courseracompletó con éxito' ,
                                    "finalNombre": 'Coursera confirmó la identidad de esta persona',
                                    "inicioCertificado" :'completó con exito',
                                    "finalCertificado": 'un proyecto en línea sin crédito académico autorizado por Coursera'}
    
    formatos_cursos["udemy"] = { "palabraClave": 'Udemy',
                                    "inicioNombre": -84,
                                    "finalNombre": 'Fecha',
                                    "inicioFecha" : 'Fecha ', "finalFecha" : 'Longitud',
                                    "inicioCertificado" :'udemy',
                                    "finalCertificado": 'structores'}
    
    
    pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
    pagina = pdf_reader.getPage(0)
    texto_pag = pagina.extractText()
    print(texto_pag)
    print(texto_pag[-10:-1]+texto_pag[-1])
    
    ##Identifica si del pdf leyó algo
    if texto_pag.strip() == "":
        #El string está vacío o está compuesto sólo por espacios, es probable que sea una imagen
        #print("imagen")
        texto_pag = lectorImagenes.PdfImagenATexto(dir_pdf)
        #print(texto_pag)
    
    plataforma = "sin identificar"
    
    ## la clave representa la plataforma donde se hizo el certificado
    for clave, valor in formatos_cursos.items():
        if valor["palabraClave"] in texto_pag: plataforma = clave
    
    ##una vez se extrae y valida la plataforma, se busca los parametros
    if plataforma == "sin identificar" :
        print("este certificado no cumple con los requisitos")
        nombre, certificado, fecha, aprobado, talentos = None,None,None,None,None
    else:
        nombre, certificado, fecha, aprobado, talentos = buscarParametrosDeRegistro(plataforma, texto_pag, formatos_cursos)
    
    return nombre, certificado, fecha, plataforma, aprobado, talentos


def coursera_Parametros(texto):
    
    posicion = len(texto) - 1  # empezamos desde la última posición del string
    contador = 0
    posiciones = {}
    cantidadSaltos = 0

    while posicion >= 0:
        
        if texto[posicion] == "\n":
            contador += 1
            if contador == 2:
                cantidadSaltos += 1
                posicionFinal = posicion
                posiciones[cantidadSaltos] = {"fin": posicionInicio, "inicio":posicionFinal}
                contador = 0
            else:
                posicionInicio = posicion
                
        posicion -= 1

    ##agregar últimas posiciones
    ultimaposicion = texto[:posicionFinal].find("\n")
    cantidadSaltos += 1 
    posiciones[cantidadSaltos] = {"fin" : posicionFinal, "inicio": ultimaposicion}
    cantidadSaltos += 1 
    posiciones[cantidadSaltos] = {"fin" : ultimaposicion, "inicio": 0}

    meses = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    for indice in posiciones:
        fecha = texto[posiciones[indice]["inicio"]:posiciones[indice]["fin"]]
        if indice-2>0: 
            nombre= texto[posiciones[indice-2]["inicio"]:posiciones[indice-2]["fin"]]
        if indice-3>0: 
            curso = texto[posiciones[indice-3]["inicio"]:posiciones[indice-3]["fin"]]


        for mes in meses:
            if mes in fecha.lower():
                fecha1 = fecha.strip()
                nombre1 = nombre.strip()
                curso1 = curso.strip()
                break
    return curso1, nombre1, fecha1
    

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
    
    if plataforma == "coursera":
        certificado, nombre, fechaSinFormato  = coursera_Parametros(texto_pag)
        
    else:
        nombre = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioNombre"],
                            formatos_cursos[plataforma]["finalNombre"])
        
        nombre = nombre.strip()

        certificado = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioCertificado"],
                            formatos_cursos[plataforma]["finalCertificado"])
        
        certificado= certificado.strip()
        
        fechaSinFormato = buscar_en_pdf(texto_pag, formatos_cursos[plataforma]["inicioFecha"],
                            formatos_cursos[plataforma]["finalFecha"])
    
    
    print(fechaSinFormato)
    fechaConFormato = formatearFecha(fechaSinFormato, plataforma)

    fechaLimite = parse("01/04/2022", dayfirst=True)
    fechaLimite = fechaLimite.strftime("%d/%m/%Y")

    
    aprobado = aprobar_pdf(fechaConFormato, fechaLimite, certificado)

    talentos_plataforma = {"ssff":5, "carso": 10, "uclaro": 5, "coursera":20, "udemy":20}

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
    #print("fecha sin formato: " + fechaSinFormato)
    try:
        ##en caso de ser carso, convierte texto a fecha
        if(plataforma == "carso"): 
            # Establecer el idioma en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            # Fecha en formato string
            fecha = fechaSinFormato.strip()
            # Convertir a objeto date
            fechaConFormato = datetime.datetime.strptime(fecha, '%d de %B del %Y').date()
            fechaConFormato = fechaConFormato.strftime("%d/%m/%Y")
        elif(plataforma == "udemy"): 
            # Establecer el idioma en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            # Fecha en formato string
            fecha = fechaSinFormato.strip()
            
            # Convertir a objeto date
            fechaConFormato = datetime.datetime.strptime(fecha, '%d de %B de %Y').date()
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
    # dir = "C:\\Users\\migue\\OneDrive\\Documentos\\pdfscertificadosclaro" #Miguel

    # pdf ="1b441572-b707-41d0-a103-6953f6544b56.pdf" #coursera
    pdf ="0019d673-4cbe-4d09-a875-2899f5354dcc.pdf"

    nombre, certificado, fecha, plataforma, aprobado, talentos =extraer_informacion("{}/{}".format(dir,pdf))
    #print(nombre)
    #print(certificado)
    print(fecha)
    # print(plataforma)
    # print(aprobado)
    # print(talentos)
    # print(nombre, certificado, fecha, plataforma, aprobado, talentos)