from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color
import textwrap
import calendar
import datetime
import jpholiday

# 用紙サイズ
A4_w, A4_h = A4
refill_w = 95*mm
refill_h = 170*mm
refill_x = A4_w/2 - refill_w/2
refill_y = A4_h/2 - refill_h/2

# ファイル名
FILENAME = 'weekly_bible.pdf'

# フォーマット定義
pdf = canvas.Canvas(FILENAME, pagesize=portrait(A4), bottomup=False)

# フォント登録
BIZUDGothicR = "./fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))
font_size = 14

# ページ数
pagenum = 106

# 余白
margin = 2*mm
ringhole = 11*mm

# 週間バーチカル表示における1日あたりの列幅
column_w = 21*mm

def PageFinder(pdf, leftpage):
    pdf.setStrokeColor(color.gray)
    pdf.setDash([2,2])
    if leftpage == True:
        # ページの左下に切り取り線
        pdf.line(refill_x+10*mm, refill_y+refill_h, refill_x, refill_y+refill_h-10*mm)
    else:
        # ページの右下に切り取り線
        pdf.line(refill_x+refill_w-10*mm, refill_y+refill_h, refill_x+refill_w, refill_y+refill_h-10*mm)

def CutLine(pdf):
    pdf.setStrokeColor(color.gray)
    pdf.setDash([2,2])
    pdf.lines([
        (0, refill_y, A4_w, refill_y),
        (0, refill_y+refill_h, A4_w, refill_y+refill_h),
        (refill_x, 0, refill_x, A4_h),
        (refill_x+refill_w, 0, refill_x+refill_w, A4_h)
    ])

def MiniCalendar(pos_x, pos_y, dis_x, dis_y, fontsize, year_num, month_num):
    weekdayShort_str = ('M', 'T', 'W', 'T', 'F', 'S', 'S') # 曜日表記
    calendar_list = calendar.monthcalendar(year_num, month_num)
    for i in range(0, len(calendar_list)): # 週
        for j in range(0, len(calendar_list[i])): # 日
            if calendar_list[i][j] != 0:
                if j == 5: # 土曜日を青文字に
                    pdf.setFillColor(color.fidblue)
                elif j == 6: # 日曜日赤文字に
                    pdf.setFillColor(color.fidred)
                else: # 平日は黒文字に
                    pdf.setFillColor(color.gray)
                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(pos_x+j*dis_x, pos_y, weekdayShort_str[j])
                if jpholiday.is_holiday(datetime.date(year_num, month_num, calendar_list[i][j])) == True: # 祝日を赤文字に
                    pdf.setFillColor(color.fidred)
                # 日の記載
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(pos_x+j*dis_x, pos_y+(i+1)*dis_y+0.5*mm, str(calendar_list[i][j]))

