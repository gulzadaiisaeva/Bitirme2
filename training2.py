
from os import walk
import CommonConstants


class Training:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.uop_array=[]
        self.uop=set([])
        self.matrix=[]

    def get_unique_code(self):
        print("***** get_unique_code *****")
        files = []
        for (dirpath, dirnames, filenames) in walk(self.folder_path):
            files.extend(filenames)
            break
        print(files)

        i = 0
        while i < len(files):
            try:
                with open(self.folder_path+"/" + files[i], "r") as filestream:
                    file = []
                    for line in filestream:
                        currentline = line.split(",")
                        for inst in currentline:
                            if inst not in file:
                                file.append(inst)
                    self.uop_array.append(file)

            except Exception as err:
                print(err)
            i += 1
        self.write_to_file(self.uop_array)

    def write_to_file(self,list):
        print("***** write_to_file *****")
        for line in list:
            for inst in line:
                with open("../uniqueopcodes.txt", "a") as myfile:
                    myfile.write(inst)
                    myfile.write(", ")
            with open("../uniqueopcodes.txt", "a") as myfile:
                myfile.write("\n\n")

    def print_list(self,list):
        print("***** print_list *****")
        for line in list:
            for inst in line:
                print(inst, end =" ")
            print("\n")

    def set_folder_path(self,new_folder):
        self.folder_path = new_folder

    def get_max_unique(self):
        print("***** get_max_unique *****")
        for line in self.uop_array:
            for inst in line:
                self.uop.add(inst)
        print(len(self.uop))

    def create_matrix(self):
        print("***** create_matrix *****")
        temp_list = []
        for i in range(len(self.uop)):
            temp_list.append(0)
        for j in range(len(self.uop)):
            self.matrix.append(temp_list)

    def fill_matrix(self, start, end):
        print("***** fill_matrix *****")
        for i in range(start, end):
            for j in range(len(self.uop_array[i])-1):
                print(self.uop_array[i][j], self.uop_array[i][j+1])
                first_index = self.find_index_in_set(self.uop, self.uop_array[i][j])
                second_index = self.find_index_in_set(self.uop, self.uop_array[i][j+1])
                self.matrix[first_index][second_index] += 1

    def find_index_in_set(self, list, element):
        index = 0
        for i in list:
            if element is i:
                return index
            index += 1
        return -1

    def print_matrix(self):
        print("***** print_matrix *****")
        for row in self.matrix:
            for col in row:
                print(col, end=" ")
            print("\n")

        '''i = 0
        for row in self.matrix:
            for col in row:
                with open("../matrix.txt", "a") as myfile:
                    myfile.write(col)
                    myfile.write("    ")
            with open("../matrix.txt", "a") as myfile:
                myfile.write("\n")'''

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
#project.print_list(project.uop_array)

for inst in project.uop:
    with open("../setofuniqueopcodes.txt", "a") as myfile:
        myfile.write(inst)
        myfile.write(" ")

project.create_matrix()
project.fill_matrix(0,25)
project.print_matrix()
