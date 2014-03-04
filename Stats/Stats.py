#! /usr/bin/env python

from urllib2 import urlopen
from bs4 import BeautifulSoup

class Stats:
  'Stats class for CSTV/GameTracker'

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
    record = [w,l]

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


  def getTeamHittingStats(self):
    hitting = self.team.find('totals').find('hitting')
    ab = int(hitting['ab'])
    r = int(hitting['r'])
    h = int(hitting['h'])
    rbi = int(hitting['rbi'])
    double = int(hitting['double'])
    triple = int(hitting['triple'])
    hr = int(hitting['hr'])
    bb = int(hitting['bb'])
    so = int(hitting['so'])
    hbp = int(hitting['hbp'])
    sb = int(hitting['sb'])
    cs = int(hitting['cs'])
    sh = int(hitting['sh'])
    gdp = int(hitting['gdp'])
    picked = int(hitting['picked'])
    hitdp = int(hitting['hitdp'])
    ground = int(hitting['ground'])
    fly = int(hitting['fly'])

    hitting_stats = dict(ab=ab, r=r, h=h, rbi=rbi, doubles=double, triples=triple, hr=hr,
                         bb=bb, so=so, hbp=hbp, sb=sb, cs=cs, sh=sh, gidp=gdp, pickoff=picked,
                         hitdp=hitdp, gout=ground, fout=fly)

    return hitting_stats


  def getTeamPitchingStats(self):
    pitching = self.team.find('totals').find('pitching')
    ip = float(pitching['ip'])
    h = int(pitching['h'])
    r = int(pitching['r'])
    er = int(pitching['er'])
    bb = int(pitching['bb'])
    so = int(pitching['so'])
    bf = int(pitching['bf'])
    ab = int(pitching['ab'])
    double = int(pitching['double'])
    triple = int(pitching['triple'])
    wp = int(pitching['wp'])
    bk = int(pitching['bk'])
    hbp = int(pitching['hbp'])
    kl = int(pitching['kl'])
    fly = int(pitching['fly'])
    ground = int(pitching['ground'])

    pitching_stats = dict(ip=ip, h=h, r=r, er=er, bb=bb, so=so, bf=bf, ab=ab,
                          doubles=double, triples=triple, wp=wp, bk=bk, kl=kl,
                          fout=fly, gout=ground)


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


#  def main():
#
#    visitor = soup.find('team', attrs={'vh': 'V'})
#    home = soup.find('team', attrs={'vh': 'H'})
