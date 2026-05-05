from reportlab.lib.units import mm
import reportlab.lib.colors as color
from bible_GlobalParam import margin, ringhole, monthStrShort

def DrawMoneyPlan(pdf, leftPageflg):

    # canvas状態を一時保存
    pdf.saveState()

    # マージン設定
    rHole = ringhole
    if leftPageflg:
        rHole = margin

    # 罫線
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    ## Horizontal
    for y in range(1, 13):
        pdf.line(rHole*mm, (margin+10*y)*mm, (rHole+80)*mm, (margin+10*y)*mm)
    ## Vertical
    pdf.line((rHole+5)*mm, margin*mm, (rHole+5)*mm, (margin+160)*mm)

    # 文字
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.rotate(270)
    ## タイトル
    pdf.setFont('BIZUDGothicR', 10)
    pdf.drawCentredString(-145*mm, (rHole+3.5)*mm, 'Money Plan')
    for i in range(1, 13):
        ## 月の数字
        pdf.setFont('BIZUDGothicR', 10)
        pdf.drawString((-134+10*i)*mm, (rHole+3.5)*mm, str(i))
        ## 月の綴り先頭3文字
        pdf.setFont('BIZUDGothicR', 7)
        pdf.drawRightString((-126+10*i)*mm, (rHole+3.5)*mm, monthStrShort[i-1])

    # canvas状態をレストア
    pdf.restoreState()

    # 改ページ
    pdf.showPage()