import pymongo
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys


def is_neutral_site(event_id):
  url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + event_id + '/related_content.xml'

  html = urlopen(url).read()
  soup = BeautifulSoup(html, 'lxml')
  #print event_id

  if soup.find('event') is not None:
    if soup.find('event')['neutral_site'] == 'yes':
      return True
    else:
      return False
  else:
    return False


'''
def build_wp_owp(code):
  opponents = []
  total_oowp = 0
  connection = pymongo.Connection()
  db = connection.scoreboard

  home_games = db.scoreboard.find({'hcode': code, 'neutral_site': False, 'vdiv': 'I'})
  games = cursor_to_list(home_games)
  home_results = get_wins_losses(games, code)
  opponents = build_opp_list(games, opponents, code)

  away_games = db.scoreboard.find({'vcode': code, 'neutral_site': False, 'hdiv': 'I'})
  games = cursor_to_list(away_games)
  away_results = get_wins_losses(games, code)
  opponents = build_opp_list(games, opponents, code)

  neutral_games = db.scoreboard.find({'$or': [{'hcode': code, 'neutral_site': True, 'vdiv': 'I'}, {'vcode': code, 'neutral_site': True, 'hdiv': 'I'}]})
  games = cursor_to_list(neutral_games)
  neutral_results = get_wins_losses(games, code)
  opponents = build_opp_list(games, opponents, code)

  total_wins = home_results[0] + away_results[0] + neutral_results[0]
  total_losses = home_results[1] + away_results[1] + neutral_results[1]

  all_results = [ total_wins, total_losses ]

  wp = get_winning_percentage(all_results)
  owp = get_opp_winning_percentage(opponents, db, code)
  connection = pymongo.Connection()
  db = connection.rpi

  db.test.insert({'_id': code, 'wp': wp, 'owp': owp, 'opponents': opponents})
  print code + ' ' + str(wp) + ' ' + str(owp) + ' inserted.'


def cursor_to_list(games):
  results = []
  for game in games:
    results.append(game)

  return results


def add_rpi(code):
  WP_FACTOR = 0.25
  OWP_FACTOR = 0.50
  OOWP_FACTOR = 0.25

  connection = pymongo.Connection()
  db = connection.rpi
  team = db.test.find_one({'_id': code})
  if 'oowp' in team:
    rpi = (team['wp'] * WP_FACTOR) + (team['owp'] * OWP_FACTOR) + (team['oowp'] * OOWP_FACTOR)
    db.test.update({'_id': code}, {'$set': {'rpi': rpi}})


def build_opp_list(games, opponents_list, code):
  for game in games:
    if code == game['hcode']:
      opponents_list.append(str(game['vcode']))
    elif code == game['vcode']:
      opponents_list.append(str(game['hcode']))

  return opponents_list


def get_winning_percentage(results):
  w = results[0]
  l = results[1]
  gp = w + l

  if gp > 0:
    return (float(w) / gp)
  else:
    return 0


def get_opp_winning_percentage(opponents, db, code):
  owp = 0
  oowp = 0
  #global opponents_opponents
  num_opp = len(opponents)

  for opp in opponents:
    home_games = db.scoreboard.find({'$and': [{'vcode': {'$nin': [code]}}, {'hcode': opp, 'neutral_site': False, 'vdiv': 'I'}]})
    games = cursor_to_list(home_games)
    home_results = get_wins_losses(games, opp)
    #oppopp = build_opp_list(games, opponents, opp)

    away_games = db.scoreboard.find({'$and': [{'hcode': {'$nin': [code]}}, {'vcode': opp, 'neutral_site': False, 'hdiv': 'I'}]})
    games = cursor_to_list(away_games)
    away_results = get_wins_losses(games, opp)
    #oppopp = build_opp_list(games, opponents, opp)

    neutral_games = db.scoreboard.find({'$and': [{'vcode': {'$nin': [code]}}, {'hcode': {'$nin': [code]}}, {'$or': [{'hcode': opp, 'neutral_site': True, 'vdiv': 'I'}, {'vcode': opp, 'neutral_site': True, 'hdiv': 'I'}]}]})
    games = cursor_to_list(neutral_games)
    neutral_results = get_wins_losses(games, opp)
    #oppopp = build_opp_list(games, opponents, code)

    total_wins = home_results[0] + away_results[0] + neutral_results[0]
    total_losses = home_results[1] + away_results[1] + neutral_results[1]

    all_results = [ total_wins, total_losses ]

    #opponents_opponents.append(dict(opp = opp, oppopp = oppopp))

    wp = get_winning_percentage(all_results)
    owp = owp + wp

  if owp > 0:
    if num_opp > 0:
      return owp / num_opp
  else:
    return 0


def set_oppopp_winning_percentage(opponents, code):
  oowp = 0
  connection = pymongo.Connection()
  db = connection.rpi
  num_opp = len(opponents)

  for opp in opponents:
    oppwp = db.test.find_one({'_id': opp}, {'_id': -1, 'wp': 1})
    oowp = oowp + oppwp['wp']

  if oowp > 0:
    if num_opp > 0:
      oowp = oowp / num_opp
  else:
    oowp = 0
  print 'Inserting: ' + str(code) + ' ' + str(oowp)
  db.test.update({'_id': code}, { '$set': {'oowp': oowp}})


def get_wins_losses(games, code):
  w = 0
  l = 0
  for game in games:
    if game['hcode'] == code:
      if game['hscore'] > game['vscore']:
        w = w + 1
      else:
        l = l + 1
    elif game['vcode'] == code:
      if game['vscore'] > game['hscore']:
        w = w + 1
      else:
        l = l + 1

  return [w, l]


def print_rpi():
 connection = pymongo.Connection()
 db = connection.rpi

 rpis = db.test.find().sort('rpi', pymongo.DESCENDING)

 for rpi in rpis:
  if 'rpi' in rpi:
    print str(rpi['_id']) + ' ' + str(rpi['rpi'])

'''
#team = sys.argv[1]
"""
build_wp_owp(team)
connection = pymongo.Connection()
db = connection.rpi
opp = db.test.find_one({'_id': team}, {'_id': -1, 'opponents': 1})

opponents = []
if opp is not None:
  for o in set(opp['opponents']):
    opps = db.test.find_one({'_id': o}, {'_id': -1, 'opponents': 1})
    if opps is not None:
      opponents.extend(opps['opponents'])
  print 'Getting opponent\'s opponent\'s WP...'
  set_oppopp_winning_percentage(opponents, team)
"""
#add_rpi(team)
#print_rpi()
