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
bible_w = 95*mm
bible_h = 170*mm
bible_x = A4_w/2 - bible_w/2
bible_y = A4_h/2 - bible_h/2

# ファイル名
FILENAME = 'monthly_bible.pdf'

# フォーマット定義
pdf = canvas.Canvas(FILENAME, pagesize=portrait(A4), bottomup=False)

# フォント登録
BIZUDGothicR = "./fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))
font_size = 14

# ページ数
pagenum = 26

# 余白
margin = 2*mm
ringhole = 11*mm

# 月間ブロックのサイズ
block_w = 21*mm
block_h = 27*mm

# 曜日ブロックの高さ
weekday_h = 8*mm

# その他変数
year_num = 2021 # 出力したい年を設定
month_str = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
weekday_str = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
weekdayShort_str = ('M', 'T', 'W', 'T', 'F', 'S', 'S') # 曜日表記
eto = {0:'申', 1:'酉', 2:'戌', 3:'亥', 4:'子', 5:'丑', 6:'寅', 7:'卯', 8:'辰', 9:'巳', 10:'午', 11:'未'}
gengou = {0:'大正', 1:'昭和', 2:'平成', 3:'令和'}

def AgeChartOutput(x, y, seireki, gengou_str, wareki, age, eto_str):
    pdf.setFillColor(color.gray)
    pdf.drawCentredString(x, y, seireki)
    pdf.drawCentredString(x+7.5*mm, y, gengou_str + wareki)
    pdf.drawCentredString(x+14*mm, y, age)
    pdf.drawCentredString(x+20*mm, y, eto_str)

def MiniCalendar(pos_x, pos_y, dis_x, dis_y, fontsize, year_num, month_num):
    calendar_list = calendar.monthcalendar(year_num, month_num)
    for i in range(0, len(calendar_list)): # 週
        for j in range(0, len(calendar_list[i])): # 日
            if calendar_list[i][j] != 0:
                if j == 5: # 土曜日を青文字に
                    pdf.setFillColor(color.fidblue)
                elif j == 6: # 日曜日・祝日を赤文字に
                    pdf.setFillColor(color.fidred)
                else: # 平日は黒文字に
                    pdf.setFillColor(color.gray)
                # 曜日の記載
                pdf.setFont('BIZUDGothicR', fontsize-2)
                pdf.drawCentredString(pos_x+j*dis_x, pos_y, weekdayShort_str[j])
                if jpholiday.is_holiday(datetime.date(year_num, month_num, calendar_list[i][j])) == True:
                    pdf.setFillColor(color.fidred)
                # 日の記載
                pdf.setFont('BIZUDGothicR', fontsize)
                pdf.drawCentredString(pos_x+j*dis_x, pos_y+(i+1)*dis_y+0.5*mm, str(calendar_list[i][j]))

def PageFinder(pdf, leftcut):
    pdf.setStrokeColor(color.gray)
    pdf.setDash([2,2])
    if leftcut == True:
        pdf.lines([
            (bible_x+10*mm, bible_y+bible_h, bible_x, bible_y+bible_h-10*mm),
            (bible_x+10*mm, bible_y, bible_x, bible_y+10*mm)
        ])
    else:
        pdf.lines([
            (bible_x+bible_w-10*mm, bible_y+bible_h, bible_x+bible_w, bible_y+bible_h-10*mm),
            (bible_x+bible_w-10*mm, bible_y, bible_x+bible_w, bible_y+10*mm)
        ])

def CutLine(pdf):
    pdf.setStrokeColor(color.gray)
    pdf.setDash([2,2])
    pdf.lines([
        (0, bible_y, A4_w, bible_y),
        (0, bible_y+bible_h, A4_w, bible_y+bible_h),
        (bible_x, 0, bible_x, A4_h),
        (bible_x+bible_w, 0, bible_x+bible_w, A4_h)
    ])

