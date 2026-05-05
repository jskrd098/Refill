from os import truncate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
# from reportlab.lib.pagesizes import A4, portrait # A4縦(portrait:縦方向)
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color
import textwrap
import calendar
import datetime
import jpholiday

FILENAME = 'bible_weekly_left.pdf' # ファイル名
# year = 2023 # 出力したい年 <- main関数内で値を指定する

# 用紙サイズ
sizeW = 95*mm
sizeH = 170*mm

# フォント登録
BIZUDGothicR = "G:/マイドライブ/Python/refill/fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

# 余白
margin = 4*mm
ringhole = 11*mm

# 日付ブロックのサイズ
indexH = 9*mm # 見出し
blockH = (sizeH - margin * 2 - indexH) / 7 # 日毎のブロックの高さ

# ミニカレンダーのサイズと間隔
miniCalSizeW = 20*mm # 全体の幅
miniCalSizeH = 15*mm # 全体の高さ
miniCalDisX = 2.7*mm # 水平方向の文字間隔
miniCalDisY = 2*mm # 垂直方向の文字間隔
miniCalFontSize = 5 # 文字の大きさ

# カレンダーデータを取得する
def GetCalendarData(year):
    buf = calendar.monthcalendar(year-1, 12) # 前年12月
    for m in range(1, 13):
        buf += calendar.monthcalendar(year, m) # 当年1～12月
    buf += calendar.monthcalendar(year+1, 1) # 翌年1月
    
    # データの加工 [29, 30, 31, 0, 0, 0, 0], [0, 0, 0, 1, 2, 3, 4]
    #          -> [29, 30, 31, 1, 2, 3, 4] にする
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

# ページの隅に切り取り線を出力する
def DrawPageFinder(pdf, leftcut):
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    pdf.setDash([2, 2])
    cutpos = 15*mm
    if leftcut == True:
        pdf.line(cutpos, sizeH, 0, sizeH-cutpos)
    else:
        pdf.line(sizeW-cutpos, sizeH, sizeW, sizeH-cutpos)

# 指定の箇所にミニカレンダーを出力する
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
                    pdf.setFillColor(color.gray) # 平日は灰色に
                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(x+j*dis_x, y, wdstsr[j])
                # 日の記載
                if jpholiday.is_holiday(datetime.date(year, month, cal_list[i][j])) == True:
                    pdf.setFillColorRGB(1, 0.5, 0.5)
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(x+j*dis_x, y+(i+1)*dis_y+0.5*mm, str(cal_list[i][j]))

# 見出しを出力する
def DrawWeeklyLeftIndex(pdf, x, y, year, month, changeYear, changeMonth, LeftPage):

    monthStrEn = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    monthStrJp = ('睦月', '如月', '弥生', '卯月', '皐月', '水無月', '文月', '葉月', '長月', '神無月', '霜月', '師走')
    pdf.setFillColor(color.gray) # 文字色を灰色に

    # 偶数ページ(左ページ)
    if month == 0:
        month = 12

    if LeftPage == True:
        
        if changeMonth == True: # 月跨ぎの場合
            pdf.setFont('BIZUDGothicR', 26)
            pdf.drawString(x, y + 7*mm, str(month) + '/' + str(month % 12 + 1)) # 月(数字)の出力

            pdf.setFont('BIZUDGothicR', 10)
            pdf.drawString(x + 24*mm, y + 3*mm, monthStrEn[month - 1] + '/' + monthStrEn[month % 12]) # 月(英語)の出力
            pdf.drawString(x + 24*mm, y + 7*mm, monthStrJp[month - 1] + '/' + monthStrJp[month % 12]) # 月(和暦)の出力

        else:
            pdf.setFont('BIZUDGothicR', 26)
            pdf.drawString(x, y + 7*mm, str(month % 12 + 1)) # 月(数字)の出力

            pdf.setFont('BIZUDGothicR', 10)
            pdf.drawString(x + 10*mm, y + 3*mm, monthStrEn[month % 12]) # 月(英語)の出力
            pdf.drawString(x + 10*mm, y + 7*mm, monthStrJp[month % 12]) # 月(和暦)の出力

    # 奇数ページ(右ページ)
    else:
        pdf.setFont('BIZUDGothicR', 10)

        # 年の出力
        if changeYear == True: # 年跨ぎの場合
            pdf.drawRightString(x - ringhole + sizeW - margin, y + indexH - 2 * mm, str(year - 1) + '/' + str(year))
        else:
            pdf.drawRightString(x - ringhole + sizeW - margin, y + indexH - 2 * mm, str(year))

        # 罫線の出力
        pdf.setStrokeColor(color.gray)
        pdf.setLineWidth(0.1)
        pdf.line(0, margin+indexH, sizeW, margin+indexH)

