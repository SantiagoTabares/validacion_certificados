import PyPDF2

archivo_pdf =  open('1-EticaLaboral.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
#print(pdf_reader.documentInfo)

page_pdf =pdf_reader.getPage(0)
text = page_pdf.extract_text()

if   text is "SANTIAGO TABARES MORALES":
    print("Si esta")
else:
    print("No esta")

print(text)
