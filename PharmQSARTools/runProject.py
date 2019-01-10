#-------------------------------------------------------------------------------
# This runs the entire program from begining to end - Run CoMFA -> H1, H2
#-------------------------------------------------------------------------------
from os import rename, listdir, remove, path, getcwd, chdir, makedirs, system
#---------------------------------------------------------------------------
#----------------------- Description of Function ---------------------------
#---------------------------------------------------------------------------
'''
This is the part of the program that actually runs each step, and this is where
you should do most of the configuration. If you have a problem with some
data sets or something didn't go well, just turn off the unnessesary steps
below and run it again.

I had been running different data sets at various levels of completedness
and I just turn off the first major loopself.

Anyway, I know this has not been the most helpful note but this code really isnt
too complicated.

At the bottom I have the list of Pharm commands for you to peruse at your leisure

'''
#---------------------------------------------------------------------------
#----------------------- Getting the directories ---------------------------
#---------------------------------------------------------------------------
#Use the hidden one below if you want to use specific sets, otherwise it'll just
#process everything
chdir("./../0.SourceFiles")
directories = listdir("./")
if ".DS_Store" in directories: directories.remove(".DS_Store")
chdir("./../PharmQSARTools")

#directories = ["ACE", "ACHE", "BZR", "CRUZAIN", "DHFR", "GPB", "THR"]


#---------------------------------------------------------------------------
#----------------------- Run PharmaScreen ----------------------------------
#---------------------------------------------------------------------------
#The reason you break it up this way is so that if there is an error with
#PharmQSAR, you don't have to run PharmaScreen again
for file in directories:
    print "-----------------------------------------------------------------"
    print "PharmScreen for : " + file
    print "-----------------------------------------------------------------"
    pythonCode = "python 1.SourceToMolFiles.py " + file
    system(pythonCode)
    print file + " : Part 1 done"
    pythonCode = "python 2.MergeFiles.py " + file
    system(pythonCode)
    print file + " : Part 2 done"
    pythonCode = "python 3.Alignment.py " + file
    system(pythonCode)
    print file + " : Part 3 done"
#---------------------------------------------------------------------------
#----------------------- Run PharmQSAR -------------------------------------
#---------------------------------------------------------------------------
for file in directories:
    print "-----------------------------------------------------------------"
    print "QSAR for  : " + file
    print "-----------------------------------------------------------------"
    pythonCode = "python 4.RemoveBadVariables.py " + file
    system(pythonCode)
    print file + " : Part 4 done"
    pythonCode = "python 5.PreQsar.py " + file
    system(pythonCode)
    print file + " : Part 5 done"
    pythonCode = "python 6.InitialQSAR.py " + file
    system(pythonCode)
    print file + " : Part 6 done"
    pythonCode = "python 7.RunRealCoMFAMOPAC.py " + file
    system(pythonCode)
    print file + " : Part 7 done"


#---------------------------------------------------------------------------
#---------------- Here is a list of the actual Codes I use -----------------
#---------------------------------------------------------------------------
'''
Examples of Code
To run PharmaScreen
./pharmscreen -i ACE.mol2 -x "+ str(dataSet) + " --single --logp yes -y esp --out mol2"

Optimization
./pharmscreen -i ACE.mol2 --single -y esp --logp yes --minimize RM1


To Initialize CoMFA
./pharmqsar --if molecules --mode projections -x CoMFA

To initialize MOPAC
./pharmqsar --if molecules2 --mode projections --grid 1.0 -x ACE -y userdefined --dmode 1 --logp userdefined

To Run CoMFA
./pharmqsar --mode pls -x CoMFA --sdthr 0.1 --norm 1 --plscfg pharmqsar_config.txt -y userdefined

To Run MOPAC H1/H2
./pharmqsar --mode pls --sdthr 0.1 --norm 1 -x H2 --plscfg plsanal_hyphar.txt -y userdefined --logp userdefined
./pharmqsar --mode pls --sdthr 0.1 --norm 1 -x H1 --plscfg plsanal_hyphar.txt -y userdefined --logp userdefined
'''

#-------------------------------------------------------------------------------
# FIN
#-------------------------------------------------------------------------------
