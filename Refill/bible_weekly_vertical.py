from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
# from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color
import textwrap 
import calendar
import datetime
import jpholiday

FILENAME = 'bible_weekly_vertical.pdf' # ファイル名

# 用紙サイズ
size_w = 95*mm
size_h = 170*mm

# 余白
margin = 4*mm
ringhole = 11*mm

# 各ブロックのサイズ
block_w = 20*mm # 列幅
blockdayindex_h = 15*mm # 日付欄の高さ

# フォント登録
BIZUDGothicR = "D:/Program/Python/refill/fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

def DrawAgeChart(pdf, year):
    eto = {0:'申', 1:'酉', 2:'戌', 3:'亥', 4:'子', 5:'丑', 6:'寅', 7:'卯', 8:'辰', 9:'巳', 10:'午', 11:'未'}
    gengou = {0:'大正', 1:'昭和', 2:'平成', 3:'令和'}

    x = 4*mm # 表の原点のx座標
    y = 12*mm # 表の原点のy座標
    
    col = 3 # 列数
    row = 34 # 行数
    line_h = 3*mm # 行の高さ
    line_w = (size_w-ringhole-x)/col # 列幅
    line_col = (0, 7.75*mm, 15.5*mm, 21*mm) # 小列幅

    datanum = 101 # 出力するデータの個数
    seireki = year - datanum # 西暦
    wareki_idx = 1912 # 元号が変更された年
    wareki = seireki - wareki_idx + 1 # 和暦
    age = datanum # 年齢
    gengou_idx = 0 # 元号(インデックス番号)
    col_idx = ('西暦', '和暦', '年齢', '干支') # 各小列見出し

    # 表のタイトル
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.setFont('BIZUDGothicR', 8)
    pdf.drawCentredString(size_w/2-4*mm, 7*mm, 'AGE CHART')
    
    # 罫線
    pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    pdf.setLineWidth(0.1)
    pdf.lines([
        (x+line_w, y-line_h+0.5*mm, x+line_w, y+line_h*row+0.5*mm),
        (x+line_w*2, y-line_h+0.5*mm, x+line_w*2, y+line_h*row+0.5*mm),
        (x, y+0.75*mm, x+line_w*col, y+0.75*mm)
    ])

    # 表の見出し
    pdf.setFont('BIZUDGothicR', 6)
    for i in range(0, col):
        pos_x = x+line_w*i+3*mm
        for k in range(0, len(col_idx)):
            pdf.drawCentredString(pos_x+line_col[k], y, col_idx[k])

    # 表の中身
    for i in range(0, col):
        pos_x = x+line_w*i+3*mm
        for j in range(0, row):
            pos_y = y+line_h*(j+1)
            pdf.drawCentredString(pos_x+line_col[0], pos_y, str(seireki))
            if seireki == 1926 or seireki == 1989 or seireki == 2019:
                gengou_idx += 1
                pdf.drawCentredString(pos_x+line_col[1], pos_y, str(wareki)+'/'+gengou[gengou_idx]+'元')
                wareki = 1
            elif i == 0 and j == 0:
                pdf.drawCentredString(pos_x+line_col[1], pos_y, gengou[gengou_idx]+str(wareki))
            else:
                pdf.drawCentredString(pos_x+line_col[1], pos_y, str(wareki))
            pdf.drawCentredString(pos_x+line_col[2], pos_y, str(age))
            pdf.drawCentredString(pos_x+line_col[3], pos_y, str(eto[seireki%12]))
            age -= 1
            seireki += 1
            wareki += 1

    # メモ欄(見出しのみ)
    pdf.drawString(x+1*mm, pos_y+line_h, "Notes:")

def GetCalendarData(year):
    # カレンダーデータの取得
    buf = calendar.monthcalendar(year-1, 12) # 前年12月
    for m in range(1, 13):
        buf += calendar.monthcalendar(year, m) # 当年1～12月
    buf += calendar.monthcalendar(year+1, 1) # 翌年1月
    
    # データの加工
    # [29, 30, 31, 0, 0, 0, 0], [0, 0, 0, 1, 2, 3, 4]
    # -> [29, 30, 31, 1, 2, 3, 4]
    cal_list = [[0, 0, 0, 0, 0, 0, 0]]
    idx_w = 0
    for w in range (0, len(buf)-1): # 最終行以外の処理
        for d in range (0, len(buf[w])):
            if buf[w][d] != 0:
                cal_list[idx_w][d] = buf[w][d]
                if d == 6:
                    cal_list.append([0, 0, 0, 0, 0, 0, 0])
                    idx_w += 1
    cal_list[idx_w] = buf[len(buf)-1] # 最終行の処理
                    
    return cal_list

