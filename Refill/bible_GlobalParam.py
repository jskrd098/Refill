from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont

# フォント登録
BIZUDGothicR = "./fonts/BIZ-UDGothicR.ttc"
pdfmetrics.registerFont(TTFont('BIZUDGothicR', BIZUDGothicR))

# 用紙サイズ[mm]
size_w = 95
size_h = 170

# 余白[mm]
margin = 5
ringhole = 10

# 年
eto = {0:'申', 1:'酉', 2:'戌', 3:'亥', 4:'子', 5:'丑', 6:'寅', 7:'卯', 8:'辰', 9:'巳', 10:'午', 11:'未'}
gengou = {0:'大正', 1:'昭和', 2:'平成', 3:'令和'}

# 月
monthStr = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
monthStrShort = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
monthStrJP = ('睦月', '如月', '弥生', '卯月', '皐月', '水無月', '文月', '葉月', '長月', '神無月', '霜月', '師走')

# 曜日
weekdayStr = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
weekdayStrShort = ('M', 'T', 'W', 'T', 'F', 'S', 'S')
weekdayStrJP = ('月', '火', '水', '木', '金', '土', '日')
