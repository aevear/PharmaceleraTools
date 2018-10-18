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
def copyFiles(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
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

def CoMFA(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    import subprocess
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #---------------------------- Loading data ---------------------------------
    #---------------------------------------------------------------------------
    stdErrors = ["0.1", "0.01", "0.001"]

    chdir("./../7.QsarResults/" + dataSet)


    for stdError in stdErrors:
        directoryName = "./" +dataSet + "-" + stdError
        chdir(directoryName)

        print "--------------------------------------------------------"
        print "Begining std error : " + stdError + " for file : " + dataSet
        print "--------------------------------------------------------"

        #---------------------------------------------------------------------------
        # CoMFA with set stdError
        #---------------------------------------------------------------------------
        bashCommand = "./pharmqsar --mode pls -x CoMFA --sdthr " + stdError + " --norm 1 --plscfg pharmqsar_config.txt -y userdefined"
        print "Running CoMFA : " + dataSet
        output = subprocess.check_output(['bash','-c', bashCommand])
        print "-Finishing CoMFA : " + dataSet
        #---------------------------------------------------------------------------
        # MOPAC
        #---------------------------------------------------------------------------
        print "Running MOPAC H1 : " + dataSet
        bashCommand = "./pharmqsar --mode pls --sdthr " + stdError + " --norm 1 -x H1 --plscfg plsanal_hyphar.txt -y userdefined --logp userdefined"
        output = subprocess.check_output(['bash','-c', bashCommand])
        print "-Finishing H1 : " + dataSet

        print "Running MOPAC H2 : " + dataSet
        bashCommand = "./pharmqsar --mode pls --sdthr " + stdError + " --norm 1 -x H2 --plscfg plsanal_hyphar.txt -y userdefined --logp userdefined"
        output = subprocess.check_output(['bash','-c', bashCommand])
        print "-Finishing H2 : " + dataSet
        #---------------------------------------------------------------------------
        chdir("./..")


#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
copyFiles(dataSet)
CoMFA(dataSet)

#
