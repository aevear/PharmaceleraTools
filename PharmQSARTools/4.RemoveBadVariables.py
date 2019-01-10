#-------------------------------------------------------------------------------
# Part 4 - This goes through the output errors for PharmScreen and removes the errors from the data sets (reason doesn't matter)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------
def removeBadVariables (dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs, path
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    So this one will need some explaining...

    Basically, PHARMSCREEN and QSAR can't really handle some molecule types, and
    so this program turns every molecule into its own thing in a list then deletes
    the nasty ones.

    It also removes anything with B and I sadly, becuase QSAR just can't handle
    it and it failed constantly. Realy shame, but maybe in the next update it
    can handle it
    '''
    #---------------------------------------------------------------------------
    #------------------------- Move to old MOL files ---------------------------
    #---------------------------------------------------------------------------



    newDirectory = "./../3.RunPharmScreen/" + dataSet
    chdir(newDirectory)

    fnames = listdir('.') #creates array from names in directory
    experimentFolder = ''
    for k in fnames:
        if k[:4] == "2018":
            experimentFolder = k

    chdir("./" + experimentFolder)

    #---------------------------------------------------------------------------
    #---------------------- Prepare to load in mol files -----------------------
    #---------------------------------------------------------------------------
    fi = open((dataSet + ".log"), 'r') #reads in the file that list the before/after file names
    errorLog = fi.read().split("\n") #reads in files

    errorLog = errorLog[11:-4]
    errorMolecules = []

    for k in errorLog:
        if k[:8] == "Molecule":
            errorMolecules.append(k[9:12].strip())
    #---------------------------------------------------------------------------
    #---------------------- Extract old mol file -------------------------------
    #---------------------------------------------------------------------------
    fi = open((dataSet + ".mol2"), 'r') #reads in the file that list the before/after file names
    originalMolfile = fi.read().split("\n") #reads in files
    #---------------------------------------------------------------------------
    #---------------------- Begin Filtering the Blocks -------------------------
    #---------------------------------------------------------------------------
    originalBlocks = []
    chunk = []
    count = 0
    record = 0
    for k in originalMolfile:
        if k == "@<TRIPOS>MOLECULE":
            record = 1
            count +=1
        if record == 1:
            chunk.append(k)
        if k == "# PHARMSCREEN v1.0 (Pharmacelera)":
            record = 0
            originalBlocks.append(chunk)
            chunk = []


    #---------------------------------------------------------------------------
    #---------------------- Check for I in files -------------------------------
    #---------------------------------------------------------------------------

    counter = -1
    for k in originalBlocks:
        counter +=1
        k = list(filter(None, k))
        for i in k[6:-1]:
            line = i.split(" ")
            line = list(filter(None, line))
            stop = 0
            if len(line) == 1:
                stop = 1
            if line[0] == "@<TRIPOS>BOND":
                break
            if stop != 1:
                if (line[1] == "I"):
                    errorMolecules.append(counter)
                if (line[1] == "B"):
                    errorMolecules.append(counter)

    count = 0
    for k in errorMolecules:
        errorMolecules[count] = int(errorMolecules[count])
        count +=1

    errorMolecules.sort()
    print "Molecules with Errors : " + str(errorMolecules)
    #---------------------------------------------------------------------------
    #---------------------- Grab old file --------------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")
    activityFileBlocks = []
    fi = open(("activity.txt"), 'r') #reads in the file that list the before/after file names
    activityFileBlocks = fi.read().split("\n") #reads in files
    activityFileBlocks = activityFileBlocks[:-1]

    fi = open((dataSet + "conversionTable.txt"), 'r') #reads in the file that list the before/after file names
    converionTable = fi.read().split("\n") #reads in files
    converionTable = converionTable[:-1]


    #---------------------------------------------------------------------------
    #---------------------- Remove Bad Blocks ----------------------------------
    #---------------------------------------------------------------------------
    count = 0
    for k in errorMolecules:
        if len(originalBlocks) == int(k)-count:
            del originalBlocks[-1]
        else:
            del originalBlocks[int(k)-count]
        count = count + 1

    #---------------------------------------------------------------------------
    #------------------ Remove file from activityFile --------------------------
    #---------------------------------------------------------------------------
    count = 1
    for k in errorMolecules:
        del activityFileBlocks[int(k)-count]
        count = count + 1

    count = 1
    for k in errorMolecules:
        del converionTable[int(k)-count]
        count = count + 1


    #---------------------------------------------------------------------------
    #---------------------- Move to /create new folder -------------------------
    #---------------------------------------------------------------------------
    newDirectory = "./../../"
    chdir(newDirectory)

    if path.isdir("4.CorrectedPharmScreen") != True:
        makedirs("4.CorrectedPharmScreen")
    chdir("./4.CorrectedPharmScreen")

    if path.isdir(dataSet) != True:
        makedirs(dataSet)
    chdir("./" + dataSet)

    #---------------------------------------------------------------------------
    #---------------------- Export Corrected Files -----------------------------
    #---------------------------------------------------------------------------
    with open((dataSet + ".mol2"), 'w') as f:
        for k in originalBlocks:
            f.write("\n")
            for i in k:
                f.write(i)
                f.write("\n")

    with open(("activity.txt"), 'w') as f:
        for k in activityFileBlocks:
            f.write(k)
            f.write("\n")

    with open((dataSet + "conversionTable.txt"), 'w') as f:
        for k in converionTable:
            f.write(k)
            f.write("\n")


#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
removeBadVariables(dataSet)


#
