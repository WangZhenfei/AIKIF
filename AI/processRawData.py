# processRawData.py   written by Duncan Murray 16/3/2014  (C) Acute Software
# script to process raw data into core tables in AIKIF, like events processes
#
# Currently hard coded to read in File and PC usage data (from a test set)
    # fullFilename,name,path,size,date,
    # "T:\user\dev\src\python\AI\tests\test_AIKIF.py","test_AIKIF.py","T:\user\dev\src\python\AI\tests","542","2014-02-27 23:31:42",
    # "P:\events\Christmas2013\20131225_075917.jpg","20131225_075917.jpg","P:\events\Christmas2013","2826606","2013-12-25 07:59:16",
    # "P:\events\Christmas2013\20131225_090017.jpg","20131225_090017.jpg","P:\events\Christmas2013","2655624","2013-12-25 09:00:16",

 
import os
import sys
import csv
import time
from datetime import datetime
sys.path.append('..//..//_AS_LIB')
import as_util_data as dat
import AIKIF_utils as aikif

rawData_fileList = r"T:\user\dev\src\python\AI\data\sample-filelist-for-AIKIF.csv"
#rawData_fileList = r"T:\user\dev\src\python\AI\data\small-filelist-for-AIKIF.csv"   # medium list creates 107,000 links - all combinations

event_fileList = r"T:\user\dev\src\python\AI\data\sample-events.csv"
object_fileList = r"T:\user\dev\src\python\AI\data\sample-objects.csv"
location_fileList = r"T:\user\dev\src\python\AI\data\sample-locations.csv"
link_fileList = r"T:\user\dev\src\python\AI\data\sample-links.csv"
#pcUsageData = dat.load_csv(

def remove_duplicates(l):
    new_list = []
    for elem in l:
        if elem not in new_list:
            new_list.append(elem)

    return new_list
    #return list(set(l))   # this is pythonic way to do it for non nested list


def BuildUniqueLocations(locListWITH_duplicates):
    newList = []
    location_key = 1
    locList = remove_duplicates(locListWITH_duplicates)
    for i in locList:
        location_key = location_key + 1
        for j in i:
            newList.append([location_key, j])
    #print(newList)
    return newList
    
def PrintList(lst):
    # local test function to print the events list
    num = 0
    for i in lst:
        num = num + 1
        print('\n' + str(num) + ' = ' )
        print(i)


        
def LoadData_FileList(fname):
    # loads a list of file metadata in the following format:
    #   fullFilename,name,path,size,date,
    #   "T:\user\dev\src\python\AI\README.md","README.md","T:\user\dev\src\python\AI","3071","",
    fileData = dat.ReadFileToList(fname, 2)
    print('processing ' + str(len(fileData)) + ' rows of filedata')
    
    # set up file structures for the data to be returned
    #todaysDate = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
    
    events = [[0, 'DATE', 'catgory', 'event details']]
    locations = [[0, 'folder']]
    objects = [[0, 'pictures']]
    #location_key = 0 - no, this is done in separate function due to duplicates
    event_key = 0
    object_key = 0
    # process the file into structures
    for line in fileData:
        if '","' in line:
            flds = line.split('","')   # what the HELL is this crap! Do this properly - TODO
        else:
            flds = line.split(',')
        lfullFilename = flds[0][1:] #[1:] removes the leading " due to split
        lname = flds[1]
        lpath = flds[2]
        lsize = flds[3]
        ldate = flds[4][0:-3]    #[0:-3]  removes the last ", from date if splitting by "," - Fix this shit
        #print('fullname = ', lfullFilename)
        #print('name     = ', lname)
        #print('path     = ', lpath)
        #print('size     = ', lsize)
        #print('date     = ', ldate)
        # Save an event for each file modified date (eg you modified file 'name' on this date)
        #events.extend([ldate, 'FileUsage', lfullFilename])    
        event_key = event_key + 1
        events.append([event_key, ldate, 'FileUsage', lfullFilename]) 
        
        # Save a list of folders as locations
        locations.append([lpath])
        
        # Save a list of Photos as objects or instations of art
        if lname[-4:] == '.jpg':
            object_key = object_key + 1
            objects.append([object_key, lname])
        
    # Step 5 - save an Event which logs that you ran this program
    event_key = event_key + 1
    events.append([event_key, '16/4/2014', 'Process', 'ran processRawData.py'])    
    
    return(events, BuildUniqueLocations(locations), objects)
 
def FindLinks(lstA, lstB):
    # function which is run after all the basic data is collected to build the links between groups.
    # The reason this is done afterwards is to allow the links to build once ALL data files are run.
    # Discussion:
    # What is the point of this function - is it simply a link table?
    # 
    links = []   #once keys are implemented into source lists
    linkID = 1
    lstA_ID = 0
    lstB_ID = 0
    match = 'N'
    print(' ======== FINDING LINKS ======== ' )
    for a in lstA:
        #print('a = ')
        #print(a)
        lstA_ID = a[0]
        for b in lstB:
            #print(b)
            # Now each list Item a and b is itself a list, so need to iterate those
            # but remember that the FIRST element of ALL lists will be the KEY 
            match = 'N'
            lstB_ID = b[0]
            for i in range(1, len(a)):   # need to exclude the KEY which is first element
                for j in range(1, len(b)):
                    
                    #print(' i and j = ')
                    #print(a[i])
                    #print(b[j])
                    if type(a[i]) is str or type(a[i]) is int  or type(b[i]) is str  or type(b[i]) is int:
                        if a[i] == b[j]:
                            match = 'Y0'
                #        else:
                #            if a[i] in b[j]:
                #                match = 'Y1'
                #            if b[j] in a[i]:
                #                match = 'Y2'
            if match != 'N':            
                print('Found lstA in lstB ')
                #print('a = ', a)
                #print('b = ', b)
                links.append([linkID, lstA_ID, lstB_ID])
                linkID = linkID + 1
    return(links)

def DisplayShortListOutput(lst, title):
    num = 1
    print('\n' + title + ' - ' + str(len(lst)) + ' elements')
    for i in lst:
        if num < 4:
            print(num, ' - ' , i)
        num = num + 1
    
 
def TEST():
    events, locations, objects = LoadData_FileList(rawData_fileList)
    #PrintList(objects)
    #PrintList(locations)
    #PrintList(events)
    
    DisplayShortListOutput(objects, 'objects')
    DisplayShortListOutput(locations, 'locations')
    DisplayShortListOutput(events, 'events')
    
    aikif.SaveFileDataToFile(locations, location_fileList)
    aikif.SaveFileDataToFile(objects, object_fileList)
    aikif.SaveFileDataToFile(events, event_fileList)
    
    # now find links between the items
    links = FindLinks(objects, locations)
    DisplayShortListOutput(links, 'links')
    aikif.SaveFileDataToFile(links, link_fileList)
    
    
    
    print('Done..')

# ---- main section for testing ----
print('processRawData.py - process raw information to core tables in AIKIF')
TEST()
