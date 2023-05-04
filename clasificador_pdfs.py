import PyPDF2
import re
import datetime 
import locale
import lectorImagenes
from dateutil.parser import parse
from unidecode import unidecode
import time
import os
import shutil
import difflib

# # Abrir el archivo PDF en modo lectura binaria
# archivo_pdf = open("..\ejemUClaro.pdf", 'rb')  

def extraer_informacion(dir_pdf):
    
    archivo_pdf = open(dir_pdf, 'rb') 

    formatos_cursos = {}
    formatos_cursos = {}
    formatos_cursos["SucessFactors"] = { "palabraClave": 'Hace constar que',
                                "inicioNombre":'Hace constar que', 
                                "finalNombre":'ha completado el curso',
                                "inicioFecha": -10, 
                                "finalFecha": -1,
                                "inicioCertificado": 'el curso', 
                                "finalCertificado": -10}
    
    formatos_cursos["Capacitate Carso"] = {"palabraClave": 'para acreditar que',
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
    
    formatos_cursos["uclaro2"] = {"palabraClave": 'UNIVERSIDAD CLARO certifica que ha superado cumpliendo con los requisitos académicos exigidos el Curso',
                                "inicioNombre": -30,
                                "finalNombre": 'UNIVERSIDAD CLARO certifica que',
                                "inicioFecha" : 'acredita.', "finalFecha" : -1,
                                "inicioCertificado" :'exigidos el Curso',
                                "finalCertificado": 'Para que así conste'}
    
    formatos_cursos["Coursera"] = { "palabraClave": 'coursera',
                                    "inicioNombre": 'ofrecido a través de Courseracompletó con éxito' ,
                                    "finalNombre": 'Coursera confirmó la identidad de esta persona',
                                    "inicioCertificado" :'completó con exito',
                                    "finalCertificado": 'un proyecto en línea sin crédito académico autorizado por Coursera'}
    
    formatos_cursos["Udemy"] = { "palabraClave": 'Udemy',
                                    "inicioNombre": -84,
                                    "finalNombre": 'Fecha',
                                    "inicioFecha" : 'Fecha ', "finalFecha" : 'Longitud',
                                    "inicioCertificado" :'udemy',
                                    "finalCertificado": 'structores'}
    
    
    pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
    pagina = pdf_reader.getPage(0)
    texto_pag = pagina.extractText()
    
    
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
    if plataforma == "sin identificar" or plataforma == "Coursera" :
        print("sin identificar")
        savepdf(dir_pdf)
        nombre, certificado, fecha, aprobado, talentos = None,None,None,None,None
    else:
        nombre, certificado, fecha, aprobado, talentos = buscarParametrosDeRegistro(plataforma, texto_pag, formatos_cursos)
    
    return nombre, certificado, fecha, plataforma, aprobado, talentos

import os
import shutil
def savepdf(dir_pdf):
    
    try:
        ##ruta destino
        ruta_carpeta_pdf_sin_identificar = "pdfs_sin_identificar\\"
        ##ruta origen 
        ruta_carpeta_origen, nombre_pdf = os.path.split(dir_pdf)
        
        src = os.path.join(ruta_carpeta_origen, nombre_pdf ) # origen
        dst = os.path.join(ruta_carpeta_pdf_sin_identificar, nombre_pdf) # destino
        
        shutil.copy(src, dst)
        
    except Exception as e:
        print("error al copiar archivo: ")
        print(e)
        

    

def coursera_Parametros(texto):
    
    # Definir patrón de búsqueda para fechas con formato mmm dd, aaaa
    patron = r'\b\w{3}\s+\d{1,2},\s+\d{4}\b'

    # Buscar la fecha en el texto usando el patrón de búsqueda
    fecha_encontrada = re.search(patron, texto)

    # Si se encontró una fecha, convertirla al formato dd/mm/aaaa
    if fecha_encontrada:
    # Convertir la fecha encontrada a un objeto datetime
        fecha_datetime = datetime.datetime.strptime(fecha_encontrada.group(), '%b %d, %Y')
        fecha_formateada = fecha_datetime.strftime('%d/%m/%Y')
    else:
        fecha_formateada = None
        print("problema al formatear fecha")
    
    return None, None, fecha_formateada
    

def aprobar_pdf(fecha ,fechaLimite , certificado):
    cursos_obligatorios = ['Protección de datos personales', 'Código de Conducta', 'Curso UCC', 'Curso Habilidades UCC',
                        'Ransomware', 'Incapacidades','Lavado de Dinero', 'Convivencia Saludable', 'Curso UCC','Curso Habilidades UCC',
                        'Introducción a la Seguridad de la Información 2022 - Carso', 'Agilidad', 'Igualdad y Equidad de Género', 'Curso UCC','Curso ET',
                        'Programa SSTA 2022', 'CURSOS UCC', 'Curso ET', 
                        'Reinducción 2023', 'Código de Conducta Local - Comcel', 'Experiencia al Colaborador ', 'Plan Maestro',
                        'Agilidad 2.0', 'Decálogo del Líder Ágil' , 'Comunicar es la Onda',#Angely
                        'Código de Etica America movil',"Introduccion a la seguridad de la información", "Prevención lavado de dinero", 
                        "Control efectivo de la corrupción- america latina", "Reinduccion2023", "sagrilaft", "Oea- operador economico autorizado", "Igualdad y equidad de genero-convivencia saludable", 
                        "Programa ssta", "Politica no alcohol,drogas y tabaco ", "Tu te cuidas, nosotros te cuidamos-Pandemia coronavirus", "Ley de proteccion de datos", "Seguridad de la información",
                        "Programa SSTA", "Convivencia saludable", "Codigo de conducta", "Introduccion a la seguridad de la información 2021", "Protección de datos personales en America movil", 
                        "Introduccion a la seguridad de la información 2022", "Código de Etica America movil", "Introduccion a la seguridad de la información ","Prevencion lavado de dinero",
                        "Protección de datos personales en America movil","Control efectivo de la corrupción- america latina ","Reinduccion2023","agrilaft","Oea- operador economico autorizado",
                        "Igualdad y equidad de genero-convivencia saludable","Programa ssta","Politica no alcohol,drogas y tabaco ","Tu te cuidas, nosotros te cuidamos-Pandemia coronavirus",
                        "Ley de proteccion de datos","Seguridad de la información","Programa SSTA","Convivencia saludable","Codigo de conducta","Introducción a la seguridad de la información 2021",
                        "Protección de datos personales en America movil","Introduccion a la seguridad de la información 2022", "Certificación SAGRILAFT", "SAGRILAFT", "RANSOMWAR", 
                        "Certificación Q2 Coor - El feedback y las conversaciones poderosas.","Q2 Junio Int y Esp - Marketing Experiencial y Valor Agregad",
                        "Certificación Q2 App - Desarrollar estrategias para ir de la simpatía a la empatía con clientes difíciles y para promover la retención",
                        "Certificación Q2 Consultor ESP-INT Técnicas de Persuasión para apalancar el valor agregado", "SUP Q2 JUNIO - Mi rol como coequipero de un equipo de alto desempeñ", 
                        "Entrenamiento Poderoso Q2 Abril: Revolución industrial 4." ]    
    
    esta_en_obligarorio = False
    
    for i in range(len(cursos_obligatorios)):
        #print(cursos_obligatorios[i].lower())
        similarity = difflib.SequenceMatcher(None, cursos_obligatorios[i].lower(), certificado.lower()).ratio()
        # print((similarity))
        
        if (similarity>0.75):
            #print(similarity)
            esta_en_obligarorio = True
            break
    fecha = time.strptime(fecha, "%d/%m/%Y")
    
    if fecha < fechaLimite or esta_en_obligarorio :
        return False
    else:
        return True


def buscarParametrosDeRegistro(plataforma, texto_pag, formatos_cursos):
    
    if plataforma == "Coursera":
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
    
        fechaConFormato = formatearFecha(fechaSinFormato, plataforma)
    
    if plataforma=="SucessFactors": fechaSinFormato = fechaSinFormato + texto_pag[-1]

    fechaConFormato = formatearFecha(fechaSinFormato, plataforma)

    # fechaLimite = parse("01/04/2022", dayfirst=True)
    # fechaLimite = fechaLimite.strftime("%d/%m/%Y")
    fechaLimite = "01/04/2022"
    fechaLimite =  time.strptime(fechaLimite, "%d/%m/%Y")

    aprobado = aprobar_pdf(fechaConFormato, fechaLimite, certificado)

    talentos_plataforma = {"SucessFactors":5, "Capacitate Carso": 10, "uclaro": 5, "Coursera":20, "Udemy":20, "uclaro2": 5}

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


def limpiar_fecha(fechaConFormato):
    if "\n" in fechaConFormato  :
        index = fechaConFormato.find("\n") + len("\n") 
        fechaConFormato = fechaConFormato[index:]
    return fechaConFormato

def formatearFecha(fechaSinFormato, plataforma):
    
    try:
        ##en caso de ser carso, convierte texto a fecha
        if(plataforma == "Capacitate Carso"): 
            # Establecer el idioma en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            # Fecha en formato string
            fecha = fechaSinFormato.strip()
            # Convertir a objeto date
            fechaConFormato = datetime.datetime.strptime(fecha, '%d de %B del %Y').date()
            fechaConFormato = fechaConFormato.strftime("%d/%m/%Y")
            
        elif(plataforma == "Udemy"): 
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
        #print("problema formateando la fecha")
        fechaConFormato = fechaSinFormato
        
    
    fechaConFormato = limpiar_fecha(fechaConFormato)
    return fechaConFormato
    


if __name__ == '__main__':    
    # dir = "C:\\Users\\Santiago\\Documents\\pdfscertificadosclaro"   
    dir = "C:\\Users\\migue\\OneDrive\\Documentos\\certificadosPdfsCompletos" #Miguel

    # pdf ="1b441572-b707-41d0-a103-6953f6544b56.pdf" #coursera
    pdf ="19f6bf79-8c69-4bc6-954f-248202bd429c.pdf"

    nombre, certificado, fecha, plataforma, aprobado, talentos =extraer_informacion("{}/{}".format(dir,pdf))
    print("nombre: " + nombre)
    print(certificado)
    print(fecha)
    print(aprobado)
    print(plataforma)
    # texto = " 125/12/2000"
    # # Definir patrón de expresión regula
    # patron = r'\d+/\d+/\d+'

    # # Buscar todas las ocurrencias del patrón en el texto
    # resultados = str(re.findall(patron, texto))
    # StrR = str(resultados[2:-2])
    # print((resultados))
    # Imprimir los resultados


    

    # print(talentos)
    # print(nombre, certificado, fecha, plataforma, aprobado, talentos)