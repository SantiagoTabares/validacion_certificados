import pandas as pd
import mysql.connector

# Leer el archivo de Excel
df = pd.read_excel('certificados_validados.xlsx')

# Establecer la conexión a la base de datos
cnx = mysql.connector.connect(user='root', password='MIGUEL123',
                              host='localhost', database='newdatabase')
cursor = cnx.cursor()

# Iterar a través de cada fila del dataframe y agregarlas a la tabla de MySQL
# id_pdf	empleado	certificado	fecha	plataforma	aprobado	talentos

for i, row in df.iterrows():
    # id = row['id_pdf']
    name = row['empleado']
    date = row['fecha']
    doc_url = row['id_pdf']
    approved = row['aprobado']
    points = row['talentos']
    # remarks = row['Remarks']
    # employee_id = row['Employeeld']
    rejected = not row['aprobado']
    platform = row['plataforma']
    
    # Comprobar si ya existe una fila con el mismo id
    query = "SELECT DocumentUrl FROM certificates WHERE DocumentUrl = %s"
    cursor.execute(query, (doc_url,))
    result = cursor.fetchone()
    
    if result:
        # Si ya existe una fila con el mismo id, actualizar los valores de la fila
        query = ("UPDATE certificates SET Name = %s, Date = %s, "
                 "Approved = %s, Points = %s, "
                 "Rejected = %s, Platform = %s WHERE DocumentUrl = %s")
        values = (name, date,  approved, points,
                  rejected, platform, doc_url)
        cursor.execute(query, values)
    # else:
        # Si no existe una fila con el mismo id, insertar una nueva fila
        # query = ("INSERT INTO certificates (id, Name, Date, DocumentUrl, Approved, "
        #          "Points, Remarks, Employeeld, Rejected, Platform) "
        #          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        # values = (id, name, date, doc_url, approved, points, remarks,
        #           employee_id, rejected, platform)
        # cursor.execute(query, values)

# Confirmar los cambios y cerrar la conexión
cnx.commit()
cursor.close()
cnx.close()
