from optparse import OptionParser
import subprocess
import sys
import os
import time
# set up options
parser = OptionParser()
parser.add_option("-d", action="store", type="str", dest="location")
parser.add_option("-m", action="store", type="str", dest="mutant")
(options, args) = parser.parse_args()

def checkforlocation():
    if options.location != None :
        print("location check")
    else :
        print("pdb file not specified")
        sys.exit(0)
def checkformutantorlist():
    l=0
    if options.mutant == None:
        print("please use -m to specify a mutant example: -m A1M")
        print("Or use -l to specify a file containing a list of mutants example: -l /yourpath/mutants.txt")
        sys.exit(0)
def buildlistofresidues():
    if options.location != None:
        tf = open(options.location)
        List_Of_Original_Residues = open("list_of_original_residues.txt", "w+")
    else:
        print("pdb file not specified")
        sys.exit(0)
    l = 0
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
                    if Sequence[n] != "SEQRES" and Sequence[n] != "" and Sequence[n] != "A" and Sequence[n] != "B" and Sequence[n] != "471" and Sequence[n].__len__() == 3:
                        List_Of_Original_Residues.write(Sequence[n] + Res_Num.__str__() + "\n")
                        n = n + 1
                        Res_Num = Res_Num + 1
                    else:
                        n = n + 1
def formatmutant():
    if options.mutant != None:
        Length_Of_Input = options.mutant.__len__()
        Original_Residue = options.mutant[0:1]
        Mutant_Residue = options.mutant[Length_Of_Input - 1:Length_Of_Input]
        Residue_id = options.mutant[1:Length_Of_Input - 1]
        print(Length_Of_Input, Residue_id, Original_Residue, Mutant_Residue)
    global Query_Residue
    global Target_Residue
    Query_Residue = " "+Residue_id+"  "+Three_Letter_Codes[Original_Residue.upper()]
    Target_Residue = " "+Residue_id+"  "+Three_Letter_Codes[Mutant_Residue.upper()]
def confirmresidue():
    with open(options.location) as search:
        Res_Num = 1
        for line in search:
            if line.find(Query_Residue) != -1:
                print("exists")
                print(line)
                break
            else:
                print("not yet")
                continue
        if line.find(Query_Residue) == -1:
            print("original residue does not exist")
            sys.exit(0)
def openmutantfile():
    tf = options.location
    f = open(tf)
    content = f.read()
    fh = open("mutant.crd", "w+")
    our_str = Query_Residue  # use spaces not tabs
    contents = content.replace(our_str, Target_Residue)  # use spaces not tabs
    fh.writelines(contents)
def checktask(a,b):
    if os.path.isfile(a) != True:
        os.system(b)
        while os.path.isfile(a) != True:
            continue
def IsJobActive(step):
    JobActive = True
    while JobActive == True:
        fh = open("checkforactive")
        os.system("qstat > checkforactive")
        QueueStatus = fh.read()
        print("step{0}_{1}".format(step,New_File_Name) in QueueStatus)
        if "step{0}_{1}".format(step,New_File_Name) in QueueStatus:
            JobActive = True
        else:
            JobActive = False
            print("job is not running")
def Make_New_Submission_File():
    if os.path.isfile("namd/{0}".format(New_File_Name)) != True:
        Script = open("namd/ssnamd.txt")
        content = Script.read()
        fh = open("namd/{0}".format(New_File_Name), "w+")
        LogFileName = "{0}step4.log".format(New_File_Name)
        New_content = content.replace("cyto", "step4_{0}".format(New_File_Name))
        New_content = New_content.replace("logfile", LogFileName)
        fh.writelines(New_content)
def Submit_Job():
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
def Submit_Production_Step():
    if os.path.isfile("{0}step4.log".format(New_File_Name)):
        Step_4_Log = open("{0}step4.log".format(New_File_Name))
        S4L_Read = Step_4_Log.read()
        if "End of program" in S4L_Read:
            print("you are here")
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
checkforlocation()
checkformutantorlist()
# buildlistofresidues()
formatmutant()
confirmresidue()
openmutantfile()
Mutant = options.mutant
New_File_Name = Mutant.upper()
Make_New_Submission_File()
Submit_Job()
