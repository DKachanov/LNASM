import re, struct
from errors import *
import os, sys

types = {
    "float" : "dd",
    "double" : "dq",
    "extended" : "dt",

    "dword" : "dd",
    "qword" : "dq",
    "tword" : "dt",
    "word" : "dw",
    "byte" : "db"
}

rax_size = {
    "byte" : "al",
    "word" : "ax",
    "dword" : "eax",
    "qword" : "rax",
    "float" : "rax",
}

conditions = {
    "==" : "je",
    "!=" : "jne",
    ">=" : "jge",
    "<=" : "jle",
    ">"  : "jg",
    "<"  : "jl",
}

fconditions = {
    "==" : "je",
    "!=" : "jne",
    ">=" : "jbe",
    "<=" : "jae",
    ">"  : "jb",
    "<"  : "ja",
}

type_num = {
    "db" : 0,
    "dw" : 1,
    "dd" : 2,
    "dq" : 3
}

spec_char_to_num = {
    "\\t" : 9,
    "\\n" : 10
}

data_size = {
    "float" : 8,

    "tword" : 10,
    "qword" : 8,
    "dword" : 4,
    "word"  : 2,
    "byte"  : 1
}

rdata_size = {
    10 : "tword",
    8 : "qword",
    4 : "dword",
    2 : "word",
    1 : "byte"
}

#skips lines with no data
syntax_nothing = re.compile(r"[ \t]+")
syntax_split = re.compile(r";(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)(?![^{]*\})")
var_search = lambda name: re.compile(rf"[ \t]*({name}(:){0,1}[ \t]+(db|dw|dd|dq)[ \t]+.*)")
func_search = lambda name: re.compile(rf"[ \t]*{name}:.*")

