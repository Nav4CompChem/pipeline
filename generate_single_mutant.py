from optparse import OptionParser
import subprocess
import sys
import os
import time

# set up options
parser = OptionParser()
parser.add_option("-d", action="store", type="str", dest="location")
parser.add_option("-l", action="store", type="str", dest="List_Of_Mutants")
parser.add_option("-m", action="store", type="str", dest="mutant")
(options, args) = parser.parse_args()
print(options.location, "exists")

# exit if no pdb file is specified
if options.location != None:
    tf = open(options.location)
    List_Of_Original_Residues = open("list_of_original_residues.txt", "w+")
else:
    print("pdb file not specified")
    sys.exit(0)
l = 0
if options.mutant == None and options.List_Of_Mutants == None:
    print("please use -m to specify a mutant example: -m A1M")
    print("Or use -l to specify a file containing a list of mutants example: -l /yourpath/mutants.txt")
    sys.exit(0)

# Build a list of amino acids in pdb file

with open(options.location) as search:
    Res_Num = 1
    for line in search:
        if line.find("SEQRES") == -1 or line.find("B") != -1:
            continue
        else:
            l = l + 1
            Sequence = line.split(" ")
            n = 0
            while (n < Sequence.__len__()):
                if Sequence[n] != "SEQRES" and Sequence[n] != "" and Sequence[n] != "A" and Sequence[n] != "B" and \
                        Sequence[n] != "471" and Sequence[n].__len__() == 3:
                    List_Of_Original_Residues.write(Sequence[n] + Res_Num.__str__() + "\n")
                    n = n + 1
                    Res_Num = Res_Num + 1
                else:
                    n = n + 1
            # print(Sequence[0:Sequence.__len__()])
            # print(line,l)

# convert mutation to proper format
if options.mutant != None:
    Length_Of_Input = options.mutant.__len__()
    Original_Residue = options.mutant[0:1]
    Mutant_Residue = options.mutant[Length_Of_Input - 1:Length_Of_Input]
    Residue_id = options.mutant[1:Length_Of_Input - 1]
    print(Length_Of_Input, Residue_id, Original_Residue, Mutant_Residue)
if options.List_Of_Mutants != None:
    Mutant_List_Directory = open(options.List_Of_Mutants)
    Mutant_List = Mutant_List_Directory.read()

Three_Letter_Codes = {"A": "ALA",
                      "R": "ARG",
                      "H": "HIS",
                      "K": "LYS",
                      "D": "ASP",
                      "E": "GLU",
                      "S": "SER",
                      "T": "THR",
                      "N": "ASN",
                      "Q": "GLN",
                      "C": "CYS",
                      "G": "GLY",
                      "P": "PRO",
                      "I": "ILE",
                      "L": "LEU",
                      "M": "MET",
                      "F": "PHE",
                      "Y": "TYR",
                      "W": "TRP",
                      "V": "VAL"
                      }

print(Three_Letter_Codes[Mutant_Residue.upper()])

Query_Residue = Three_Letter_Codes[Original_Residue.upper()] + " P   " + Residue_id
Target_Residue = Three_Letter_Codes[Mutant_Residue.upper()] + " P   " + Residue_id

with open(options.location) as search:
    Res_Num = 1
    for line in search:
        if line.find(Query_Residue) != -1:
            print("original residue does exist")
            break
        else:
            continue
    if line.find(Query_Residue) == -1:
        print("original residue does not exist")
        sys.exit(0)
print(Query_Residue, Target_Residue)

n = 0
m = sys.argv.__len__()

print(type(n) == int)
o = sys.argv[0]
print(type(n))

"""while (n < m):
    if (type(sys.argv[n]) == str):
        print (sys.argv[n]+"is a string")
        print (type(sys.argv[n]))
        n += 1
    else:
        print (sys.argv[n]+"is an int")
        print (type(sys.argv[n]))
        n += 1"""

tf = options.location
f = open(tf)
content = f.read()
fh = open("mutant.pdb", "w+")

our_str = Query_Residue  # use spaces not tabs
contents = content.replace(our_str, Target_Residue)  # use spaces not tabs
fh.writelines(contents)

# os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm < step1_pdbreader.inp > step1_pdbreader.log")
print(os.path.isfile("step1_pdbreader.log") != True, "helo")
while os.path.isfile("step1_pdbreader.log") != True:
    continue
if os.path.isfile("step2.1_waterbox.prm") != True:
    os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm < step2.1_waterbox.inp > step2.1_waterbox.log")
    while os.path.isfile("step2.1_waterbox.prm") != True:
        continue
if os.path.isfile("step2.2_ions.prm") != True:
    os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm < step2.2_ions.inp > step2.2_ions.log")
    while os.path.isfile("step2.2_ions.prm") != True:
        continue
