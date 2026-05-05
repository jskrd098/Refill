from os import truncate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color
import textwrap
import calendar
import datetime
import jpholiday

FILENAME = 'mini6_weekly_血圧記録表_R2.pdf' # ファイル名

# 台紙サイズ(A4)
A4_w, A4_h = A4

# 用紙サイズ(システム手帳 ミニ6)
sizeX = 80*mm
sizeY = 126*mm

# 4ページ分に均等割付したときの各原点座標
origin = (((A4_w-2*sizeX)/3, (A4_h-2*sizeY)/3), ((2*A4_w-sizeX)/3, (A4_h-2*sizeY)/3), ((A4_w-2*sizeX)/3, (2*A4_h-sizeY)/3), ((2*A4_w-sizeX)/3, (2*A4_h-sizeY)/3))

# フォント登録
BIZUDGothicR = "D:/Program/Python/refill/fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

# 余白
marginY = 4*mm # 上余白
marginXRing = 11*mm # リング穴が左側にあるときの左余白、またはリング穴が右側にあるときの右余白
marginX = 4*mm # リング穴が右側にあるときの左余白、またはリング穴が左側にあるときの右余白

lines = 18 # 行数
blockY = (sizeY - marginY * 2) / lines # 行の高さ

# トンボ線を描画する
def DrawTomboLine(pdf):
    pdf.setStrokeColor(color.gray)
    pdf.setLineWidth(0.1)
    pdf.setDash([2, 2])

    tLen = 10*mm

    for i in range (0, 4):
        pdf.line(origin[i][0]      , origin[i][1]      , origin[i][0]-tLen      , origin[i][1]           )
        pdf.line(origin[i][0]      , origin[i][1]      , origin[i][0]           , origin[i][1]-tLen      )
        pdf.line(origin[i][0]+sizeX, origin[i][1]      , origin[i][0]+sizeX+tLen, origin[i][1]           )
        pdf.line(origin[i][0]+sizeX, origin[i][1]      , origin[i][0]+sizeX     , origin[i][1]-tLen      )
        pdf.line(origin[i][0]      , origin[i][1]+sizeY, origin[i][0]-tLen      , origin[i][1]+sizeY     )
        pdf.line(origin[i][0]      , origin[i][1]+sizeY, origin[i][0]           , origin[i][1]+sizeY+tLen)
        pdf.line(origin[i][0]+sizeX, origin[i][1]+sizeY, origin[i][0]+sizeX+tLen, origin[i][1]+sizeY     )
        pdf.line(origin[i][0]+sizeX, origin[i][1]+sizeY, origin[i][0]+sizeX     , origin[i][1]+sizeY+tLen)
        
    pdf.setDash([])

# 罫線を描画する
def DrawRecordSheetLines(originX, originY, pdf, leftPage):

    pdf.setStrokeColor(color.gray) # 線色を指定する
    pdf.setLineWidth(0.1) # 線幅を指定する
    
    if leftPage:
        mL = marginXRing
        mR = marginX
    else:
        mL = marginX
        mR = marginXRing
    mH = marginY

    # 横方向の罫線の描画
    for i in range(0, lines + 1):
        if i == 1: # 見出しの行を分割する線
            sX = originX + mL + 15*mm # 始点X座標
        elif i > 16: # 1週間の平均欄を上下分割する線
            sX = originX + sizeX - mR - ((sizeX-mL-mR-15*mm) / 3) - 5*mm # 始点X座標
        elif i % 2 == 1: # 各日付の記入欄を上下2分割する線
            sX = originX + mL + 10*mm # 始点X座標
        else: # 日付ごとの区切り線
            sX = originX + mL # 始点X座標
        eX = originX + sizeX - mR # 終点X座標
        sY = originY + mH + blockY * i # 始点Y座標
        eY = sY # 終点Y座標
        pdf.line(sX, sY, eX, eY) # 罫線描画

    # 縦方向の罫線の描画
    for i in range(0, 7):
        if i == 0: # 外枠左側
            sX = originX + mL # 始点X座標
            sY = originY + mH # 始点Y座標
            eY = originY + sizeY - marginY - blockY * 2 # 終点Y座標
        elif i == 1:
            sX = originX + mL + 10*mm # 始点X座標
            sY = originY + mH + blockY * 2 # 始点Y座標
            eY = originY + sizeY - marginY - blockY * 2 # 終点Y座標
        elif i == 2:
            sX = originX + mL + 15*mm # 始点X座標
            sY = originY + mH # 始点Y座標
            eY = originY + sizeY - marginY - blockY * 2 # 終点Y座標
        elif i == 3:
            sX = originX + mL + 15*mm + ((sizeX-mL-mR-15*mm) / 3)
            sY = originY + mH # 始点Y座標
            eY = originY + sizeY - marginY - blockY * 2 # 終点Y座標
        elif i == 4:
            sX = originX + mL + 10*mm + ((sizeX-mL-mR-15*mm) / 3 * 2)
            sY = originY + sizeY - marginY - blockY * 2 # 始点Y座標
            eY = originY + sizeY - marginY # 終点Y座標
        else:
            sX = originX + mL + 15*mm + ((sizeX-mL-mR-15*mm) / 3 * (i-3))
            sY = originY + mH # 始点Y座標
            eY = originY + sizeY - marginY # 終点Y座標
        
        eX = sX  # 終点X座標
        pdf.line(sX, sY, eX, eY) # 罫線描画

