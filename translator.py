import sys, os

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
            print(f"[ERROR]: No such file as \"{file}\"")
            exit(1)
        #appending file data to main file with open(file).read()
        self._append += "; Appended " + file + ":\n" + data + "\n\n"
    def translate(self):
        #packing all strings together in 1
        if self.bss == "section .bss\n\n":
            return self.coms + "\n\n\n" + self.text + "\n\n\n" + self.data + "\n\n\n" + self._append
        return self.coms + "\n\n\n" + self.text + "\n\n\n" + self.data + "\n\n\n" + self.bss + "\n\n\n" + self._append