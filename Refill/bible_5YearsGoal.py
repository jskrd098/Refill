from reportlab.lib.units import mm
import reportlab.lib.colors as color
from bible_GlobalParam import margin, ringhole

def Draw5YearsPlanChart(pdf, leftPageFlg):

    # canvas状態を一時保存
    pdf.saveState()

    # マージン設定
    rHole = ringhole
    if leftPageFlg:
        rHole = margin

    # 罫線
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    ## Horizontal
    for y in range(1, 6):
        pdf.line(rHole*mm, (margin+24*y)*mm, (rHole+80)*mm, (margin+24*y)*mm)
    ## Vertical
    pdf.line((rHole+5)*mm, margin*mm, (rHole+5)*mm, (margin+160)*mm)

    # 文字
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.rotate(270)
    ## タイトル
    pdf.setFont('BIZUDGothicR', 10)
    pdf.drawCentredString(-145*mm, (rHole+3.5)*mm, '5Years Plan Chart')

    # canvas状態をレストア
    pdf.restoreState()

    # 改ページ
    pdf.showPage()