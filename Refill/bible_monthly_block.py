from reportlab.lib.units import mm
import calendar
import datetime
import jpholiday
from bible_GlobalParam import size_w, size_h, margin, ringhole, monthStr, monthStrJP, weekdayStr, weekdayStrJP

# 変数定義と初期化
title_h = 10 # タイトル部分の高さ
weekdayIdx = 5 # 曜日表示部分の高さ
block_w = 20 # ブロックの幅
block_h = 0 # ブロックの高さ(その月の週の数によって異なる)

# 罫線の描画
def DrawMonthlyBlockLine(pdf, pg, cal_list):

    # canvas状態を一時保存
    pdf.saveState()

    block_h = (size_h - margin*2 - title_h - weekdayIdx)/len(cal_list) # ブロックの高さ(その月の週の数によって異なる)

    # 線の色と太さの設定
    pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    pdf.setLineWidth(0.1)
    
    # 垂直
    if pg == 0:
        x1 = margin*mm
    else:
        x1 = ringhole*mm 
    x2 = x1
    y1 = (margin + title_h)*mm
    y2 = (size_h - margin)*mm
    for i in range(0, 3):
        x1 = x1 + 20*mm
        x2 = x1
        pdf.line(x1, y1, x2, y2)

    # 水平
    ## 曜日表示部分
    if pg == 0:
        x1 = margin*mm
        x2 = (size_w - ringhole)*mm
    else:
        x1 = ringhole*mm
        x2 = (size_w - margin - block_w)*mm
    y1 = (title_h + margin)*mm
    y2 = y1
    pdf.line(x1, y1, x2, y2)
    y1 = y1 + weekdayIdx*mm
    y2 = y1
    pdf.line(x1, y1, x2, y2)

    ## カレンダー本体部分
    if pg == 0:
        x2 = (size_w - ringhole)*mm
    else:
        x2 = (size_w - margin - block_w)*mm
    for i in range(1, len(cal_list)):
        y1 = y1 + block_h*mm
        y2 = y1
        pdf.line(x1, y1, x2, y2)

    # canvas状態をレストア
    pdf.restoreState()

# 月の記載
def DrawMonthlyBlockMonth(pdf, pg, year, month):

    if pg == 1: return # 右ページの場合は何もしない

    pdf.setFillColorRGB(0.6, 0.6, 0.6)

    # 月(数字)の記載
    x = (margin + title_h / 2)*mm
    y = (margin + title_h / 2 + 3)*mm
    pdf.setFont('BIZUDGothicR', 26)
    pdf.drawCentredString(x, y, str(month))

    # 月(EN/JP)の記載
    pdf.setFont('BIZUDGothicR', 10)
    x = x + 6*mm
    pdf.drawString(x, y, monthStr[month - 1] + ' ' + monthStrJP[month - 1])

    # 年の記載
    y = y - 4.5*mm
    pdf.drawString(x, y, str(year) + ' 令和' + str(year - 2018) + '年')

# 曜日の記載
def DrawMonthlyBlockWeekday(pdf, pg):
    # canvas状態を一時保存
    pdf.saveState()


    for i in range(0, 7):

        # 文字色の設定
        if i == 6: # 日曜日の場合
            pdf.setFillColorRGB(1, 0.5, 0.5)
        elif i == 5: # 土曜日の場合
            pdf.setFillColorRGB(0.5, 0.5, 1)
        else:
            pdf.setFillColorRGB(0.6, 0.6, 0.6)

        if (pg == 0 and i < 4) or (pg == 1 and i >= 4):

            # 英語表記
            pdf.setFont('BIZUDGothicR', 7)
            if pg == 0 and i < 4:
                x = (margin + block_w*(i + 1) - 0.5)*mm
            elif pg == 1 and i >= 4:
                x = (ringhole + block_w*(i - 3) - 0.5)*mm
            y = (margin + title_h + weekdayIdx - 1)*mm
            pdf.drawRightString(x, y, weekdayStr[i])

            # 漢字表記
            pdf.setFont('BIZUDGothicR', 10)
            if pg == 0 and i < 4:
                x = (margin + block_w*i + 2)*mm
            elif pg == 1 and i >= 4:
                x = (ringhole + block_w*(i - 4) + 2)*mm
            pdf.drawCentredString(x, y, weekdayStrJP[i])

    # canvas状態をレストア
    pdf.restoreState()

