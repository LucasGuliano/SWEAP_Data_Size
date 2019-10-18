# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import glob
import csv
#set the data allocation path
data_ALC_path = '/psp/data/teams/psp_soc/orbit_'

#Read in orbit dates from saved text file
Dates_of_Orbits = open('Dates_of_Orbits.txt', 'r').read()

#function to determine how much data was used for each orbit
def data_size(Orbit_Dates):
    Orbit_Dates = eval(Orbit_Dates)
    Data_Usage = []
    #Get the info for each orbit date range (last orbit will not yet have an end date so is skipped)
    for ORBS in range(len(Orbit_Dates)-1):
        Date_Range = Orbit_Dates[ORBS]
        start_year =Date_Range[1]
        end_year = Date_Range[3]
        start_day =Date_Range[2]
        end_day = Date_Range[4]

        total = 0 
        #If the orbit is fully in one year
        if start_year == end_year:
            #match the file structure for each day of year
            for jdate in range(start_day,end_day):
                if jdate < 10:
                    data_folder_name = '00'+str(jdate)
                if jdate >= 10 and jdate<100:
                    data_folder_name = '0'+str(jdate)  
                if jdate >= 100:
                    data_folder_name = str(jdate) 
                #set the path to look for EA files
                path = '/psp/data/moc_data_products/ssr_telemetry/'+str(end_year)+'/'+data_folder_name
                #Only operate on folders that exist (some are missing so important to check)
                if os.path.isdir(path) == True:
                    for path, dirs, files in os.walk(path):
                        for f in files:
                            #ignore these files that show up
                            if f != '.DS_Store':
                                fp = os.path.join(path, f)
                                #All SWEAP data ends with EA 
                                if fp[-2:] == 'EA':
                                   total += os.path.getsize(fp)
       
        #if the orbit spans multuple years, slice it and get the files from both sections
        else:  
            for jdate in range(start_day,365):
                if jdate < 10:
                    data_folder_name = '00'+str(jdate)
                if jdate >= 10 and jdate<100:
                    data_folder_name = '0'+str(jdate)  
                if jdate >= 100:
                    data_folder_name = str(jdate) 
                
                path = '/psp/data/moc_data_products/ssr_telemetry/'+str(start_year)+'/'+data_folder_name
                if os.path.isdir(path) == True:
                    for path, dirs, files in os.walk(path):
                        for f in files:
                            if f != '.DS_Store':
                                fp = os.path.join(path, f)
                                if fp[-2:] == 'EA':
                                    total += os.path.getsize(fp)
                                    
            for jdate in range(1,end_day):
                if jdate < 10:
                    data_folder_name = '00'+str(jdate)
                if jdate >= 10 and jdate<100:
                    data_folder_name = '0'+str(jdate)  
                if jdate >= 100:
                    data_folder_name = str(jdate) 
                
                path = '/psp/data/moc_data_products/ssr_telemetry/'+str(end_year)+'/'+data_folder_name
                if os.path.isdir(path) == True:
                    for path, dirs, files in os.walk(path):
                        for f in files:
                            if f != '.DS_Store':
                                fp = os.path.join(path, f)
                                if fp[-2:] == 'EA':
                                    total += os.path.getsize(fp)
            
        #Convert from bytes to gigaBites
        total = total/(1.25*100000000)
        
        #Save the total data for each orbit  (writes as gigaBites)
        Data_Info = Date_Range[0], start_year, end_year, start_day, end_day, total
        Data_Usage.append(Data_Info)   
            
    return Data_Usage

#function to determine the allocated amount of data for each orbit
def data_allocation(Orbit_Number,Sub_Orbit):
    #match folder structure 
    if Orbit_Number <10:
        Orbit_Folder = '0'+str(Orbit_Number) 
        Sub_Orbit = '0'+Sub_Orbit
    else:
        Orbit_Folder = str(Orbit_Number)
        
    #grab every data allocation file for the given orbit
    Orbit_Path = data_ALC_path + Orbit_Folder+'/SPWG/'
    data_files_list = glob.glob(Orbit_Path+'DVPS_'+Sub_Orbit+'*')
    
    #if none exist (hopefully they will) then record N/A
    if len(data_files_list) < 1:
        return 'N/A'
    
    #get the most recent file and grab the info on data allocation 
    correct_data_file = data_files_list[-1]
    with open(correct_data_file) as alc_csv:
        alc_csv = csv.reader(alc_csv,delimiter=',')
        data_alc_list = list(alc_csv)[1]
        SWEAP_Data_alc = data_alc_list[2]
    
    return SWEAP_Data_alc

