import easygui
from os import walk
import hashlib
import shutil
import CommonConstants


arguments = False
autocompress = False

def virusdetected(viruspath, sha1):
    print("\n\nVirus detected...\n\n")
    if (autocompress == False):
        flavor = easygui.buttonbox(
            "A virus has been detected: \n" + viruspath + "\nWith md5: " + sha1 + "\nDo you want to move the virus to quarantine?",
            choices=['Yes', 'No'])
    else:
        flavor = "Yes"
    if (flavor == "Yes"):
        try:
            shutil.move("../exetemp/" + viruspath, "../quarantine")
            print('moving file')
            if (autocompress == False):
                easygui.msgbox("Virus was moved to quarantine.")
        except Exception as err:
            easygui.msgbox("Error:\n" + str(err))
        print(viruspath)


def Checkfile(folderpath, filepath):
    print("\n\nStarting scan of file: " + filepath)
    with open(folderpath + "/" + filepath, 'rb') as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()
    print(md5_returned)

    print("\nsearch database")

    isExist = CommonConstants.response_collection.find_one({'md5': md5_returned})

    if (isExist != None):
        virusdetected(filepath.replace("\n", ""), md5_returned)

def Checkfolder(folderpath):
    print("\nStarting scan of folder: " + folderpath)

    files = []
    for (dirpath, dirnames, filenames) in walk(folderpath):
        files.extend(filenames)
        break
    print(files)

    i = 0
    while i < len(files):
        try:
            Checkfile(folderpath, files[i])
        except Exception as err:
            print(err)
        i += 1
    print("Finished with following results:")


Checkfolder(CommonConstants.dir_name)
