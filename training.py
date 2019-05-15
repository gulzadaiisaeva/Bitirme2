
from os import walk
import CommonConstants


class Training:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.uniqOpCodeArray=[]

    def getUniqueCode(self):
        files = []
        for (dirpath, dirnames, filenames) in walk(self.folderpath):
            files.extend(filenames)
            break
        print(files)

        i = 0
        while i < len(files):
            try:
                with open(self.folderpath+"/" + files[i], "r") as filestream:
                    thisset = []
                    for line in filestream:
                        currentline = line.split(",")
                        for inst in currentline:
                            if(inst not in thisset):
                                thisset.append(inst)
                    self.uniqOpCodeArray.append(thisset)

            except Exception as err:
                print(err)
            i += 1
        print("Unique code:")
        self.printList(self.uniqOpCodeArray)

    def printList(self,list):
        print(len(list))
        for line in list:
            #print(line)
            print(len(line))
            for inst in line:
                with open("../uniqueopcodes.txt", "a") as myfile:
                    myfile.write(inst)
                    myfile.write(", ")
            with open("../uniqueopcodes.txt", "a") as myfile:
                myfile.write("\n\n")


project = Training(CommonConstants.dir_name+"/opcode")
project.getUniqueCode()
