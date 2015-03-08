from GameTracker.Stats import Stats
from GameTracker.PlayByPlay import PlayByPlay
import time

today = time.strftime("%Y%m%d")

okst = Stats(today, 'okst')
okst_pitching = okst.pitching
okst_hitting = okst.hitting
okst_info = okst.info
okst_runs = okst.runs
okst_hits = okst.hits
okst_erorrs = okst.errors
okst_linescore = okst.linescore
okst_situational_hitting = okst.situational_hitting
okst_opponent = okst.opponent

print "Hitting: "
print okst_hitting
print "Situational Hitting: "
print okst_situational_hitting

print "Pitching: "
print okst_pitching

okst_event_ids = okst.event_ids  # list of games for that day

okst_pbp = PlayByPlay(okst_event_ids[0])
print okst_pbp.playbyplay()
