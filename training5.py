
from os import walk
import CommonConstants
from graph import Graph
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

from numpy import genfromtxt
import numpy as np


class Training:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.uop_array = []
        self.all_uop = []
        self.matrix = []
        self.threshold = 1
        self.vector = []
        self.N = 0  # N ← The number of unique opcodes in S;

    def extract_unique_opcode(self):
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
                if inst not in self.all_uop and inst != "":
                    self.all_uop.append(inst)
        self.N = len(self.all_uop)
        print("size uop: ", self.N)

    def create_matrix(self, size):
        print("***** create_matrix *****")
        self.matrix = []
        for j in range(size):
            temp_list = []
            for i in range(size):
                temp_list.append(0)
            self.matrix.append(temp_list)

    def fill_matrix(self, start, end):
        print("***** fill_matrix *****")
        for i in range(start, end):
            for j in range(0,(len(self.uop_array[i]))-1):
                for k in range(j+1, len(self.uop_array[i])):
                    try:
                        first_index = self.all_uop.index(self.uop_array[i][j])
                        second_index = self.all_uop.index(self.uop_array[i][k])
                    except ValueError:
                        print("Errrror ****************************")
                    self.matrix[second_index][first_index] += 1
                    self.matrix[first_index][second_index] += 1

        self.normalization(self.N)
        self.eliminate_weak_relations()

    def normalization(self, uop):
        print("***** normalization *****")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] /= uop

    def eliminate_weak_relations(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] < self.threshold:
                    self.matrix[i][j] = 0

    def print_arr(self, arr):
        print("***** print_list *****")
        for line in arr:
            for inst in line:
                print(inst, end =" ")
            print("\n")

    def print_matrix(self):
        print("***** print_matrix *****")
        for row in self.matrix:
            for col in row:
                print(col, end=" ")
            print("\n")

    def set_folder_path(self, new_folder):
        self.folder_path = new_folder

    def write_vectors_to_file(self):
        print("***** write_vectors_to_file *****")
        for i in self.vector:
            with open("../vector.txt", "a") as myfile:
                myfile.write(str(i))
                myfile.write(",")
        with open("../vector.txt", "a") as myfile:
            myfile.write("\n")

    def write_matrix_to_csv(self, filename):
        print("***** write_csv *****")
        with open(filename, 'w') as csvFile:
            writer = csv.writer(csvFile)
            temprow = []
            temprow.append('')
            for inst in self.all_uop:
                temprow.append(inst)
            writer.writerow(temprow)

            i = 0
            for row in self.matrix:
                temprow = []
                temprow.append(self.all_uop[i])
                for col in row:
                    temprow.append(col)
                writer.writerow(temprow)
                i += 1
        csvFile.close()

    def write_uniqs_to_file(self, arr):
        print("***** write_uniqs_to_file *****")
        '''for line in arr:
            for inst in line:
                with open("../uniqueopcodes.txt", "a") as myfile:
                    myfile.write(inst)
                    myfile.write(", ")
            with open("../uniqueopcodes.txt", "a") as myfile:
                myfile.write("\n\n")'''

        for inst in self.all_uop:
            with open("../setofuniqueopcodes.txt", "a") as myfile2:
                myfile2.write(inst)
                myfile2.write(" ")

    def empty_matrix(self):
        print("***** empty_matrix *****")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = 0

    def construct_co_opcode_graphs(self):
        print("***** construct_co_opcode_graphs *****")
        j = 0
        for i in range(0, len(self.uop_array), CommonConstants.family_size):
            filename = "../dataset/matrix_csv/matrix" + str(j) + ".csv"
            self.create_matrix(self.N)
            self.fill_matrix(i, i + CommonConstants.family_size)
            #self.write_matrix_to_csv(filename)
            index, cc = self.largest_connected_component()
            self.extract_engine_signature(cc[index])
            self.write_vectors_to_file()
            j += 1

    def run(self):
        if os.path.exists("../uniqueopcodes.txt"):
            os.remove("../uniqueopcodes.txt")
        if os.path.exists("../setofuniqueopcodes.txt"):
            os.remove("../setofuniqueopcodes.txt")
        if os.path.exists("../vector.txt"):
            os.remove("../vector.txt")
        self.extract_unique_opcode()
        self.set_folder_path("../dataset/MPCGEN")
        self.extract_unique_opcode()
        self.set_folder_path("../dataset/MWOR_backup")
        self.extract_unique_opcode()
        self.set_folder_path("../dataset/NGVCK")
        self.extract_unique_opcode()
        self.set_folder_path("../dataset/PSMPC")
        self.extract_unique_opcode()
        self.get_all_uop()
        self.write_uniqs_to_file(self.uop_array)
        self.construct_co_opcode_graphs()

    def largest_connected_component(self):
        print("\n***** largest_connected_component *****")
        g = Graph(len(self.matrix))
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    g.addEdge(i, j)
        cc = g.connectedComponents()

        maximum = 0
        index = -1
        for i in range(len(cc)):
            if maximum < len(cc[i]):
                maximum = len(cc[i])
                index += 1

        return index, cc

    def extract_engine_signature(self, arr):
        print("\n***** construct_vector *****")
        self.vector = []
        for i in range(0, self.N):
            self.vector.append(0)

        for i in arr:
            self.vector[i] = 1
        print("size vector: ", len(self.vector))
        print(self.vector)

project = Training("../dataset/G2")
project.run()
