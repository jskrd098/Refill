# 本プログラムの実行には、事前に下記ライブラリのインストールが必要
#
# ＜必要なライブラリ＞
# reportlab : PDFを出力するためのライブラリ
# jpholiday : 日本の祝日を取得するライブラリ
#
# ＜インストール方法＞
# Pythonプロンプトで下記のコマンドを実行
# > pip install reportlab
# > pip install jpholiday

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import calendar
import datetime
import jpholiday

FILENAME = 'bible_monthly.pdf' # ファイル名
year = 2025 # 出力したい年

# フォント登録
BIZUDGothicR = "./fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

# 用紙サイズ
size_w = 95*mm
size_h = 170*mm

# 余白
ringhole = 11*mm

# 月間ブロックのサイズ
block_w = 20*mm
block_h = 27*mm

# 曜日ブロックのサイズ
weekday_w = block_w
weekday_h = 8*mm

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

def DrawPageFinder(pdf, leftcut):
    pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    pdf.setLineWidth(0.1)
    pdf.setDash([2, 2])
    cutpos = 15*mm
    if leftcut == True:
        pdf.lines([(cutpos, size_h, 0, size_h-cutpos), (cutpos, 0, 0, cutpos)])
    else:
        pdf.lines([(size_w-cutpos, size_h, size_w, size_h-cutpos), (size_w-cutpos, 0, size_w, cutpos)])

def DrawMiniCalendar(pdf, x, y, dis_x, dis_y, fontsize, year, month):
    # x, y:原点(左上)
    # dis_x:列間隔, dis_y:行間隔
    # fontsize:文字サイズ
    # year, month:出力する年月の値
    wdstsr = ('M', 'T', 'W', 'T', 'F', 'S', 'S')
    cal_list = calendar.monthcalendar(year, month)

    pdf.setFillColorRGB(0.6, 0.6, 0.6)
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
                    pdf.setFillColorRGB(0.6, 0.6, 0.6) # 平日は黒文字に
                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(x+j*dis_x, y, wdstsr[j])
                # 日の記載
                if jpholiday.is_holiday(datetime.date(year, month, cal_list[i][j])) == True:
                    pdf.setFillColorRGB(1, 0.5, 0.5)
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(x+j*dis_x, y+(i+1)*dis_y+0.5*mm, str(cal_list[i][j]))

