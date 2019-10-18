#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 17:25:19 2019

@author: lguliano
"""

def RAT_Hunter(RAT_list):
    #search for all encounter labels in seperated text output
    Encounter_List = [' 1 ',' 1A ',' 1B ',' 1C ',' 1D ',' 2 ',' 2A ',' 2B ',' 2C ',' 2D ',' 3 ',' 3A ',' 3B ',' 3C ',' 3D ',' 4 ',' 4A ',' 4B ',' 4C ',' 4D ',' 5 ',' 5A ',' 5B ',' 5C ',' 5D ',' 6 ',' 6A ',' 6B ',' 6C ',' 6D ',' 7 ',' 7A ',' 7B ',' 7C ',' 7D ',' 8 ',' 8A ',' 8B ',' 8C ',' 8D ',' 9 ',' 9A ',' 9B ',' 9C ',' 9D ',' 10 ',' 10A ',' 10B ',' 10C ',' 10D ',' 11 ',' 11A ',' 11B ',' 11C ',' 11D ',' 12 ',' 12A ',' 12B ',' 12C ',' 12D ',' 13 ',' 13A ',' 13B ',' 13C ',' 13D ',' 14 ',' 14A ',' 14B ',' 14C ',' 14D ',' 15 ',' 15A ',' 15B ',' 15C ',' 15D ',' 16 ',' 16A ',' 16B ',' 16C ',' 16D ',' 17 ',' 17A ',' 17B ',' 17C ',' 17D ',' 18 ',' 18A ',' 18B ',' 18C ',' 18D ',' 19 ',' 19A ',' 19B ',' 19C ',' 19D ',' 20 ',' 20A ',' 20B ',' 20C ',' 20D ',' 21 ',' 21A ',' 21B ',' 21C ',' 21D ',' 22 ',' 22A ',' 22B ',' 22C ',' 22D ',' 23 ',' 23A ',' 23B ',' 23C ',' 23D ',' 24 ',' 24A ',' 24B ',' 24C ',' 24D ',' 25 ',' 25A ',' 25B ',' 25C ',' 25D ',' 26 ',' 26A ',' 26B ',' 26C ',' 26D ',' 27 ',' 27A ',' 27B ',' 27C ',' 27D ',' 28 ',' 28A ',' 28B ',' 28C ',' 28D ',' 29 ',' 29A ',' 29B ',' 29C ',' 29D ']
    # make a list of every result found with the grep search for " RAT "
    RAT_Updates = RAT_list.split('ORB_')
    RAT_Updates = RAT_Updates[1:len(RAT_Updates)]
    Orbit_List = []
    
    #Check which of the orbits actaully has data for it/exists then create a list of those orbits
    for i in range(len(Encounter_List)):
        if any(Encounter_List[i] in s for s in RAT_Updates):
            Orbit_List.append(Encounter_List[i])
   
    #Treat orbits labeled a A the same as orbits labeled with just the number
    Removal_list = []
    for i in range(len(Orbit_List)-1):
        if Orbit_List[i+1].split(' ')[1] == Orbit_List[i].split(' ')[1]+'A':
            Removal_list.append(Orbit_List[i]) 
    for i in range(len(Removal_list)):
        Orbit_List.remove(Removal_list[i])
    
    #Get the start and end date of each encounter
    Date_List = []
    Start_List = []
    for i in range(len(Orbit_List)):
       RAT_List = []
       for j in range(len(RAT_Updates)):
           if Orbit_List[i] in RAT_Updates[j] or Orbit_List[i].split(' ')[1]+'A' in RAT_Updates[j] :
               RAT_List.append(RAT_Updates[j])
       
       Encounter_Start_File = RAT_List[-1]
       Start_Year = int(Encounter_Start_File.split(':')[1].split(':')[0])
       Start_Date = int(Encounter_Start_File.split(':')[2].split(' ')[0])
       Starts = [Start_Year, Start_Date]
       Start_List.append(Starts)

       with  open('RAT_List.txt','a') as RAT_file:
           RAT_file.write(Orbit_List[i].strip()+'\n')
           RAT_file.write(Encounter_Start_File.strip()+'\n')
           RAT_file.close()
         
    for i in range(len(Start_List)-1):
        data_entry = Orbit_List[i],Start_List[i][0],Start_List[i][1],Start_List[i+1][0],Start_List[i+1][1]
        Date_List.append(data_entry)
    #the last orbit wont have a set end yet, so set to a huge number  
    data_entry= Orbit_List[-1],Start_List[-1][0],Start_List[-1][1], '999', '999'   
    Date_List.append(data_entry)
    
    print(Date_List)
    return Date_List

if __name__ == "__main__":
    #Get results of serach for RAT uploads from text file saving results
    RAT_List = open('RAT_List.txt', 'r').read()
    RAT_Hunter(RAT_List)