def DrawWeeklyVertical(pdf):

    year_num = 2021
    month_num = 11
    month_num_h = month_num # 祝日判定用引数
    double_month = False
    month_str = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    weekday_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    hl_margin = 1*mm
    
    # カレンダーデータの取得
    calendar_list = calendar.monthcalendar(year_num-1, 12)
    for m in range(1, 13):
        calendar_list += calendar.monthcalendar(year_num, m)
    calendar_list += calendar.monthcalendar(year_num+1, 1)
    
    # データの加工 [29, 30, 31, 0, 0, 0, 0], [0, 0, 0, 1, 2, 3, 4] -> [29, 30, 31, 1, 2, 3, 4]
    weeks = len(calendar_list)
    w = 1
    while w < weeks-1: # 最初と最後の週はスルー
        delflg = False
        for d in range(0, len(calendar_list[w])):
            if calendar_list[w][d] == 0:
                calendar_list[w][d] = calendar_list[w+1][d]
                delflg = True
        if delflg == True:
            del calendar_list[w+1]
            weeks -= 1
        w += 1

    # P1
    leftpage = False
    PageFinder(pdf, leftpage)
    CutLine(pdf)
    pdf.showPage()

    # P2～
    year_num -= 1 # 最初に前年12月分の日付を記入するため
    for w in range(4, len(calendar_list)-5):

        # 月跨ぎの週かどうかを判定する + 日付から月の値を求める
        for d in range(0, len(calendar_list[w])):
            if d > 0 and calendar_list[w][d-1] > calendar_list[w][d]:
                double_month = True
                month_num += 1
                month_num = month_num % 12
            elif d == 0 and calendar_list[w-1][6] > calendar_list[w][0]:
                month_num += 1
                month_num = month_num % 12

        for d in range(0, len(calendar_list[w])):

            # 水平方向の位置決めと左ページかどうかの判定
            pos_x = refill_x
            if d >= 0 and d < 3:
                leftpage = True
            else:
                leftpage = False
                pos_x += ringhole

            if (d > 0 and calendar_list[w][d-1] > calendar_list[w][d]) or (d == 0 and calendar_list[w-1][6] > calendar_list[w][0]):
                month_num_h += 1
                month_num_h = month_num_h % 12

            # 日付と曜日の文字色を設定
            if jpholiday.is_holiday(datetime.date(year_num, month_num_h+1, calendar_list[w][d])) == True: # 祝日を赤文字に + 祝日名を記載
                pdf.setFillColor(color.fidred)
                pdf.setFont('BIZUDGothicR', 4)
                pdf.drawRightString(pos_x+column_w*((d+1)%4)+20*mm, refill_y+margin+5*mm, jpholiday.is_holiday_name(datetime.date(year_num, month_num_h+1, calendar_list[w][d])))
            elif d == 5: # 土曜日を青文字に
                pdf.setFillColor(color.fidblue)
            elif d == 6: # 日曜日を赤文字に
                pdf.setFillColor(color.fidred)
            else:
                pdf.setFillColor(color.gray)

            # 日付
            pdf.setFont('BIZUDGothicR', 12)
            pdf.drawCentredString(pos_x+column_w*((d+1)%4)+3*mm, refill_y+margin+4*mm, str(calendar_list[w][d]))

            # 曜日
            pdf.setFont('BIZUDGothicR', 8)
            pdf.drawRightString(pos_x+column_w*((d+1)%4)+20*mm, refill_y+margin+3*mm, weekday_str[d])

            # ページ毎の処理
            if d == 2 or d == 6: # 日付記入後に行う
                # 左ページのみ
                if leftpage == True:
                    # 年月
                    pdf.setFillColor(color.gray)
                    if double_month == False:
                        pdf.setFont('BIZUDGothicR', 8)
                        pdf.drawString(pos_x+margin, refill_y+margin+9*mm, str(year_num))
                        pdf.setFont('BIZUDGothicR', 16)
                        pdf.drawString(pos_x+margin, refill_y+margin+5*mm, str(month_num+1))
                        pdf.setFont('BIZUDGothicR', 6)
                        pdf.drawRightString(pos_x+column_w-1*mm, refill_y+margin+2*mm, month_str[month_num])
                    else: # 月跨ぎの週
                        pdf.setFont('BIZUDGothicR', 16)
                        pdf.drawString(pos_x+margin, refill_y+margin+5*mm, '／')
                        if month_num == 0: # 年跨ぎの週
                            pdf.setFont('BIZUDGothicR', 8)
                            pdf.drawString(pos_x+margin, refill_y+margin+9*mm, str(year_num)+'/'+str(year_num+1))
                            pdf.drawString(pos_x+margin, refill_y+margin+2*mm, '12')
                            pdf.drawString(pos_x+margin+4*mm, refill_y+margin+5*mm, '1')
                            pdf.setFont('BIZUDGothicR', 6)
                            pdf.drawRightString(pos_x+column_w-1*mm, refill_y+margin+2*mm, month_str[11])
                            pdf.drawRightString(pos_x+column_w-1*mm, refill_y+margin+4.5*mm, month_str[month_num])
                            year_num += 1
                        else:
                            pdf.setFont('BIZUDGothicR', 8)
                            pdf.drawString(pos_x+margin, refill_y+margin+9*mm, str(year_num))
                            pdf.drawString(pos_x+margin, refill_y+margin+2*mm, str(month_num))
                            pdf.drawString(pos_x+margin+4*mm, refill_y+margin+5*mm, str(month_num+1))
                            pdf.setFont('BIZUDGothicR', 6)
                            pdf.drawRightString(pos_x+column_w-1*mm, refill_y+margin+2*mm, month_str[month_num-1])
                            pdf.drawRightString(pos_x+column_w-1*mm, refill_y+margin+4.5*mm, month_str[month_num])
                        double_month = False

                    # ミニカレンダー
                    # 当月
                    MiniCalendar(pos_x+margin, refill_y+refill_h-margin-20*mm, 2.8*mm, 2*mm, 5, year_num, month_num+1)
                    pdf.setFillColor(color.gray)
                    pdf.setFont('BIZUDGothicR', 10)
                    pdf.drawString(pos_x+margin-1*mm, refill_y+refill_h-margin-22*mm, str(month_num+1))

                # 全ページ
                # 罫線(縦方向)
                pdf.setStrokeColor(color.gray)
                pdf.setLineWidth(0.1)
                for x in range(1, 4):
                    pdf.lines([
                        (pos_x+column_w*x, refill_y+margin, pos_x+column_w*x, refill_y+margin+12*mm),
                        (pos_x+column_w*x, refill_y+margin+123*mm, pos_x+column_w*x, refill_y+margin+123.5*mm),
                        (pos_x+column_w*x, refill_y+refill_h-margin-0.5*mm, pos_x+column_w*x, refill_y+refill_h-margin)
                    ])
                    # pdf.line(pos_x+column_w*x, refill_y+margin, pos_x+column_w*x, refill_y+margin+12*mm)
                # 罫線(横方向)
                for y in range(0, 4):
                    for x in range(0, 4):
                        if leftpage == True and x == 0:
                            x += 1
                        pdf.line(pos_x+column_w*x+hl_margin, refill_y+margin+y*36*mm+13.5*mm, pos_x+column_w*(x+1)-hl_margin, refill_y+margin+y*36*mm+13.5*mm)
                pdf.setDash([1,1])
                for y in range(1, 18):
                    for x in range(0, 4):
                        if leftpage == True and x == 0:
                            x += 1
                        if y != 6 or y != 18:
                            pdf.line(pos_x+column_w*x+hl_margin, refill_y+margin+y*6*mm+13.5*mm, pos_x+column_w*(x+1)-hl_margin, refill_y+margin+y*6*mm+13.5*mm)
                # 時間軸
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 4)
                for col_num in range(1, 4):
                    for hour_num in range(6, 25):
                        pdf.drawCentredString(pos_x+column_w*col_num, refill_y+margin+(hour_num-4)*6*mm+2*mm, str(hour_num))
                        if hour_num < 24:
                            pdf.drawCentredString(pos_x+column_w*col_num, refill_y+margin+(hour_num-4)*6*mm+5*mm, '・')
                # ページファインダー切り取り線
                if d == 2:
                    PageFinder(pdf, True)
                elif d == 6:
                    PageFinder(pdf, False)
                # トンボ
                CutLine(pdf)

                # 改ページ
                pdf.showPage()
   
def main():
    
    DrawWeeklyVertical(pdf)

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()