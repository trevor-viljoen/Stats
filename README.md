Example usage:
```python
  import Stats
  import pbp
  
  okst = Stats.Stats('20140302', 'okst')
  okst_pitching = okst.pitching
  okst_hitting = okst.hitting
  okst_info = okst.info
  okst_runs = okst.runs
  okst_hits = okst.hits
  okst_erorrs = okst.errors
  okst_linescore = okst.linescore
  okst_situational_hitting = okst.situationl_hitting
  okst_opponent = okst.opponent
  
  okst_event_ids = okst.event_ids  # list of games for that day
  
  okst_pbp = pbp.PlayByPlay(okst_event_ids[0])
  print okst_pbp.playbyplay()
```
## Demo:

![gif](http://i.imgur.com/bjvmGhq.gif)