def DrawPageFinder(pdf, leftcut):
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    pdf.setDash([2, 2])
    cutpos = 15*mm
    if leftcut == True:
        pdf.line(cutpos, size_h, 0, size_h-cutpos)
    else:
        pdf.line(size_w-cutpos, size_h, size_w, size_h-cutpos)

def DrawMiniCalendar(pdf, x, y, dis_x, dis_y, fontsize, year, month):
    # x, y:原点(左上)
    # dis_x:列間隔, dis_y:行間隔
    # fontsize:文字サイズ
    # year, month:出力する年月の値
    wdstsr = ('M', 'T', 'W', 'T', 'F', 'S', 'S')
    cal_list = calendar.monthcalendar(year, month)

    pdf.setFillColor(color.gray)
    pdf.setFont('BIZUDGothicR', fontsize+5)
    pdf.drawString(x-dis_x/4, y-fontsize, str(month)) # 月
    
    for i in range(0, len(cal_list)): # 週
        for j in range(0, len(cal_list[i])): # 日
            if cal_list[i][j] != 0:
                if j == 6: 
                    pdf.setFillColorRGB(1, 0.5, 0.5) # 日曜日・祝日を赤文字に
                elif j == 5: 
                    pdf.setFillColorRGB(0.5, 0.5, 1) # 土曜日を青文字に
                else: 
                    pdf.setFillColor(color.gray) # 平日は黒文字に
                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(x+j*dis_x, y, wdstsr[j])
                # 日の記載
                if jpholiday.is_holiday(datetime.date(year, month, cal_list[i][j])) == True:
                    pdf.setFillColorRGB(1, 0.5, 0.5)
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(x+j*dis_x, y+(i+1)*dis_y+0.5*mm, str(cal_list[i][j]))

def DrawWeeklyIndex(pdf, x, y, year, month, change_year, change_month):
    month_str = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    monthjp_str = ('睦月', '如月', '弥生', '卯月', '皐月', '水無月', '文月', '葉月', '長月', '神無月', '霜月', '師走')
    
    # 見出し部分の表示
    pdf.setFillColor(color.gray)
    if change_month == True: # 月跨ぎの場合
        # num
        pdf.setFont('BIZUDGothicR', 30)
        pdf.drawCentredString(x+block_w/2, 15.5*mm, '／')
        pdf.setFont('BIZUDGothicR', 15
        )
        pdf.drawCentredString(x+block_w/2-3*mm, 10.5*mm, str(month))
        pdf.drawCentredString(x+block_w/2+3*mm, 15.5*mm, str(month%12+1))
        # en
        pdf.setFont('BIZUDGothicR', 6)
        pdf.drawCentredString(x+block_w/2, 21*mm, month_str[month-1]+'/'+month_str[month%12])
        # jp
        pdf.setFont('BIZUDGothicR', 8)
        pdf.drawCentredString(x+block_w/2, 25*mm, monthjp_str[month-1]+'/'+monthjp_str[month%12])
    else:
        # num
        pdf.setFont('BIZUDGothicR', 30)
        pdf.drawCentredString(x+block_w/2, 15.5*mm, str(month))
        # en
        pdf.setFont('BIZUDGothicR', 12)
        pdf.drawCentredString(x+block_w/2, 21*mm, month_str[month-1])
        # jp
        pdf.setFont('BIZUDGothicR', 8)
        pdf.drawCentredString(x+block_w/2, 25*mm, monthjp_str[month-1])

    if change_year == True: # 年跨ぎの場合
        pdf.setFont('BIZUDGothicR', 8)
        pdf.drawCentredString(x+block_w/2, 29*mm, str(year)+'/'+str(year+1))
    else:
        pdf.setFont('BIZUDGothicR', 12)
        pdf.drawCentredString(x+block_w/2, 30*mm, str(year))
    
    # ミニカレンダーの表示
    if change_month == True: # 月跨ぎの場合
        DrawMiniCalendar(pdf, x+1.5*mm, size_h-42*mm, 2.7*mm, 2*mm, 5, year, month)
        if month%12+1 == 1:
            DrawMiniCalendar(pdf, x+1.5*mm, size_h-24*mm, 2.7*mm, 2*mm, 5, year+1, month%12+1)
        else:
            DrawMiniCalendar(pdf, x+1.5*mm, size_h-24*mm, 2.7*mm, 2*mm, 5, year, month%12+1)
    else:
        DrawMiniCalendar(pdf, x+1.5*mm, size_h-24*mm, 2.7*mm, 2*mm, 5, year, month)

