
from os import walk
from sklearn.metrics.cluster import normalized_mutual_info_score
import CommonConstants
import os


class Testing:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.uop_array = []
        self.uop = []
        self.vector = []
        self.data_set = []

    def extract_opcodes(self):
        print("\n***** extract_opcodes *****")
        self.uop_array = []
        files = []
        for (dirpath, dirnames, filenames) in walk(self.folder_path):
            files.extend(filenames)
            break
        print(files)

        i = 0
        while i < len(files):
            try:
                with open(self.folder_path + "/" + files[i], "r") as filestream:
                    for line in filestream:
                        current_line = line.split(',')
                        for inst in current_line:
                            if inst not in self.uop_array and inst != "" and inst != "\n":
                                self.uop_array.append(inst)

            except Exception as err:
                print(err)
            if os.path.exists(self.folder_path + "/" + files[i]):
                os.remove(self.folder_path + "/" + files[i])
            i += 1

        print("size arr: ", len(self.uop_array))
        print(self.uop_array)

    def construct_vector(self):
        print("\n***** construct_vector *****")
        for i in range(0, len(self.uop)):
            self.vector.append(0)

        for i in self.uop_array:
            try:
                index = self.uop.index(i)
                self.vector[index] = 1
            except ValueError:
                None

        print("size vector: ", len(self.vector))
        print(self.vector)

    def get_uop_array(self,filename):
        print("\n***** get_uop_array *****")
        self.uop = []
        with open(filename, "r") as filestream:
            for line in filestream:
                current_line = line.split()
                for inst in current_line:
                    if inst not in self.uop and inst != "" and inst != "\n":
                        self.uop.append(inst)
        print("size uop: ", len(self.uop))
        print(self.uop)

    def print_arr(self, arr):
        print("***** print_arr *****")
        for i in arr:
            print(i)

    def read_data_set(self):
        print("***** read_data_set *****")
        self.data_set = []
        try:
            with open("../vector.txt", "r") as filestream:
                for line in filestream:
                    file = []
                    current_line = line.split(",")
                    for inst in current_line:
                        if inst != "" and inst != "\n":
                            file.append(inst)
                    self.data_set.append(file)

        except Exception as err:
            print(err)
        self.print_arr(self.data_set)

    def testing_run(self):
        print("***** testing_run *****")
        self.folder_path = self.folder_path + "/opcode"
        self.extract_opcodes()
        self.get_uop_array(CommonConstants.setofuniquecodes)
        self.construct_vector()
        self.read_data_set()

        result = []
        for i in range(len(self.data_set)):
            print(normalized_mutual_info_score(self.vector, self.data_set[i]))
            result.append(normalized_mutual_info_score(self.vector, self.data_set[i]))

        if max(result) > 0.3:
            return True
        else:
            return False



