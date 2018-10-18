#-------------------------------------------------------------------------------
# Run CoMFA -> H1, H2
#-------------------------------------------------------------------------------
import os

#directories = ["ACE", "ACHE", "BZR", "CRUZAIN", "DHFR", "GPB", "THR"]
directories = ["testCRUZAIN"]

for file in directories:
    print "Working on : " + file
    pythonCode = "python 1.SourceToMolFiles.py " + file
    os.system(pythonCode)
    print "Part 1 done"
    pythonCode = "python 2.MergeFiles.py " + file
    os.system(pythonCode)
    print "Part 2 done"
    pythonCode = "python 3.RunPharmScreen.py " + file
    os.system(pythonCode)
    print "Part 3 done"
    pythonCode = "python 4.RemoveBadVariables.py " + file
    os.system(pythonCode)
    print "Part 4 done"
    pythonCode = "python 5.PreQsar.py " + file
    os.system(pythonCode)
    print "Part 5 done"
    pythonCode = "python 6.InitialQSAR.py " + file
    os.system(pythonCode)
    print "Part 6 done"
    pythonCode = "python 7.RunRealCoMFAMOPAC.py " + file
    os.system(pythonCode)
    print "Part 7 done"



#-------------------------------------------------------------------------------
# FIN
#-------------------------------------------------------------------------------
