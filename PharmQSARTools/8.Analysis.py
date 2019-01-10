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
def extractData(fileSource):
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    This pulls from the source files provided and pulls the q2 values. Part 9
    should have a real similar function but I haven't build it yet lol

    '''
    q2results, errorresults = [], []
    toggle = 0 #God aren't toggles that most awful thing? But idk how to do better stuff
    with open(fileSource, 'r') as f:
        SourceFile = f.read().split("\n")
        for k in SourceFile:
            if k[:2] == "q2":
                if toggle == 1:
                    q2results.append(k[4:11])
                    errorresults.append(k[23:31])
                    toggle = 0
                elif toggle == 0:
                    toggle = 1
        return q2results[:-1]


def makeTable(dataSet):
    #---------------------------------------------------------------------------
    #---------------------------- Load in Libraries ----------------------------
    #---------------------------------------------------------------------------
    from os import rename, listdir, remove, path, getcwd, remove, chdir, makedirs
    #---------------------------------------------------------------------------
    #----------------------- Description of Function ---------------------------
    #---------------------------------------------------------------------------
    '''
    This is a little tool I made to quickly look at all the q2 values so I didn't
    have to open them all by hand like a god damn pleb.

    It doesn't inherintly do anything, but the next part will let you pull
    directly from whatever section you view as the best into a text file (I
    haven't made it yet and I am already hyping it up too much).

    If there is not functional part 9 then I didn't feel like doing it, i am
    sorry

    Anyway, this cycles through source data and makes a big table for you
    to view all the q2 values

    '''
    #---------------------------------------------------------------------------
    #-------------------- Navigate to the source folder-------------------------
    #---------------------------------------------------------------------------
    chdir("./../7.QsarResults/" + dataSet)
    CoMFAResults, H1Results, H2Results = [], [], []

    stdErrors = ["0.1","0.01","0.001"]

    for k in stdErrors:
        chdir("./" + dataSet + "-" + k)
        CoMFAResults.append(extractData("CoMFA.pls"))
        H1Results.append(extractData("H1.pls"))
        H2Results.append(extractData("H2.pls"))
        chdir("./..")

    #---------------------------------------------------------------------------
    #-------------------- Getting Results --------------------------------------
    #---------------------------------------------------------------------------
    print "-----------------------------------------------------------------------"
    print " Q2 Results : CoMFA"
    print "-----------------------------------------------------------------------"
    print "---------------------- | ---------------------- | ----------------------"
    print "StdError of :  0.1                 0.01                     0.001"
    print "---------------------- | ---------------------- | ----------------------"
    counter = 0
    for k in enumerate(CoMFAResults[0]):
        print "Set " + str(counter + 1) + "        " + CoMFAResults[0][counter] + "              " + CoMFAResults[1][counter] + "                  " + CoMFAResults[2][counter]
        counter +=1

    #---------------------------------------------------------------------------
    #-------------------- Setting up for H1 ------------------------------------
    #---------------------------------------------------------------------------
    print "-----------------------------------------------------------------------"
    print " Q2 Results : H1"
    print "-----------------------------------------------------------------------"
    print "---------------------- | ---------------------- | ----------------------"
    print "StdError of :  0.1                 0.01                     0.001"
    print "---------------------- | ---------------------- | ----------------------"
    counter = 0
    for k in enumerate(H1Results[0]):
        print "Set " + str(counter + 1) + "        " + H1Results[0][counter] + "              " + H1Results[1][counter] + "                  " + H1Results[2][counter]
        counter +=1


    #---------------------------------------------------------------------------
    #-------------------- Setting up for H2 ------------------------------------
    #---------------------------------------------------------------------------
    print "-----------------------------------------------------------------------"
    print " Q2 Results : H2"
    print "-----------------------------------------------------------------------"
    print "---------------------- | ---------------------- | ----------------------"
    print "StdError of :  0.1                 0.01                     0.001"
    print "---------------------- | ---------------------- | ----------------------"
    counter = 0
    for k in enumerate(H2Results[0]):
        print "Set " + str(counter + 1) + "        " + H2Results[0][counter] + "              " + H2Results[1][counter] + "                  " + H2Results[2][counter]
        counter +=1



#-------------------------------------------------------------------------------
# Remove the bad data sets
#-------------------------------------------------------------------------------
dataSet = sys.argv[1]
makeTable(dataSet)

#
