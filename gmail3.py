#!/usr/bin/env python
##  Show No of emails on screen
##  Graham Errington 13 September 2014
##
import feedparser, time
import commands
import math
import time
import datetime
import Adafruit_CharLCD as LCD

def write_to_lcd(lcd, framebuffer, num_cols):
    lcd.clear()
    for row in framebuffer:
        lcd.message(row.ljust(num_cols)[:num_cols])
        lcd.message("\n")

USERNAME = "grahamraspberrypi3"     
PASSWORD = "g3rpix5"

#USERNAME = "grahamraspberrypi1"
#PASSWORD = "rpg1x5"
NEWMAIL_OFFSET = 0        # my unread messages never goes to zero, yours might
LOTSMAIL = 5        # my unread messages never goes to zero, yours might

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()
#lcd.set_color(1.0, 1.0, 1.0) # White
lcd.set_color(0, 0, 0) # Off
lcd.clear()

# If late in the day then switch off screen - will switch back on if weather ale
rt is in effect
now = datetime.datetime.now().strftime('%H')

if int(now) > 6 and int(now) < 21:
    lcd.set_color(1,1,1)





lcd.message('Checking email...')

framebuffer=['Hello', '']
newmails = feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.googl
e.com/gmail/feed/atom")["feed"]["fullcount"]

if int(newmails) > 0:
	url="https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/mail/feed/
atom"
	walesIP=commands.getoutput("wget -qO- "+ url).split("New IP is")[1].spli
t("<")[0].strip()
else:
	walesIP = 'off-line.'

lcd.clear()
if int(newmails) == 1:
	#Display 'mail' otherwise 'mails'.
	lcd.message('RPI3: '+ newmails+ ' email.\n')
else:
	lcd.message('RPI3: '+ newmails+ ' emails.\n')

now = datetime.datetime.now().strftime('%d %B %y')
lcd.message(now)
time.sleep(1.0)

now = datetime.datetime.now().strftime('%X')
lcd.message('\n' + now + '        ')
lcd.message(now)

if int(newmails) == 0:
	# Make it green.
#	lcd.set_color(0,1,0)
    lcd.message(".")

##  Show IP address on display
##  Graham Errington 13 September 2014
##

localip=commands.getoutput("/sbin/ifconfig wlan0").split("\n")[1].split()[1][5:]
extip=commands.getoutput("wget -qO- http://checkip.dyndns.org/").split(":")[1].s
plit("<")[0]
time.sleep(1.0)
lcd.clear()
lcd.message('I:' + localip + '\n')
lcd.message('E:' + extip)

##  Show uptime information on display
##  Graham Errington 13 September 2014
##
time.sleep(1.0)
lcd.clear()
uptimeresult=commands.getoutput("uptime")
# Print the whole of uptime - it gives more information.  Split into 16 characte
r chunks (like the weather).

remain = uptimeresult[10:len(uptimeresult)].split("  ")
no_of_bits = len(remain)

if no_of_bits == 4:
    # Time up is in 2 fields
    lcd.message(remain[0] +'\n')
    lcd.message(remain[1])

    # Users
    time.sleep(1)
    lcd.clear()
    lcd.message(remain[2])

    # Load Average
    time.sleep(1)
    lcd.clear()
    lcd.message("Load Average:"+ "\n")
        lcd.message(remain[3].split(":")[1].strip())
else:
    #Time is only 1 field if not on for very long (or other reasons)
    lcd.message(remain[0] + '\n')
    # Users
    lcd.message(remain[1])

    # Load Average
    time.sleep(1)
    lcd.clear()
    lcd.message("Load Average:"+ "\n")
    lcd.message(remain[2].split(":")[1].strip())

##

time.sleep(1)

# Display the Wales IP address
lcd.clear()
lcd.message('Wales IP:\n' + walesIP)

if walesIP == 'off-line.':
	lcd.clear()
	lcd.message('Wales is \nunavailable.')
time.sleep(1)

##  Weather Warning alert system
##  Graham Errington 14 September 2014
##

# Weather alert comes from here:
# http://alerts.weather.gov/cap/wwaatmget.php?x=GAC135&y=1 
# Los Angeles = CAC037
# Sugar Hill = GAC135

lcd.clear()
lcd.message(' WEATHER ALERT\n ??????? ?????')

walert2 = feedparser.parse("http://alerts.weather.gov/cap/wwaatmget.php?x=GAC135
&y=0")
time.sleep(1)

#print len(walert2['entries']) # number of alert entries
# Change colour if alerts > 0  - changed from len(walert2['entries']) > 0:
if walert2['entries'][0]['title'] <> "There are no active watches, warnings or a
dvisories" :
	lcd.set_color(1,0,0)

for alert in range (0, len(walert2['entries'])):
    # print title and summary for each alert

#    print walert2['entries'][alert]['summary']
#    print walert2['entries'][alert]['cap_certainty']
#    print walert2['entries'][alert]['cap_urgency']

    mymsg=walert2['entries'][alert]['title']

    for i in range(len(mymsg) -32 +1):
        framebuffer[0]=mymsg[i:i+16]
        framebuffer[1]=mymsg[i+16:i+32]
        write_to_lcd(lcd, framebuffer, 16)
        time.sleep(0.2)


time.sleep(1)

# Display the Wales IP address
lcd.clear()
lcd.message('Wales IP:\n' + walesIP)
if walesIP == 'off-line.':
	lcd.clear()
	lcd.message('Wales is offline\n ')
	lcd.message('')
time.sleep(3.0)