def DrawYearCalendar(pdf, y):
    month_str = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    # 年
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.setFont('BIZUDGothicR', 20)
    pdf.drawCentredString((size_w+ringhole)/2, 18*mm, str(y))
    # 月
    for m in range(1, 13):
        cal_list = calendar.month(y, m)
        DrawMiniCalendar(pdf, ringhole+2*mm+(m-1)%3*27.5*mm, 35*mm+(m-1)//3*33*mm, 3.6*mm, 3.5*mm, 7, y, m)

def DrawYearMonth(pdf, x, y, m):
    month_str = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    monthjp_str = ('睦月', '如月', '弥生', '卯月', '皐月', '水無月', '文月', '葉月', '長月', '神無月', '霜月', '師走')
    pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.setFont('BIZUDGothicR', 30)
    pdf.drawCentredString(x+block_w/2, block_h/2+2*mm, str(m))
    pdf.setFont('BIZUDGothicR', 12)
    pdf.drawCentredString(x+block_w/2, 21*mm, month_str[m-1])
    pdf.setFont('BIZUDGothicR', 8)
    pdf.drawCentredString(x+block_w/2, 25*mm, monthjp_str[m-1])
    pdf.setFont('BIZUDGothicR', 12)
    pdf.drawCentredString(x+block_w/2, 30*mm, str(y))

def DrawWeekDay(pdf, w, h, wd):
    weekday_str = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    # pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    # pdf.setLineWidth(0.1)
    # pdf.line(w, h+weekday_h, w+block_w, h+weekday_h) # 下辺
    # if wd != 2 and wd != 6:
    #     pdf.line(w+block_w, h, w+block_w, h+weekday_h) # 右辺
    # if wd != 3:
    #     pdf.line(w, h, w, h+weekday_h) # 左辺
    if wd == 6:
        pdf.setFillColorRGB(1, 0.5, 0.5)
    elif wd == 5:
        pdf.setFillColorRGB(0.5, 0.5, 1)
    else:
        pdf.setFillColorRGB(0.6, 0.6, 0.6)
    pdf.setFont('BIZUDGothicR', 8)
    pdf.drawCentredString(w+block_w/2, h+weekday_h-1*mm, weekday_str[wd])

def DrawDay(pdf, w, h, y, m, d, wd):
    # pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    # pdf.setLineWidth(0.1)
    if d != 0:
        # if wd != 2 and wd != 6:
        #     pdf.line(w+block_w, h, w+block_w, h+block_h) # 右辺
        # if wd != 3:
        #     pdf.line(w, h, w, h+block_h) # 左辺
        # pdf.lines([
        #     (w, h+block_h, w+block_w, h+block_h), # 下辺
        #     (w, h, w+block_w, h), # 上辺
        #     ])
        if jpholiday.is_holiday(datetime.date(y, m, d)) == True:
            pdf.setFillColorRGB(1, 0.5, 0.5)
            pdf.setFont('BIZUDGothicR', 4)
            pdf.drawString(w+0.8*mm, block_h+h-1*mm, jpholiday.is_holiday_name(datetime.date(y, m, d)))
        elif wd == 6:
            pdf.setFillColorRGB(1, 0.5, 0.5)
        elif wd == 5:
            pdf.setFillColorRGB(0.5, 0.5, 1)
        else:
            pdf.setFillColorRGB(0.6, 0.6, 0.6)
        pdf.setFont('BIZUDGothicR', 10)
        pdf.drawString(w+0.5*mm, h+3.5*mm, str(d))

def main():
    y = year
    # フォーマット定義
    pdf = canvas.Canvas(FILENAME, bottomup=False)
    pdf.setPageSize((size_w, size_h))

    # P1:年間カレンダー
    DrawYearCalendar(pdf, y)
    DrawPageFinder(pdf, False)
    pdf.showPage() # 改ページ

    for midx in range(1, 16): # 1月～来年3月
        m = (midx-1)%12+1
        # データの取得
        cal_list = calendar.monthcalendar(y, m)

        ## 偶数ページ

        # 左端の余白を設定
        x = size_w-block_w*4-ringhole

        # 月の見出し
        DrawYearMonth(pdf, x, y, m)

        # ミニカレンダー
        prevy = y
        prevm = m-1
        nexty = y
        nextm = m+1
        if m == 1:
            prevy = y-1
            prevm = 12
        elif m == 12:
            nexty = y+1
            nextm = 1
        DrawMiniCalendar(pdf, x+1*mm, size_h-42*mm, 2.7*mm, 2*mm, 5, prevy, prevm)
        DrawMiniCalendar(pdf, x+1*mm, size_h-24*mm, 2.7*mm, 2*mm, 5, nexty, nextm)

        # 罫線描画
        pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
        pdf.setLineWidth(0.1)
        for i in range(0, 3):
            pdf.line(block_w*(i+1)+x, 0, block_w*(i+1)+x, size_h) # 縦の線
        for i in range(0, 6):
            pdf.line(block_w+x, weekday_h+i*block_h, size_w-ringhole, weekday_h+i*block_h) # 横の線
            
        # 月～水
        for wd in range(0, 3):
            DrawWeekDay(pdf, block_w*(wd+1)+x, 0, wd)
        for w in range(0, len(cal_list)):
            for wd in range(0, 3):
                DrawDay(pdf, block_w*(wd+1)+x, weekday_h+block_h*w, y, m, cal_list[w][wd], wd)
        DrawPageFinder(pdf, True)
        pdf.showPage() # 改ページ

        ## 奇数ページ

        # 罫線描画
        pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
        pdf.setLineWidth(0.1)
        for i in range(0, 3):
            pdf.line(block_w*(i+1)+ringhole, 0, block_w*(i+1)+ringhole, size_h-block_h) # 縦の線
        for i in range(0, 6):
            pdf.line(ringhole, weekday_h+i*block_h, size_w, weekday_h+i*block_h) # 横の線
        
        # 木～日
        for wd in range(3, 7):
            DrawWeekDay(pdf, block_w*(wd-3)+ringhole, 0, wd)
        for w in range(0, len(cal_list)):
            for wd in range(3, 7):
                DrawDay(pdf, block_w*(wd-3)+ringhole, weekday_h+block_h*w, y, m, cal_list[w][wd], wd)
        DrawPageFinder(pdf, False)
        pdf.showPage() # 改ページ

        if m == 12:
            y = y+1

    # 最終ページ:年齢早見表
    # DrawAgeChart(pdf, year)
    # DrawPageFinder(pdf, True)
    # pdf.showPage()

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()