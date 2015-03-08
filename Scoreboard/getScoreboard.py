#!/usr/bin/env python

import sys, datetime
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pymongo
import rpi

def get_scoreboard(scoreboard_date):
  connection = pymongo.Connection()
  db = connection.scoreboard

  scoreboard_year = scoreboard_date[:4]

  # http://www.cstv.com/gametracker/universe/
  url = "http://livestats.www.cstv.com/scoreboards/m-basebl/" + scoreboard_year + "/" + scoreboard_date + "-m-basebl-scoreb.xml"

  html = urlopen(url).read()
  soup = BeautifulSoup(html, "lxml")

  scoreboard = []
  print scoreboard_date

  for event in soup.findAll('event'):
    event_id = event['event_id']
    summary_url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + event_id + '/summary2.xml'
    xml2 = urlopen(summary_url).read()
    s = BeautifulSoup(xml2, 'lxml')
    try:
      venue = s.find('venue')
      if venue:
        umpires = venue.umpires.attrs
        venue_dict = venue.attrs
        drop_attrs = ['homeid', 'homename', 'visid', 'visname']
        venue_info = {k: v for (k, v) in venue_dict.iteritems() if k not in drop_attrs}
        venue_info['attend'] = int(venue_info['attend'])
        venue_info['schedinn'] = int(venue_info['schedinn'])
        slash =  [i for i in range(len(venue.attrs['date'])) if venue.attrs['date'].startswith('/', i)]
        venue_info['date'] = datetime.datetime(int(venue_info['date'][slash[1] + 1:len(venue_info['date'])]), int(venue_info['date'][0:slash[0]]), int(venue_info['date'][slash[0] + 1:slash[1]]))
      else:
        umpires = None
        venue_info = None
    except:
      e = sys.exc_info()[0]
      print 'event_id: ' + event_id + '\n' + summary_url +'\n\nError: ' + str(e)
    vname = event['vname']
    vcode = event['vcode']
    hname = event['hname']
    hcode = event['hcode']
    if event['started'] == 'N':
      vscore = 0
      hscore = 0
    else:
      vscore = int(event['vscore'])
      hscore = int(event['hscore'])
    gdate = event['date']
    gtime = event['time']
    gtlink = event['gametracker'].split("'")[1][:-1]

    if event.has_attr('vconf'):
      vconf = event['vconf']
    else:
      vconf = ""
    if event.has_attr('vdiv'):
      vdiv = event['vdiv']
    else:
      vdiv = ""
    if event.has_attr('hconf'):
      hconf = event['hconf']
    else:
      hconf = ""
    if event.has_attr('hdiv'):
      hdiv = event['hdiv']
    else:
      hdiv = ""

    neutral_site = rpi.is_neutral_site(event_id)

    #scoreboard.append({ '_id': event_id, 'vname': vname, 'vcode': vcode, 'vscore': vscore, 'hname': hname, 'hcode': hcode, 'hscore': hscore, 'gdate': gdate, 'gtime': gtime,
    #                   'gtlink': gtlink, 'vconf': vconf, 'vdiv': vdiv, 'hconf': hconf, 'hdiv': hdiv })
    #scrbd = { '_id': event_id, 'vname': vname, 'vcode': vcode, 'vscore': vscore, 'hname': hname, 'hcode': hcode, 'hscore': hscore, 'gdate': gdate, 'gtime': gtime,
    #          'gtlink': gtlink, 'vconf': vconf, 'vdiv': vdiv, 'hconf': hconf, 'hdiv': hdiv }
    game = db.scoreboard.find_one({'_id': event_id})

    if game is None:
      print 'Inserting ' + event_id + ': ' + vname + ' vs. ' + hname + ' on ' + gdate + ', with score: (' + str(vscore) + '-' + str(hscore) + ') into the database.'
      db.scoreboard.insert({'_id': event_id, 'vname': vname, 'vcode': vcode, 'vscore': vscore, 'hname': hname, 'hcode': hcode, 'hscore': hscore, 'gdate': gdate, 'gtime': gtime,
        'gtlink': gtlink, 'vconf': vconf, 'vdiv': vdiv, 'hconf': hconf, 'hdiv': hdiv, 'neutral_site': neutral_site, 'umpires': umpires, 'venue': venue_info})
    else:
      game = db.scoreboard.find_one({'_id': event_id, 'hcode': hcode, 'vcode': vcode, 'vscore': vscore, 'hscore': hscore, 'neutral_site': neutral_site, 'umpires': umpires})

      if game is None:
        print 'Updating database for ' + event_id # + ': with a new score. '  + vname + ', ' + str(vscore) + ', ' + hname + ' ' + str(hscore) + '.'
        db.scoreboard.update({ '_id': event_id}, {'$set': {'vname': vname, 'vcode': vcode, 'vconf': vconf, 'hname': hname, 'hcode': hcode , 'hconf': hconf, 'gdate': gdate, 'gtime': gtime, 'gtlink': gtlink, 'vdiv': vdiv, 'hdiv': hdiv, 'vscore': vscore, 'hscore': hscore, 'neutral_site': neutral_site, 'umpires': umpires, 'venue': venue_info}}, upsert=True)


get_scoreboard(sys.argv[1])
