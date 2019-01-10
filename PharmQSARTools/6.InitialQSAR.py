#-------------------------------------------------------------------------------
# Part 6 - Creating the configuration files and Setting up initial files for CoMFA and MOPAC
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------
def trainTestNumber(data):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    This basically checks out the sheet that we have been copying over and
    updating since the begining and uses that to figure out how many training
    and test sets survived the purge of bad data that was part 4.

    It just counts up how many of each there are, not too complex really.

    '''
    #---------------------------------------------------------------------------
    #---------------------------- Loading data      ----------------------------
    #---------------------------------------------------------------------------
    fnames = listdir('.') #creates array from names in directory
    trainingNumber, testNumber = 0,0
    with open(data + 'conversionTable.txt', 'r') as f:
        conversionTable = f.read().split("\n")
        conversionTable = conversionTable[:-1]
        for k in conversionTable:
            i = k.split("\t")
            if str(i[3]) == "1":
                trainingNumber += 1
            if str(i[3]) == "2":
                testNumber += 1
        return (trainingNumber, testNumber)


def configurationCreator(trainingNumber, testNumber):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    So this function create the needed configuration table, which again isn't
    really all that nessesary. Its almost no work to do it by hand. But the point
    of this program is to do nothing by hand so I made this anyway.

    Anyway, it looks to see if simgrd_out whatever file is there, then pulls
    from the first line to populate the configuration file. I was told only
    a few things changed (training, test, and simgrd stuff) so the majority
    is static, though you could make it dynamic if you wanted idk/idc.

    '''
    #---------------------------------------------------------------------------
    #---------------------------- Loading data      ----------------------------
    #---------------------------------------------------------------------------
    fnames = listdir('.') #creates array from names in directory
    trainingNumber = int(trainingNumber)
    testNumber = int(testNumber)
    #checks to see if the name is called mol, if nothing is called mol, than it kills the process later

    with open('CoMFA_config.txt', 'w') as f:
        f.write("Training_molecules: " + str(trainingNumber))
        f.write("\n")
        f.write("Test_molecules: " + str(testNumber))
        f.write("\n")
        f.write("Number_of_components: 10")
        f.write("\n")
        f.write("Number_of_fields: 2")
        f.write("\n")
        f.write("activity.txt")
        f.write("\n")
        for k in fnames:
            if k == "simgrd_out_eel.va0":
                fi = open("simgrd_out_eel.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_eel.va0\n")
                f.write(data)
            elif k == "simgrd_out_evw.va0":
                fi = open("simgrd_out_evw.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_evw.va0\n")
                f.write(data)
        print "CoMFA_config file was succesfully created!"

    with open('H1_Config.txt', 'w') as f:
        f.write("Training_molecules: " + str(trainingNumber))
        f.write("\n")
        f.write("Test_molecules: " + str(testNumber))
        f.write("\n")
        f.write("Number_of_components: 10")
        f.write("\n")
        f.write("Number_of_fields: 2")
        f.write("\n")
        f.write("activity.txt")
        f.write("\n")
        for k in fnames:
            if k == "simgrd_out_logpe.va0":
                fi = open("simgrd_out_logpe.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_logpe.va0\n")
                f.write(data)
            if k == "simgrd_out_evw.va0":
                fi = open("simgrd_out_evw.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_evw.va0\n")
                f.write(data)
        print "H1_Config file was succesfully created!"


    with open('H2_Config.txt', 'w') as f:
        f.write("Training_molecules: " + str(trainingNumber))
        f.write("\n")
        f.write("Test_molecules: " + str(testNumber))
        f.write("\n")
        f.write("Number_of_components: 10")
        f.write("\n")
        f.write("Number_of_fields: 2")
        f.write("\n")
        f.write("activity.txt")
        f.write("\n")
        for k in fnames:
            if k == "simgrd_out_logpe.va0":
                fi = open("simgrd_out_logpe.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_logpe.va0\n")
                f.write(data)
            if k == "simgrd_out_logpc.va0":
                fi = open("simgrd_out_logpc.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_logpc.va0\n")
                f.write(data)
        print "H1_Config file was succesfully created!"

    return 1

def initialQsar (dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    So this part does the inital steps of setting up the grid for both CoMFA and
    MOPAC and then in the next step is duplicated 9 times.

    It really here just to save calculation time as why the hell would I need to
    do this 3 times when I can just do it once here?

    Anyway, it makes the grid, then the config files.

    '''
    #---------------------------------------------------------------------------
    #--------------------------- Copy for QSAR ---------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")

    if path.isdir("6.QSAR") != True:
        makedirs("6.QSAR")
    chdir("./6.QSAR/")
    #---------------------------------------------------------------------------
    #--------------------------- Move to dataSet -------------------------------
    #---------------------------------------------------------------------------
    from distutils.dir_util import copy_tree
    copy_tree(("./../5.PreQsar/" + dataSet), ("./" + dataSet))
    chdir("./" + dataSet)


    #---------------------------------------------------------------------------
    # Run pre-CoMFA
    #---------------------------------------------------------------------------
    bashCommand = "./pharmqsar --if molecules --mode projections -x CoMFA"
    print dataSet + " : Preparing CoMFA Grid"
    output = subprocess.check_output(['bash','-c', bashCommand])


    #---------------------------------------------------------------------------
    #--------------------- Create initial Files for MOPAC ----------------------
    #---------------------------------------------------------------------------
    bashCommand = "./pharmqsar --if molecules2 --mode projections --grid 1.0 -x " + dataSet + " -y userdefined --dmode 1 --logp userdefined"
    print dataSet + " : Preparing H1/H2 Grid"
    output = subprocess.check_output(['bash','-c', bashCommand])


    #---------------------------------------------------------------------------
    #--------------------- Create Configuration dataSet ------------------------
    #---------------------------------------------------------------------------
    trainingNumber, testNumber = trainTestNumber(dataSet)
    configurationCreator(trainingNumber, testNumber)


#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
initialQsar(dataSet)

#
