from reportlab.lib.units import mm
import calendar
from bible_GlobalParam import size_w, margin, ringhole
from DrawMiniCalender import DrawMiniCalendar

def DrawYearCalendar(pdf, y, leftPageFlg):

    # canvas状態を一時保存
    pdf.saveState()

    # マージン設定
    rHole = ringhole
    if leftPageFlg:
        rHole = margin

    # 年の記載
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.setFont('BIZUDGothicR', 20)
    pdf.drawCentredString((size_w+rHole)/2*mm, 18*mm, str(y))
    
    # 各月の記載
    for m in range(1, 13):
        cal_list = calendar.month(y, m)
        DrawMiniCalendar(pdf, (rHole+2+(m-1)%3*27.5)*mm, (35+(m-1)//3*33)*mm, 3.6*mm, 3.5*mm, 7, y, m)

    # canvas状態をレストア
    pdf.restoreState()

    pdf.showPage() # 改ページ