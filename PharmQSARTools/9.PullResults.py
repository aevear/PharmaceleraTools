#-------------------------------------------------------------------------------
# Part 8 - Analysis
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Libraries needed
#-------------------------------------------------------------------------------
import sys
#-------------------------------------------------------------------------------
# Function
#-------------------------------------------------------------------------------
def extractData(fileSource, block, stdError):
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    This pulls from the source files provided and pulls the q2 values. Part 9
    should have a real similar function but I haven't build it yet lol

    Values that I need :
    r2(train)
    q2(train)
    S
    Spress
    r2(test)
    S(test)
    Nc
    ELE
    NELE

    '''
    results = []
    r2Train = 0.0
    q2Train = 0.0
    S = 0.0
    Spress = 0.0
    r2Test = 0.0
    STest = 0.0
    Nc = 0.0
    ELE = 0.0
    NELE = 0.0
    record = 0
    toggle = 0 #God aren't toggles that most awful thing? But idk how to do better stuff

    realTraining = []
    calculatedTraining = []
    differenceTraining = []
    realTest = []
    calculatedTest = []
    differenceTest = []
    q2Values = []


    with open(fileSource, 'r') as f:
        SourceFile = f.read().split("\n")
        skip = 0
        for k in SourceFile:
            if k == str("Modelo de componentes: " + str(block)):
                toggle = 1
            if k == str("Modelo de componentes: " + str(int(block) + 1)):
                toggle = 0
            if toggle == 1:
                #r2(train)
                #S
                if k[:3] == "r2=":
                    fragments = k.split(" ")
                    r2Train = fragments[1]
                    S = fragments[3]
                #Q2 Value
                if k[:3] == "q2=":
                    fragments = k.split(" ")
                    q2Train = fragments[1]
                #Spress
                #Nc
                if k[:6] == "spress":
                    fragments = k.split(" ")
                    Spress = fragments[1]
                    Nc = fragments[3]
                #r2(test)
                #S(test)

                #ELE
                if k[:9] == "Field 1 =":
                    fragments = k.split(" ")
                    ELE = fragments[3]
                #NELE
                if k[:9] == "Field 2 =":
                    fragments = k.split(" ")
                    NELE = fragments[3]

                fragments = k.split(" ")
                fragments = list(filter(None, fragments))


                skip = 0
                if k:
                    try:
                        if fragments[0] == "1":
                            record = record + 1
                        if fragments[0] == "-------------------------":
                            record = record + 1
                            skip = 1
                        if fragments[0] == "field":
                            record = record +1
                        if (record == 2) and (skip == 0):
                            realTraining.append(fragments[1])
                            calculatedTraining.append(fragments[2])
                            differenceTraining.append(fragments[3])
                        if (record == 3) and (skip == 0):
                            realTest.append(fragments[1])
                            calculatedTest.append(fragments[2])
                            differenceTest.append(fragments[3])
                        if (record == 5) and (skip == 0):
                            q2Values.append(fragments[2])
                    except TypeError:
                        skip = 1




        print "---------------------------------------"
        print "r2 (train) : " + str(r2Train)
        print "q2 (train) : " + str(q2Train)
        print "S          : " + str(S)
        print "Spress     : " + str(Spress)
        print "r2 (test)  : " + str(r2Test)
        print "sTest      : " + str(STest)
        print "Nc         : " + str(Nc)
        print "ELE        : " + str(ELE)
        print "NELE       : " + str(NELE)
        print "---------------------------------------"

        firstLine = str(len(realTraining)) + "\t" + str(r2Train[:4]) + "\t" + str(q2Train[:4]) + "\t" + str(S[:4]) + "\t" + str(Spress[:4])
        firstLine = firstLine + "\t\t\t" + str(len(realTest)) + "\t" + str(r2Test) + "\t" + str(STest)
        firstLine = firstLine + "\t\t1\t" + str(stdError) + "\t" + block + "\t" + str(ELE) + "\t" + str(NELE)

        print firstLine
        print "---------------------------------------"
        count = -1
        for k in realTraining:
            count += 1
            print str(count+1) + "\t" + "mol" + str(count+1).zfill(3) + "\t" + realTraining[count] + "\t" + calculatedTraining[count] + "\t" + q2Values[count] + "\t" + differenceTraining[count]
        print "------------Test--------------"
        internalCount = -1
        for k in realTest:
            internalCount +=1
            count += 1
            print str(count+1) + "\t" + "mol" + str(count+1).zfill(3) + "\t" + (realTest[internalCount]) + "\t" + calculatedTest[internalCount] + "\t" + q2Values[internalCount] + "\t" + differenceTest[internalCount]






        print "---------------------------------------"


def extractResults(dataSet, type, stdError, block):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''



    '''
    #---------------------------------------------------------------------------
    #-------------------- Navigate to the source folder-------------------------
    #---------------------------------------------------------------------------
    results = []

    chdir("./../7.QsarResults/" + dataSet + "/" + dataSet + "-" + stdError)

    results = extractData((type + ".pls"), block, stdError)

    chdir("./..")




#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
type = sys.argv[2]
stdError = sys.argv[3]
block = sys.argv[4]
extractResults(dataSet, type, stdError, block)

#
