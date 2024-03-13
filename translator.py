import sys, os
from errors import fileNotFound, nameError
from syntax import var_search, func_search

class Translator:

    def __init__(self) -> None:
        self.data = "section .data\n\n"
        self.text = "section .text\n\n"
        self.bss = "section .bss\n\n"
        self.coms = ""
        self._append = ""
        self.path = ""
        self.f_requires = []
        self.f_heads = []
        self.c = 0
        self.lines_len = 0
        self.notdef_c = 0
        self.vars = []
        self.set_bits = 0
        self.c = 0
        self.cc = 0
        self.print_lines = False

    def write_to_data(self, string):
        #writes string to data section
        self.data += string + "\n"
    def write_to_text(self, string):
        #writes string to text section
        self.text += string + "\n"
    def write_to_bss(self, string):
        #writes string to bss section
        self.bss += string + "\n"
    def write_to_coms(self, string):
        self.coms += "; " + string + "\n"
    def append(self, file):
        if os.path.isfile(file):
            data = open(file).read()
        elif os.path.isfile(os.path.join(sys.path[0], file)):
            data = open(os.path.join(sys.path[0], file)).read()
        else:
            fileNotFound(self.c, f"[ERROR]: No such file as \"{file}\"")
        #appending file data to main file with open(file).read()
        self._append += "; Appended " + file + ":\n" + data + "\n\n"
    def translate(self):
        #packing all strings together in 1
        if self.bss == "section .bss\n\n":
            return self.coms + "\n\n\n" + self.text + "\n\n\n" + self.data + "\n\n\n" + self._append
        return self.coms + "\n\n\n" + self.text + "\n\n\n" + self.data + "\n\n\n" + self.bss + "\n\n\n" + self._append

    def check_name(self, name):
        if name in self.vars or var_search(name).search(self.data) or func_search(name).search(self.text):
            nameError(self.c, f"name \"{name}\" is already used in this file\n")
        elif var_search(name).search(self._append):
            nameError(self.c, f"{name} is already used in one of appended files\n")

    def check_all_names(self):
        for x in self.vars:
            if var_search(x).search(self._append) or func_search(x).search(self.text):
                nameError("", f"Search for {x}, it's already used in this appended file")