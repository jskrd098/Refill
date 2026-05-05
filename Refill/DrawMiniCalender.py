from reportlab.lib.units import mm
import calendar
import datetime
import jpholiday
from bible_GlobalParam import weekdayStrShort

def DrawMiniCalendar(pdf, x, y, dis_x, dis_y, fontsize, year, month):
    # x, y:原点(左上)
    # dis_x:列間隔, dis_y:行間隔
    # fontsize:文字サイズ
    # year, month:出力する年月の値
    # wdstsr = ('M', 'T', 'W', 'T', 'F', 'S', 'S')
    cal_list = calendar.monthcalendar(year, month)

    # フォントの設定
    pdf.setFont('BIZUDGothicR', fontsize+5)

    # 文字色の設定
    pdf.setFillColorRGB(0.6, 0.6, 0.6)

    # 月の記載
    pdf.drawString(x-dis_x/4, y-fontsize, str(month))
    
    for i in range(0, len(cal_list)): # 週
        for j in range(0, len(cal_list[i])): # 日
            if cal_list[i][j] != 0:

                # 文字色の設定
                if j == 6: 
                    pdf.setFillColorRGB(1, 0.5, 0.5) # 日曜日・祝日を赤文字に
                elif j == 5: 
                    pdf.setFillColorRGB(0.5, 0.5, 1) # 土曜日を青文字に
                else: 
                    pdf.setFillColorRGB(0.6, 0.6, 0.6) # 平日は黒文字に

                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(x+j*dis_x, y+1*mm, weekdayStrShort[j])

                # 日の記載
                if jpholiday.is_holiday(datetime.date(year, month, cal_list[i][j])) == True:
                    pdf.setFillColorRGB(1, 0.5, 0.5)
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(x+j*dis_x, y+(i+1)*dis_y+0.5*mm, str(cal_list[i][j]))