#function to write the results and display
def data_printer(Orbit_Dates):
    #create lists to write to the CSV file later
    Orbit_Line = []
    Start_Line = []
    End_Line = []
    DA_Line = []
    DU_Line = []
    Percent_Line = []
    #populate the lists
    for i in range(len(data_usage)):
        Orbit_Line.append(data_usage[i][0])
        Start_Line.append(str(data_usage[i][1])+'-'+str(data_usage[i][3]))
        End_Line.append(str(data_usage[i][2])+'-'+str(data_usage[i][4]))
        DU_Line.append(str(data_usage[i][5]))
        
    #Data allocation files are sorted by numbered orbit, so need to look for orbits without the letter included
    for i in range(len(Orbit_Line)):
        orbit_number = Orbit_Line[i].split('A')[0].split('B')[0].split('C')[0].split('D')[0]
        
        # if orbit is without a letter, search for orbit+A first, then if empty search for just orbit
        if Orbit_Line[i] == orbit_number:
            SWEAP_Data_Alc = data_allocation(int(orbit_number), Orbit_Line[i].strip()+'A')
            if SWEAP_Data_Alc == 'N/A':
                 SWEAP_Data_Alc = data_allocation(int(orbit_number), Orbit_Line[i].split()[0])
        
        #B and beyond orbits can be handled normally
        else:
            SWEAP_Data_Alc = data_allocation(int(orbit_number), Orbit_Line[i].split()[0])   
        
        #populate list with results and calcualte percentage used
        DA_Line.append(SWEAP_Data_Alc) 
        if SWEAP_Data_Alc == 'N/A':
            Percent_Line.append('N/A')
        else:    
            Percent_Line.append(round(100*(float(DU_Line[i])/float(SWEAP_Data_Alc)), 2))
   #write all list data to the CSV file
    with open('data_used_SWEAP.csv', mode='w') as DU_file:
        DU_writer = csv.writer(DU_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        DU_writer.writerow(['Orbit','Start Date', 'End Date', 'SWEAP Data Allocation', 'SWEAP Data Used', 'Percentage Utilized (%)'])
        for i in range(len(Orbit_Line)):
            row = Orbit_Line[i], Start_Line[i], End_Line[i], DA_Line[i], round(float(DU_Line[i]),2), Percent_Line[i]
            DU_writer.writerow(row)

   #print out results
    data_file = open('data_used_SWEAP.csv')
    data_record = data_file.read()
    data_list = data_record.split('\r\n')
    for i in range(len(data_list)-2):
        Orbit = data_list[i+1].split(',')[0]
        Start = data_list[i+1].split(',')[1]
        Data_Alc = data_list[i+1].split(',')[3]
        Data_Used = data_list[i+1].split(',')[4]
        Percentage = data_list[i+1].split(',')[5]
        print('Orbit'+str(Orbit)+'started '+str(Start)+' and used '+str(Data_Used)+' out of '+str(Data_Alc)+ ' GigaBits ('+str(Percentage)+')')
   
    #Print out start date of most recent update
    Orbit_Dates = eval(Orbit_Dates)
    print('Orbit '+str(Orbit_Dates[-1][0])+'will begin on '+str(Orbit_Dates[-1][1])+' '+str(Orbit_Dates[-1][2]))
    
    #BONUS show how much data has been taken on the mission so far
    Grand_Total = 0
    for i in range(len(DU_Line)):
     	Grand_Total = Grand_Total + float(DU_Line[i])	
    print('Total SWEAP Data Used: '+str(round(Grand_Total,2))+' GigaBits')   
    
if __name__ == "__main__":    
    #get how much data was used in each orbit
    data_usage = data_size(Dates_of_Orbits)
    data_printer(Dates_of_Orbits)            
    
    
    
    
    
    
    
