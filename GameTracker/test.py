#! /usr/bin/env python

import pbp, Stats

okst = Stats.Stats('20140415', 'okst')
okst_pbp = pbp.PlayByPlay(okst.event_ids[0])
print okst_pbp.playbyplay()
