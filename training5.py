
from os import walk
import CommonConstants
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
        self.uop = []
        self.matrix = []
        self.threshold = 0.75

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
            for j in range(0,(len(self.uop_array[i]))-1):
                for k in range(j+1, len(self.uop_array[i])):
                    try:
                        first_index = self.uop.index(self.uop_array[i][j])
                        second_index = self.uop.index(self.uop_array[i][k])
                    except ValueError:
                        print("Errrror ****************************")
                    self.matrix[second_index][first_index] += 1
                    #self.matrix[first_index][second_index] += 1

        maximum = max(self.matrix)
        self.normalization(len(self.uop))
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

    def write_matrix_to_file(self):
        print("***** write_matrix_to_file *****")
        for row in self.matrix:
            for col in row:
                with open("../matrix.txt", "a") as myfile:
                    myfile.write(str(col))
                    myfile.write("    ")
            with open("../matrix.txt", "a") as myfile:
                myfile.write("\n\n")

    def write_matrix_to_csv(self, filename):
        print("***** write_csv *****")
        with open(filename, 'w') as csvFile:
            writer = csv.writer(csvFile)
            temprow = []
            temprow.append('')
            for inst in self.uop:
                temprow.append(inst)
            writer.writerow(temprow)

            i = 0
            for row in self.matrix:
                temprow = []
                temprow.append(self.uop[i])
                for col in row:
                    temprow.append(col)
                writer.writerow(temprow)
                i += 1
        csvFile.close()

    def write_uniqs_to_file(self, arr):
        print("***** write_uniqs_to_file *****")
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

    def empty_matrix(self):
        print("***** empty_matrix *****")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = 0

    def oper_data_set(self):
        print("***** oper_data_set *****")
        j = 0
        for i in range(0, 1500, 300):
            filename = "../dataset/matrix_csv/matrix" + str(j) + ".csv"
            self.fill_matrix(i, i + 300)
            self.write_matrix_to_csv(filename)
            self.empty_matrix()
            j += 1

if os.path.exists("../uniqueopcodes.txt"):
    os.remove("../uniqueopcodes.txt")
if os.path.exists("../setofuniqueopcodes.txt"):
    os.remove("../setofuniqueopcodes.txt")

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
project.write_uniqs_to_file(project.uop_array)
project.create_matrix(len(project.uop))
project.oper_data_set()

