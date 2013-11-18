#Virker kun på stefans

import locale, datetime, time
locale.setlocale(locale.LC_ALL, 'da_DK.utf8') 
date = '10 augustus 2005 om 17:26'
print time.strptime(date, "%d %B %Y om %H:%M")
