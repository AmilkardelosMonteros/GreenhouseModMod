from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from .base import add_table, add_text,style,ts

from utils.create_folders import date

def add_table(pdf,data,reg,x,y):
    data = dic_to_list(data,reg)
    table = Table(data)
    table.setStyle(style)
    table.setStyle(ts)
    table.wrapOn(pdf,400,100)
    table.drawOn(pdf, x, y)

def dic_to_list(data,reg):
    lista = list()
    for k, v in data.items():   # iter on both keys and values
        if reg != None:
            if k.startswith(reg):
                lista.append([k, str(v.val),v.units,v.ok])
        else:
            lista.append([k, str(v.val),v.units,v.ok])
    lista.insert(0, ['Nombre', 'Valor','Unidades','Info'])
    return lista


def Constants(dic_constants,PATH=''):
    CONSTANTS = dic_constants['CONSTANTS']
    INPUTS = dic_constants['INPUTS']
    CONTROLS = dic_constants['CONTROLS']
    OTHER_CONSTANTS= dic_constants['OTHER_CONSTANTS']
    STATE_VARS = dic_constants['STATE_VARS']
    fileName = 'reports/Reporte_constantes.pdf'
    fileName = PATH + '/' + fileName
    documentTitle = 'Document title!'
    title = 'Reporte de constantes ' + date() 
    subTitle = ''
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    pdf.drawCentredString(300, 800, title)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Courier-Bold", 26)
    pdf.drawCentredString(290,720, subTitle)
    x = 50
    add_text(pdf,['Alpha'],x, 750)
    add_table(pdf,CONSTANTS,'alpha',x,540)
    add_text(pdf,['Beta'],x, 510)
    add_table(pdf,CONSTANTS,'beta',x,405)
    add_text(pdf,['Gamma'],x, 370)
    add_table(pdf,CONSTANTS,'gamma',x,200)
    pdf.showPage()
    add_text(pdf,['Delta'],x, 770)
    add_table(pdf,CONSTANTS,'delta',x,590)
    add_text(pdf,['Epsilon'],x, 545)
    add_table(pdf,CONSTANTS,'epsi',x,390)
    add_text(pdf,['Eta'],x, 350)
    add_table(pdf,CONSTANTS,'eta',x,40)
    pdf.showPage()
    add_text(pdf,['Lambda'],x, 770)
    add_table(pdf,CONSTANTS,'lamb',x,590)
    add_text(pdf,['Rho'],x, 545)
    add_table(pdf,CONSTANTS,'rho',x,420)
    add_text(pdf,['Tau'],x, 390)
    add_table(pdf,CONSTANTS,'tau',x,290)
    add_text(pdf,['Nu'],x, 260)
    add_table(pdf,CONSTANTS,'nu',x,60)
    pdf.showPage()
    add_text(pdf,['Phi'],x, 770)
    add_table(pdf,CONSTANTS,'phi',x,570)
    add_text(pdf,['Psi'],x, 535)
    add_table(pdf,CONSTANTS,'psi',50,430)
    add_text(pdf,['Omega'],x, 390)
    add_table(pdf,CONSTANTS,'omega',x,290)
    pdf.showPage()
    add_text(pdf,['Inputs'],x, 780)
    add_table(pdf,INPUTS,None,x,490)
    add_text(pdf,['Controles'],x, 450)
    add_table(pdf,CONTROLS,None,x,215)
    add_text(pdf,['Otras'],x, 180)
    add_table(pdf,OTHER_CONSTANTS,None,x,3)
    pdf.showPage()
    add_text(pdf,['Estados'],x, 780)
    add_table(pdf,STATE_VARS,None,x,660)

    pdf.save() 
