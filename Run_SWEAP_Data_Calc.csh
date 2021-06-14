#!/bin/tcsh

#1. Set up directory where script is located
#2. Change to folder on Laz containing the orbit activity files
#3. Search for OAF files
#4. Change back to SWEAP_Data_Calc folder
#5. Write OAF files to text file for storage
#6. Run Python RAT Hunter script to get dates based on RAT updates in OAF files
#7. Write orbit dates to text file
#8. Calculate data size with Python script (prints and writes to CSV)

set SWEAP_Data_Work_Dir = `pwd`
cd /psp/data/moc_data_products/orbit_activity_file/
set filelist=`grep 'SWEAP_ALLOC=' */ORB_*.oaf`
cd /${SWEAP_Data_Work_Dir}
echo ${filelist} > RAT_List.txt
set dates=`python RAT_Hunter.py`
echo ${dates} > Dates_of_Orbits.txt
python SWEAP_Data_Size.py

#end 
