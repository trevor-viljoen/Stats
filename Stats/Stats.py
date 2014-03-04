#! /usr/bin/env python

from urllib2 import urlopen
from bs4 import BeautifulSoup


class Stats:
  'Stats class for CSTV/GameTracker'
  DEBUG = False

  def __init__(self, date, code, home_visitor):
    self.date = date
    self.code = code
    self.setHomeOrVisitor(home_visitor)
    self.rank = self.getRank()
    self.record = self.getRecord()
    self.name = self.getName()
    self.runs = self.getRuns()
    self.hits = self.getHits()
    self.errors = self.getErrors()
    self.linescore = self.getLinescore()

  def debug(self):
    Stats.DEBUG = True

  def setSoup(self):
    event_ids = self.getEventIDs()
    if len(event_ids) == 1:
      event_id = event_ids[0]
      url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + event_id + '/player_stats.xml'
      html = urlopen(url).read()
      print url

      soup = BeautifulSoup(html, 'lxml')

      return soup

  def setHomeOrVisitor(self, home_visitor):
    soup = self.setSoup()
    if home_visitor == 'visitor':
      self.team = soup.find('team', attrs={'vh': 'V'})
    elif home_visitor == 'home':
      self.team = soup.find('team', attrs={'vh': 'H'})

  def getEventIDs(self):
    event_ids = []
    url = 'http://livestats.www.cstv.com/scoreboards/' + self.date + '-m-basebl-scoreb.xml'
    print url

    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    events = soup.findAll('event')

    for event in events:
        if event['hcode'] == self.code:
          event_ids.append(event['event_id'])
        if event['vcode'] == self.code:
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

  def getBattingStats(self):
    hitting = self.team.find('totals').find('hitting')

    if hitting.has_attr('ab'):
      ab = int(hitting['ab'])
    else:
      ab = 0
    if hitting.has_attr('r'):
      r = int(hitting['r'])
    else:
      r = 0
    if hitting.has_attr('h'):
      h = int(hitting['h'])
    else:
      h = 0
    if hitting.has_attr('rbi'):
      rbi = int(hitting['rbi'])
    else:
      rbi = 0
    if hitting.has_attr('double'):
      double = int(hitting['double'])
    else:
      double = 0
    if hitting.has_attr('triple'):
      triple = int(hitting['triple'])
    else:
      triple = 0
    if hitting.has_attr('hr'):
      hr = int(hitting['hr'])
    else:
      hr = 0
    if hitting.has_attr('bb'):
      bb = int(hitting['bb'])
    else:
      bb = 0
    if hitting.has_attr('so'):
      so = int(hitting['so'])
    else:
      so = 0
    if hitting.has_attr('hbp'):
      hbp = int(hitting['hbp'])
    else:
      hbp = 0
    if hitting.has_attr('sb'):
      sb = int(hitting['sb'])
    else:
      sb = 0
    if hitting.has_attr('cs'):
      cs = int(hitting['cs'])
    else:
      cs = 0
    if hitting.has_attr('sh'):
      sh = int(hitting['sh'])
    else:
      sh = 0
    if hitting.has_attr('gdp'):
      gdp = int(hitting['gdp'])
    else:
      gdp = 0
    if hitting.has_attr('picked'):
      picked = int(hitting['picked'])
    else:
      picked = 0
    if hitting.has_attr('hitdp'):
      hitdp = int(hitting['hitdp'])
    else:
      hitdp = 0
    if hitting.has_attr('ground'):
      ground = int(hitting['ground'])
    else:
      ground = 0
    if hitting.has_attr('fly'):
      fly = int(hitting['fly'])
    else:
      fly = 0

    hitting_stats = dict(ab=ab, r=r, h=h, rbi=rbi, doubles=double, triples=triple, hr=hr,
                         bb=bb, so=so, hbp=hbp, sb=sb, cs=cs, sh=sh, gidp=gdp, pickoff=picked,
                         hitdp=hitdp, gout=ground, fout=fly)

    return hitting_stats

  def getPitchingStats(self):
    pitching = self.team.find('totals').find('pitching')

    if pitching.has_attr('ip'):
      ip = float(pitching['ip'])
    else:
      ip = 0.0
    if pitching.has_attr('h'):
      h = int(pitching['h'])
    else:
      h = 0
    if pitching.has_attr('r'):
      r = int(pitching['r'])
    else:
      r = 0
    if pitching.has_attr('er'):
      er = int(pitching['er'])
    else:
      er = 0
    if pitching.has_attr('bb'):
      bb = int(pitching['bb'])
    else:
      bb = 0
    if pitching.has_attr('so'):
      so = int(pitching['so'])
    else:
      so = 0
    if pitching.has_attr('bf'):
      bf = int(pitching['bf'])
    else:
      bf = 0
    if pitching.has_attr('ab'):
      ab = int(pitching['ab'])
    else:
      ab = 0
    if pitching.has_attr('double'):
      double = int(pitching['double'])
    else:
      double = 0
    if pitching.has_attr('triple'):
      triple = int(pitching['triple'])
    else:
      triple = 0
    if pitching.has_attr('wp'):
      wp = int(pitching['wp'])
    else:
      wp = 0
    if pitching.has_attr('bk'):
      bk = int(pitching['bk'])
    else:
      bk = 0
    if pitching.has_attr('hbp'):
      hbp = int(pitching['hbp'])
    else:
      hbp = 0
    if pitching.has_attr('kl'):
      kl = int(pitching['kl'])
    else:
      kl = 0
    if pitching.has_attr(''):
      fly = int(pitching['fly'])
    else:
      fly = 0
    if pitching.has_attr(''):
      ground = int(pitching['ground'])
    else:
      ground = 0

    pitching_stats = dict(ip=ip, h=h, r=r, er=er, bb=bb, so=so, bf=bf, ab=ab,
                          doubles=double, triples=triple, wp=wp, bk=bk, hbp=hbp,
                          kl=kl, fout=fly, gout=ground)

    return pitching_stats

  def isNeutral(self, other):
    if self.team['neutralgame'] == 'Y' and other.team['neutralgame'] == 'Y':
      neutralgame = True
    else:
      neutralgame = False

    return neutralgame

  def info(self):
    self.id = self.team['id']
    self.name = self.team['name']
    self.code = self.team['code']
    self.rank = self.team['rank']
    self.record = self.team['record'].split('-')

    return dict(id=self.id, name=self.name, code=self.code, rank=self.rank,
                record=self.record)
