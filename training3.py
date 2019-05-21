
from os import walk
import CommonConstants
import csv
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Training:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.uop_array = []
        self.uop = []
        self.matrix = []

    def fill_unique_code_arr(self):
        print("***** fill_unique_code_arr *****")
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
                        current_line = line.split(",")
                        for inst in current_line:
                            if inst not in file and inst != "" and inst !="\n":
                                file.append(inst)
                    self.uop_array.append(file)

            except Exception as err:
                print(err)
            i += 1

        print("size arr: ", len(self.uop_array))

    def get_all_uop(self):
        print("***** get_all_uop *****")
        for line in self.uop_array:
            for inst in line:
                if inst not in self.uop and inst != "":
                    self.uop.append(inst)
        print("size uop: ", len(self.uop))

    def create_matrix(self, size):
        print("***** create_matrix *****")
        for j in range(size):
            temp_list = []
            for i in range(size):
                temp_list.append(0)
            self.matrix.append(temp_list)

    def fill_matrix(self, start, end):
        print("***** fill_matrix *****")
        for i in range(start, end):
            #print("range: ", (len(self.uop_array[i])) - 1)
            for j in range((len(self.uop_array[i]))-1):
                try:
                    first_index = self.uop.index(self.uop_array[i][j])
                    second_index = self.uop.index(self.uop_array[i][j+1])
                except ValueError:
                    print("Errrror ****************************")
                self.matrix[second_index][first_index] += 1
                self.matrix[first_index][second_index] += 1

    def write_to_file(self, arr):
        print("***** write_to_file *****")
        for line in arr:
            for inst in line:
                with open("../uniqueopcodes.txt", "a") as myfile:
                    myfile.write(inst)
                    myfile.write(", ")
            with open("../uniqueopcodes.txt", "a") as myfile:
                myfile.write("\n\n")

        for inst in self.uop:
            with open("../setofuniqueopcodes.txt", "a") as myfile2:
                myfile2.write(inst)
                myfile2.write(" ")

    def print_arr(self, arr):
        print("***** print_list *****")
        for line in arr:
            for inst in line:
                print(inst, end =" ")
            print("\n")

    def print_matrix(self):
        print("***** print_matrix *****")
        '''for row in self.matrix:
            for col in row:
                print(col, end=" ")
            print("\n")'''

        i = 0
        for row in self.matrix:
            for col in row:
                with open("../matrix.txt", "w") as myfile:
                    myfile.write(str(col))
                    myfile.write("    ")
            with open("../matrix.txt", "w") as myfile:
                myfile.write("\n\n")

    def set_folder_path(self, new_folder):
        self.folder_path = new_folder

    def write_csv(self):
        with open('matrix.csv', mode='w') as csv_file:
            for line in self.matrix:
                csv_file.write(str(line))
                csv_file.write('\n')

    def draw_graph(self, graph):

        # extract nodes from graph
        nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

        # create networkx graph
        G = nx.Graph()

        # add nodes
        for node in nodes:
            G.add_node(node)

        # add edges
        for edge in graph:
            G.add_edge(edge[0], edge[1])

        # draw graph
        pos = nx.shell_layout(G)
        nx.draw(G, pos)

        # show graph
        plt.show()

project = Training("../dataset/G2")
project.fill_unique_code_arr()
project.set_folder_path("../dataset/MPCGEN")
project.fill_unique_code_arr()
project.set_folder_path("../dataset/MWOR_backup")
project.fill_unique_code_arr()
project.set_folder_path("../dataset/NGVCK")
project.fill_unique_code_arr()
project.set_folder_path("../dataset/PSMPC")
project.fill_unique_code_arr()
project.get_all_uop()
#project.print_arr(project.uop_array)
project.write_to_file(project.uop_array)
project.create_matrix(len(project.uop))
project.fill_matrix(0, 15)
project.print_matrix()
#project.write_csv()




# draw example
graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
project.draw_graph(graph)
