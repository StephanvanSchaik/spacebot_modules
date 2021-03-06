import urllib2
import time
import willie

statetracking = 0

def checkstate():
  response = urllib2.urlopen('http://techinc.nl/space/spacestate')
  html = response.read()
  return html

def changestate(state):
  print 'State: %s' % state
  response = urllib2.urlopen('http://techinc.nl/space/index.php?state=%s&key=securepassword' % state)
  html = response.read()
  return html


@willie.module.commands('trackstate')
def trackstate(bot, trigger):
  global statetracking
  if statetracking != 1:
    statetracking = 1
    currentstate = checkstate()
    bot.say('Now tracking spacestate')

    while True:
      newstate = checkstate()
      if newstate != currentstate:
        bot.say('The space is now ' + newstate)
        newtopic = 'Welcome to Technologia Incognita, we are ' + newstate + '. https://www.techinc.nl/ - Social night every Wednesday at ACTA'
        channel = trigger.sender.lower()
        bot.write(('TOPIC', channel + ' :' + newtopic))
        currentstate = newstate
      time.sleep(5)
  else:
    bot.say('Already tracking spacestate')

@willie.module.commands('togglestate')
def togglestate(bot, trigger):
  currentstate = checkstate()
  bot.say('Changing Spacestate')
  if currentstate == 'open':
    state = 'closed'
  else:
    state = 'open'
  changestate(state)

