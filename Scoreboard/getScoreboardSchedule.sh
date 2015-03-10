#!/bin/bash

#start_reg_season="20140214"
#end_reg_season="20140525"
if [ $# -lt 2 ]
then
  start_reg_season="$(date +%Y%m%d)"
  end_reg_season="$start_reg_season"
else
  start_reg_season="$1"
  end_reg_season="$2"
fi

this_date=$start_reg_season

until [ "$this_date" -gt "$end_reg_season" ]
do
  python getScoreboard.py $this_date
  if [ "$(uname)" == "Darwin" ]
  then
    this_date=$(date -v+1d -jf %Y%m%d "${this_date}" +%Y%m%d)
  else
    this_date=$(date --date="$this_date 1 day" +%Y%m%d)
  fi
  #   python getNCAAScoreboard.py $this_date
  #   python getGameXMLData.py "okst" $this_date
done