if os.path.isfile("step2_solvator.str") != True:
    os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm < step2_solvator.inp > step2_solvator.log")
    while os.path.isfile("step2_solvator.str") != True:
        continue
if os.path.isfile("step3_pbcsetup.str") != True:
    os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm < step3_pbcsetup.inp > step3_pbcsetup.log")
    while os.path.isfile("step3_pbcsetup.str") != True:
        continue
if os.path.isfile("namd/restraints/sc_rmsd.ref") != True:
    os.system("/RQusagers/nkooner/charmm/exec/gnu/charmm step3_input.inp > step3_input.log")
    while os.path.isfile("namd/restraints/sc_rmsd.ref") != True:
        continue
Mutant = options.mutant
New_File_Name = Mutant.upper()
if os.path.isfile("namd/{0}".format(New_File_Name)) != True:
    Script = open("namd/ssnamd.txt")
    content = Script.read()
    fh = open("namd/{0}".format(New_File_Name), "w+")
    LogFileName = "{0}step4.log".format(New_File_Name)
    New_content = content.replace("cyto", "step4_{0}".format(New_File_Name))
    New_content = New_content.replace("logfile", LogFileName)
    fh.writelines(New_content)

fh = open("checkforactive")
os.system("qstat > checkforactive")

if "step4_{0}".format(New_File_Name) not in fh.read():
    print("you're in first level")
    if os.path.isfile("{0}step4.log".format(New_File_Name)):
        Step_4_Log = open("{0}step4.log".format(New_File_Name))
        S4L_Read = Step_4_Log.read()
        if "End of program" not in S4L_Read:
            os.system("qsub namd/{0} >> submission.log".format(New_File_Name))
        else:
            print("no submission")
    else:
        os.system("qsub namd/{0} >> submission.log".format(New_File_Name))

else:
    print("no submission")

def IsJobActive(step):
    JobActive = True
    while JobActive == True:
        fh = open("checkforactive")
        os.system("qstat > checkforactive")
        QueueStatus = fh.read()
        print("step{0}_{1}".format(step,New_File_Name) in QueueStatus)
        if "step{0}_{1}".format(step,New_File_Name) in QueueStatus:
            JobActive = True
            print("job is running")
            time.sleep(60)
        else:
            JobActive = False
            print("job is not running")

IsJobActive("4")

JobActive = True
while JobActive == True:
    fh = open("checkforactive")
    os.system("qstat > checkforactive")
    QueueStatus = fh.read()
    print("step4_{0}".format(New_File_Name) in QueueStatus)
    if "step4_{0}".format(New_File_Name) in QueueStatus:
        JobActive = True
        print("job is running")
        time.sleep(60)
    else:
        JobActive = False
        print("job is not running")

if os.path.isfile("{0}step4.log".format(New_File_Name)):
    Step_4_Log = open("{0}step4.log".format(New_File_Name))
    S4L_Read = Step_4_Log.read()
    if "End of program" in S4L_Read:
        if os.path.isfile("namd/{0}step5".format(New_File_Name)) != True:
            Script = open("namd/ssnamd.txt")
            content = Script.read()
            fh = open("namd/{0}step5".format(New_File_Name), "w+")
            LogFileName = "{0}step5.log".format(New_File_Name)
            New_content = content.replace("cyto", "step5_{0}".format(New_File_Name))
            New_content = New_content.replace("step4_equilibration.inp", "step5_production.inp")
            New_content = New_content.replace("logfile", LogFileName)
            fh.writelines(New_content)
        fh = open("checkforactive")
        os.system("qstat > checkforactive")
        if "step5_{0}".format(New_File_Name) not in fh.read():
            if os.path.isfile("{0}step5.log".format(New_File_Name)):
                tf = open("{0}step5.log".format(New_File_Name))
                Check_For_Step_5 = tf.read()
                if "End of program" not in Check_For_Step_5:
                    os.system("qsub namd/{0}step5 >> submission.log".format(New_File_Name))
                else:
                    print("no submission")
            elif not os.path.isfile("{0}step5.log".format(New_File_Name)):
                os.system("qsub namd/{0}step5 >> submission.log".format(New_File_Name))
            else:
                print("no submission")



else:
    print("equilibration not done")
    sys.exit(0)
JobActive = True
while JobActive == True:
    fh = open("checkforactive")
    os.system("qstat > checkforactive")
    QueueStatus = fh.read()
    print("step5_{0}".format(New_File_Name) in QueueStatus)
    if "step5_{0}".format(New_File_Name) in QueueStatus:
        JobActive = True
        print("job is running")
        time.sleep(60)
    else:
        JobActive = False
        print("job is not running")

"""import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=str, nargs='+', help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const', const=, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()
print args.accumulate(args.integers)"""