#!/bin/bash

#start_reg_season="20140214"
#end_reg_season="20140525"
start_reg_season="$1"
end_reg_season="$2"

this_date=$start_reg_season

until [ "$this_date" == "$end_reg_season" ]
do
  this_date=$(date --date="$this_date 1 day" +%Y%m%d)
  python getScoreboard.py $this_date
  #   python getNCAAScoreboard.py $this_date
  #   python getGameXMLData.py "okst" $this_date
done