# 日付の記載
def DrawMonthlyBlockChar(pdf, pg, year, month, cal_list, cal_list_prev, cal_list_next):

    # canvas状態を一時保存
    pdf.saveState()

    block_h = (size_h - margin*2 - title_h - weekdayIdx)/len(cal_list) # ブロックの高さ(その月の週の数によって異なる)

    # カレンダーデータの前月、翌月の連結
    for i in range(0, 7):
        if cal_list[0][i] == 0:
            cal_list[0][i] = cal_list[0][i] + cal_list_prev[len(cal_list_prev)-1][i]
        if cal_list[len(cal_list)-1][i] == 0:
            cal_list[len(cal_list)-1][i] = cal_list[len(cal_list)-1][i] + cal_list_next[0][i]
    
    ## フォントの設定
    pdf.setFont('BIZUDGothicR', 10)

    ## 年月の値の取得
    nowMonth = month - 1
    nowYear = year
    if nowMonth == 0:
        nowMonth = 12
        nowYear -= 1

    ## 各日付の記載
    for i in range(0, len(cal_list)):
        for j in range(0, 7):

            ### 月を跨いだとき、月の値を更新
            if cal_list[i][j] == 1:
                nowMonth += 1

                ### 年を跨いだとき、年と月の値を更新
                if nowMonth == 13:
                    nowMonth = 1
                    nowYear += 1

            ### 文字色の設定
            if j == 6 or jpholiday.is_holiday(datetime.date(nowYear, nowMonth, cal_list[i][j])): # 日曜日・祝日の場合
                pdf.setFillColorRGB(1, 0.5, 0.5, 1)
                if nowMonth != month:
                    pdf.setFillColorRGB(1, 0.5, 0.5, 0.5)
            elif j == 5: # 土曜日の場合
                pdf.setFillColorRGB(0.5, 0.5, 1, 1)
                if nowMonth != month:
                    pdf.setFillColorRGB(0.5, 0.5, 1, 0.5)
            else:
                pdf.setFillColorRGB(0.6, 0.6, 0.6, 1)
                if nowMonth != month:
                    pdf.setFillColorRGB(0.6, 0.6, 0.6, 0.5)

            ### 記載位置の設定
            y = (margin + title_h + weekdayIdx + 4)*mm 
            if pg == 0 and j < 4:
                x = (margin + block_w*j + 2)*mm
            elif pg == 1 and j >= 4:
                x = (ringhole + block_w*(j - 4) + 2)*mm
            if (pg == 0 and j < 4) or (pg == 1 and j >= 4):
                y = y + block_h*i*mm

                ### 記載
                pdf.drawCentredString(x, y, str(cal_list[i][j]))

                ### 祝日名の記載
                x = x + (block_w - 2.5)*mm
                y = y - 2*mm
                if (jpholiday.is_holiday(datetime.date(nowYear, nowMonth, cal_list[i][j])) == True):
                    pdf.setFont('BIZUDGothicR', 4) # 一時的に文字サイズを変更
                    pdf.drawRightString(x, y, jpholiday.is_holiday_name(datetime.date(nowYear, nowMonth, cal_list[i][j])))
                    pdf.setFont('BIZUDGothicR', 10) # 元に戻す

    # canvas状態をレストア
    pdf.restoreState()

# 月間ブロックページ作成
def DrawMonthlyBlock(pdf, year, month):

    # 左右ページでそれぞれ1回ずつ実行
    for pg in range(0, 2):

        # カレンダーデータの取得
        ## 前月
        if month == 1:
            cal_list_prev = calendar.monthcalendar(year - 1, 12)
        else:
            cal_list_prev = calendar.monthcalendar(year, month - 1)
        ## 当月
        cal_list = calendar.monthcalendar(year, month)
        ## 翌月
        if month == 12:
            cal_list_next = calendar.monthcalendar(year + 1, 1)
        else:
            cal_list_next = calendar.monthcalendar(year, month + 1)

        # 罫線の描画
        DrawMonthlyBlockLine(pdf, pg, cal_list)

        # 月の記載
        DrawMonthlyBlockMonth(pdf, pg, year, month)

        # 曜日の記載
        DrawMonthlyBlockWeekday(pdf, pg)

        # 日付の記載
        DrawMonthlyBlockChar(pdf, pg, year, month, cal_list, cal_list_prev, cal_list_next)

        # ページ更新
        pdf.showPage()