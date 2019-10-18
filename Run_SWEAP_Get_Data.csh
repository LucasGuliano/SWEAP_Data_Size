#!/bin/tcsh
cd /psp/data/moc_data_products/orbit_activity_file/
set filelist=`grep 'SWEAP_ALLOC=' */ORB_*.oaf`
cd /home/lguliano/Data_Size
echo ${filelist} > RAT_List.txt
set dates=`python RAT_Hunter.py`
echo ${dates} > Dates_of_Orbits.txt
python SWEAP_Data_Size.py

#end 