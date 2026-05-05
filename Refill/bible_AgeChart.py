from reportlab.lib.units import mm

from bible_GlobalParam import size_w, ringhole, eto, gengou

def DrawAgeChart(pdf, year):

    # canvas状態を一時保存
    pdf.saveState()
    
    x = 4 # 表の原点のx座標
    y = 12*mm # 表の原点のy座標
    
    col = 3 # 列数
    row = 34 # 行数
    line_h = 3*mm # 行の高さ
    line_w = (size_w-ringhole-x)*mm/col # 列幅
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
    pdf.drawString(x*mm, 7*mm, 'AGE CHART')
    
    # 罫線
    pdf.setStrokeColorRGB(0.6, 0.6, 0.6)
    pdf.setLineWidth(0.1)
    pdf.lines([
        (x*mm+line_w, y-line_h+0.5*mm, x*mm+line_w, y+line_h*row+0.5*mm),
        (x*mm+line_w*2, y-line_h+0.5*mm, x*mm+line_w*2, y+line_h*row+0.5*mm),
        (x*mm, y+0.75*mm, x*mm+line_w*col, y+0.75*mm)
    ])

    # 表の見出し
    pdf.setFont('BIZUDGothicR', 6)
    for i in range(0, col):
        pos_x = x*mm+line_w*i+3*mm
        for k in range(0, len(col_idx)):
            pdf.drawCentredString(pos_x+line_col[k], y, col_idx[k])

    # 表の中身
    for i in range(0, col):
        pos_x = x*mm+line_w*i+3*mm
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
    # pdf.drawString(
    
    # canvas状態をレストア
    pdf.restoreState()

    # ページ更新
    pdf.showPage()