from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
import reportlab.lib.colors as color

# 用紙サイズ
A4_w, A4_h = A4
refill_w = 95*mm
refill_h = 170*mm
refill_x = A4_w/2 - refill_w/2
refill_y = A4_h/2 - refill_h/2

def CutLine(pdf):
    pdf.setStrokeColor(color.gray)
    pdf.setDash([2,2])
    pdf.lines([
        (0, refill_y, A4_w, refill_y),
        (0, refill_y+refill_h, A4_w, refill_y+refill_h),
        (refill_x, 0, refill_x, A4_h),
        (refill_x+refill_w, 0, refill_x+refill_w, A4_h)
    ])

def DrawGrid2mmIndex(pdf, idx):
    title_h = 10*mm

    # 表面(右ページ)
    pdf.setStrokeColor(color.darkgray)
    pdf.setLineWidth(0.1)
    # 縦線
    lx = refill_x + refill_w - 2*mm
    while lx > refill_x:
        pdf.line(lx, refill_y+title_h, lx, refill_y+refill_h)
        lx -= 2*mm
    # 横線
    ly = refill_y + title_h
    while ly < refill_y + refill_h:
        pdf.line(refill_x, ly, refill_x+refill_w, ly)
        ly += 2*mm
    # ページ端の見出し
    pdf.setFillColor(color.darkgray)
    pdf.rect(refill_x+refill_w-2*mm, refill_y+title_h+idx*16*mm, 2*mm, 16*mm, fill=1)

    CutLine(pdf)

    # 改ページ
    pdf.showPage()

    # 裏面(左ページ)
    pdf.setStrokeColor(color.darkgray)
    pdf.setLineWidth(0.1)
    # 縦線
    lx = refill_x
    while lx < refill_x + refill_w:
        pdf.line(lx, refill_y+title_h, lx, refill_y+refill_h)
        lx += 2*mm
    # 横線
    ly = refill_y + 10*mm
    while ly < refill_y + refill_h:
        pdf.line(refill_x, ly, refill_x+refill_w, ly)
        ly += 2*mm
    # ページ端の見出し
    pdf.setFillColor(color.darkgray)
    pdf.rect(refill_x, refill_y+title_h+idx*16*mm, 2*mm, 16*mm, fill=1)
     
    CutLine(pdf)

def main():

    # ファイル名
    FILENAME = 'grid_2mm_index.pdf'

    # フォーマット定義
    pdf = canvas.Canvas(FILENAME, pagesize=portrait(A4), bottomup=False)

    for i in range(0, 10):
        DrawGrid2mmIndex(pdf, i)
        pdf.showPage()

    # ファイルに保存
    pdf.save()

if __name__ == '__main__':
    main()