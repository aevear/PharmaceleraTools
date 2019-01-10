#-------------------------------------------------------------------------------
# Part 3 - Runs PharmScreen Bascially
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------

def runPharmScreen (dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''

    '''
    #---------------------------------------------------------------------------
    #---------------------------- Saying Hello ---------------------------------
    #---------------------------------------------------------------------------
    print "-----------------------------------------------------------------"
    print "Begining Running PharmScreen for " + dataSet
    print "-----------------------------------------------------------------"


    #---------------------------------------------------------------------------
    #------------------------- Make a NewFolder  -------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")

    if path.isdir("3.RunPharmScreen") != True:
        makedirs("3.RunPharmScreen")
    chdir("./3.RunPharmScreen")


    #---------------------------------------------------------------------------
    #------------------------- Copy to a new folder  ---------------------------
    #---------------------------------------------------------------------------
    from distutils.dir_util import copy_tree
    copy_tree(("./../2.PharmScreen/" + dataSet), ("./" + dataSet))
    chdir(dataSet)

    #---------------------------------------------------------------------------
    #------------------------- Align Molecules ---------------------------------
    #---------------------------------------------------------------------------
    bashCommand = "./pharmscreen -i " + str(dataSet) + ".mol2 --single -y esp --logp yes --minimize RM1"
    print bashCommand
    output = subprocess.check_output(['bash','-c', bashCommand])


    #---------------------------------------------------------------------------
    #------------------------- Run PharmScreen  --------------------------------
    #---------------------------------------------------------------------------
    bashCommand = "./pharmscreen -i " + str(dataSet) + ".mol2 -x "+ str(dataSet) + " --single --logp yes -y esp --out mol2"
    print bashCommand
    output = subprocess.check_output(['bash','-c', bashCommand])


    print "------------------------------"
    print "Finished PharmaScreen for : " + dataSet + "!"
    print "------------------------------"


#-------------------------------------------------------------------------------
#------------------------ Run/test the script ----------------------------------
#-------------------------------------------------------------------------------
#referenceFile = "ACEdata.txt"
#referenceFile = raw_input("What is the name of the file?: \n-------------------------------------------\n")
dataSet = str(sys.argv[1])
runPharmScreen(dataSet)
#-------------------------------------------------------------------------------
#------------------------------------ Fin --------------------------------------
#-------------------------------------------------------------------------------