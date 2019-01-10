#-------------------------------------------------------------------------------
# Part 7 - Running CoMFA, MOPAC for 0.1, 0.01, 0.001
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------
def copyFiles(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    Lolz, this is such a simple part of the program. Anyway it just duplicates
    the thing that we calculated in the last part 3 times into new folders
    '''
    #---------------------------------------------------------------------------
    #--------------------------- Create part 8 ---------------------------------
    #---------------------------------------------------------------------------
    chdir("./..")

    if path.isdir("7.QsarResults") != True:
        makedirs("7.QsarResults")
    chdir("./7.QsarResults")

    if path.isdir(dataSet) != True:
        makedirs(dataSet)

    #---------------------------------------------------------------------------
    #--------------- Create file with 0.1, 0.01, 0.001 -------------------------
    #---------------------------------------------------------------------------
    from distutils.dir_util import copy_tree

    if path.isdir(dataSet + "0.1") != True:
        copy_tree(("./../6.QSAR/" + dataSet), ("./" + dataSet + "/" + dataSet + "-0.1"))
    if path.isdir(dataSet + "0.01") != True:
        copy_tree(("./../6.QSAR/" + dataSet), ("./" + dataSet + "/" + dataSet + "-0.01"))
    if path.isdir(dataSet + "0.001") != True:
        copy_tree(("./../6.QSAR/" + dataSet), ("./" + dataSet + "/" + dataSet + "-0.001"))


def QSAR(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    So this is one of the key parts of the program, it actually runs CoMFA, Mopac
    on the files

    As you can see, it just cycles through each part and preforms the
    calculations before continuing, not really too complex.

    '''
    #---------------------------------------------------------------------------
    #---------------------------- Loading data ---------------------------------
    #---------------------------------------------------------------------------
    stdErrors = ["0.1", "0.01", "0.001"]

    chdir("./../7.QsarResults/" + dataSet)


    for stdError in stdErrors:
        directoryName = "./" + dataSet + "-" + stdError
        chdir(directoryName)

        print "--------------------------------------------------------"
        print "Begining std error : " + stdError + " for file : " + dataSet
        print "--------------------------------------------------------"

        #---------------------------------------------------------------------------
        # CoMFA with set stdError
        #---------------------------------------------------------------------------
        print dataSet + " : Running CoMFA"
        bashCommand = "./pharmqsar --mode pls -x CoMFA --sdthr " + stdError + " --norm 1 --plscfg CoMFA_config.txt -y userdefined"
        output = subprocess.check_output(['bash','-c', bashCommand])
        #---------------------------------------------------------------------------
        # MOPAC
        #---------------------------------------------------------------------------
        print dataSet + " : MOPAC H1"
        bashCommand = "./pharmqsar --mode pls --sdthr " + stdError + " --norm 1 -x H1 --plscfg H1_Config.txt -y userdefined --logp userdefined"
        output = subprocess.check_output(['bash','-c', bashCommand])

        print dataSet + " : MOPAC H2"
        bashCommand = "./pharmqsar --mode pls --sdthr " + stdError + " --norm 1 -x H2 --plscfg H2_Config.txt -y userdefined --logp userdefined"
        output = subprocess.check_output(['bash','-c', bashCommand])
        #---------------------------------------------------------------------------
        chdir("./..")


#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
copyFiles(dataSet)
QSAR(dataSet)

#
