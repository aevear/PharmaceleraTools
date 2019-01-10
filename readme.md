# PharmaceleraTools

This is a set of tools I created/used during my internship at Pharmacelera that I later made into a fully automated program. It automates the majority of a task that previously took two months to preform in a matter of hours (or maybe a full couple of days depending on what you use).

## Goal of the Project

This code actually preformed my entire masters thesis project aside from a small amount of human analysis at the end. Other than that it would run through the entire set of imported molecule libraries at the beginning and preforms Molecular Parameterization then several QSAR processes. After that, it extracts the relevant data that we used to conclude our analysis for the user to read with greater ease.

## Getting Started

While this is not the most elegant set of code it was cobbled together based on several scripts that I ended up creating to solve smaller scale problems at my internship that I eventually tied together and turned into a fully functional program.

Unfortunately since the code requires use of Pharmacelera's Programs it will not be runnable by most people (aside from those who subscribe to their product). This is more of an education process detailing how it would be done.


### Prerequisites

The code requires use of Pharmacelera PharmQSAR and PharmScreen to fully run and will most likely not be available to most people as it is proprietary. It runs python without many imported libraries so you shouldn't have to worry about that.




## Code Breakdown

### Part 0: Run the Project Script

The comments in the code should already be able to explain how it works in more detail so this will just be an overview. What this code does is read all of the directories that are located in 0.SourceFiles then begin to cycle through each of them in order for part 1, 2 and 3 for a single batch of molecules before switching to the next batch.

#### Run PharmScreen

After all of the batches of molecules have been Parameterized (which is far and away the most time and computer resource intensive task involved here) it begins to perform a variety of QSAR analysis on each of the batches in order.

#### Run PharmQSAR

This part runs the QSAR portion of the program, cycling though each of the directories found in the original SourceFile Directory.

The reason for the break is that if there were errors, it would be easier to break the process in half and save having to redo the entire process again.

#### Actual Code that I used

This was more for my use than anyone else's but it contained the code that would be needed for each part of the program. It was a good place to store a list of commands that can be referenced later.

### Part 1: Renaming/Absent Script

This was one of the first thing that I made ( I would have a lot more functions but it really was meant originally to be a one time thing).

So what this code does is go through each of the molecules found in whatever molecular batch we are looking into at the moment and looks to see if they exist in a "Directory" of molecules located also in the Directory.

It then copies over all the files and changes their name to be mol1, mol2....etc. It also will list all of the molecules that did not work out so that the user of the code can examine what went wrong if need be.

While renaming it also splits the entire list into training and test data, with the test data going later in the list.

After performing the reorganization process, the renaming process and ejecting all of the failed molecules it will then generate a table detailing what all happened called "(dataset)conversionTable" so that later we have a reference.


### Part 2: Merge Files

Quite a simple part but still difficult to implement. This section merges all of the molecule files into a single file that can be used by PharmaScreen for Parameterization.


### Part 3: Alignment/runPharmScreen

Here there are actually two files named "3.whatever". This is because in later testing we wanted to use PharmaScreen Alignment tool to see if we could get better results. Use the alignment tool if you want alignments.

Otherwise this program exports all the data to a new folder and runs PharmaScreen on it. Simple really.


### Part 4: Remove Bad Variables

So this one will need some explaining...

Basically, PHARMSCREEN and QSAR can't really handle some molecule types, due to its fairly unpolished nature. Therefore I found it necessary to just remove anything that cannot be processed by PharmaScreen. Not the most accurate system but this is what we found happened.


### Part 5: Pre-QSAR

This section details cleaning up the post-parameterization file into a more usable file for PharmQSAR. PharmScreen requires that everything is in one merged file while PharmQSAR requires that each molecule is separate. Not optimal at all in any way.

This section is also just a bit buggy as it is based on mol2 but has a few numbers changed as PharmScreen uses variables not used in other Parameterization process so that it is incompatible with anyone else's code.

They also did not use a new name, just continued to use mol2. Very confusing. This section also had issues due to errors in part to the ridiculous text format used here that really shouldn't exist. They delimitate the different sections by spaces that sometimes in large molecules or those with strange components to merge together in the text file. Truly strange but what do I know.

My single most buggy section of code I hope that no one else will ever have to deal with. Edit at your own risk.

### Part 6: Initial QSAR

This part is after the data is cleaned and ready to go. Here we need to set up the architecture that we will need for performing QSAR on the files as it requires some specific parts. We need to...
* Move over the corrected version table file for the configuration file
* Generate config files for each of the three types of QSAR that we will be performing.
* Set up the needed files for QSAR that basically consist of giant empty grids that will use later.

Mostly just cleaning everything up for the QSAR program as it is not robust at all.


### Part 7: Run QSAR

Ok now we are actually performing QSAR. This program runs three different ones. First is CoMFA then Pharmacelera's H1 and H2 that uses different properties of a molecule to gain more accurate at estimating its potential reactivity.

It also performs QSAR for all three of these systems with three different stdErrors, 0.1, 0.01, 0.001 respectively.


### Part 8: Analysis

This part was just to stop myself from getting a headache. It pulls all the data needed for a person to make an estimated guess on which of the systems performed the best and at what stdError. Just pulls out the data and makes a pretty table to pull from. Very nice really.


### Part 9: Pull Results

This part takes whatever you decided is the best for each molecular set and StrError and gives you a copy and paste version of the results that gives all the interesting data points one might need. Again, this was mostly just to stop myself from having to spend an entire day copy and pasting data.

It provides the information on...
* r2 (train)
* q2
* S
* Spress
* r2 (test)
* sTest
* Nc
* ELE
* NELE



## Conclusion

Well I hope that was somewhat explanatory, albeit it might be hard to see for sure if it works without using their software. (Try their trial version?)
