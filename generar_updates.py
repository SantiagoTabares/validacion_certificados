import pandas as pd
# Leer el archivo de Excel
df = pd.read_excel('certificados_validados.xlsx')

# Crear un archivo de texto para guardar las consultas
file = open("updates.txt", "w", encoding="utf-8")

# Iterar a través de cada fila del dataframe y agregarlas a la tabla de PostgreSQL
# id_pdf	empleado	certificado	fecha	plataforma	aprobado	talentos

mensaje_aprobado = "Hola, gracias por participar en nuestras iniciativas, te invitamos a que sigas cargando tus certificados, recuerda que estos deben tener fecha del 01 de abril al 2022 en adelante. Ten presente que estos dichos certificados deben ser de las plataformas oficiales de Gestión del Talento, como los son Success Factors (cursos transversales), GetAbstract, Capacitate Carso y Coursera o participando en nuestras iniciativas con la Mega voz o nuestro club de lectura (Érase un Café)"
mensaje_rechazado ="Hola, Gracias por participar en nuestras iniciativas, recuerda que los certificados que cargues deben tener fecha del 01 de Abril al 2022 en adelante, ten presente que estos deben ser de las plataformas oficiales de Gestión del Talento, como los son Success Factors (cursos transversales, no obligatorios), GetAbstract, Capacitate Carso y Coursera o participando en nuestras iniciativas con la Mega voz o nuestros club de lectura ( Érase un Café)."



for i, row in df.iterrows():
    # id = row['id_pdf']
    name = row['empleado']
    date = row['fecha']
    doc_url = row['id_pdf'] 
    approved = bool(row['aprobado'])
    points = row['talentos']
    # remarks = row['Remarks']
    # employee_id = row['Employeeld']
    rejected = not row['aprobado']
    platform = row['plataforma']
    if (type(name) != float):
        # Si ya existe una fila con el mismo id, actualizar los valores de la fila
        if approved:
            mensaje = mensaje_aprobado
        else:
            mensaje = mensaje_rechazado
        query = "UPDATE certificates SET  Date ='"+ str(date)+"', Approved = "+ str(int(approved))+", Points = "+ str(points)+", Rejected = "+ str(rejected)+" , Platform = '"+ str(platform)+"' , Remarks = '"+ mensaje +"' WHERE DocumentUrl = '"+ str(doc_url)+"'"

        # Guardar la consulta en el archivo de texto
        file.write(query+ ";\n")
        # ese:
            # Si no existe una fila con el mismo id, insertar una nueva fila
            # query = ("INSERT INTO certificates (id, Name, Date, DocumentUrl, Approved, "
            #          "Points, Remarks, Employeeld, Rejected, Platform) "
            #          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            # values = (id, name, date, doc_url, approved, points, remarks,
            #           employee_id, rejected, platform)
            # cursor.execute(query, values)
