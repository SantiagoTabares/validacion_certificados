import os
import pandas as pd
import clasificador_pdfs

# Comprobar si el archivo ya existe
if os.path.isfile("certificados_validados.xlsx"):
    df = pd.read_excel("certificados_validados.xlsx")
    
else:
    # Si no existe, crear el archivo
    df = pd.DataFrame(columns=["id_pdf", "empleado","certificado", "fecha", "plataforma", "aprobado", "talentos"])
    df.to_excel("certificados_validados.xlsx", index=False)
    print("Se ha creado el archivo 'certificados_validados.xlsx'.")
    

#directorio = "C:\\Users\\migue\\OneDrive\\Documentos\\pdfscertificadosclaro"  # Directorio Miguel
directorio = "C:\\Users\\Santiago\\Documents\\pdfscertificadosclaro"           # Directorio Santigo
lis = []
var =0
listaDocumentosRaros = [];

## se recorre cada archivo en la carpeta del directorio
for archivo in os.listdir(directorio):
    
    ##genera la ruta completa del archivo
    ruta_archivo = os.path.join(directorio, archivo) 
    ##valida que el archivo existe
    if os.path.isfile(ruta_archivo):
        try:
            ##se valida si hay algún archivo repetido
            if (not df['id_pdf'].isin([archivo]).any()):
                ##se extrae la información del certificado
                nombre, certificado, fecha, plataforma, aprobado, talentos = clasificador_pdfs.extraer_informacion("{}/{}".format(directorio,archivo))
                ##se crea un nuevo registro a partir de la información
                nuevo_valor = pd.DataFrame({"id_pdf":[archivo], "empleado":[nombre],"certificado":[certificado],
                                            "fecha":[fecha], "plataforma":[plataforma], "aprobado":[aprobado], "talentos":[talentos]})
                ##se guarda el registro en el objeto df
                df = pd.concat([df,nuevo_valor] )    
                
        except Exception as e:
            print("\n Se ha producido un error:", e)       
            print("\n problema de lectura con el archivo: ",ruta_archivo)
            listaDocumentosRaros.append(ruta_archivo)
                        
df.to_excel("certificados_validados.xlsx", index=False)


# Abrir un archivo en modo escritura ('w')
with open('documentosRaros.txt', 'w') as archivo:
    # Convertir la lista en una cadena de texto separada por comas
    lista_como_texto = "\n".join(map(str, listaDocumentosRaros))
    # Escribir la cadena de texto en el archivo
    archivo.write(lista_como_texto)