def DrawDay(pdf, x, y, year, month, day, weekday):
    weekday_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    dis_h = 0

    # 罫線の表示
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    pdf.setDash([])
    pdf.line(x, y, x, y+blockdayindex_h-1*mm)

    # 時間軸の表示
    for hour in range(0, 25):
        hour = hour % 24
        pdf.setFillColor(color.gray)
        pdf.setFont('BIZUDGothicR', 4)
        pdf.drawCentredString(x, y+blockdayindex_h+dis_h+0.5*mm, str(hour))
        if hour == 0:
            pdf.setDash([])
        elif hour == 6 or hour == 12 or hour == 18:
            pdf.setDash([1,1])
        else:
            pdf.setDash([0.2, 1])
        pdf.line(x+1*mm, y+blockdayindex_h+dis_h, x+block_w-1*mm, y+blockdayindex_h+dis_h)
        if hour < 6:
            dis_h += 3*mm
        else:
            if hour < 24:
                pdf.drawCentredString(x, y+blockdayindex_h+dis_h+3.5*mm, '・')
            dis_h += 6*mm
        
    # 日付・曜日の表示
    if jpholiday.is_holiday(datetime.date(year, month, day)) == True: # 祝日の場合
        pdf.setFillColorRGB(1, 0.5, 0.5)
        pdf.setFont('BIZUDGothicR', 4)
        pdf.drawRightString(x+block_w-1*mm, y+5*mm, jpholiday.is_holiday_name(datetime.date(year, month, day)))
    elif weekday == 6: # 日曜日の場合
        pdf.setFillColorRGB(1, 0.5, 0.5)
    elif weekday == 5: # 土曜日の場合
        pdf.setFillColorRGB(0.5, 0.5, 1)
    else:
        pdf.setFillColor(color.gray)
    pdf.setFont('BIZUDGothicR', 12)
    pdf.drawString(x+1*mm, y+4*mm, str(day))
    pdf.setFont('BIZUDGothicR', 8)
    pdf.drawRightString(x+block_w-1*mm, y+3*mm, weekday_str[weekday])

def DrawWeeklyVertical(pdf, year):
    cal_list = GetCalendarData(year)
    year -= 1
    month = 12
    
    for w in range(5, len(cal_list)-4):

        # 見出しの表示
        # 表示する月を計算
        if cal_list[w][0] == 1: # 月曜日が1日の場合
            DrawWeeklyIndex(pdf, margin, margin, year, month%12+1, False, False)
        elif 1 in cal_list[w][1:6]: # 火曜日～日曜日のどこかで月を跨ぐ場合
            if month == 12: # さらに年を跨ぐ場合
                DrawWeeklyIndex(pdf, margin, margin, year, month, True, True)
            else:
                DrawWeeklyIndex(pdf, margin, margin, year, month, False, True)
        else:
            DrawWeeklyIndex(pdf, margin, margin, year, month, False, False)
        
        # 日の表示
        for d in range(0, 7):
            if cal_list[w][d] == 1:
                if month == 12:
                    year += 1
                month = month%12 + 1
            if d < 3:
                DrawDay(pdf, margin+block_w*(d+1), margin, year, month, cal_list[w][d], d)
            else:
                DrawDay(pdf, ringhole+block_w*(d-3), margin, year, month, cal_list[w][d], d)
            # 改ページ
            if d == 2: # 週の前半(水曜日)まで表示したら改ページ
                # 週見出しの表示
                DrawPageFinder(pdf, True)
                pdf.showPage()
            elif d == 6: # 週の最後(日曜日)まで表示したら改ページ
                DrawPageFinder(pdf, False)
                pdf.showPage()

def main():

    # 出力する年を指定
    year = 2025

    # フォーマット定義
    pdf = canvas.Canvas(FILENAME, bottomup=False)
    pdf.setPageSize((size_w, size_h))
    
    # P1は白紙とする
    DrawPageFinder(pdf, False)
    pdf.showPage()

    # P2から内容を表示する
    DrawWeeklyVertical(pdf, year)

    # 最終ページ:年齢早見表
    DrawAgeChart(pdf, year)
    DrawPageFinder(pdf, True)
    pdf.showPage()

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()