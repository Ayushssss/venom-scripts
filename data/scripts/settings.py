import bs
from datetime import datetime
date = datetime.now().strftime('%d')

enableTop5effects = False
enableTop5commands = False
enableCoinSystem = False

enableStats = True

print 'Enable Stats: ', enableStats

spamProtection=True

enableChatFilter = True

coinTexts = ['Welcome to YOYO Official','Use "/shop commands" to see commands available to buy.','Use "/shop effects" to see effects available and their price.','Use "/me" or "/stats" to see your '+bs.getSpecialChar('ticket')+' and your stats in this server', 'Use "/buy" to buy effects that you like','Use "/donate" to give some of your tickets to other players','Use "/scoretocash" to convert some of your score to '+bs.getSpecialChar('ticket')+'\nCurrent Rate: 5scores = '+bs.getSpecialChar('ticket')+'1']

questionDelay = 85 #85 #seconds
questionsList = {'Who is the owner of this server?': 'venom', 'Who is the editor of this server?': 'venom','What Should we wear during corona ': 'mask','Which is the biggest planet in our solar System?': 'jupiter','In which country Eiffel Tower located?': 'paris','In which country taj mahal located?': 'india','Which month of the year has least number of days?': 'february','Which is the largest animal in the world?': 'blue whale','In which direction does the sunrise?': 'east','which is the Continent with most number of countries?': 'africa','Did you joined our Discord Server?': 'yes','What is the Name of this game?': 'bombsquad','Bombsquad is coded in Which Language?': 'python','What is the currency of india?': 'rupee','What is the Currency of U.S?': 'dollar','In which continent is India Located?': 'asia','what is the name of world smallest Country?': 'vatican city','Which is the world most common Religion?': 'christianity',
       'add': None, 
       'multiply': None}

availableCommands = {'/nv': 50, 
   '/ooh': 5, 
   '/playSound': 10, 
   '/box': 30, 
   '/boxall': 60, 
   '/spaz': 50, 
   '/spazall': 100, 
   '/inv': 40, 
   '/invall': 80, 
   '/tex': 80, 
   '/texall': 250, 
   '/freeze': 10000, 
   '/freezeall': 33350, 
   '/sleep': 800, 
   '/sleepall': 2250, 
   '/thaw': 100, 
   '/thawall': 200, 
   '/kill': 100, 
   '/killall': 222250, 
   '/end': 1150, 
   '/hug': 90, 
   '/hugall': 250, 
   '/tint': 900000, 
   '/sm': 150, 
   '/fly': 100, 
   '/flyall': 200050, 
   '/heal': 100, 
   '/healall': 250, 
   '/gm': 500000, 
   '/custom': 100000000}

availableEffects = {'ice': 500, 
   'sweat': 750, 
   'scorch': 500, 
   'glow': 400, 
   'distortion': 750, 
   'slime': 500, 
   'metal': 500, 
   'surrounder': 1000}
