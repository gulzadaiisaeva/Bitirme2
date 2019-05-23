import os
from featurework.core import MAIL, MAILBigram, MAILTrigram, OpCode, OpCodeBigram, OpCodeTrigram, ByteCode, \
    ByteCodeBigram, ByteCodeTrigram, Disassembler, Strings, Binary2image, PEHeader
from featurework.feature import peInfo, graph, hash, exifInfo, anomalies, winApiFrequency, winImportFunctionFrequency, \
    histogramCalculater
from featurework.lib import fileutil, output

import csv
import json
from pymongo import MongoClient
import CommonConstants


# import PEID,cuckoo


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def core_process(process_function, output_ext, delimeter=',', dataset='dataset', extensionList=['.exe', '.dll'],
                 feature_type="text"):
    """
    Get a dataset collect all information and  write them into file.

    Attention ! Assume that filename is file hash value or unique value for the file

    :param data_name: Dataset name
    :type data_name:str
    :param extensionList: File extension list
    :type extensionList: list
    :return : void
    """
    if os.path.isfile(dataset):
        pass
    elif os.path.isdir(dataset):
        listOfFile = fileutil.getFilePaths(dataset, extensionList)

        # Collect information from source file
        for index, filename in enumerate(listOfFile):

            # Get content
            content = process_function(filename, delimeter=delimeter)
            if content is not None:
                try:
                    if feature_type == "seq":
                        output.writeFeatureAsSequence(filename, output_ext, content)
                    else:
                        output.writeIntoFile(filename, output_ext, content)
                except IOError as ioe:
                    print(str(ioe))
                    pause()
            print(str(index) + "  -  " + str(len(listOfFile)))
    else:
        print('File type must be file or directory.')


def feature_extraction(process_function, outputfilename, delimeter=',', dataset='dataset',
                       extensionList=['.exe', '.dll']):
    """
    Get a dataset collect all information and  write them into file.

    Attention ! Assume that filename is file hash value or unique value for the file
    :param process_function: the function pointer which will be executed to extract feature. Key point here is that its return type is dictionary
    :type process_function:func*
    :param outputfilename: name of documentary which the result of csv file will be put
    :type outputfilename: str
    :param dataset: Dataset name
    :type dataset:str
    :param extensionList: File extension list whose is on processing
    :type extensionList: list

    :return : void
    """

    if os.path.isfile(dataset):
        pass
    elif os.path.isdir(dataset):
        listOfFile = fileutil.getFilePaths(dataset, extensionList)

        # Collect information from source file
        content_list = []
        content_lsm = {}

        for index, filename in enumerate(listOfFile):
            # Assume that filename is file hash value
            hash_id = os.path.basename(filename).split('.')[0]
            class_id = os.path.dirname(filename)
            # Get content
            # filename = os.getcwd()+os.sep+filename

            content = process_function(filename, delimeter=delimeter)

            if content is not None:
                content['hash'] = hash_id
                content['class_id'] = class_id
                content_list.append(content)
                # content_lsm[class_id]=content
            print(outputfilename + "-" + str(index) + "  -  " + str(len(listOfFile)))

            # Write informations into csv file
            outfile = os.path.dirname(filename) + os.sep + 'csv' + os.sep + outputfilename
            if not (outfile in content_lsm.keys()):
                content_lsm[outfile] = []
            content_lsm[outfile].append(content)

        try:
            alloutfile = dataset + os.sep + outputfilename + os.sep + "allinone.csv"
            output.writeSingleIntoCSVFile(alloutfile, content_list, delimeter)
            for of in content_lsm.keys():
                output.writeSingleIntoCSVFile(of, content_lsm[of], delimeter)
        except IOError as ioe:
            print(str(ioe))
            pause()

    else:
        print('File type must be file or directory.')


def pause():
    wait = input("PRESS ENTER TO CONTINUE.")


