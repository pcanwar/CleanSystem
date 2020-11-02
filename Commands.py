import re
import os
import hashlib
import shutil


class Commands:
    def __init__(self):
        self.commandsSwitch = {"quit": None, "language": self.language, "remove": self.remove, "hash": self.hash,
                               "help": self.printHelp, "clean": self.clean}

    def doWork(self, comandName, args):
        """Read commands to switch amongs commands on the app"""

        f = self.commandsSwitch[comandName]
        if not comandName in ['help', 'clean', 'lang'] and len(args) == 0:
            print(f"{comandName} must have one argument")
            return
        f(args)

    def printHelp(self, args):
        print("""
        
    help -              Print this help information
    quit -              Quit this system
    clean -             Cleaning  Files
    language -              Remove Language Files
    remove {dmg} -      Remove file time 
    
    """)

    def hash(self, args):
        hashOb = hashlib.sha512()
        self.name = ''.join(args)
        hashOb.update(self.name.encode('utf-8'))

        print(f"The hash is: {hashOb.hexdigest()}")

    def language(self, args):

        dir_size = 0
        for root, dirs, files in os.walk("/Users/pcanw"):
            for dir in dirs:
                if '.lproj' in dir:
                    if 'en.lproj' not in dir and \
                            'Base.lproj' not in dir and \
                            'en_US.lproj' not in dir and \
                            'English.lproj' not in dir and \
                            'us.lproj' not in dir and \
                            'ar.lproj' not in dir:
                        dir_size += os.path.getsize(os.path.join(root, dir))
                        shutil.rmtree(os.path.join(root, dir))
                        # print(os.path.join(root, dir))
        print(dir_size)


    def remove(self, args):
        """remove any files .dmg
        TODO: allow some types of files
        :param args: file type
        :return: size of the files
        """


        file_size = 0
        for root, dirs, files in os.walk("~"):
            for file in files:
                if file.endswith(f".{''.join(map(str, args))}"):
                    dmg_file = os.path.join(root, file)
                    file_size += os.path.getsize(dmg_file)
                    os.remove(dmg_file)
        print(f"removed : {file_size}")

    def clean(self, args):
        """
        IN:
        To find log files
        System Log Folder: /var/log
        System Log: /var/log/system.log
        Mac Analytics Data: /var/log/DiagnosticMessages
        System Application Logs: /Library/Logs
        System Reports: /Library/Logs/DiagnosticReports
        User Application Logs: ~/Library/Logs
        User Reports: ~/Library/Logs/DiagnosticReports

        :param args: no needed it
        :return:
        """

        datadir = ["/var/log",
                   "~/Library/Caches",
                   "~/Library/Logs",
                   "~/Library/Developer/Xcode/DerivedData",
                   "~/Library/Developer/Xcode/iOS Device Logs",

                   ]
        for dir in datadir:
            dir_list = os.listdir(dir)
            for d in dir_list:
                dir_path = dir + "/" + d
                if os.path.isfile(dir_path):
                    os.remove(dir_path)
                elif os.path.isdir(dir_path):
                    shutil.rmtree(dir_path, ignore_errors=True)

    def process(self, command):
        command = command.strip()
        arr = re.split(r'\s+', command, 1)
        commandName = arr[0]
        if not commandName in self.commandsSwitch.keys():
            print(f"{commandName} is not a valid command, try again")
            return True
        if commandName == "quit":
            return False
        else:
            self.doWork(commandName, arr[1:])
            return True
