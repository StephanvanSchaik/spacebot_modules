import urllib2
import time
import willie
import sys
from mpd import (MPDClient, CommandError)
from socket import error as SocketError

HOST = '10.0.20.3'
PORT = '6600'
PASSWORD = 'password goes here'

mpd_commands = {
  i: show_state for i in ['playing', 'state'],
  i: lambda client, action: do_action(client, action, j) for i, j in zip(
    ['play', 'pause', 'stop', 'next'], [True, False, False, True]),
}

# Just use replacement identifiers, as they are close to lazy evaluation.
mpd_messages = {
  'is_play': 'Now playing: {artist} - {title}',
  'is_pause': 'Music is currently paused ({artist})',
  'is_stop': 'No music is playing',
  'play': 'Pressing play on mpd...',
  'pause': 'Pausing mpd...',
  'stop': 'Stopping mpd...',
  'next': 'Moving to next song on mpd...',
}

@willie.module.commands('mpd')
def mpd(bot, trigger):
  rulenum = trigger.group(2)

  ## MPD object instance
  client = MPDClient()

  try:
    client.connect(host=HOST, port=PORT)
  except SocketError:
    bot.say('socketerror')
    exit(1)


  # Auth if password is set non False
  if PASSWORD:
    try:
      client.password(PASSWORD)
    except CommandError:
      client.disconnect()
      sys.exit(2)

  # Dispatch the MPD command to a handler, if there is one.
  mpd_command = str(rulenum)

  if mpd_command in mpd_commands:
    mpd_commands[mpd_command](client, mpd_command)
  else:
    bot.say('Invalid mpd command.')

# Shows the current state of MPD.
def show_state(client, action):
  current_song = client.currentsong()
  current_state = client.status()['state']

  if 'is_' + current_state in mpd_messages:
    bot.say(mpd_messages['is_' + current_state].format(
      artist=current_song['artist'], title=current_song['title']))

# Shows the current song.
def show_current_song(client):
  current_song = client.currentsong()
  bot.say(mpd_messages['is_playing'].format(artist=current_song['artist'],
    title=current_song['title']))

# Performs a client action, shows the associated message and, if desired, shows
# the current song.
def do_action(client, action, show_song=False):
  if action in mpd_messages:
    bot.say(mpd_messages[action])

  if getattr(client, action):
    getattr(client, action)()

  if show_song:
    show_current_song()