def read_csv(file, database):
    csv_rows = []
    with open(file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
        save_json(csv_rows, database)


# Convert csv data into json and write it
def save_json(data, database):
    with open('parsed.json', "w") as f:
        f.write(json.dumps(data))
    with open('parsed.json', 'r') as f:
        json_object = json.load(f)
    for jsonres in json_object:
        isExist = database.find_one({'hash': jsonres.get('hash')})
        if isExist == None:
            database.insert(jsonres)
        else:
            print(bcolors.FAIL + " Is already exist in database " + bcolors.OKBLUE)


def save_feature():
    read_csv("../exetemp/csv/anomalies.csv", CommonConstants.anomalies_collection)
    read_csv("../exetemp/csv/hash.csv", CommonConstants.hash_collection)
    read_csv("../exetemp/csv/pe_info.csv", CommonConstants.peinfo_collection)


def run_main():
    datasets = [
        # "dataset"

        CommonConstants.dir_name,

    ]

    for dataset in datasets:
        extensionList = [".exe", ".dll"]
        # Core feature extraction
        # core_process(Disassembler.getDisassembledCode,  'diasm',            delimeter='\n',extensionList=extensionList, dataset=dataset)  # Get disaasembled code
        # print(bcolors.WARNING + "\nGetting Assembly code" + bcolors.OKBLUE)
        # core_process(Disassembler.getAssemblyCode,      'asm',extensionList=extensionList,dataset=dataset              )  # Get assembly code sequence

        print(bcolors.WARNING + "\nGetting Opcode " + bcolors.OKBLUE)
        core_process(OpCode.getOpcode, 'opcode', extensionList=extensionList, dataset=dataset)  # Get opcode sequence
        # core_process(MAIL.getMAILCodeSequence,          'mail',             extensionList=['.exe'],dataset=dataset)  # Get MAIL Code Sequence
        # core_process(Strings.getStrings,                'strings',          delimeter='\n',extensionList=extensionList,dataset=dataset)  # Get Strings

        # print(bcolors.WARNING + "\nGetting Byte code" + bcolors.OKBLUE)
        # core_process(ByteCode.getByteCodeSequence,      'bytecode',         delimeter='',extensionList=extensionList,dataset=dataset) # Get hexcode sequence
        # core_process(Binary2image.createGreyScaleImage, 'greyscale',extensionList=extensionList,dataset=dataset        )

        # print(bcolors.WARNING + "\nGetting RGB Image" + bcolors.OKBLUE)
        # core_process(Binary2image.createRGBImage,       'rgb',extensionList=extensionList,dataset=dataset              )

        # print(bcolors.WARNING + "\nGetting Opcode Bigram" + bcolors.OKBLUE)
        # core_process(OpCodeBigram.getOpCodeBigram,      'opcodebigram',     extensionList=['.opcode'],dataset=dataset)

        # print(bcolors.WARNING + "\nGetting Opcode Tigram" + bcolors.OKBLUE)
        # core_process(OpCodeTrigram.getOpCodeTrigram,    'opcodetrigram',    extensionList=['.opcode'],dataset=dataset)

        # print(bcolors.WARNING + "\nGetting ByteCode Bigram" + bcolors.OKBLUE)
        # core_process(ByteCodeBigram.getByteCodeBigram,  'bytecodebigram',   extensionList=['.bytecode'],dataset=dataset)

        # print(bcolors.WARNING + "\nGetting ByteCode Tigram" + bcolors.OKBLUE)
        # core_process(ByteCodeTrigram.getByteCodeTrigram,'bytecodetrigram',  extensionList=['.bytecode'],dataset=dataset)
        # core_process(MAILBigram.getMAILBigram,          'mailbigram',       extensionList=['.mail'],dataset=dataset)
        # core_process(MAILTrigram.getMAILTrigram,        'mailtrigram',      extensionList=['.mail'],dataset=dataset)
        # core_process(PEHeader.getPeHeaderInformation,   'peheader',extensionList=extensionList,dataset=dataset)

        # print(bcolors.WARNING + "\nFeature extraction! Getting Hash Values" + bcolors.OKBLUE)
        # feature_extraction(hash.getHashValues,                          'hash',extensionList=extensionList,dataset=dataset)

        # feature_extraction(exifInfo.getExifInfo,                        'exif_info',extensionList=extensionList,dataset=dataset)
        # print(bcolors.WARNING + "\nFeature extraction! Getting Information from PE Header" + bcolors.OKBLUE)
        # feature_extraction(peInfo.getInformationFromPEHeader,           'pe_info',extensionList=extensionList,dataset=dataset)
        # feature_extraction(graph.getDirectedGraph,                      'directed_graph',extensionList=extensionList,dataset=dataset)
        # feature_extraction(graph.getUndirectedGraph,                    'undirected_graph',extensionList=extensionList,dataset=dataset)
        # print(bcolors.WARNING + "\nFeature extraction! Getting Anomalies" + bcolors.OKBLUE)
        # feature_extraction(anomalies.getAnomalies,                      'anomalies',extensionList=extensionList,dataset=dataset)

        # feature_extraction(winImportFunctionFrequency.getImportTable,   'winimportfunction_frequency',extensionList=extensionList,dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'opcode_histogram',             extensionList=['.opcode'],dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'opcode_bigram_histogram',      extensionList=['.opcodebigram'],dataset=dataset)

        # feature_extraction(histogramCalculater.getHistogram,            'opcode_trigram_histogram',     extensionList=['.opcodetrigram'],dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'bytecode_histogram',           extensionList=['.bytecode'],dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'bytecode_bigram_histogram',    extensionList=['.bytecodebigram'],dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'opcode_trigram_histogram',     extensionList=['.bytecodetrigram'],dataset=dataset)
        # feature_extraction(histogramCalculater.getHistogram,            'mail_bigram_histogram',        extensionList=['.mailbigram'],dataset=dataset)
        # feature_ext

        # feature_extraction(histogramCalculater.getHistogram,            'mail_histogram',               extensionList=['.mail'],dataset=dataset)

    # save_feature()
