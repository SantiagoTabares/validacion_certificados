import pytesseract
from PIL import Image
import aspose.words as aw
import os

def PdfImagenATexto(direccion_pdf):
        
    ##direcciones
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
   
    ##crear ruta para guardar y leer la imagen
    ruta_carpeta_imagen = "G:\\Mi unidad\\TRABAJO\\Claro\\certificadosClasificador\\validacion_certificados\\pdfs_convertido_imagenes\\"
    nombre_imagen = os.path.basename(direccion_pdf).split('.')[0]
    direccion_imagen = ruta_carpeta_imagen + nombre_imagen + '.jpeg'
   
    ##lee el pdf
    document = aw.Document(direccion_pdf)

    ##guarda pdf como imagen
    document.save(direccion_imagen)
    
    ##lee la imagen
    imagen = Image.open(direccion_imagen)
    
    ##convierte la imagen a texto
    texto = pytesseract.image_to_string(imagen, lang='spa')
    
    return texto       


# direccion_pdf = "C:\\Users\\migue\\OneDrive\\Documentos\\pdfscertificadosclaro\\1cf0331b-06e4-4994-a02b-cfcfe97520d4.pdf"
# PdfImagenATexto(direccion_pdf)