# 日付ブロックを出力する
def DrawDayLeft(pdf, x, y, year, month, day, weekday):
    weekday_str = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    # 罫線の出力
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    pdf.line(0, y, sizeW, y)
    pdf.line(35*mm, y, 35*mm, y+1*mm)
    pdf.line(60*mm, y, 60*mm, y+1*mm)
    if (weekday != 6):
        pdf.line(35*mm, y+blockH, 35*mm, y+blockH-1*mm)
        pdf.line(60*mm, y+blockH, 60*mm, y+blockH-1*mm)

    # 日付・曜日の表示
    #   文字色の設定
    if jpholiday.is_holiday(datetime.date(year, month, day)) == True: # 祝日の場合
        pdf.setFillColorRGB(1, 0.5, 0.5) # 文字色を赤色に
        pdf.setFont('BIZUDGothicR', 4)
        pdf.drawString(x + 1*mm, y + 10*mm, jpholiday.is_holiday_name(datetime.date(year, month, day))) # 祝日の名前(何の日か)を出力する
    elif weekday == 6: # 日曜日の場合
        pdf.setFillColorRGB(1, 0.5, 0.5) # 文字色を赤色に
    elif weekday == 5: # 土曜日の場合
        pdf.setFillColorRGB(0.5, 0.5, 1) # 文字色を青色に
    else:
        pdf.setFillColor(color.gray) # 文字色を灰色に

    #   日付の出力
    pdf.setFont('BIZUDGothicR', 12)
    pdf.drawString(x + 1*mm, y + 5*mm, str(day))

    #   曜日の出力
    pdf.setFont('BIZUDGothicR', 8)
    pdf.drawString(x + 1*mm, y + 8*mm, weekday_str[weekday])

# 1年分のレフト式週間カレンダーを出力する
def DrawWeeklyLeft(pdf, year):
    cal_list = GetCalendarData(year)
    year -= 1
    month = 12
    changeYear = False
    changeMonth = False

    # 1年間の週の数 
    #   4=前年１２月最終週
    #   len(cal_list)-5=翌年1月初週
    #   len(cal_list)=前年12月初週～翌年1月最終週
    for w in range(4, len(cal_list)-5):
        
        # 年跨ぎまたは月跨ぎの週であるかを判定
        if 1 in cal_list[w][1:7]: # 火～日曜日のどこかで月を跨ぐ場合
            changeMonth = True
            if month == 12: # 更に年を跨ぐ場合
                changeYear = True
            else:
                changeYear = False
        else: # 月曜日が1日または月跨ぎではない場合
            changeYear = False
            changeMonth = False

        # 偶数ページ(左ページ)

        #   日付ブロックを表示
        x = margin
        y = margin + indexH
        for d in range(0, 7):
            day = cal_list[w][d]
            if day == 1:
                if month == 12:
                    year += 1
                month = month % 12 + 1
            DrawDayLeft(pdf, x, y, year, month, day, d)
            y += blockH

        #   見出しを表示(月の値を計算する関係上、日付ブロックの後に見出しを出力する)
        y = margin
        DrawWeeklyLeftIndex(pdf, x, y, year, month - 1, changeYear, changeMonth, True)

        #   改ページ処理
        DrawPageFinder(pdf, True)
        pdf.showPage()

        # 奇数ページ(右ページ)

        #   見出しを表示
        x = ringhole
        y = margin
        DrawWeeklyLeftIndex(pdf, x, y, year, month, changeYear, changeMonth, False)

        #   左下隅にミニカレンダーを表示(横並びに2ヶ月分)
        x = ringhole
        y = sizeH - margin - miniCalSizeH
        if changeMonth == True:
            if month == 1:
                DrawMiniCalendar(pdf, x, y, miniCalDisX, miniCalDisY, miniCalFontSize, year - 1, 12)
                DrawMiniCalendar(pdf, x + miniCalSizeW, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, 1)
            else:
                DrawMiniCalendar(pdf, x, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, month - 1)
                DrawMiniCalendar(pdf, x + miniCalSizeW, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, month)
        elif month == 12:
            DrawMiniCalendar(pdf, x, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, month)
            DrawMiniCalendar(pdf, x + miniCalSizeW, y, miniCalDisX, miniCalDisY, miniCalFontSize, year + 1, month % 12 + 1)
        else:
            DrawMiniCalendar(pdf, x, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, month)
            DrawMiniCalendar(pdf, x + miniCalSizeW, y, miniCalDisX, miniCalDisY, miniCalFontSize, year, month % 12 + 1)

        #   改ページ処理
        DrawPageFinder(pdf, False)
        pdf.showPage()

def main():

    # 出力する年を指定
    year = 2023

    # フォーマット定義
    pdf = canvas.Canvas(FILENAME, bottomup=False) # ページ左上を原点とする
    pdf.setPageSize((sizeW, sizeH))
    
    # P1は白紙とする
    DrawPageFinder(pdf, False)
    pdf.showPage() # 改ページ

    # P2から内容を表示する
    # DrawWeeklyVertical(pdf, year)
    DrawWeeklyLeft(pdf, year)

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()