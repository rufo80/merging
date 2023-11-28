from PyPDF2 import PdfReader, PdfWriter
from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject
from reportlab.pdfgen import canvas
import os

class Merging:
    def __init__(self, file_selected, dimensione):
        self.file_selected = file_selected
        self.directory, self.nome_file = os.path.split(self.file_selected)
        self.dimensione = dimensione

    def merge_file(self, output_path_file_cornice, width, height):
        input1 = PdfFileReader(open(output_path_file_cornice, "rb"), strict=False)

        page1 = input1.pages[0]
        page2 = input1.pages[0]

        if(width < height):
            total_width = page1.mediaBox.upperRight[0] + page2.mediaBox.upperRight[0]
            total_height = max([page1.mediaBox.upperRight[1], page2.mediaBox.upperRight[1]])
            width_mm = float(page1.mediaBox.upperRight[0]) * 0.3528
            numero_merge = int(self.dimensione / width_mm)
            new_page = PageObject.createBlankPage(None, (page1.mediaBox.upperRight[0] * numero_merge), total_height)
            new_page.mergePage(page1)
            dim_merge = page1.mediaBox.upperRight[0]
            for ciclo in range(numero_merge):
                new_page.mergeTranslatedPage(page2, dim_merge , 0)
                dim_merge = dim_merge + page1.mediaBox.upperRight[0]
        else:
            total_width = max([page1.mediaBox.upperRight[0], page2.mediaBox.upperRight[0]])
            total_height = page1.mediaBox.upperRight[1] + page2.mediaBox.upperRight[1]
            height_mm = float(page1.mediaBox.upperRight[1]) * 0.3528
            width_mm = float(page1.mediaBox.upperRight[0]) * 0.3528
            numero_merge = int(self.dimensione / height_mm) 
            new_page = PageObject.createBlankPage(None, total_width, (numero_merge * page1.mediaBox.upperRight[1]))
            dim_merge = 0
            for ciclo in range(numero_merge):
                new_page.mergeTranslatedPage(page2, 0, dim_merge)
                dim_merge = dim_merge + page1.mediaBox.upperRight[1]
   
        out_merge = "merge"
        
        output_merge = os.path.join(self.directory, out_merge)
        if not os.path.exists(output_merge):
            os.makedirs(output_merge)
            
        pdf_merged = os.path.join(output_merge, self.nome_file)

        output = PdfFileWriter()
        output.addPage(new_page)
        output.write(open(pdf_merged, "wb"))
        os.remove('tmp.pdf')
        

    def cornice_file(self):
        # Apri il file PDF di input
        pdf = PdfReader(self.file_selected)
        # Crea un oggetto PDF di output
        output = PdfWriter()
                
        page = pdf.pages[0]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        
        # Crea un canvas ReportLab per disegnare la cornice
        c = canvas.Canvas('tmp.pdf', pagesize=(width, height))
        c.setLineWidth(0.283)  # Spessore della cornice: 1 mm
        
        # Disegna la cornice interna
        c.rect(1, 1, width - 2, height - 2)
        c.showPage()
        c.save()
        
        # Unisci il file PDF di input con il file temporaneo contenente la cornice
        tmp_pdf = PdfReader('tmp.pdf')
        page.merge_page(tmp_pdf.pages[0])
        
        # Aggiungi la pagina modificata al file PDF di output
        output.add_page(page)
        
        # Dividi il percorso in directory e nome del file
        #directory, nome_file = os.path.split(file_selected)
        path = "cornice"
        output_path = os.path.join(self.directory, path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path_file_cornice = os.path.join(output_path, self.nome_file)
            
        # Salva il file PDF di output
        with open(output_path_file_cornice, 'wb') as f:
            output.write(f)
    
            # Elimina il file temporaneo
            #os.remove('tmp.pdf')

        self.merge_file(output_path_file_cornice, width, height)
            
##################################
   

       