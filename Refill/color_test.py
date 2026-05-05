from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color
import textwrap

FILENAME = 'color_test.pdf'

BIZUDGothicR = "./fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

pdf = canvas.Canvas(FILENAME, pagesize=portrait(A4), bottomup=False)


pdf.setFont('BIZUDGothicR', 20)
for i in range(0, 10):
    if i == 0:
        pdf.setFillColor(color.crimson)
    elif i == 1:
        pdf.setFillColor(color.darkred)
    elif i == 2:
        pdf.setFillColor(color.firebrick)
    elif i == 3:
        pdf.setFillColor(color.red)
    elif i == 4:
        pdf.setFillColor(color.deepskyblue)
    elif i == 5:
        pdf.setFillColor(color.dodgerblue)
    elif i == 6:
        pdf.setFillColor(color.fidblue)
    elif i == 7:
        pdf.setFillColor(color.blue)
    elif i == 8:
        pdf.setFillColor(color.royalblue)
    elif i == 9:
        pdf.setFillColor(color.skyblue)
    pdf.drawString((i+1)*10*mm, 10*mm, '8')
pdf.save()