
from os import walk
import CommonConstants


class Training:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.uniqOpCodeArray=[]
        self.setOfAllUniqueCode=set([])
    def get_unique_code(self):
        files = []
        for (dirpath, dirnames, filenames) in walk(self.folderpath):
            files.extend(filenames)
            break
        print(files)

        i = 0
        while i < len(files):
            try:
                with open(self.folderpath+"/" + files[i], "r") as filestream:
                    file = []
                    for line in filestream:
                        currentline = line.split(",")
                        for inst in currentline:
                            if inst not in file:
                                file.append(inst)
                    self.uniqOpCodeArray.append(file)

            except Exception as err:
                print(err)
            i += 1
        print("Unique code:")
        self.write_to_file(self.uniqOpCodeArray)

    def write_to_file(self,list):
        print("printList")
        for line in list:
            for inst in line:
                with open("../uniqueopcodes.txt", "a") as myfile:
                    myfile.write(inst)
                    myfile.write(", ")
            with open("../uniqueopcodes.txt", "a") as myfile:
                myfile.write("\n\n")

    def set_folder_path(self,newFolder):
        self.folderpath = newFolder

    def get_max_unique(self):
        print("get_max_unique")
        for line in self.uniqOpCodeArray:
            for inst in line:
                self.setOfAllUniqueCode.add(inst)
        print(len(self.setOfAllUniqueCode))

project = Training("../dataset/G2")
project.get_unique_code()
project.set_folder_path("../dataset/MPCGEN")
project.get_unique_code()
project.set_folder_path("../dataset/MWOR_backup")
project.get_unique_code()
project.set_folder_path("../dataset/NGVCK")
project.get_unique_code()
project.set_folder_path("../dataset/PSMPC")
project.get_unique_code()
project.get_max_unique()