# テキストを描画する
def DrawRecordSheetText(originX, originY, pdf, leftPage):

    if leftPage:
        mL = marginXRing
        mR = marginX
    else:
        mL = marginX
        mR = marginXRing
    mH = marginY

    ### 見出し上段の記入項目名の文字配置
    sX = originX + mL + 15*mm + (sizeX-mL-mR-15*mm) / 6 # 文字列の左下位置のX座標を設定
    sY = originY + mH + blockY * 0.5 + 1*mm # 文字列の左下位置のY座標を設定
    pdf.setFont('BIZUDGothicR', 7) # 文字の大きさを設定
    pdf.setFillColor(color.gray) # 文字色を設定
    pdf.drawCentredString(sX, sY, '1回目測定値') # 見出し文字列を記入する

    sX += (sizeX-mL-mR-15*mm) / 3
    pdf.drawCentredString(sX, sY, '2回目測定値')

    sX += (sizeX-mL-mR-15*mm) / 3
    sY -= 0.2*mm
    pdf.setFont('BIZUDGothicR', 5)
    pdf.drawCentredString(sX, sY, '家庭血圧値(平均)')

    ### 見出し下段の記入項目名の文字配置
    sY = originY + mH + blockY * 1.5 + 0.5*mm
    pdf.setFont('BIZUDGothicR', 4)
    for i in range (0, 3):
        sX = originX + mL + 15*mm + (2*i+1) * (sizeX-mL-mR-15*mm) / 6 # i * (sizeX-mL-mR-15*mm) / 3 + (sizeX-mL-mR-15*mm) / 6 の式をまとめた形
        pdf.drawCentredString(sX, sY, '最高血圧/最低血圧/脈拍')

    ### 日付記入欄
    sX = originX + mL + 5*mm
    sY = originY + mH + blockY * 2.5 + 2*mm
    pdf.setFont('BIZUDGothicR', 7)
    for i in range (0, 7):
        pdf.drawCentredString(sX, sY, '/')
        pdf.drawCentredString(sX, sY+blockY, '(   )')
        sY += blockY * 2

    ### 記入欄右隣の"朝""夜"の文字配置
    sX = originX + mL + 12.5*mm
    sY = originY + mH + blockY * 2.5 + 1*mm # 文字列の左下位置のY座標を設定
    pdf.setFont('BIZUDGothicR', 7)
    for i in range (0, 16):
        if i == 14:
            sX += (sizeX-mL-mR-15*mm) * 2 / 3
        if i % 2 == 0:
            pdf.drawCentredString(sX, sY, '朝')
        else:
            pdf.drawCentredString(sX, sY, '夜')
        sY += blockY

    ### 最下段の"1週間の平均値"欄の文字配置
    sX = originX + mL + 27*mm
    sY = originY + sizeY - marginY - blockY + 1*mm
    pdf.setFont('BIZUDGothicR', 10)
    pdf.drawCentredString(sX, sY, '1週間の平均値 ⇒')

    ### 記入欄の"/"を配置
    sX = originX + mL + 15*mm + (sizeX-mL-mR-15*mm) / 6
    pdf.setFont('BIZUDGothicR', 6)
    for i in range (0, 3):
        sY = originY + mH + blockY * 2.5 + 1*mm
        for j in range (0, 16):
            if i < 2 and j >= 14:
                break
            pdf.drawCentredString(sX, sY, '/    /')
            sY += blockY
        sX += (sizeX-mL-mR-15*mm) / 3

# シートを作成する
def DrawRecordSheet(pdf):

    origin = (((A4_w-2*sizeX)/3, (A4_h-2*sizeY)/3), ((2*A4_w-sizeX)/3, (A4_h-2*sizeY)/3), ((A4_w-2*sizeX)/3, (2*A4_h-sizeY)/3), ((2*A4_w-sizeX)/3, (2*A4_h-sizeY)/3))

    # 罫線の書式設定
    pdf.setStrokeColor(color.gray) # 線色を指定する
    pdf.setLineWidth(0.1) # 線幅を指定する

    blockY = (sizeY - marginY * 2) / lines # 行の高さ
    
    DrawTomboLine(pdf)
    
    for i in range (0, 4):
        # 表側（リング穴が左側）の罫線を描画
        DrawRecordSheetLines(origin[i][0], origin[i][1], pdf, True)
        # 表側（リング穴が左側）のテキストを描画
        DrawRecordSheetText(origin[i][0], origin[i][1], pdf, True)

    pdf.showPage()

    DrawTomboLine(pdf)
    
    for i in range (0, 4):
        # 裏側（リング穴が右側）の罫線を描画
        DrawRecordSheetLines(origin[i][0], origin[i][1], pdf, False)
        # 裏側（リング穴が右側）のテキストを描画
        DrawRecordSheetText(origin[i][0], origin[i][1], pdf, False)

def main():

    pdf = canvas.Canvas(FILENAME, A4, bottomup=False) # ページ左上を原点とする
    # pdf = canvas.Canvas(FILENAME, bottomup=False) # ページ左上を原点とする
    # pdf.setPageSize((sizeX, sizeY)) # 用紙サイズを指定する

    DrawRecordSheet(pdf)

    pdf.save() # ファイルに保存

if __name__ == '__main__':
    main()