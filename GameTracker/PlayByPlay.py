from bs4 import BeautifulSoup
from urllib2 import urlopen


class PlayByPlay:
  'PlayByPlay output for CSTV/GameTracker'

  def __init__(self, event_id):
    self.event_id = event_id

  def __inning_output(self, line, pad, output):
    inn = 1
    for inning in line:
      if len(pad) > 0:
        for ip in pad:
          if ip['inn'] == inn:
            if ip['inn'] > 1:
              if inning == 'X':
                output = output + ' ' + str(inning)
              else:
                if inning > 9:
                  output = output + '  ' + str(inning)
                  break
                else:
                  if inn > 9:
                    output = output + ' ' * ip['pad'] + ' ' + str(inning)
                  else:
                    output = output + ' ' * ip['pad'] + str(inning)
                  break
            else:
              output = output + ' ' * ip['pad'] + str(inning)
              break
      else:
        output = output + ' ' + str(inning)
      inn = inn + 1

    return output

  def __spacing(self, vt, ht, output, lob=False):
    if lob is True:
      padding = '  '
    else:
      padding = ' '

    if vt > 9 or ht > 9:
      if vt > 9 and ht <= 9:
        output = output + padding + str(vt)
      elif ht > 9 and vt <= 9:
        output = output + padding + ' ' + str(vt)
      else:
        output = output + padding + str(vt)
    else:
      output = output + padding + str(vt)

    return output

  def __rhelob_spacing(self, vtr, vth, vte, vtlob, htr, hth, hte, htlob, output):
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
      output = output + ' LOB'
    else:
      output = output + ' LOB'

    return output

  def playbyplay(self):
    url = 'http://origin.livestats.www.cstv.com/livestats/data/m-basebl/' + self.event_id + '/play_by_play.xml'
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
          output = output + '\nTop ' + inn
        else:
          home = bat['id']
          output = output + '\nBot ' + inn

        for play in bat.findAll('play'):
          output = output + '\n\t' + play.find('narrative')['text']

        inning_summary = bat.find('innsummary')

        r = int(inning_summary['r'])
        h = int(inning_summary['h'])
        e = int(inning_summary['e'])
        lob = int(inning_summary['lob'])

        output = output + '\n\n' + str(r) + ' runs ' + str(h) + ' hits ' + str(e) + ' errors and ' + str(lob) + ' left on base.\n'

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

    output = output + '\n'

    # special case for 10 or more runs in the 1st inning
    if hline[0] > 9 or vline[0] > 9:
      home = home + ' '
      visitor = visitor + ' '
    #

    if len(home) > len(visitor):
      padding = len(home)
      visitor = visitor + ' ' * (padding - len(visitor))
    elif len(visitor) > len(home):
      padding = len(visitor)
      home = home + ' ' * (padding - len(home))
    else:
      padding = len(home)

    output = output + ' ' * padding

    inn_pad = []
    inn = 1

    for inning in vline:
      if inning > 9:
        inn_pad.append({'inn': inn, 'pad': 2})
      else:
        inn_pad.append({'inn': inn, 'pad': 1})
      inn = inn + 1

    inn = 1
    for inning in hline:
      if inning == 'X':
        inning = 0
      if inning > 9:
        inn_pad.append({'inn': inn, 'pad': 2})
      else:
        inn_pad.append({'inn': inn, 'pad': 1})
      inn = inn + 1

    inn_pad = {ip['inn']: ip for ip in inn_pad}.values()

    for inning in range(1, total_innings + 1):
      if len(inn_pad) > 0:
        for ip in inn_pad:
          if ip['inn'] == inning:
            if ip['pad'] == 2:
              output = output + '  ' + str(inning)
            else:
              output = output + ' ' + str(inning)
      else:
        output = output + ' ' + str(inning)

    output = self.__rhelob_spacing(vtr, vth, vte, vtlob, htr, hth, hte, htlob, output)

    output = output + '\n' + visitor
    output = self.__inning_output(vline, inn_pad, output)
    output = output + ' '
    output = self.__spacing(vtr, htr, output)
    output = self.__spacing(vth, hth, output)
    output = self.__spacing(vte, hte, output)
    output = self.__spacing(vtlob, htlob, output, True)

    output = output + '\n' + home
    output = self.__inning_output(hline, inn_pad, output)
    output = output + ' '
    output = self.__spacing(htr, vtr, output)
    output = self.__spacing(hth, vth, output)
    output = self.__spacing(hte, vte, output)
    output = self.__spacing(htlob, vtlob, output, True)

    return output
