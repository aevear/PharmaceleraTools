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
def trainTestNumber(data):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #---------------------------- Loading data      ----------------------------
    #---------------------------------------------------------------------------
    fnames = listdir('.') #creates array from names in directory
    trainingNumber, testNumber = 0,0
    with open(data + 'conversionTable.txt', 'r') as f:
        conversionTable = f.read().split("\n")
        for k in conversionTable:
            if str(k[3]) == "1":
                trainingNumber += 1
            if str(k[3]) == "2":
                testNumber += 1
        return (trainingNumber, testNumber)

def configurationCreator(trainingNumber, testNumber):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #---------------------------- Loading data      ----------------------------
    #---------------------------------------------------------------------------
    fnames = listdir('.') #creates array from names in directory
    trainingNumber = int(trainingNumber)
    testNumber = int(testNumber)
    #checks to see if the name is called mol, if nothing is called mol, than it kills the process later

    with open('plsanal_hyphar.txt', 'w') as f:
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
            if k == "simgrd_out_logpt.va0":
                fi = open("simgrd_out_logpt.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_logpt.va0\n")
                f.write(data)
            if k == "simgrd_out_logpe.va0":
                fi = open("simgrd_out_logpe.va0", 'r') #reads in the file that list the before/after file names
                data = fi.readline()
                data = data.strip(" ").strip("\t")
                data = data[2:]
                data = data.strip(" ").strip("\t")
                f.write("simgrd_out_logpe.va0\n")
                f.write(data)
        print "Config2 file was succesfully created!"

    with open('pharmqsar_config.txt', 'w') as f:
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
        print "Config1 file was succesfully created!"
        return 1

def initialQsar (dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #--------------------------- Copy for QSAR ---------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")

    if path.isdir("6.Qsar") != True:
        makedirs("6.Qsar")

    from distutils.dir_util import copy_tree
    copy_tree(("./5.PreQsar/" + dataSet), ("./6.QSAR/" + dataSet))


    #---------------------------------------------------------------------------
    #--------------------------- Move to dataSet -------------------------------
    #---------------------------------------------------------------------------
    chdir("./6.QSAR/" + dataSet)


    #---------------------------------------------------------------------------
    # Run pre-CoMFA
    #---------------------------------------------------------------------------
    bashCommand = "./pharmqsar --if molecules --mode projections -x CoMFA"
    print "Pre-CoMFA Running : " + dataSet
    output = subprocess.check_output(['bash','-c', bashCommand])
    print "Pre-CoMFA Done : " + dataSet


    #---------------------------------------------------------------------------
    #--------------------- Create initial Files for MOPAC ----------------------
    #---------------------------------------------------------------------------
    bashCommand = "./pharmqsar --if molecules2 --mode projections --grid 1.0 -x " + dataSet + " -y userdefined --dmode 1 --logp userdefined"
    print "Preparing for H1/H2 Grid : " + dataSet
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