def main():
    month_cnt = 1 # ページ数に応じた月の値を表示

    ## 各ページ記載内容
    for page in range(1, pagenum+1):

        # 月間ブロック h=27mm, w=21mm
        pdf.setStrokeColor(color.gray)
        pdf.setLineWidth(0.1)

        if page == 1: # 表紙

            ## 年間カレンダー
            # 年の記載
            pdf.setFillColor(color.grey)
            pdf.setFont('BIZUDGothicR', 20)
            pdf.drawCentredString(
                bible_x+(ringhole+bible_w)/2-1*mm,
                bible_y+18*mm,
                str(year_num)
            )
            pdf.setFont('BIZUDGothicR', 8)

            for month_num in range(0, 12): # 各月毎の処理    
                # 年間カレンダーの文字列を取得
                calendar_list = calendar.monthcalendar(year_num, month_num+1) 
                # 月の記載
                pdf.setFillColor(color.lightgrey)
                pdf.setFont('BIZUDGothicR', 40)
                pdf.drawCentredString(
                    bible_x+ringhole+2*mm+month_num%3*28*mm+11*mm,
                    bible_y+bible_h*0.25+month_num//3*32*mm+12*mm,
                    str(month_num+1)
                )
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 6)
                pdf.drawCentredString(
                    bible_x+ringhole+13*mm+month_num%3*28*mm,
                    bible_y+bible_h*0.25+month_num//3*32*mm-4*mm,
                    month_str[month_num]
                )
                # 日、曜日の記載
                for i in range(0, len(calendar_list)): # 週
                    for j in range(0, len(calendar_list[i])): # 日
                        if calendar_list[i][j] != 0:
                            if j == 5: # 土曜日を青文字に
                                pdf.setFillColor(color.fidblue)
                            elif j == 6 or jpholiday.is_holiday(datetime.date(year_num, month_num+1, calendar_list[i][j])) == True: # 日曜日・祝日を赤文字に
                                pdf.setFillColor(color.fidred)
                            else: # 平日は黒文字に
                                pdf.setFillColor(color.gray)
                            # 曜日の記載
                            if month_num < 3:
                                pdf.setFont('BIZUDGothicR', 5)
                                pdf.drawCentredString(
                                    bible_x+ringhole+2*mm+month_num%3*28*mm+j*3.6*mm,
                                    bible_y+bible_h*0.2,
                                    weekdayShort_str[j]
                                )
                            # 日の記載
                            pdf.setFont('BIZUDGothicR', 8)
                            pdf.drawCentredString(
                                bible_x+ringhole+2*mm+month_num%3*28*mm+j*3.6*mm,
                                bible_y+bible_h*0.25+month_num//3*32*mm+i*3.5*mm,
                                str(calendar_list[i][j])
                            )
                            
            # ページファインダー切り取り線
            PageFinder(pdf, False)

        elif page == pagenum: # 最終ページ
            ## 年齢早見表

            # 表の中身
            column_w = (bible_w-ringhole)/3 # 列の幅
            line_h = 3.5*mm # 行の高さ
            table_x = bible_x + 2*mm # 表の原点x座標
            table_y = bible_y + 11*mm # 表の原点y座標
            table_h = table_y + 122.5*mm # 表の高さ

            datanum = 101 # 出力するデータの個数
            seireki = 0 # 西暦
            wareki = 0 # 和暦
            wareki_idx = 1912 # 元号が変更された年
            age = 0 # 年齢
            gengou_idx = 0 # 元号(インデックス番号)
            
            # 罫線
            pdf.lines([
                (table_x+(bible_w-ringhole)/3-1*mm, table_y-3*mm, table_x+(bible_w-ringhole)/3-1*mm, table_h+1*mm),
                (table_x+(bible_w-ringhole)*2/3-1*mm, table_y-3*mm, table_x+(bible_w-ringhole)*2/3-1*mm, table_h+1*mm),
                (table_x,table_y+1*mm, table_x+bible_w-ringhole, table_y+1*mm)
            ])

            # 表のタイトル
            pdf.setFillColor(color.gray)
            pdf.setFont('BIZUDGothicR', 10)
            pdf.drawCentredString(bible_x+bible_w/2-4*mm, bible_y+7*mm, 'AGE CHART')

            # フォントの設定
            pdf.setFont('BIZUDGothicR', 7)

            # 表の見出し
            for i in range(0, 3):
                data_x = bible_x+(bible_w-ringhole)/24+i*column_w+2*mm
                data_y = table_y
                AgeChartOutput(data_x, data_y, '西暦', '', '和暦', '年齢', '干支')
            
            # 表の初期出力位置
            data_x = table_x+(bible_w-ringhole)/24
            data_y = table_y+line_h
            
            # データの計算、位置決め、出力
            for y in range(0, datanum+1):
                # データの計算
                seireki = year_num - datanum + y
                age = datanum - y
                wareki = seireki - wareki_idx + 1
                # 改行
                if y == 34 or y == 69:
                    data_x += column_w
                    data_y = table_y+line_h
                # データ出力
                if y == 0:
                    # 1行目だけ強制的に元号を表示する
                    AgeChartOutput(data_x, data_y, str(seireki), gengou[gengou_idx], str(wareki), str(age), str(eto[seireki%12]))
                else:
                    AgeChartOutput(data_x, data_y, str(seireki), '', str(wareki), str(age), str(eto[seireki%12]))
                data_y += line_h
                if seireki == 1926 or seireki == 1989 or seireki == 2019:
                    wareki_idx = seireki
                    wareki = 1
                    gengou_idx += 1
                    AgeChartOutput(data_x, data_y, str(seireki), gengou[gengou_idx], '元', str(age), str(eto[seireki%12]))
                    data_y += line_h

            # メモ欄
            pdf.drawString(table_x, table_h+5*mm, "Notes:")

            # ページファインダー切り取り線
            PageFinder(pdf, True)

        elif page % 2 == 1: # 奇数ページ
            ## 月間カレンダー
            
            # 罫線(横方向)
            for i in range(0, 6):
                pdf.line(
                        bible_x+ringhole, bible_y+weekday_h+block_h*i,
                        bible_x+bible_w-margin, bible_y+weekday_h+block_h*i
                    )
            
            # 罫線(縦方向)
            for i in range(0, 3):
                pdf.line(
                        bible_x+ringhole+block_w*(i+1), bible_y+margin, 
                        bible_x+ringhole+block_w*(i+1), bible_y+bible_h-block_h
                    )
            
            # 曜日
            pdf.setFont('BIZUDGothicR', 8)
            for i in range(3, len(weekday_str)):
                if i == 5:
                    pdf.setFillColor(color.fidblue)
                elif i == 6:
                    pdf.setFillColor(color.fidred)
                else:
                    pdf.setFillColor(color.gray)
                pdf.drawCentredString(
                    bible_x+ringhole+block_w*(i-2.5), bible_y+weekday_h-1*mm, weekday_str[i]
                )
            
            # 日付
            calendar_list = calendar.monthcalendar(year_num, month_cnt)
            for i in range(0, len(calendar_list)): # 週
                for j in range(3, len(calendar_list[i])): # 日
                    if calendar_list[i][j] != 0:
                        # 日の記載
                        if j == 5: # 土曜日を青文字に
                            pdf.setFillColor(color.fidblue)
                        elif j == 6: # 日曜日を赤文字に
                            pdf.setFillColor(color.fidred)
                        elif jpholiday.is_holiday(datetime.date(year_num, month_cnt, calendar_list[i][j])) == True: # 祝日を赤文字にして祝日名を表示する
                            pdf.setFillColor(color.fidred)
                            pdf.setFont('BIZUDGothicR', 4)
                            pdf.drawString(
                                bible_x+ringhole+(j-3)*block_w+0.8*mm,
                                bible_y+weekday_h+(i+1)*block_h-1*mm,
                                jpholiday.is_holiday_name(datetime.date(year_num, month_cnt, calendar_list[i][j]))
                            )
                        else: # 平日は黒文字に
                            pdf.setFillColor(color.gray)
                        pdf.setFont('BIZUDGothicR', 10)
                        pdf.drawString(
                            bible_x+ringhole+(j-3)*block_w+0.5*mm,
                            bible_y+weekday_h+i*block_h+3.5*mm,
                            str(calendar_list[i][j])
                        )

            # 右下に翌月のミニカレンダーを表示
            if month_cnt+1 > 12:
                MiniCalendar(bible_x+bible_w-block_w+2*mm, bible_y+bible_h-20.5*mm, 2.8*mm, 2*mm, 5, year_num+1, 1)
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 10)
                pdf.drawString(bible_x+bible_w-block_w+1*mm, bible_y+bible_h-23*mm, '1')
                pdf.setFont('BIZUDGothicR', 5)
                pdf.drawString(bible_x+bible_w-block_w+3*mm, bible_y+bible_h-23*mm, str(year_num+1))
            else:
                MiniCalendar(bible_x+bible_w-block_w+2*mm, bible_y+bible_h-20.5*mm, 2.8*mm, 2*mm, 5, year_num, month_cnt+1)
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 10)
                pdf.drawString(bible_x+bible_w-block_w+1*mm, bible_y+bible_h-23*mm, str(month_cnt+1))
            
            # 右下に前月のミニカレンダーを表示
            if month_cnt-1 < 1:
                MiniCalendar(bible_x+bible_w-block_w*2+2*mm, bible_y+bible_h-20.5*mm, 2.8*mm, 2*mm, 5, year_num-1, 12)
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 10)
                pdf.drawString(bible_x+bible_w-block_w*2+1*mm, bible_y+bible_h-23*mm, '12')
                pdf.setFont('BIZUDGothicR', 5)
                pdf.drawString(bible_x+bible_w-block_w*2+5*mm, bible_y+bible_h-23*mm, str(year_num-1))
            else:
                MiniCalendar(bible_x+bible_w-block_w*2+2*mm, bible_y+bible_h-20.5*mm, 2.8*mm, 2*mm, 5, year_num, month_cnt-1)
                pdf.setFillColor(color.gray)
                pdf.setFont('BIZUDGothicR', 10)
                pdf.drawString(bible_x+bible_w-block_w*2+1*mm, bible_y+bible_h-23*mm, str(month_cnt-1))

            month_cnt += 1

            # ページファインダー切り取り線
            PageFinder(pdf, False)

        else: # 偶数ページ
            ## 月間カレンダー

            # 年月(見出し)の表示
            pdf.setFillColor(color.gray)
            pdf.setFont('BIZUDGothicR', 30)
            pdf.drawCentredString(bible_x+block_w/2, bible_y+block_h/2, str(month_cnt))
            pdf.setFont('BIZUDGothicR', 12)
            pdf.drawCentredString(bible_x+block_w/2, bible_y+20*mm, month_str[month_cnt-1])
            pdf.drawCentredString(bible_x+block_w/2, bible_y+25*mm, str(year_num))

            # 罫線(横方向)
            for i in range(0, 6):
                pdf.line(
                        bible_x+block_w, bible_y+weekday_h+block_h*i,
                        bible_x+bible_w-ringhole, bible_y+weekday_h+block_h*i
                    )

            # 罫線(縦方向)
            for i in range(0, 3):
                pdf.line(
                        bible_x+block_w*(i+1), bible_y+margin,
                        bible_x+block_w*(i+1), bible_y+bible_h-margin
                    )
            
            # 曜日
            pdf.setFillColor(color.gray)
            pdf.setFont('BIZUDGothicR', 8)
            for i in range(0, len(weekday_str)-4):
                pdf.drawCentredString(
                    bible_x+block_w*(i+1.5), bible_y+weekday_h-1*mm,
                    weekday_str[i]
                )
            
            # 日付
            calendar_list = calendar.monthcalendar(year_num, month_cnt)
            for i in range(0, len(calendar_list)): # 週
                for j in range(0, len(calendar_list[i])-4): # 日
                    if calendar_list[i][j] != 0:
                        # 日の記載
                        if j == 6: # 日曜日を赤文字に
                            pdf.setFillColor(color.fidred)
                        elif jpholiday.is_holiday(datetime.date(year_num, month_cnt, calendar_list[i][j])) == True: # 祝日を赤文字にして祝日名を表示する
                            pdf.setFillColor(color.fidred)
                            pdf.setFont('BIZUDGothicR', 4)
                            pdf.drawString(
                                bible_x+(j+1)*block_w+0.8*mm,
                                bible_y+weekday_h+(i+1)*block_h-1*mm,
                                jpholiday.is_holiday_name(datetime.date(year_num, month_cnt, calendar_list[i][j]))
                            )
                        else: # 平日は黒文字に
                            pdf.setFillColor(color.gray)
                        pdf.setFont('BIZUDGothicR', 10)
                        pdf.drawString(
                            bible_x+(j+1)*block_w+0.5*mm,
                            bible_y+weekday_h+i*block_h+3.5*mm,
                            str(calendar_list[i][j])
                        )
            


            # ページファインダー切り取り線
            PageFinder(pdf, True)
           
        # 切り取り線
        CutLine(pdf)
        
        # 改ページ
        pdf.showPage()

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()