import pandas as pd
from datetime import datetime,timedelta
import PyGnuplot as pg

#d=pd.read_html("https://finance.yahoo.com/quote/WAF.DE/history?period1=1549148400&period2=1570831200&interval=1d&filter=history&frequency=1d")
#d=pd.read_html("https://finance.yahoo.com/quote/SHA.DE/history?period1=1569880800&period2=1570831200&interval=1d&filter=history&frequency=1d")
d=pd.read_html("https://finance.yahoo.com/quote/IUSE.L/history?period1=1569880800&period2=1570831200&interval=1d&filter=history&frequency=1d")

buy_price = 62.4124
df=d[0]

dates = []
for i in df['Date']:
	x = i.replace(",", "")
	dates.append(x)
dates.reverse()
dates.pop(0)

format_date = []
for i in range(len(dates)):
	format_date.append(datetime.strptime(dates[i], '%b %d %Y').strftime('%y%m%d'))

close_price = []
for i in df['Close*']:
	close_price.append(i)
close_price.reverse()
close_price.pop(0)

percent = []
for i in range(len(close_price)):
	a=float(100*(-buy_price+float(close_price[i]))/buy_price)
        print close_price[i],dates[i],a
	percent.append(a)

pg.c('set xdata time')
pg.c('set timefmt "%y%m%d"')
pg.s([format_date,percent])
pg.c('set format x "%y%m%d"')
#pg.c('set xrange ["190523":"191011"]')
#pg.c('set xtics ("190523", 2592000, "191011")')
pg.c('plot "tmp.dat" u 1:2 w lp')
