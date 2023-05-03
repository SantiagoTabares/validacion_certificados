import pandas as pd
# Leer el archivo de Excel
df = pd.read_excel('certificados_validados.xlsx')

# Crear un archivo de texto para guardar las consultas
file = open("updates.txt", "w", encoding="utf-8")

# Iterar a través de cada fila del dataframe y agregarlas a la tabla de PostgreSQL
# id_pdf	empleado	certificado	fecha	plataforma	aprobado	talentos

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
        query = "UPDATE certificates SET  Date ="+ str(date)+", Approved = "+ str(approved)+", Points = "+ str(points)+", Rejected = "+ str(rejected)+" , Platform = "+ str(platform)+" WHERE DocumentUrl = "+ str(doc_url)

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
