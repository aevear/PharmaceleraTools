#-------------------------------------------------------------------------------
# Merge files into a PharmaScreen ready file
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------
def checkDataType(sampleFile):
    fileEnding = sampleFile[-4:]
    if fileEnding == "mol2":
        return "mol2"
    elif fileEnding == ".pdb":
        return "pdb"
    elif fileEnding == ".sdf":
        return "sdf"
    print "The file that you have provided does not contain either sdf, pdb or mol2"
    return 0


def mergeFiles (dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs


    #---------------------------------------------------------------------------
    #------------------------- Move to old MOL files ---------------------------
    #---------------------------------------------------------------------------
    newDirectory = "./../1.RenamedFiles/" + dataSet
    chdir(newDirectory)

    #---------------------------------------------------------------------------
    #---------------------- Prepare to load in mol files -----------------------
    #---------------------------------------------------------------------------
    fnames = listdir('.') #creates array from names in directory

    fi = open("activity.txt", 'r') #reads in the file that list the before/after file names
    activityFile = fi.read() #reads in files

    fi = open((str(dataSet) + "conversionTable.txt"), 'r') #reads in the file that list the before/after file names
    conversionTable = fi.read() #reads in files

    fnames.remove("activity.txt")
    if path.isdir(".DS_Store") == True:
        fnames.remove(".DS_Store")
    fnames.remove(str(dataSet) + "conversionTable.txt")

    completeArray = []

    #---------------------------------------------------------------------------
    #--------------- Load in the Old Mol Files in the right order --------------
    #---------------------------------------------------------------------------
    counter = 1
    for k in fnames:
        molName = "mol" + str(counter).zfill(3) + ".mol2"
        fi = open(molName, 'r') #reads in the file that list the before/after file names
        file_input = fi.read().split("\n") #reads in files
        completeArray.append(file_input)
        counter +=1


    #---------------------------------------------------------------------------
    #------------------------- Move to new molecules ---------------------------
    #---------------------------------------------------------------------------
    chdir("./../..")
    if path.isdir("2.PharmScreen") != True:
        makedirs("2.PharmScreen")

    chdir("./2.PharmScreen")

    if path.isdir(dataSet) != True:
        makedirs(dataSet)

    newDirectory = "./" + dataSet
    chdir(newDirectory)


    #---------------------------------------------------------------------------
    #------------------------- Export new molecules ----------------------------
    #---------------------------------------------------------------------------
    fileName = dataSet + "." + checkDataType(fnames[1])
    with open(fileName, 'w') as f:
        for k in completeArray:
            for i in k:
                f.write(i)
                f.write("\n")


    #---------------------------------------------------------------------------
    #------------------------- Move over old files  ----------------------------
    #---------------------------------------------------------------------------
    with open("activity.txt", 'w') as f:
        f.write(activityFile)

    with open((str(dataSet) + "conversionTable.txt"), 'w') as f:
        f.write(conversionTable)

    chdir("./../")
    from shutil import copy2
    copy2("./../PharmQSARTools/pharmscreen", str("./" + dataSet))


#-------------------------------------------------------------------------------
# Merge files into a PharmaScreen ready file
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
mergeFiles(dataSet)

#
