from bs4 import BeautifulSoup
from urllib2 import urlopen
from getGameXMLData import get_gameids
import sys


team = sys.argv[1]
gdate = sys.argv[2]

def inning_output(line, pad, output):
  inn = 1
  for inning in line:
    inn = inn + 1
    if len(pad) > 0:
      for ip in inn_pad:
        if ip['inn'] == inn:
          if ip['pad'] == 2:
            output = output + '  ' + str(inning)
        else:
          output = output + ' ' + str(inning)
    else:
      output = output + ' ' + str(inning)

  return output


def spacing(vt, ht, output):
  if vt > 9 or ht > 9:
    if vt > 9 and ht <= 9:
      output = output + ' ' + str(vt)
    elif ht > 9 and vt <= 9:
      output = output + '  ' + str(vt)
    else:
      output = output + ' ' + str(vt)
  else:
    output = output + ' ' + str(vt)

  return output


def rhelob_spacing(vtr, vth, vte, vtlob, htr, hth, hte, htlob, output):
  if vtr > 9 or htr > 9:
    output = output + '   R'
  else:
    output = output + '  R'
  if vth > 9 or hth > 9:
    output = output + '  H'
  else:
    output = output + ' H'
  if vte > 9 or hte > 9:
    output = output + '  E'
  else:
    output = output + ' E'
  if vtlob > 9 or htlob > 9:
    output = output + '  LOB'
  else:
    output = output + ' LOB'

  return output


def main():
  #html = open('/mnt/d/baseball/20140227/okst/play_by_play.xml')
  event_ids = get_gameids(team, gdate)
  game = 0
  print event_ids
  url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + event_ids[game]['event_id'] + '/play_by_play.xml'
  print url
  html = urlopen(url).read()
  soup = BeautifulSoup(html, 'lxml').findAll('inning')
  vtr = 0
  htr = 0
  vth = 0
  hth = 0
  vte = 0
  hte = 0
  vtlob = 0
  htlob = 0

  vline = []
  hline = []
  total_innings = 0
  output = ''

  for inning in soup:
    total_innings = total_innings + 1
    inn = inning['number']
    batting = inning.findAll('batting')
    for bat in batting:
      at_plate = bat['vh']
      if at_plate == 'V':
        visitor = bat['id']
        print 'Top ' + inn
      else:
        home = bat['id']
        print 'Bot ' + inn

      for play in bat.findAll('play'):
        print '\t' + play.find('narrative')['text']

      inning_summary = bat.find('innsummary')

      r = int(inning_summary['r'])
      h = int(inning_summary['h'])
      e = int(inning_summary['e'])
      lob = int(inning_summary['lob'])

      print '\n' + str(r) + ' runs ' + str(h) + ' hits ' + str(e) + ' errors and ' + str(lob) + ' left on base.'

      if at_plate == 'V':
        vline.append(r)
        vtr = vtr + r
        vth = vth + h
        hte = hte + e
        vtlob = vtlob + lob
      else:
        hline.append(r)
        htr = htr + r
        hth = hth + h
        vte = vte + e
        htlob = htlob + lob
  if len(vline) > len(hline):
    hline.append('X')

  print '\n'
  if len(home) > len(visitor):
    padding = len(home)
    visitor = visitor + ' '
  elif len(visitor) > len(home):
    padding = len(visitor)
    home = home + ' '
  else:
    padding = len(home)

  output = output + ' ' * padding

  inn_pad = []
  inn = 1

  for inning in vline:
    inn = inn + 1
    if inning > 9:
      inn_pad.append({'inn': inn, 'pad': 2})

  inn = 1
  for inning in hline:
    inn = inn + 1
    if inning == 'X':
      inning = 0
    if inning > 9:
      inn_pad.append({'inn': inn, 'pad': 2})

  inn_pad = list(set(inn_pad))

  inn = 1
  for inning in range(1, total_innings + 1):
    inn = inn + 1
    if len(inn_pad) > 0:
      for ip in inn_pad:
        if ip['inn'] == inn:
          if ip['pad'] == 2:
            output = output + '  ' + str(inning)
          else:
            output = output + ' ' + str(inning)
    else:
      output = output + ' ' + str(inning)

  output = rhelob_spacing(vtr, vth, vte, vtlob, htr, hth, hte, htlob, output)

  print output
  output = visitor
  output = inning_output(vline, inn_pad, output)
  output = output + ' '
  output = spacing(vtr, htr, output)
  output = spacing(vth, hth, output)
  output = spacing(vte, hte, output)
  output = spacing(vtlob, htlob, output)

  print output

  output = home
  output = inning_output(hline, inn_pad, output)
  output = output + ' '
  output = spacing(htr, vtr, output)
  output = spacing(hth, vth, output)
  output = spacing(hte, vte, output)
  output = spacing(htlob, vtlob, output)

  print output


main()
