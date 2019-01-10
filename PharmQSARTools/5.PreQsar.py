#-------------------------------------------------------------------------------
# Part 5 - Converts mol2 files to our specific file type
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


def mol2ToPDB(mol2DataSet, counter):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    Truthfully, this is a rather intricate part of the program and one I have
    had no end of errors with. The program constantly gave slightly wrong format
    that would cause QSAR to fail completely. Real pain let me tell you

    Anyway, if you have to edit this file god help you. Honestly its a mess
    as I initially had x idea then switched to y when I realized it was better.
    however I didn't remove the old relics, so you have to sift the old garbage
    to see what is relevant. I really should clean it up but fuck it it works
    and I really, really hate this file. Plus god forbid if it errored up again
    '''
    #---------------------------------------------------------------------------
    #Here we will declare the various parts of the file that we will take and store
    #---------------------------------------------------------------------------
    #I know this could be done cleaner, but I wanted it to be clear and obvious
    name = ""
    number = 0
    atomName = ""
    xCoordinate = 0.0
    yCoordinate = 0.0
    zCoordinate = 0.0
    gCharges = 0.0
    logPtot = 0.0
    logPele = 0.0
    logPcav = 0.0
    logPvW = 0.0
    remark = 0
    #---------------------------------------------------------------------------
    #In this part, we will import each line of the code into the appropriate line
    #---------------------------------------------------------------------------
    startToggle = 0 #0 is off, 1 is on - starts after we find the first line
    breakToggle = 0 #This cuts the lines apart
    nameTrigger = 0 #this is used just to get the name
    remarkTrigger = 0 #used to grab the remark
    newFileLine = ''
    newFileLine2 = ""

    mol2DataSet = mol2DataSet.split("\n")
    for line in mol2DataSet:
        #---------------------------------------------------------------------------
        # This is used to get the name of the file
        #---------------------------------------------------------------------------
        if line.strip() == "@<TRIPOS>MOLECULE": #need to extract the name
            nameTrigger = 1
        elif nameTrigger == 1:
            name = str(counter).zfill(3)
            nameTrigger = 0 #Turns off name, only used to get this one bit of data
            outputFileName = "output" + str(name).zfill(3) + "q.pdb"
            output2FileName = "mol" + str(name).zfill(3) + "q.pdb"


        #---------------------------------------------------------------------------
        # This part grabs the great mass of the data, the first two things just turn on/off the catcher
        #---------------------------------------------------------------------------
        elif line.strip() == "@<TRIPOS>ATOM": #turns it on
            startToggle = 1
        elif line.strip() == "@<TRIPOS>BOND": #Turns it off
            startToggle = 0

        elif startToggle == 1: #elif to skip the first line (garbage line)
            line = line.split()

            #---------------------------------------------------------------------------
            # Here we load in all the variables we will use for the next part
            #---------------------------------------------------------------------------
            number = str(line[0])
            atomName = str(line[1])
            xCoordinate = str(line[2])[:-1]
            yCoordinate = str(line[3])[:-1]
            zCoordinate = str(line[4])[:-1]
            gCharges = str(line[8])[:-1]
            logPtot = str(line[9])[:-2]
            logPele = str(line[10])[:-2]
            logPcav = str(line[11])[:-2]
            logPvW = str(line[12])[:-2]

            #2 is mol, 1 is output

            if (len(atomName) == 1) and (len(number) == 1):
                formattedAtom1 = " " + number + "  " + atomName + number + " "
                formattedAtom2 = " " + number + "  " + atomName + "  "
            elif (len(atomName) == 2) and (len(number) == 1):
                formattedAtom1 = " " + number + " " + atomName + number + " "
                formattedAtom2 = " " + number + " " + atomName + "  "


            elif (len(atomName) == 1) and (len(number) == 2):
                formattedAtom1 = number + "  " + atomName + number
                formattedAtom2 = number + "  " + atomName + "  "
            elif (len(atomName) == 2) and (len(number) == 2):
                formattedAtom1 = number + " " + atomName + number
                formattedAtom2 = number + " " + atomName + "  "

            #---------------------------------------------------------------------------
            # This part we will generate output01q.pdb and molq outputs - It's ugly I know
            #---------------------------------------------------------------------------
            newFileLine =   newFileLine + "ATOM     " + formattedAtom2 + " MOL     1      " + "{:>6}".format(xCoordinate) + "{:>8}".format(yCoordinate) + "{:>8}".format(zCoordinate) + "{:>6}".format(logPtot) + "{:>6}".format(logPele) + "{:>6}".format(logPcav) + "{:>6}".format(logPvW) + "\n"
            newFileLine2 = newFileLine2 + "ATOM     " + formattedAtom1 + " MOL     1      " + "{:>6}".format(xCoordinate) + "{:>8}".format(yCoordinate) + "{:>8}".format(zCoordinate) + "  0.00" + "{:>7}".format(gCharges) + "{:>11}".format(atomName) + "\n"

    newFileLine = newFileLine.split("\n")
    newFileLine2 = newFileLine2.split("\n")

    #---------------------------------------------------------------------------
    # Molq File
    #---------------------------------------------------------------------------
    if path.isdir("molecules") != True:
        makedirs("molecules")
    chdir("./molecules")

    with open((output2FileName), 'w') as fMolq:
        counter = 0
        fMolq.write("REMARK " + str(len(newFileLine)-1) + "\n")
        for line in newFileLine2:
            fMolq.write(line)
            if int(counter) < int(number):
                fMolq.write("\n")
            counter +=1
        fMolq.write("TER")

    chdir("./..")
    #---------------------------------------------------------------------------
    # Output File
    #---------------------------------------------------------------------------
    if path.isdir("molecules2") != True:
        makedirs("molecules2")
    chdir("./molecules2")

    with open((outputFileName), 'w') as fOutput:
        counter = 0
        fOutput.write("REMARK " + str(len(newFileLine)-1) + "\n")
        for line in newFileLine:
            fOutput.write(line)
            if int(counter) < int(number):
                fOutput.write("\n")
            counter +=1
        fOutput.write("TER")

    chdir("./..")
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------


def preQsar(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    I think this program is rather cleaver (I mean not that cleaver but still).
    The goal is to break apart the single corrected mol file from the last part
    of the program and converts it into the right file type.

    We have two types that it converts, mol001q.mol2 and output something idk

    Anyway, this specific function takes the big file, breaks it into single
    molecules, then feeds the molecules to the mol2toPDB function to create the
    converted format.

    I might be able to combine this with the previous program as there is quite
    a bit of overlap, but I already had this one done and didn't want to monkey
    with it too much tbqh
    '''
    #---------------------------------------------------------------------------
    #------------------------- Move to old MOL files ---------------------------
    #---------------------------------------------------------------------------
    newDirectory = "./../4.CorrectedPharmScreen/" + dataSet
    chdir(newDirectory)
    #---------------------------------------------------------------------------
    #---------------------- Prepare to load in mol files -----------------------
    #---------------------------------------------------------------------------
    activityFile = ""
    originalMolfile = []

    with open((dataSet + ".mol2"), 'r') as f:
        originalMolfile = f.read().split("@<TRIPOS>MOLECULE")

    originalMolfile = originalMolfile[1:]

    count = 0
    for k in originalMolfile:
        k = k.split("\n")
        k = k[1:-1]
        originalMolfile[count] = k
        count = count + 1

    #---------------------------------------------------------------------------
    #---------------------- read in two tables ---------------------------------
    #---------------------------------------------------------------------------
    with open(("activity.txt"), 'r') as f:
        activityFile = f.readlines()

    with open((dataSet + "conversionTable.txt"), 'r') as f:
        converionTable = f.readlines()


    #---------------------------------------------------------------------------
    #---------------------- Move to new folder ---------------------------------
    #---------------------------------------------------------------------------
    chdir("./../..")

    if path.isdir("5.PreQsar") != True:
        makedirs("5.PreQsar")
    chdir("./5.PreQsar")

    if path.isdir(dataSet) != True:
        makedirs(dataSet)
    chdir("./" + dataSet)

    #---------------------------------------------------------------------------
    #---------------------- Send to format function ----------------------------
    #---------------------------------------------------------------------------
    counter = 0
    for k in originalMolfile:
        counter +=1
        sendFile = "\n".join(k)
        sendFile = "@<TRIPOS>MOLECULE\n" + sendFile
        mol2ToPDB(sendFile, counter)

    #---------------------------------------------------------------------------
    #-------------------- Export Activity  -------------------------------------
    #---------------------------------------------------------------------------
    with open(("activity.txt"), 'w') as f:
        for k in activityFile:
            f.write(k)

    with open((dataSet + "conversionTable.txt"), 'w') as f:
        for k in converionTable:
            f.write(k)

    #---------------------------------------------------------------------------
    #-------------------- Move PharmQSAR here  ---------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")
    from shutil import copy2
    copy2("./../PharmQSARTools/pharmqsar", str("./" + dataSet))


#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
preQsar(dataSet)

#
