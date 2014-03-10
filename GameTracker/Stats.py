#! /usr/bin/env python

from urllib2 import urlopen
from bs4 import BeautifulSoup
import json
import sys
import re


class Stats:
  'Stats class for CSTV/GameTracker'
  __DEBUG = False

  def init_game(self, event_id):
    self.soup = self.__setSoup(event_id)
    self.__isHomeVisitor(self.home_visitor, event_id)
    self.__setTeam(event_id)
    if self.team is not None:
      self.rank = self.getRank()
      self.record = self.getRecord()
      self.name = self.getName()
      self.runs = self.getRuns()
      self.hits = self.getHits()
      self.errors = self.getErrors()
      self.linescore = self.getLinescore()
      self.pitching = self.getPitchingStats()
      self.hitting = self.getHittingStats()
      self.order = self.getBattingOrder()
      self.lineup = self.getStarters()
      self.info = self.getInfo()
      self.situational_hitting = self.getHSitSummary()
      self.fielding = self.getFieldingStats()

  def __init__(self, date, code, event_id = None):
    self.num_games = 0
    self.home_visitor = []
    self.team = None
    self.ishome = False
    self.isvisitor = False
    self.date = date
    self.code = code
    self.event_ids = self.__getEventIDs()
    self.num_games = len(self.event_ids)
    if event_id is None:
      if self.num_games == 1:
        self.soup = self.__setSoup(self.event_ids[0])
        self.__setTeam(self.event_ids[0])
    else:
      self.soup = self.__setSoup(event_id)
      self.__setTeam(event_id)
    if self.team is not None:
      self.rank = self.getRank()
      self.record = self.getRecord()
      self.name = self.getName()
      self.runs = self.getRuns()
      self.hits = self.getHits()
      self.errors = self.getErrors()
      self.linescore = self.getLinescore()
      self.pitching = self.getPitchingStats()
      self.hitting = self.getHittingStats()
      self.order = self.getBattingOrder()
      self.lineup = self.getStarters()
      self.info = self.getInfo()
      self.situational_hitting = self.getHSitSummary()
      self.fielding = self.getFieldingStats()

  def debug(self):
    Stats.__DEBUG is True

  def __isHomeVisitor(self, hvlist, event_id):
    for game in hvlist:
      if game['event_id'] == event_id:
          if game.has_key('home'):
            self.ishome = True
            self.isvisitor = False
            self.opponent = game['ocode']
          elif game.has_key('visitor'):
            self.isvisitor = True
            self.ishome = False
            self.opponent = game['ocode']

  def __setSoup(self, eid):
    if eid is not None:
      event_id = eid
      url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + event_id + '/player_stats.xml'
      html = urlopen(url).read()
      if Stats.__DEBUG is True:
        print url
      soup = BeautifulSoup(html, 'lxml')
    else:
      soup = None

    return soup

  def __setTeam(self, event_id):
    if self.soup is not None:
      if self.ishome:
        self.team = self.soup.find('team', {'vh': 'H'})
      elif self.isvisitor:
        self.team = self.soup.find('team', {'vh': 'V'})
    else:
      self.team = None

  def __getEventIDs(self):
    event_ids = []
    url = 'http://livestats.www.cstv.com/scoreboards/' + self.date + '-m-basebl-scoreb.xml'

    if Stats.__DEBUG is True:
      print url

    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    events = soup.findAll('event')

    for event in events:
      if event['hcode'] == self.code:
        self.home = self.home_visitor.append(dict(event_id=event['event_id'], home=True, ocode=event['vcode']))
        event_ids.append(event['event_id'])
      if event['vcode'] == self.code:
        self.visitor = self.home_visitor.append(dict(event_id=event['event_id'], visitor=True, ocode=event['hcode']))
        event_ids.append(event['event_id'])

    return event_ids

  def getStarters(self):
    starting_lineup = []
    starters = self.team.find('starters').findAll('starter')

    for starter in starters:
      spot = int(starter['spot'])
      name = str(starter['name'])
      number = int(starter['uni'])
      position = str(starter['pos'])

      starting_lineup.append(dict(spot=spot, name=name, number=number, position=position))

    return starting_lineup

  def getBattingOrder(self):
    batting_order = []
    ba_order = self.team.find('batords').findAll('batord')

    for player in ba_order:
      spot = int(player['spot'])
      name = str(player['name'])
      number = int(player['uni'])
      position = str(player['pos'])

      batting_order.append(dict(spot=spot, name=name, number=number, position=position))

    return batting_order

  def getCode(self):
    code = str(self.team['code']).lower()

    return code

  def getName(self):
    name = str(self.team['name'])

    return name

  def getRank(self):
    rank = int(self.team['rank'])

    return rank

  def getRecord(self):
    w = int(self.team['record'].split('-')[0])
    l = int(self.team['record'].split('-')[1])
    record = [w, l]

    return record

  def getLinescore(self):
    linescore = self.team.find('linescore')['line']

    return linescore.split(',')

  def getRuns(self):
    runs = int(self.team.find('linescore')['runs'])

    return runs

  def getHits(self):
    hits = int(self.team.find('linescore')['hits'])

    return hits

  def getErrors(self):
    errors = int(self.team.find('linescore')['errs'])

    return errors

  def getLOB(self):
    lob = int(self.team.find('linescore')['lob'])

    return lob

  def getHittingStats(self):
    'Situational Hitting Summary'
    return self.__getAttrs('hitting')

  def getPitchingStats(self):
    'Fielding Stats'
    return self.__getAttrs('pitching')

  def getFieldingStats(self):
    'Fielding Stats'
    return self.__getAttrs('fielding')

  def getHSitSummary(self):
    'Situational Hitting Summary'
    return self.__getAttrs('hsitsummary')

  def getPSitSummary(self):
    'Situational Pitching Summary'
    return self.__getAttrs('psitsummary')

  def __maptotype(self, v):
    if len(re.findall('^[0-9]*\.[0-9]+$', v)) > 0:
      return float(v)
    elif len(re.findall('^[0-9]+$', v)) > 0:
      return int(v)
    else:
      return str(v)

  def __getAttrs(self, stat):
    hk = []
    hv = []
    vl = []
    stats = self.team.find('totals').find(stat)

    for k, v in stats.attrs.iteritems():
      vx = v.split(',')
      vxr = vx
      if len(vx) > 1:
        for i in range(0, vx.count(',')):
          vxr = vx.remove(',')
        vl = [self.__maptotype(x) for x in vxr]

        hk.append(k)
        hv.append(vl)
      else:
        hk.append(k)
        hv.append(self.__maptotype(v))

    return dict(zip(hk, hv))

  def __getPlayerAttrs(self, player):
    hk = []
    hv = []
    vl = []

    for k, v in player.attrs.iteritems():
      if type(v) is list:
        if len(v) == 1:
          v = v[0]
      if k == 'shortname':
        vx = v
        hk.append(k)
        hv.append(self.__maptotype(v))
      else:
        vx = v.split(',')
        vxr = vx
        if len(vx) > 1:
          for i in range(0, vx.count(',')):
            vxr = vx.remove(',')
          vl = [self.__maptotype(x.strip()) for x in vxr]

          hk.append(k)
          hv.append(vl)
        else:
          hk.append(k)
          hv.append(self.__maptotype(v))

    return dict(zip(hk, hv))

  def __isNeutral(self, other):
    if self.team['neutralgame'] == 'Y' and other.team['neutralgame'] == 'Y':
      neutralgame = True
    else:
      neutralgame = False

    return neutralgame

  def isHomeTeam(self):
    return self.home

  def isVisitingTeam(self):
    return self.visiting

  def getPlayerStats(self, name):
    player_name = self.team.find('player')['name']
    #for player in players:

      #player_stats.append(self.__getPlayerAttrs(player))
    return player_name

  def getRoster(self):
    roster = []
    players = self.team.findAll('player')

    for player in players:
      roster.append(self.__getPlayerAttrs(player))

    return roster

  def getInfo(self):
    self.id = self.team['id']
    self.name = self.team['name']
    self.code = self.team['code']
    self.rank = self.team['rank']
    self.record = self.team['record'].split('-')

    return dict(id=self.id, name=self.name, code=self.code, rank=self.rank,
                record=self.record)

  def pretty(self, obj):
    try:
      print json.dumps(obj, indent=4)
    except:
        sys.exc_info()[0]
