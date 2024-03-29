import argparse
from syntax import syntax_com, ToASM
from translator import Translator
import os, time


parser = argparse.ArgumentParser(description='')
parser.add_argument("--name", type=str, required=True, help="input file")
parser.add_argument("--outfile", type=str, required=True, help="output file")
parser.add_argument("--print-lines", action='store_const', const=True, default=False, required=False, help="print all lines\n(help with debug)")
parser.add_argument("--translateToElf64Program", action='store_const', const=True, default= False, required=False, help="use nasm -f elf64 -o *.asm *.o | ld *.o -o *")
args = parser.parse_args()
name = args.name[::-1].split(".", 1)[1][::-1]

lines = open(args.name, "r").read()


Start_time = time.time()
translator = Translator()
translator.print_lines = args.print_lines

translator.lines_len = len(str(len(lines)))
undefined_c = 0

ToASM(lines, translator)

#add defines
translator.write_to_coms(f"""
%define __version__ "0.1.3", 0
%define __file__    "{name}", 0
%define true 1
%define false 0
%define NULL 0
%macro pushaq 0
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
%endmacro

%macro popaq 0
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

%macro __funcpushaq 0
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
%endmacro

%macro __funcpopaq 0
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
%endmacro

section .data
    __used_for_nums dq 0
""")


open(args.outfile, "w").write(translator.translate())
print(f"Translate time: {round(time.time() - Start_time, 9)} seconds")

if args.translateToElf64Program:
    #auto compiling asm code with nasm and ld
    os.system(f"nasm -f elf64 -o {name}.o {args.outfile}")
    os.system(f"ld {name}.o -o {name}")