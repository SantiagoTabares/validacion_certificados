import os
import pandas as pd

# Comprobar si el archivo ya existe
if os.path.isfile("certificados_validados.xlsx"):
    print("El archivo ya existe.")
    df = pd.read_excel("certificados_validados.xlsx")
else:
    # Si no existe, crear el archivo
    df = pd.DataFrame(columns=["id_pdf", "empleado","certificado", "fecha", "plataforma", "aprobado", "talentos"])
    df.to_excel("certificados_validados.xlsx", index=False)
    print("Se ha creado el archivo 'certificados_validados.xlsx'.")
directorio = "C:\\Users\\Santiago\\Documents\\pdfscertificadosclaro"  

lis = []
for archivo in os.listdir(directorio):
    ruta_archivo = os.path.join(directorio, archivo)
    if os.path.isfile(ruta_archivo):
        # Aquí puedes hacer lo que quieras con cada archivo
        if not df['id_pdf'].isin([archivo]).any():
            #lis.append(archivo)
            nuevo_valor = pd.DataFrame({"id_pdf":[archivo], "empleado":[None],"certificado":[None],
                                         "fecha":[None], "plataforma":[None], "aprobado":[None], "talentos":[None]})
            df = pd.concat([df,nuevo_valor] )

print(df)
df.to_excel("certificados_validados.xlsx", index=False)
