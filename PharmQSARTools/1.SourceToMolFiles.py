#testing set renamer 2
#!/usr/bin/python

import sys


def renamerScript(dataSet):
    #-------------------------------------------------------------------------------
    #------------------------------- Renamer Script --------------------------------
    #-------------------------------------------------------------------------------
    '''
    Needs to be fed 3 columns - name, activity, catagory
    '''
    #-------------------------------------------------------------------------------
    #---------------------------- Load in Libraries --------------------------------
    #-------------------------------------------------------------------------------
    import sys, subprocess
    from os import rename, listdir, remove, path, getcwd, chdir, makedirs
    #-------------------------------------------------------------------------------
    #---------------------------- Change Directory ---------------------------------
    #-------------------------------------------------------------------------------
    newDirectory = "./../0.SourceFiles/" + dataSet
    chdir(newDirectory)

    tableFile = dataSet + "Table.txt"
    #-------------------------------------------------------------------------------
    #--------------------------- Checks File Paths ---------------------------------
    #-------------------------------------------------------------------------------
    if path.isfile(tableFile) != True:
        print "Error: Source file is not here"
        return 0;


    #-------------------------------------------------------------------------------
    #-------------------------- Discover File Ending -------------------------------
    #-------------------------------------------------------------------------------
    fnames = listdir('.') #reates array from names in directory
    fnames.sort()
    counter = 0
    fnames.remove(tableFile)
    if path.isfile(".DS_Store") == True:
        fnames.remove(".DS_Store")
    counter = 0
    for k in fnames:
        k = k[:-5]
        rename(fnames[counter], k.upper() + ".mol2")
        counter +=1

    #-------------------------------------------------------------------------------
    #--------------------------- Extract Mol Folder --------------------------------
    #-------------------------------------------------------------------------------
    for idx, k in enumerate(fnames):
        fnames[idx] = fnames[idx][ :-5 ]

    #-------------------------------------------------------------------------------
    #-------------------------- Extract data from ACEdata --------------------------
    #-------------------------------------------------------------------------------
    tableFile = str(tableFile)
    fi = open(tableFile, 'r') #reads in the file that list the before/after file names
    file_input = fi.read().split("\n") #reads in files
    file_input = file_input[:-1] #cuts off the end of the list (its empty I hope)
    counter = 0
    for k in file_input:
        file_input[counter] = k.upper()
        counter +=1
    #-------------------------------------------------------------------------------
    #-------------------------- Creates the ACE data sets --------------------------
    #-------------------------------------------------------------------------------
    fileName, fileCatagory, fileActivity, filePosition, tempList = [], [], [], [], []
    count = 0
    for line in file_input:
        tempList = line.split("\t") #reads in files
        for k in fnames:
            if tempList[0] == k:
                fileName.append(tempList[0].strip("\""))
                fileActivity.append(tempList[1])
                fileCatagory.append(tempList[2])
                filePosition.append(count)
                count +=1

    #-------------------------------------------------------------------------------
    #---------------------- Copy then move to a new directory ----------------------
    #-------------------------------------------------------------------------------
    chdir("./../..")

    if path.isdir("1.RenamedFiles") != True:
        makedirs("1.RenamedFiles")
    chdir("./1.RenamedFiles")

    if path.isdir(dataSet) != True:
        makedirs(dataSet)

    #-------------------------------------------------------------------------------
    #---------------------- Creating the list of bad names -------------------------
    #-------------------------------------------------------------------------------
    badList = []
    count = 0
    for k in fileName:
        if k not in fnames:
            badList.append(k)
            del fileName[count]
            del fileActivity[count]
            del fileCatagory[count]
            del filePosition[count]
        count +=1
    print "List of files that are on the list but do not have files for and will be removed : " + str(badList)

    from shutil import copy2
    for idx, k in enumerate(fileName):
        copy2("./../0.SourceFiles/"+ dataSet +"/" + fileName[idx] + ".mol2", str("./" + dataSet))
    chdir("./" + dataSet)

    #-------------------------------------------------------------------------------
    #---------------------- Seperate files into two groups -------------------------
    #-------------------------------------------------------------------------------
    fileNameOne, fileActivityOne, filePositionOne, fileCatagoryOne = [], [], [], []
    fileNameTwo, fileActivityTwo, filePositionTwo, fileCatagoryTwo = [], [], [], []
    for idx in range(len(fileName)):
        if fileName[idx] in badList:
            count += 1
        if fileCatagory[idx] == '1':
            fileNameOne.append(fileName[idx])
            fileActivityOne.append(fileActivity[idx])
            filePositionOne.append(filePosition[idx])
            fileCatagoryOne.append('1')

        elif fileCatagory[idx] == '2':
            fileNameTwo.append(fileName[idx])
            fileActivityTwo.append(fileActivity[idx])
            filePositionTwo.append(filePosition[idx])
            fileCatagoryTwo.append('2')

    #-------------------------------------------------------------------------------
    #---------------------- Combine the Two groups together ------------------------
    #-------------------------------------------------------------------------------
    newFileName, newFileActivity, newFilePosition = [], [], []
    counter = 0
    for idx in range(len(fileNameOne)):
        newFileName.append(fileNameOne[counter])
        newFileActivity.append(fileActivityOne[counter])
        newFilePosition.append(filePositionOne[counter])
        counter +=1
    counter = 0
    for idx in range(len(fileNameTwo)):
        newFileName.append(fileNameTwo[counter])
        newFileActivity.append(fileActivityTwo[counter])
        newFilePosition.append(filePositionTwo[counter])
        counter +=1
    #---------------------------------------------------------------------------
    #------------------------- Rename the files --------------------------------
    #---------------------------------------------------------------------------
    counter = 1
    newNameList = []

    for k in newFileName:
        oldName = k + ".mol2"
        newName =  "mol" + str(counter).zfill(3) + ".mol2"
        newNameList.append(newName[:-5])
        rename(oldName, newName)
        counter += 1
    #---------------------------------------------------------------------------
    #---------------------- Makes the activity Sheet ---------------------------
    #---------------------------------------------------------------------------
    with open('activity.txt', 'w') as f:
        for k in fileActivityOne:
            f.write(k)
            f.write('\n')
        for k in fileActivityTwo:
            f.write(k)
            f.write('\n')

    conversionTableName = dataSet + "conversionTable.txt"
    fileCatagory = []
    fileCatagoryOne.extend(fileCatagoryTwo)

    with open(conversionTableName, 'w') as f:
        # need to make a table with newName, Old name, activity, group
        counter = 0
        for k in newFileName:
            f.write(newNameList[counter])
            f.write("\t")
            f.write(newFileName[counter])
            f.write("\t")
            f.write(newFileActivity[counter])
            f.write("\t")
            f.write(str(fileCatagoryOne[counter]))
            f.write("\n")
            counter +=1



#-------------------------------------------------------------------------------
#------------------------ Run/test the script ----------------------------------
#-------------------------------------------------------------------------------
#dataSet = "ACEdata.txt"
#dataSet = raw_input("What is the name of the file?: \n-------------------------------------------\n")
dataSet = sys.argv[1]
renamerScript(dataSet)
#-------------------------------------------------------------------------------
#------------------------------------ Fin --------------------------------------
#-------------------------------------------------------------------------------
