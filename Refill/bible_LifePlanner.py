from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from bible_GlobalParam import size_w, size_h
from bible_5YearsGoal import Draw5YearsPlanChart
from bible_YearlyCalender import DrawYearCalendar
from bible_YearlyGoal import DrawYearlyPlanChart
from bible_AgeChart import DrawAgeChart
from bible_monthly_block import DrawMonthlyBlock

# 出力ファイル名
FILENAME = 'bible_LifePlanner.pdf'

# 出力したい年
year = 2026 

def main():
    # フォーマット定義
    pdf = canvas.Canvas(FILENAME, bottomup=False) # ページ左上を原点とする
    pdf.setPageSize((size_w * mm, size_h * mm))
    
    # ページ更新
    pdf.showPage()

    ### 5年計画表 ###
    Draw5YearsPlanChart(pdf, True)

    ### 年間計画表 ###
    DrawYearlyPlanChart(pdf, False)

    ### 年間カレンダー ###
    DrawYearCalendar(pdf, year, True)
    DrawYearCalendar(pdf, year + 1, False)

    ### 月間ブロック ###
    for i in range(1, 13):
        DrawMonthlyBlock(pdf, year, i)
    for i in range(1, 4): # 翌年3ヶ月分
        DrawMonthlyBlock(pdf, year + 1, i)

    ### 年齢早見表 ###
    DrawAgeChart(pdf, year)

    # ファイルに保存
    pdf.save()
    
if __name__ == '__main__':
    main()