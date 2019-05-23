import easygui
from os import walk
import hashlib
import shutil
import CommonConstants
import testing
import extract_opcode

class SignatureBased:
    def __init__(self, folderpath):
        self.arguments = False
        self.autocompress = False
        self.folderpath = folderpath

    def virus_detected(self, viruspath, sha1):
        print("\n\nVirus detected...\n\n")
        if self.autocompress is False:
            flavor = easygui.buttonbox(
                "A virus has been detected: \n" + viruspath + "\nWith md5: " + sha1 + "\nDo you want to move the virus to quarantine?",
                choices=['Yes', 'No'])
        else:
            flavor = "Yes"

        if flavor is "Yes":
            try:
                shutil.move(self.folderpath + '/' + viruspath, "../quarantine")
                print('moving file')
                if self.autocompress is False:
                    easygui.msgbox("Virus was moved to quarantine.")
            except Exception as err:
                easygui.msgbox("Error:\n" + str(err))
            print(viruspath)

    def check_file(self, filepath):
        print("\n\nStarting scan of file: "+filepath)

        with open(self.folderpath+"/"+filepath, 'rb') as file_to_check:
            data = file_to_check.read()
            md5_returned = hashlib.md5(data).hexdigest()
        print(md5_returned)

        print("\nsearch database")
        is_exist = CommonConstants.virus_collection.find_one({'md5': md5_returned})
        if is_exist is not None:
            print("\nFounded in database")
            self.virus_detected(filepath.replace("\n", ""), md5_returned)
        else:
            print("\nNot in database")
            file_opcode_path = self.folderpath+"/opcode/"+filepath[0:len(filepath)-3] + "opcode"
            testing_project = testing.Testing(file_opcode_path)
            flag = testing_project.testing_run()
            if flag is True:
                self.virus_detected(filepath.replace("\n", ""), md5_returned)
                jsonFile = {
                    "md5": md5_returned
                }
                CommonConstants.virus_collection.insert(jsonFile)
                print("Status:", "   Data successfully stored in MongoDB!! md5 : ", str(jsonFile['md5']))

            else:
                flavor2 = easygui.buttonbox(
                    "A file " + filepath + " is not virus!\n",
                    choices=['OK'])

    def check_folder(self):
        print("\nStarting scan of folder: " + self.folderpath)

        files = []
        for (dirpath, dirnames, filenames) in walk(self.folderpath):
            files.extend(filenames)
            break
        print(files)
        extract_opcode.run_main()
        i = 0
        while i < len(files):
            try:
                self.check_file(files[i])
            except Exception as err:
                print(err)
            i += 1
        print("Finished with following results:")