#coms
syntax_com = re.compile(r"/\*(.+?)(?=(\*/))\*/(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
syntax_comma = re.compile(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")

#not defined strings
syntax_not_defined_string = re.compile(r'''("[^"]){0}notdef[ \t]+"[^"]*"''')
syntax_not_defined_array  = re.compile(r"(\[[^\]]){0}notdef[ \t]+\[[^\]]*\]")
numbyte = re.compile(r'\\+x[0-9abcdef]{2}')
spec_char = re.compile(r'\\+[n|t]')

#data
syntax_int_data         = re.compile(r"[ \t]*(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+.+")
syntax_int_data_no_args = re.compile(r"[ \t]*(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*(,[ \t]+[a-z|A-Z|_][\w|\.]*)*[ \t]*")
syntax_res_int_data     = re.compile(r"[ \t]*RES[ \t]+(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*\[.+\][ \t]*")
syntax_float            = re.compile(r"[ \t]*(float|double|extended)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+.+[ \t]*")
syntax_list             = re.compile(
    r"[ \t]*list[ \t]+(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+\[(.*\,[ ]*)*.*\][ \t]*")
syntax_string           = re.compile(r"[ \t]*string[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+\".*\"[ \t]*")
syntax_const            = re.compile(r"[ \t]*const[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+= .+")

#instructions
syntax_push       = re.compile(r"[ \t]*push .+")
syntax_pop        = re.compile(r"[ \t]*pop .+")
syntax_pushpop_aq = re.compile(r"[ \t]*(pushaq|popaq)[ \t]*") 
syntax_ret        = re.compile(r"[ \t]*ret[ \t]+.+")
syntax_jmp        = re.compile(r"[ \t]*jmp .+")
syntax_call       = re.compile(r"[ \t]*call[ \t]+[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_int        = re.compile(r"[ \t]*int .+")
syntax_logic      = re.compile(r"[ \t]*(and|or|xor|test|not) .*, .*")
syntax_mov        = re.compile(r".* -> .*")
syntax_inc        = re.compile(r"[ \t]*.+\+\+[ \t]*")
syntax_dec        = re.compile(r"[ \t]*.+\-\-[ \t]*")
syntax_syscall    = re.compile(r"[ \t]*syscall( .+){0,1}[\t ]*")

#macros
syntax_func                = re.compile(r"[ \t]*(void[ \t]+){0,1}function[ \t]+[a-z|A-Z|_][\.\w]*\((.*\,[ ]*)*.*\)[ \t]+(nosave[ \t]+){0,1}[ \t]*")
syntax_global              = re.compile(r"[ \t]*#global [a-z|A-Z|_][\.\w]*.*")
syntax_append              = re.compile(r"[ \t]*#append .*")
syntax_syntax              = re.compile(r"[ \t]*#syntax .*")
syntax_if                  = re.compile(r"[ \t]*if[ \t]*\(.+[ \t]+(==|!=|>|<|>=|<=)[ \t]+.+\)[ \t]+")
syntax_call_with_args      = re.compile(r"[ \t]*[a-z|A-Z|_][\w|\.]*\(.*\)[ \t]*")
syntax_call_with_args_rets = re.compile(r"[ \t]*.*[ \t]+=[ \t]+[a-z|A-Z|_][\w|\.]*\(.*\)[ \t]*")
syntax_asm                 = re.compile(r"[ \t]*#asm[ \t]+\.(text|data|bss) \{[^\}]+\}[ \t]*")
syntax_point               = re.compile(r"[ \t]*::\.*[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_extern              = re.compile(r"[ \t]*#extern[ \t]+[a-z|A-Z|_][\.\w]*.*")
syntax_def                 = re.compile(r"[ \t]*#define[ \t]+[a-z|A-Z|_][\.\w]*[ \t]+.*")
syntax_undef               = re.compile(r"[ \t]*#undefine[ \t]+[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_from                = re.compile(r"[ \t]*#from[ \t]+\"[^\"]+\"[ \t]+append[ \t]+\"[^\"]+\"[ \t]*")
syntax_head                = re.compile(r'[ \t]*#head[ \t]+.+[ \t]*')
syntax_while               = re.compile(r'[ \t]*while(.*)')
syntax_return              = re.compile(r'[ \t]*return[ \t]*')
syntax_bits                = re.compile(r'[ \t]*#BITS[ \t]+(16|32|64)[ \t]*')

#imath
syntax_add_instr  = re.compile(r"[ \t]add[ \t]+.*,.*")
syntax_sub_instr  = re.compile(r"[ \t]sub[ \t]+.*,.*")
syntax_add        = re.compile(r"[ \t]*.*\+=.*")
syntax_sub        = re.compile(r"[ \t]*.*-=.*")
syntax_macro_div  = re.compile(r"[ \t]*.*/=.*")
syntax_macro_idiv = re.compile(r"[ \t]*.*//=.*")
syntax_macro_rem  = re.compile(r"[ \t]*.*%=.*")
syntax_macro_mul  = re.compile(r"[ \t]*.*\*=.*")
syntax_div        = re.compile(r"[ \t]*div .*")
syntax_mul        = re.compile(r"[ \t]*mul .*")

syntax_shift     = re.compile(r"[ \t]*.* (<<|>>) .*")

#fmath
syntax_fadd         = re.compile(r"[ \t]*fadd .*, .*, .*")
syntax_fsub         = re.compile(r"[ \t]*fsub .*, .*, .*")
syntax_fdiv         = re.compile(r"[ \t]*fdiv .*, .*, .*")
syntax_fmul         = re.compile(r"[ \t]*fmul .*, .*, .*")
syntax_float_to_int = re.compile(r"[ \t]*fti .*, .*")
syntax_int_to_float = re.compile(r"[ \t]*itf .*, .*")
syntax_int_conv     = re.compile(r"[ \t]*int .*")
syntax_float_conv   = re.compile(r"[ \t]*float .*")
syntax_convto       = re.compile(r"[ \t]*convto[ \t]+(float|double|int)[ \t]+.+")

reg_list = ['rax', 'rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9']
#if
_else  = re.compile(r"\belse\b")
_float = re.compile(r"\bfloat\b")
_cond  = re.compile(r"(.+)")
_comb  = re.compile(r"(==|!=|>=|<=|>|<)")
_regs  = re.compile(r"[^[]*\b(rbp|ebp|bp|es|fs|gs|ss|rax|eax|rbx|ebx|rcx|ecx|rdx|edx|rsp|esp|sp|rsi|esi|si|rdi|edi|di|(a|b|c|d)(x|h|l))\b[^]]*")
#imath
ops = re.compile(r"(\+=|-=|\*=|/=|//=|%=)")
dsize = re.compile(r"(byte|word|dword|qword)")
_float_num = re.compile(r"\b[0-9]+\.[0-9]+\b")
_int_num   = re.compile(r"\b([0-9abcdefABCDEF]+h|0x[0-9abcdefABCDEF]+|[0-9]+)\b")
_q = re.compile(r"[^[]*\b(r[abcd]x|r(si|di|sp|bp)|r(8|9|10|11|12|13|14|15))\b[^]]*")
_d = re.compile(r"[^[]*\b(e[abcd]x|e(si|di|sp|bp))\b[^]]*")
#float
_float_types = re.compile(r"\b(float|double|extended)\b")
#data func
def _syntax_int_data(string, translator, c):
    """
        *type* *name* = *number*

        makes a number variable

        type: byte, word, dword, qword
    """
    translator.write_to_data(f"; [{c}]: {string}")

    var, value = string.split("=")
    type, var = var.split()[:2]

    translator.check_name("".join(var.split()))
    translator.vars.append("".join(var.split()))

    translator.write_to_data(f"{var} {types[type]} {value}")

def _syntax_int_data_no_args(string, translator, c):
    """
        *type* *name*

        makes a variable

        type: byte, word, dword, qword
    """
    translator.write_to_data(f"; [{c}]: {string}")

    find = re.compile(r"(byte|word|dword|qword)")
    type = find.search(string).group().split()[0]
    vars = string.split(type)[1].split(",")
    for var in vars:
        translator.check_name("".join(var.split()))
        translator.vars.append("".join(var.split()))

        translator.write_to_data(f"{var} {types[type]} 0")


def _syntax_res_int_data(string, translator, c):
    """
        RES type name[value]
    
        writes variable in .data section with times

        type: size of each block (byte, word, dword, qword)
        name: name of the variable
        value: amount of blocks
    """
    translator.write_to_data(f"; [{c}]: {string}")

    type, name_value = string.split()[1:]
    name, value = name_value.split("[")
    value = value[:len(value)-1]

    translator.check_name("".join(name.split()))
    translator.vars.append("".join(name.split()))
    
    translator.write_to_data(f"{name}: TIMES {value} d{types[type][1]} 0")


def _syntax_string(string, translator, c):
    """
        string *name* = "*text*"

        makes a string
    """
    translator.write_to_data(f"; [{c}]: {string}")

    var, value = string.split("=", 1)
    value = "\"" + value.split("\"", 2)[1] + "\", 0"
    var = var.replace("string", "")
    
    value = rep_spec_chars(value)

    translator.check_name("".join(var.split()))
    translator.vars.append("".join(var.split()))

    translator.write_to_data(f"{var} db {value}")
    translator.write_to_data(f"{''.join(var.split())}.len equ $ - {var}")

def _syntax_const(string, translator, c):
    """
        const *name* = *any*

        makes a const (equ)
    """
    translator.write_to_data(f"; [{c}]: {string}")

    var, value = string.split("=", 1)
    var = var.replace("const ", "")

    translator.vars.append("".join(var.split()))
    translator.check_name("".join(var.split()))

    translator.write_to_data(f"{var} equ {value}")

def _syntax_float(string, translator, c):
    """ 
        float/double/extended *name* = *value*
        
        makes float/double/extended variable
    
    """
    translator.write_to_data(f"; [{c}]: {string}")

    tn, value = string.split("=", 1)
    type, name = _float_types.search(tn).group(), re.compile(r"\b(float|double|extended)\b").sub("", tn)
    type = "".join(type.split())
    
    translator.check_name("".join(name.split()))
    translator.vars.append("".join(name.split()))

    if not if_float(value):
        valueError(c, f"{value} is not a float number")
    translator.write_to_data(f"{name} {types[type]} {value}")

def _syntax_double(string, translator, c):
    """ 
        double *name* = *value*
        
        makes double (dq) variable
    
    """
    translator.write_to_data(f"; [{c}]: {string}")

    name = string.split("double")[1].split()[0]
    value = string.split("=")[1]
    
    translator.check_name("".join(name.split()))
    translator.vars.append("".join(name.split()))
    
    if not if_float(value):
        valueError(c, f"{value} is not a float number")
    translator.write_to_data(f"{name} dq {value}")

def _syntax_extended(string, translator, c):
    """ 
        extended *name* = *value*
        
        makes extended (dt) variable
    
    """
    translator.write_to_data(f"; [{c}]: {string}")

    name = string.split("extended")[1].split()[0]
    value = string.split("=")[1]
    
    translator.check_name("".join(name.split()))
    translator.vars.append("".join(name.split()))

    if not if_float(value):
        valueError(c, f"{value} is not a float number")
    translator.write_to_data(f"{name} dt {value}")

def _syntax_list(string, translator, c):
    """
        list *type* *name* = [...,]

        example: list byte = [31h, 32h, 33h, 34h,]

        makes an array of integers
        to get length: *name*.len
        to get data type: *name*.type
            types:
                byte = 0
                word = 1
                dword = 2
                qword = 3

        type: byte, word, dword, qword

    """
    translator.write_to_data(f"; [{c}]: {string}")
    
    x = string.split("list")[1]

    type, name, _, data = x.split(maxsplit=3)
    type = types[type]

    data = data[1:].split("]", 1)[0]
    data_len = len(data.split(','))

    translator.check_name("".join(name.split()))
    translator.vars.append("".join(name.split()))

    translator.write_to_data(f"{name} {type} {data}")
    translator.write_to_data(f"{name}.len dq {data_len}")
    translator.write_to_data(f"{name}.type dq {type_num[type]}")



#instructions func
def _syntax_mov(string, translator, c):
    """
        *any1* -> *any2*

        mov instruction

        raw: mov any2, any1
    """
    translator.write_to_text(f"; [{c}]: {string}")

    src, dest = string.split(" -> ")
    translator.write_to_text(f"mov {dest}, {src}")

def _syntax_incdec(string, translator, c):
    """
        *var*++
        *var*--

        inc/dec instruction

        var: any
    """
    translator.write_to_text(f"; [{c}]: {string}")

    if "++" in string:
        translator.write_to_text("inc " + string.replace("++", ""))
    else:
        translator.write_to_text("dec " + string.replace("--", ""))


def _syntax_syscall(string, translator, c):
    """
        Can be used as instruction "syscall"
        or "syscall arg(1), ..., arg(n)"
    """

    if re.compile(r"[ \t]*syscall[ \t]*").fullmatch(string):
        translator.write_to_text(string)
        return

    unpack = syntax_comma.split(string.split("syscall", 1)[1])
    if len(unpack) > len(reg_list):
        valueError(c, f"Too many values to unpack ({len(unpack)})")
    for r, u in zip(reg_list, unpack):
        translator.write_to_text(f"mov {r}, {u}")
    translator.write_to_text("syscall")


def _syntax_pushpop_aq(string, translator, c):
    """
        Push all registers
        and
        Pop all registers
    """
    if "pushaq" in string:
        translator.write_to_text("pushaq")
    else:
        translator.write_to_text("popaq")
#macros func

def _syntax_bits(string, translator, c):
    bits = int("".join(string.split("#BITS", 1)[1].split()))
    if translator.set_bits != bits and translator.set_bits:
        fileFormatError(c, f"Cannot reset file bit format to other ({translator.set_bits} to {bits})")
    
    translator.coms += string.replace("#", "")
    translator.set_bits = bits

def _syntax_call_with_args_rets(string, translator, c):
    """
    qword [a] = func(...) -> func(...) + rax -> qword [a]
    """

    translator.write_to_text(f"; [{c}]: {string}")
    place, string = string.split("=")
    func = string.split("(")[0]
    args = string.split("(", 1)[1][::-1].split(")", 1)[1][::-1].split(",")
    args.reverse()
    if not args == ['']:
        for arg in args:
            translator.write_to_text("push " + arg)
    translator.write_to_text("call " + func)

    size = place.split("[")[0].replace(" ", "").replace("\t", "")
    if not size in rax_size.keys():
        expressionWarning(c, "operation size is not specified (Setted qword operation size as defualt)")
        translator.write_to_text(f"mov {place}, rax")
    else:
        translator.write_to_text(f"mov {place}, {rax_size[size]}")


def _s_return(name):
    def f(string, translator, c):
        translator.write_to_text(f"jmp __function{name}_end")

    return f

def _syntax_func(string, translator, c):
    """
    function func1(qword a, qword b, qword c) {
        ...;
    };
    """
    head = re.compile(r"[a-z|A-Z|_][\.\w]*\((.*\,[ ]*)*.*\)").search(string).group()
    name, args = head.split("(", 1)
    args = args.split(")", 1)[0].split(",")
    translator.write_to_text(f"{name}:")
    translator.write_to_text(f"push rbp")
    translator.write_to_text(f"mov rbp, rsp")
    void = False
    nosave = False


    if "nosave" in string.split("{", 1)[0].split(")", 1)[1]:
        nosave = True
    else:
        if "void" in string.split("function", 1)[0]:
            translator.write_to_text(f"pushaq")
            void = True
        else:
            translator.write_to_text(f"__funcpushaq")

    c = 8
    names = []
    if args != ['']:
        for arg in args:
            c += 8
            search = re.compile(r"(qword|dword|word|float)").search(arg)
            if search:
                s = search.group()
                n = arg.split(s)[1]
                names.append(n)
                translator.write_to_text(f"%define {n} {s} [rbp+{c+8-data_size[s]}]")
            else:
                if search and search.group():
                    dataSizeError(c, "Bytes cannot be pushed")
                else:
                    dataSizeError(c, "Unknown data size")
    lines = re.compile(r"\)[ \t]+(nosave[ \t]+){0,1}\{").split(string, maxsplit=1)[::-1][0][::-1].split("}", maxsplit=1)[1][::-1]
    syntax.update({syntax_return : _s_return(name)})
    ToASM(lines, translator)
    translator.write_to_text(f"__function{name}_end:")

    for n in names:
        translator.write_to_text(f"%undef {n}")
    if not nosave:
        if void:
            translator.write_to_text("popaq")
        else:
            translator.write_to_text("__funcpopaq")
    translator.write_to_text("mov rsp, rbp")
    translator.write_to_text("pop rbp")
    translator.write_to_text(f"ret 8*{len(names)}")

def _syntax_global(string, translator, c):
    """
        #global *any*

        globalizing any varibale or point
    """
    translator.write_to_coms(f"[{c}]: {string}")

    translator.write_to_text(f"global {string.split('#global ')[1]}")

def _syntax_extern(string, translator, c):
    """
        #extern *any*

        externs functionss
    """
    translator.write_to_coms(f"[{c}]: {string}")

    translator.write_to_text(f"extern{string.split('#extern')[1]}")



def _syntax_point(string, translator, c):
    """
        ::*name*
        
        makes a point
    """
    translator.write_to_text(f"; [{c}]: {string}")

    translator.write_to_text(f"{string.replace('::', '').replace(' ', '')}:")

def _syntax_append(string, translator, c):
    """
        #append *path*

        appends an asm file to main file
    """
    translator.write_to_coms(f"[{c}]: {string}")

    file = string.split(maxsplit=1)[1]
    translator.append(file)

def _syntax_syntax(string, translator, c):
    """
        #syntax *path*

        executes python file
    """
    translator.write_to_coms(f"[{c}]: {string}")
    file = string.split(maxsplit=1)[1]

    if os.path.isfile(file):
        data = open(file).read()
    elif os.path.isfile(os.path.join(sys.path[0], file)):
        data = open(os.path.join(sys.path[0], file)).read()
    else:
        fileNotFound(f"No such file as \"{string.split('#syntax ')[1]}\"")
    
    exec(data)

def _syntax_call_with_args(string, translator, c):
    """
        *func*(*arg1*, *arg2*, ...)

        calls function (func) with pushed arguments

        func: function
        args: any

        WARNING! push instruction pushes only max block size
        64-bit: qword
        32-bit: dword

        You cannot push dword [x] in 64-bit mode
    """
    
    translator.write_to_text(f"; [{c}]: {string}")
    
    func = string.split("(")[0]
    args = string.split("(", 1)[1][::-1].split(")", 1)[1][::-1].split(",")
    args.reverse()
    if not args == ['']:
        for arg in args:
            translator.write_to_text("push " + arg)
    translator.write_to_text("call " + func)

def _syntax_asm(string, translator, c):
    """
        #asm .*section* ...

        writes raw string in section

        section: text, data, bss
    """
    translator.write_to_text(f"; [{c}]: {string}")

    sec, code = string.split("#asm", 1)[1].split(maxsplit=1)
    if sec == ".text":
        call = translator.write_to_text
    elif sec == ".data":
        call = translator.write_to_data
    else:
        call = translator.write_to_bss

    for line in syntax_split.split(code.replace("{", "").replace("}", "")):
        call(line)
        translator.c += 1

def _clean_asm_text(string, translator, c):
    """
        writes raw asm string in text section
    """
    translator.write_to_text(f"; [{c}]: {string}")

    translator.write_to_text(string)




def _syntax_if(string, translator, line):
    """
        if (...) {
            ...;
        } else if (...) {
            ...;
        } else {
            ...;
        };
    """
    size = "qword" if translator.set_bits == 0 or translator.set_bits == 64 else "dword"
    translator.cc += 1
    l = 0
    blocks = []
    for x in _else.finditer(string):
        block = string[l:x.start()]
        if len(block.split("{")) != len(block.split("}")):
            continue
        l = x.span()[1]
        blocks.append(block)

    noelse = False
    if blocks == []:
        blocks.append(string)
        noelse = True
    else:
        _else_block = string[l:]

    z = 0
    for cond in blocks:
        z+=1

        '''
        AND & OR
        '''

        c = _cond.match(cond)
        if not c:
            syntaxError(line, f"Invalid format {c}")
        c = c.group()[1:len(c.group())-1]
        m = _comb.search(c)
        if m:
            c = c.split("{", 1)[0].replace("if", "").replace("(", "").replace(")", "")
            a,b = c.split(m.group())
            f = _float.search(a), _float.search(b)
            if f[0] or f[1]:
                if _regs.search(a.lower()) or _regs.search(b.lower()):
                    expressionWarning(line, f"register cannot be used as a value in float comparament (can be used as []) ({c})")


                try:
                    int(a)
                    translator.write_to_text(f"mov {size} [__used_for_nums], {a.split('float', 1)[1] if f[0] else a}")
                    translator.write_to_text(f"fld {size} [__used_for_nums]" if f[0] else f"fild {size} [__used_for_nums]")
                except:
                    translator.write_to_text(f"fld {a.split('float', 1)[1]}" if f[0] else f"fild {a}")

                try:
                    int(b)
                    translator.write_to_text(f"mov {size} [__used_for_nums], {b.split('float', 1)[1] if f[1] else b}")
                    translator.write_to_text(f"fld {size} [__used_for_nums]" if f[1] else f"fild {size} [__used_for_nums]")
                except Exception as e:
                    print(e)
                    translator.write_to_text(f"fld {b.split('float', 1)[1]}" if f[1] else f"fild {b}")


                translator.write_to_text("fcomi st0, st1")
                translator.write_to_text(f"{fconditions[m.group()]} _if_construction{z}_{translator.cc}")
            else:
                translator.write_to_text(f"cmp {a}, {b} ; {c}")
                translator.write_to_text(f"{conditions[m.group()]} _if_construction{z}_{translator.cc}")
        
    if not noelse:
        ToASM(_else_block.split("{", 1)[1][::-1].split("}", 1)[1][::-1], translator)
    translator.write_to_text(f"jmp _if_construction{translator.cc}_end")

    z = 0
    for cond in blocks:
        z+=1
        translator.write_to_text(f"_if_construction{z}_{translator.cc}:")
        ToASM(cond.split("{", 1)[1][::-1].split("}", 1)[1][::-1], translator)
        translator.write_to_text(f"jmp _if_construction{translator.cc}_end")

    translator.write_to_text(f"_if_construction{translator.cc}_end:")



def _syntax_defundef(string, translator, c):
    """
        define something
    """

    translator.write_to_text(f"; [{c}]: {string}")

    translator.write_to_text(string.replace("#", "%", 1))


def _syntax_from(string, translator, c):
    """
    #from "file" append "function"
    appends from a "file" a function
    """

    f, file, a, func, n = string.split("\"")
    if os.path.isfile(file):
        data = open(file).read()
    elif os.path.isfile(os.path.join(sys.path[0], file)):
        data = open(os.path.join(sys.path[0], file)).read()
    else:
        fileNotFound(f"No such file as \"{file}\"")

    translator._append += f"\n; [{c}] appended from {file} function {func}\n"
    if ";;required" in data:
        if not (
            file in translator.f_requires
            or
            os.path.join(sys.path[0], file) in translator.f_requires):

            translator.f_requires.append(file if file in translator.f_requires else os.path.join(sys.path[0], file))
            translator._append += f"\n{data.split(';;required')[0]}\n"
        data = data.split(";;required")[1]

    splited = data.split(";;endfunc")
    found = False


    for x in splited:
        if (func + ":") in x:
            translator._append += f"\nsection .text\n{x}\n"
            found = True
            break

    if not found:
        nameError(c, f"No such function as \"{func}\"")

def _syntax_head(string, translator, c):

    h, file = string.split("#head")
    file = file[::-1].split(maxsplit=1)[0][::-1]
    if os.path.isfile(file):
        data = open(file).read()
    elif os.path.isfile(os.path.join(sys.path[0], file)):
        data = open(os.path.join(sys.path[0], file)).read()
    else:
        fileNotFound(c, f"No such file as \"{file}\"")

    translator._append += f"\n; [{c}] appended head from {file}\n"
    if ";;head" in data:
        if not (
            file in translator.f_heads
            or
            os.path.join(sys.path[0], file) in translator.f_heads):

            translator.f_heads.append(file if file in translator.f_heads else os.path.join(sys.path[0], file))
            translator.coms += f"\n{data.split(';;head')[0]}\n"

    else:
        headError(c, f"No head in file \"{file}\"")



def _syntax_while(string, translator, c):
    """
    while(...) {
        ...;
    }
    """
    translator.cc += 1
    always_true = False
    name = f"__whileConstruction{translator.cc}"
    print(f"While start (for while in line {c})")
    condition = re.compile(r"\)[ \t]*\{").split(string)[0].split("while")[1].replace("(", "", 1)
    if not re.compile(r"[ \t]*true[ \t]*").fullmatch(condition):
        search = _comb.search(condition)

        if search == None:
            expressionError(c, f"There is an error in condition \"{condition}\"")

        search = search.group()
        fir, sec = condition.split(search)
        jmp = conditions[search]
    else:
        always_true = True

    translator.write_to_text(name + ":")

    lines = re.compile(r"\)[ \t]*\{").split(string, maxsplit=1)[1][::-1].split("}", maxsplit=1)[1][::-1]
    ToASM(lines, translator)

    if always_true:
        translator.write_to_text(f"jmp __whileConstruction{translator.cc}")    
    else:
        translator.write_to_text(f"cmp {fir}, {sec}\n{jmp} __whileConstruction{translator.cc}")
    print(f"While end (for while in line {c})")


#math func

def _syntax_imath(string, translator, c):
    """

    +=|-=|*=|/=|//=|%=
    +=  add<br />
    -=  sub<br />
    *=  mul<br />
    /=  div (returns float)<br />
    //= div (returns int)<br />
    %=  div (returns remainder)<br /><br />
    Also, add *float* before value, to use float functions<br />
    Examples:<br />
        dword [a] += dword [b] (returns int)<br />
        float dword [a] -= dword [b] (returns float)
    <br />
        dword [a] /= dword [b] (returns float)<br />
        dword [a] //= dword [b] (returns int)<br />
        dword [a] %= dword [b] (returns remainder)<br />
    **BUT**<br />
    Using floats with %= is forbidden

    """
    size = "qword" if translator.set_bits == 0 or translator.set_bits == 64 else "dword"
    _float = re.compile(r'\bfloat\b')
    translator.write_to_text(f"; [{c}]: {string}")
    fn = False

    a, op, b = ops.split(string, 1)
    A, B = _float.search(a), _float.search(b)
    """    if _regs.match(a) and _regs.match(b):

            if op == "+=":
                translator.write_to_text(f"add {a}, {b}")
            elif op == "-=":
                translator.write_to_text(f"sub {a}, {b}")
    """

    if _float_num.search(b):
        B = True
        fn = True
        b = "".join(b.split())
    _float = A or B
    a = a.replace("float", "", 1)
    b = b.replace("float", "", 1)
    tw = ()


    if _float:
        try:
            float(a)
            expressionError(c, "Expression error")
        except:
            pass
        try:
            if re.compile(r"\b([0-9abcdefABCDEF]+h|0x[0-9abcdefABCDEF]+|[0-9]+(\.[0-9]+){0,1})\b").search(b):
                if fn:
                    hex = double_to_hex(float(b))[2:]
                    hex = hex[:8], hex[8:]
                    if size == "qword":
                        tw = (f"mov dword [__used_for_nums+4], 0x{hex[0]}", f"mov dword [__used_for_nums], 0x{hex[1]}")
                    else:
                        tw = (f"mov dword [__used_for_nums], {float_to_hex(float(b))}")
                else:
                    tw = (f"mov {size} [__used_for_nums], {b}", )
                _b = b
                b = f"{size} [__used_for_nums]"
        except Exception as e:
            print(e)

    x = [z.group() for z in dsize.finditer(string)]

    if len(x) >= 1:
        regx = rax_size[x[0]]
        regy = rax_size[x[0]].replace('a', 'b') if len(x) == 1 else rax_size[x[1]].replace('a', 'b')

    else:
        regx = rax_size[size]
        regy = rax_size[size].replace('a', 'b')

    if translator.set_bits == 0:
        if len(x) > 0:
            d, e = data_size[x[0]]*8 > translator.set_bits, (data_size[x[1]]*8 > translator.set_bits if len(x) > 1 else data_size[x[0]]*8)
            if d or e:
                dataSizeError(c, f"{x[0] if d else x[1]} is too big for {translator.set_bits}-bits registers", f"#BITS {translator.set_bits} has been used")
            
        _pd = "rdx"
    else:
        _pd = rax_size[rdata_size[translator.set_bits//8]].replace("a", "d")


    if op == "+=":
        qa, da, qb, db = (
            _q.search(a),
            _d.search(a),
            _q.search(b),
            _d.search(b)
            )
        if _float:

            if qa:
                translator.write_to_text(f"mov qword [__used_for_nums], {a}")
                translator.write_to_text(f"fld qword [__used_for_nums]" if A else f"fild qword [__used_for_nums]")
                reg = True
                regs = "q"
            elif da:
                translator.write_to_text(f"mov dword [__used_for_nums], {a}")
                translator.write_to_text(f"fld dword [__used_for_nums]" if A else f"fild dword [__used_for_nums]")
                reg = True
                regs = "d"

            if qb:
                translator.write_to_text(f"mov qword [__used_for_nums], {b}")
                translator.write_to_text(f"fld qword [__used_for_nums]" if B else f"fild qword [__used_for_nums]")
                reg = True
            elif db:
                translator.write_to_text(f"mov dword [__used_for_nums], {b}")
                translator.write_to_text(f"fld dword [__used_for_nums]" if B else f"fild dword [__used_for_nums]")
                reg = True

            translator.write_to_text(f"fadd\nfstp " + (f"qword [__used_for_nums]\nmov {a}, qword [__used_for_nums]" if regs == "q" else f"dword [__used_for_nums]\nmov {a}, dword [__used_for_nums]"))

        else:
            if len(x) > 1:
                translator.write_to_text(f"""
    push {regx}")
    mov {regx}, {b}
    add {a}, {regx}
    pop {regx}""")

            else:
                translator.write_to_text(f"add {a}, {b}")

    elif op == "-=":
        qa, da, qb, db = (
            _q.search(a),
            _d.search(a),
            _q.search(b),
            _d.search(b)
            )
        if _float:

            if qa:
                translator.write_to_text(f"mov qword [__used_for_nums], {a}")
                translator.write_to_text(f"fld qword [__used_for_nums]" if A else f"fild qword [__used_for_nums]")
                reg = True
                regs = "q"
            elif da:
                translator.write_to_text(f"mov dword [__used_for_nums], {a}")
                translator.write_to_text(f"fld dword [__used_for_nums]" if A else f"fild dword [__used_for_nums]")
                reg = True
                regs = "d"

            if qb:
                translator.write_to_text(f"mov qword [__used_for_nums], {b}")
                translator.write_to_text(f"fld qword [__used_for_nums]" if B else f"fild qword [__used_for_nums]")
                reg = True
            elif db:
                translator.write_to_text(f"mov dword [__used_for_nums], {b}")
                translator.write_to_text(f"fld dword [__used_for_nums]" if B else f"fild dword [__used_for_nums]")
                reg = True

            translator.write_to_text(f"fsub\nfstp " + (f"qword [__used_for_nums]\nmov {a}, qword [__used_for_nums]" if regs == "q" else f"dword [__used_for_nums]\nmov {a}, dword [__used_for_nums]"))

        else:
            if len(x) > 1:
                translator.write_to_text(f"""
    push {regx}
    mov {regx}, {b}
    sub {a}, {regx}
    pop {regx}""")

            else:
                translator.write_to_text(f"sub {a}, {b}")

    elif op == "*=":
        if not _float:
            if len(x) > 1:
                translator.write_to_text(f"""
    push {regx}
    push {regy}
    push {_pd}
    mov {regx}, 0
    mov {regy}, 0
    mov {_pd}, 0
    {f'mov {regx}, {a}' if regx != a else ''}
    {f'mov {regy}, {b}' if regy != b else ''}
    mul {regy}
    mov {a}, {regx}
    pop {_pd}
    pop {regy}
    pop {regx}""")
            else:
                a = ''.join(a.split())
                b = ''.join(b.split())
                A = regx != a
                B = regy != a
                D = _pd != a


                translator.write_to_text(f"""
    {f'push {_pd}' if D else ''}
    {f'push {regx}' if A else ''}
    {f'push {regy}' if B else ''}

    push {a}
    push {b}
    pop {regy}
    pop {regx}
    mov {_pd}, 0

    mul {regy}
    {f'mov {a}, {regx}' if A else ''}
    {f'pop {regy}' if B else ''}
    {f'pop {regx}' if A else ''}
    {f'pop {_pd}' if D else ''}
""")


        else:
            translator.write_to_text(f"fld {a}" if A else f"fild {a}")
            for x in tw:
                translator.write_to_text(x)
            translator.write_to_text(f"fld {b}" if B else f"fild {b}")

            translator.write_to_text(f"fmul\nfstp " + a)

    elif op == "//=":
        if not _float:
            if len(x) > 1:
                translator.write_to_text(f"""
    push {regx}
    push {regy}
    push {_pd}
    {f'mov {regx}, {a}' if regx != a else ''}
    {f'mov {regy}, {b}' if regy != b else ''}
    mov {_pd}, 0
    div {regy}
    mov {a}, {regx}
    pop {_pd}
    pop {regy}
    pop {regx}""")
            else:
                a = ''.join(a.split())
                b = ''.join(b.split())
                
                A = regx != a
                B = regy != a
                D = _pd != a


                translator.write_to_text(f"""
    {f'push {_pd}' if D else ''}
    {f'push {regx}' if A else ''}
    {f'push {regy}' if B else ''}

    push {a}
    push {b}
    pop {regy}
    pop {regx}
    mov {_pd}, 0

    div {regy}
    {f'mov {a}, {regx}' if A else ''}
    {f'pop {regy}' if B else ''}
    {f'pop {regx}' if A else ''}
    {f'pop {_pd}' if D else ''}
""")


        else:
            translator.write_to_text(f"fld {a}" if A else f"fild {a}")
            for x in tw:
                translator.write_to_text(x)
            translator.write_to_text(f"fld {b}" if B else f"fild {b}")
            
            translator.write_to_text(f"fdiv\nfistp " + a)

    elif op == "%=":
        if not _float:
            if len(x) > 1:
                translator.write_to_text(f"""
    push {regx}
    push {regy}
    push {_pd}
    mov {regx}, 0
    mov {regy}, 0
    {f'mov {regx}, {a}' if regx != a else ''}
    {f'mov {regy}, {b}' if regy != b else ''}
    mov {_pd}, 0
    div {regy}
    mov {a}, {regx.replace('a', 'd')}
    pop {_pd}
    pop {regy}
    pop {regx}""")
            else:
                a = ''.join(a.split())
                b = ''.join(b.split())
                A = regx != a
                B = regy != a
                D = _pd != a


                translator.write_to_text(f"""
    {f'push {_pd}' if D else ''}
    {f'push {regx}' if A else ''}
    {f'push {regy}' if B else ''}

    push {a}
    push {b}
    pop {regy}
    pop {regx}
    mov {_pd}, 0

    div {regy}
    {f'mov {a}, {_pd}' if D else ''}
    {f'pop {regy}' if B else ''}
    {f'pop {regx}' if A else ''}
    {f'pop {_pd}' if D else ''}
""")
        else:
            syntaxError(c, "Cannot use float operand to get remainder (use fti if it's required)")

    elif op == "/=":

        qa, da, qb, db = (
            _q.search(a),
            _d.search(a),
            _q.search(b),
            _d.search(b)
            )


        reg = False

        if qa:
            translator.write_to_text(f"mov qword [__used_for_nums], {a}")
            translator.write_to_text(f"fld qword [__used_for_nums]" if A else f"fild qword [__used_for_nums]")
            reg = True
            regs = "qword"
            print(1)
        elif da:
            translator.write_to_text(f"mov dword [__used_for_nums], {a}")
            translator.write_to_text(f"fld dword [__used_for_nums]" if A else f"fild dword [__used_for_nums]")
            reg = True
            regs = "dword"

        else:
            if _int_num.search(a) or _regs.search(a):
                translator.write_to_text(f"mov {size} [__used_for_nums], {a}")
                translator.write_to_text(f"fld {size} [__used_for_nums]" if A else f"fild {size} [__used_for_nums]")

            else:
                translator.write_to_text(f"fld {a}" if A else f"fild {a}")
        
        if qb:
            translator.write_to_text(f"mov qword [__used_for_nums], {b}")
            translator.write_to_text(f"fld qword [__used_for_nums]" if B else f"fild qword [__used_for_nums]")
        elif db:
            translator.write_to_text(f"mov dword [__used_for_nums], {b}")
            translator.write_to_text(f"fld dword [__used_for_nums]" if B else f"fild dword [__used_for_nums]")

        else:
            for x in tw:
                translator.write_to_text(x)
            if tw:
                translator.write_to_text(f"fld {size} [__used_for_nums]" if B else f"fild {size} [__used_for_nums]")
            else:
                translator.write_to_text(f"fld {b}" if B else f"fild {b}")
        
        translator.write_to_text("fdiv")
        if reg:
            translator.write_to_text(f"fstp {regs} [__used_for_nums]\nmov {a}, {regs} [__used_for_nums]")
        else:
            translator.write_to_text(f"fstp {a}")


def _syntax_shift(string, translator, c):
    """
        shifts first 
        a >> b
        a << b
        shr a, b
        shl a, b
    """
    translator.write_to_text(f"; [{c}]: {string}")

    if "<<" in string:
        a, b = string.split("<<")
        translator.write_to_text(f"shl {a}, {b}")
    else:
        a, b = string.split(">>")
        translator.write_to_text(f"shr {a}, {b}")


#fmath func

def _syntax_fadd(string, translator, c):
    """
        fadd *value1*, *value2*, *result*

        If you have integers you can use

        fadd int *value1*, *value2*, *result*
        or
        fadd *value1*, int *value2*, *result*

        return value to *result*
    """
    translator.write_to_text(f"; [{c}]: {string}")

    global syntax_int_conv
    value1, value2, result = string.split(", ")
    value1 = value1.split("fadd ", 1)[1]


    translator.write_to_text(f"fild {value1.split('int ')[1]}" if syntax_int_conv.fullmatch(value1) else f"fld {value1}")
    translator.write_to_text(f"fild {value2.split('int ')[1]}" if syntax_int_conv.fullmatch(value2) else f"fld {value2}")
    translator.write_to_text(f"fadd")
    translator.write_to_text(f"fstp " + result)


def _syntax_fsub(string, translator, c):
    """
        fsub *value1*, *value2*, *result*

        If you have integers you can use

        fsub int *value1*, *value2*, *result*
        or
        fsub *value1*, int *value2*, *result*

        return value to *result*
    """
    translator.write_to_text(f"; [{c}]: {string}")

    value1, value2, result = string.split(", ")
    value1 = value1.split("fsub ", 1)[1]


    translator.write_to_text(f"fild {value1.split('int ')[1]}" if syntax_int_conv.fullmatch(value1) else f"fld {value1}")
    translator.write_to_text(f"fild {value2.split('int ')[1]}" if syntax_int_conv.fullmatch(value2) else f"fld {value2}")
    translator.write_to_text(f"fsub")
    translator.write_to_text(f"fstp " + result)




def _syntax_fmul(string, translator, c):
    """
        fmul *value1*, *value2*, *result*
        
        If you have integers you can use

        fmul int *value1*, *value2*, *result*
        or
        fmul *value1*, int *value2*, *result*

        return value to *result*
    """
    translator.write_to_text(f"; [{c}]: {string}")

    value1, value2, result = string.split(", ")
    value1 = value1.split("fmul ", 1)[1]


    translator.write_to_text(f"fild {value1.split('int ')[1]}" if syntax_int_conv.fullmatch(value1) else f"fld {value1}")
    translator.write_to_text(f"fild {value2.split('int ')[1]}" if syntax_int_conv.fullmatch(value2) else f"fld {value2}")

    translator.write_to_text(f"fmul")
    translator.write_to_text(f"fstp " + result)



def _syntax_fdiv(string, translator, c):
    """
        fdiv *value1*, *value2*, *result*

        If you have integers you can use

        fdiv int *value1*, *value2*, *result*
        or
        fdiv *value1*, int *value2*, *result*

        return value to *result*
    """
    translator.write_to_text(f"; [{c}]: {string}")

    value1, value2, result = string.split(", ")
    value1 = value1.split("fdiv ", 1)[1]

    translator.write_to_text(f"fild {value1.split('int ')[1]}" if syntax_int_conv.fullmatch(value1) else f"fld {value1}")
    translator.write_to_text(f"fild {value2.split('int ')[1]}" if syntax_int_conv.fullmatch(value2) else f"fld {value2}")
    
    translator.write_to_text(f"fdiv")
    translator.write_to_text(f"fstp " + result)


def _syntax_float_to_int(string, translator, c):
    """ 
        fti qword [*name*]
        fti - Float To Int
        
        converts float to int
    """
    translator.write_to_text(f"; [{c}]: {string}")

    name, dest = string.split("fti ")[1].split(", ")
    translator.write_to_text(f"fld {name}")
    translator.write_to_text(f"fistp {dest}")

def _syntax_int_to_float(string, translator, c):
    """ 
        itf qword [*name*]
        itf - Int To Float
        
        converts int to float
    """
    translator.write_to_text(f"; [{c}]: {string}")

    name, dest = string.split("itf ")[1].split(", ")
    translator.write_to_text(f"fild {name}")
    translator.write_to_text(f"fstp {dest}")

def _syntax_convto(string, translator, c):
    """
    convto float *size* [x]
    convto double *size* [x]
    convto int *size* [x]

    convto float rax
    convto double eax
    convto int (rax/eax)
    """
    translator.write_to_text(f"; [{c}]: {string}")

    t, n = string.split("convto", 1)[1].split(maxsplit=1)
    i = False
    r = _q.search(n), _d.search(n)

    if syntax_int_conv.search(n):
        n = n.replace("int", "", 1)
        i = True

    if r[0]:
        r = True, r[0].group(), "qword"

    elif r[1]:
        r = True, r[1].group(), "dword"

    if t == "float":
        if r[0]:
            translator.write_to_text(f"""
            mov [__used_for_nums], {r[1]}
            {'fild' if i else 'fld'} {r[2]} [__used_for_nums]
            """)

        else:
            translator.write_to_text(f"{'fild' if i else 'fld'} {n}")
        translator.write_to_text(f"""
        fstp dword [__used_for_nums]
        mov eax, [__used_for_nums]
        """)

    elif t == "double":
        if r[0]:
            translator.write_to_text(f"""
            mov [__used_for_nums], {r[1]}
            {'fild' if i else 'fld'} {r[2]} [__used_for_nums]
            """)

        else:
            translator.write_to_text(f"{'fild' if i else 'fld'} {n}")

        translator.write_to_text(f"""
        fstp qword [__used_for_nums]
        mov rax, [__used_for_nums]
        """)

    elif t == "int":
        if r[0]:
            translator.write_to_text(f"""
            mov [__used_for_nums], {r[1]}
            {'fild' if i else 'fld'} {r[2]} [__used_for_nums]
            """)

        else:
            translator.write_to_text(f"{'fild' if i else 'fld'} {n}")

        translator.write_to_text(f"""
        fistp qword [__used_for_nums]
        mov rax, [__used_for_nums]
        """)

syntax = {
    #data
    syntax_int_data         : _syntax_int_data,
    syntax_int_data_no_args : _syntax_int_data_no_args,
    syntax_res_int_data     : _syntax_res_int_data,
    syntax_string           : _syntax_string,
    syntax_const            : _syntax_const,
    syntax_list             : _syntax_list,
    syntax_float            : _syntax_float,

    #macros
    syntax_global               : _syntax_global,
    syntax_extern               : _syntax_extern,
    syntax_append               : _syntax_append,
    syntax_syntax               : _syntax_syntax,
    syntax_call_with_args       : _syntax_call_with_args,
    syntax_call_with_args_rets  : _syntax_call_with_args_rets,
    syntax_asm                  : _syntax_asm,
    syntax_point                : _syntax_point,
    syntax_def                  : _syntax_defundef,
    syntax_from                 : _syntax_from,
    syntax_head                 : _syntax_head,
    syntax_bits                 : _syntax_bits,

    #instructions
    syntax_mov        : _syntax_mov,
    syntax_int        : _clean_asm_text,
    syntax_call       : _clean_asm_text,
    syntax_push       : _clean_asm_text,
    syntax_pop        : _clean_asm_text,
    syntax_jmp        : _clean_asm_text,
    syntax_ret        : _clean_asm_text,
    syntax_logic      : _clean_asm_text,
    syntax_syscall    : _syntax_syscall,
    syntax_pushpop_aq : _syntax_pushpop_aq,
    
    #math
    syntax_add_instr  : _clean_asm_text,
    syntax_sub_instr  : _clean_asm_text,
    syntax_add        : _syntax_imath,
    syntax_sub        : _syntax_imath,
    syntax_macro_idiv : _syntax_imath,
    syntax_macro_div  : _syntax_imath,
    syntax_macro_rem  : _syntax_imath,
    syntax_macro_mul  : _syntax_imath,
    syntax_div        : _clean_asm_text,
    syntax_mul        : _clean_asm_text,
    syntax_inc        : _syntax_incdec,
    syntax_dec        : _syntax_incdec,
    syntax_shift      : _syntax_shift,

    #fmath
    syntax_convto : _syntax_convto,

    syntax_fadd : _syntax_fadd,
    syntax_fsub : _syntax_fsub,
    syntax_fmul : _syntax_fmul,
    syntax_fdiv : _syntax_fdiv,

}


def _macros_not_defined_array():
    pass

macros = {
    syntax_not_defined_array : 0,
    syntax_not_defined_string : 0,
}

def rep_spec_chars(value):
    chars = [a for a in spec_char.finditer(value)][::-1]

    for x in chars:
        g = x.group()
        if (len(g.split("\\"))-1) % 2 != 0:
            a, b = x.span()
            a += (len(g.split("\\"))-1) // 2
            value = value[:a] + f"\", {spec_char_to_num[g]}, \"" + value[b:]


    numbytes = [a for a in numbyte.finditer(value)][::-1]

    for x in numbyte.finditer(value):
        g = x.group()
        if (len(g.split("\\"))-1) % 2 != 0:
            a, b = x.span()
            a += (len(g.split("\\"))-1) // 2
            value = value[:a] + f"\", 0x{g[-4::][2:]}, \"" + value[b:]
    value = value.replace("\\\\", "\\")

    return value

def split(text, char):
    quotes   = 0
    brackets = 0
    matches  = []

    before = -1
    comm = False

    for c, i in enumerate(text):
        if comm:
            if i == "*":
                if len(text) > c:
                    if text[c+1] == "/":
                        comm = False
                        before = c+1
        else:
            if i == "\"" and not text[c-1] == "\\":
                quotes = 0 if quotes else 1
            elif not quotes:
                if i == "{":
                    brackets += 1
                elif i == "}":
                    brackets -= 1
                if not brackets:
                    if i == char and not brackets:
                        matches.append(text[before+1:c])
                        before = c
                    elif i == "/":
                        if len(text) > c:
                            if text[c+1] == "*":
                                comm = True
    return matches

def ToASM(lines, translator, _syntax=syntax, print_lines = False):
    
    _lines = lines.split("\n")

    for line in split(lines.replace("\n", ""), ";"):
        translator.c += 1


        if syntax_nothing.fullmatch(line) or line == "":
            #if line is fullmatches(r"[ \t]*") -> skipping line
            continue

        if translator.print_lines:
            print(f"[{translator.c}]: {' '*(translator.lines_len - len(str(translator.c)))}{line}")

        if syntax_not_defined_string.search(line):
            for i in syntax_not_defined_string.finditer(line):
                g = i.group()
                res = g
                replaced = False

                rep = f"__notdef_string.n{translator.notdef_c}"


                g = rep_spec_chars(g)

                for l in translator.data.split("\n"):
                    if "__notdef_string" == l[:15]:
                        if f" db {g.replace('notdef', '')}, 0" == l.split(":")[1]:
                            line = line.replace(res, l.split(":")[0])
                            replaced = True

                if not replaced:
                    line = line.replace(res, rep)

                    translator.write_to_data(f"; [{translator.c}]: notdef string\n__notdef_string.n{translator.notdef_c}: db {g.replace('notdef', '')}, 0")


                translator.notdef_c += 1

        if syntax_not_defined_array.search(line):
            for i in syntax_not_defined_array.finditer(line):
                g = i.group()
                res = g
                replaced = False

                rep = f"__notdef_array.n{translator.notdef_c}"
                array = g.split("notdef", 1)[1].split("[")[1].split("]")[0].split(",")


                e = True
                translator.write_to_data(f"; [{translator.c}]: notdef array\n{rep}:")
                for a in array:
                    for t in types.keys():
                        if t in a:
                            translator.write_to_data(f"    {types[t]} {a.replace(t, '', 1)}")
                            e = False
                            break
                    if e:
                        if "__notdef_string.n" in a:
                            translator.write_to_data(f"    dq {a.replace(t, '', 1)}")
                        else:
                            valueError(translator.c, "No size specified")
                    e = True

                line = line.replace(res, rep)
                translator.notdef_c += 1

        not_matched = True

        if "if" in line and "{" in line:
            if syntax_if.match(line.split("{")[0]):
                _syntax_if(line, translator, translator.c)
                not_matched = False

        if "while" in line and "{" in line:
            if syntax_while.match(line.split("{")[0]):
                _syntax_while(line, translator, translator.c)
                not_matched = False

        if "function" in line and "{" in line:
            if syntax_func.match(line.split("{")[0]):
                _syntax_func(line, translator, translator.c)
                not_matched = False

        if not_matched:
            for s in _syntax.keys():
                if s.match(line):
                    _syntax[s](line, translator, translator.c)
                    not_matched = False
                    
                    break
            
        if not_matched:
            #if line does not fullmatch any syntax pattern
            #it shows error
            syntaxError(translator.c, f"Syntax error in line", line)

        translator.check_all_names()


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])

def if_float(s):
    return True if _float_num.search(s) else False 