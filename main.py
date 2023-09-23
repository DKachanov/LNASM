import argparse
from syntax import syntax, syntax_nothing, syntax_com, syntax_not_defined_string, rep_spec_chars
from translator import Translator
import os, time


parser = argparse.ArgumentParser(description='')
parser.add_argument("--name", type=str, required=True, help="input file")
parser.add_argument("--outfile", type=str, required=True, help="output file")
parser.add_argument("--translateToElf64Program", required=False, help="use nasm -f elf64 -o *.asm *.o | ld *.o -o *")
args = parser.parse_args()

name = args.name[::-1].split(".", 1)[1][::-1]

lines = open(args.name, "r").readlines()

Start_time = time.time()
translator = Translator()

c = 0

str_num_lines_len = len(str(len(lines)))
undefined_c = 0

for line in lines:
    c += 1 #line counter
    
    line = line.replace("\n", "").replace("\t", "")

    if syntax_com.search(line):
        #removing coms
        line = syntax_com.split(line)[0]

    if syntax_nothing.fullmatch(line) or line == "":
        #if line is fullmatches(r"[ \t]*") -> skipping line
        continue

    print(f"[{c}]: {' '*(str_num_lines_len - len(str(c)))}{line}")

    if syntax_not_defined_string.search(line):
        for i in syntax_not_defined_string.finditer(line):
            g = i.group()
            res = g
            replaced = False

            rep = f"__undefined_string.n{undefined_c}"


            g = rep_spec_chars(g)

            for l in translator.data.split("\n"):
                if "__undefined_string" == l[:18]:
                    if f" db {g.replace('undefined', '')}, 0" == l.split(":")[1]:
                        line = line.replace(res, l.split(":")[0])
                        replaced = True

            if not replaced:
                line = line.replace(res, rep)

                translator.write_to_data(f"; {c} undefined string\n__undefined_string.n{undefined_c}: db {g.replace('undefined', '')}, 0")


            undefined_c += 1


    not_matched = True
    
    for s in syntax.keys():
        if s.fullmatch(line):
            syntax[s](line, translator, c)
            not_matched = False
            
            break
    
    if not_matched:
        #if line does not fullmatch any syntax pattern
        #it shows error
        print(f"Syntax error in line {c}: {line}")
        exit(0)

#add defines
translator.write_to_coms(f"""
%define __version__ "0.1.2", 0
%define __file__    "{name}", 0
%define true 1
%define false 1
%define NULL 0
""")


open(args.outfile, "w").write(translator.translate())


print(f"Translate time: {round(time.time() - Start_time, 9)} seconds")

if args.translateToElf64Program:
    #auto compiling asm code with nasm and ld
    os.system(f"nasm -f elf64 -o {name}.o {args.outfile}")
    os.system(f"ld {name}.o -o {name}")