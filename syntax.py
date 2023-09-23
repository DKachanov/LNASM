from re import compile
import os, sys

types = {
    "byte" : "db",
    "word" : "dw",
    "dword" : "dd",
    "qword" : "dq"
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
    ">=" : "jae",
    "<=" : "jbe",
    ">"  : "ja",
    "<"  : "jb",
}

type_num = {
    "db" : 0,
    "dw" : 1,
    "dd" : 2,
    "dq" : 3
}

spec_char_to_num = {
    "t" : 9,
    "n" : 10
}

#skips lines with no data
syntax_nothing = compile(r"[ \t]+")

#coms
syntax_com = compile(r";(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")

#not defined strings
syntax_not_defined_string = compile(r'''("[^"]){0}undefined[ \t]+"[^"]*"''')
numbyte = compile(r'\\+x[0-9abcdef]{2}')
spec_char = compile(r'\\+[n|t]')

#data
syntax_int_data         = compile(r"[ \t]*(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+.+")
syntax_int_data_no_args = compile(r"[ \t]*(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]*")
syntax_res_int_data     = compile(r"[ \t]*RES[ \t]+(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*\[.+\][ \t]*")
syntax_float            = compile(r"[ \t]*float[ \t]+(dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+.+[ \t]*")
syntax_list             = compile(
    r"[ \t]*list[ \t]+(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+\[(.*\,[ ]*)*.*\][ \t]*")
syntax_string           = compile(r"[ \t]*string[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+\".*\"[ \t]*")
syntax_const            = compile(r"[ \t]*const[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+= .+")

#instructions
syntax_push    = compile(r"[ \t]*push .+")
syntax_pop     = compile(r"[ \t]*pop .+")
syntax_ret     = compile(r"[ \t]*ret[ \t]*")
syntax_jmp     = compile(r"[ \t]*jmp .+")
syntax_call    = compile(r"[ \t]*call[ \t]+[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_int     = compile(r"[ \t]*int .+")
syntax_mov     = compile(r".* -> .*")
syntax_inc     = compile(r"[ \t]*.+\+\+[ \t]*")
syntax_dec     = compile(r"[ \t]*.+\-\-[ \t]*")
syntax_syscall = compile(r"[ \t]*syscall[\t ]*")

#macros
syntax_global         = compile(r"[ \t]*#global [a-z|A-Z|_][\.\w]*.*")
syntax_append         = compile(r"[ \t]*#append .*")
syntax_syntax         = compile(r"[ \t]*#syntax .*")
syntax_if             = compile(r"[ \t]*if .+ (==|!=|>|<|>=|<=) .+:[ \t]+\.*[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_call_with_args = compile(r"[ \t]*[a-z|A-Z|_][\w|\.]*\(.*\)[ \t]*")
syntax_asm            = compile(r"[ \t]*#asm[ \t]+\.(text|data|bss) .*")
syntax_point          = compile(r"[ \t]*::\.*[a-z|A-Z|_][\.\w]*[ \t]*")
syntax_extern         = compile(r"[ \t]*#extern[ \t]+[a-z|A-Z|_][\.\w]*.*")
syntax_def            = compile(r"[ \t]*#define[ \t]+[a-z|A-Z|_][\.\w]*[ \t]+.*")
syntax_undef          = compile(r"[ \t]*#undefine[ \t]+[a-z|A-Z|_][\.\w]*[ \t]*")


#imath
syntax_add = compile(r"[ \t]*add .*, .*")
syntax_sub = compile(r"[ \t]*sub .*, .*")
syntax_div = compile(r"[ \t]*div .*")
syntax_mul = compile(r"[ \t]*mul .*")

#fmath
syntax_fadd         = compile(r"[ \t]*fadd .*, .*, .*")
syntax_fsub         = compile(r"[ \t]*fsub .*, .*, .*")
syntax_fdiv         = compile(r"[ \t]*fdiv .*, .*, .*")
syntax_fmul         = compile(r"[ \t]*fmul .*, .*, .*")
syntax_float_to_int = compile(r"[ \t]*fti .*, .*")
syntax_int_conv     = compile(r"[ \t]*int .*")
syntax_float_conv   = compile(r"[ \t]*float .*")


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

    translator.write_to_data(f"{var} {types[type]} {value}")

def _syntax_int_data_no_args(string, translator, c):
    """
        *type* *name*

        makes a variable

        type: byte, word, dword, qword
    """
    translator.write_to_data(f"; [{c}]: {string}")

    find = compile(r"(byte|word|dword|qword)[ \t]+[a-z|A-Z|_][\w|\.]*")
    type, var = find.search(string).group().split()

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

    translator.write_to_data(f"{var} db {value}")

def _syntax_const(string, translator, c):
    """
        const *name* = *any*

        makes a const (equ)
    """
    translator.write_to_data(f"; [{c}]: {string}")

    var, value = string.split("=", 1)
    var = var.replace("const ", "")
    translator.write_to_data(f"{var} equ {value}")

def _syntax_float(string, translator, c):
    """ 
        float (qword|dword) *name* = *value*
        
        makes float variable
    
    """
    translator.write_to_data(f"; [{c}]: {string}")

    type = string.split("float")[1].split()[0]
    data = types[type]
    name = string.split("float ")[1].split()[1]
    value = string.split("=")[1]
    
    translator.write_to_data(f"{name} {data} {value}")


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



#macros func
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
        print(f"[ERROR]: No such file as \"{string.split('#syntax ')[1]}\"")
        exit(1)
    
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
    args = string.split("(")[1].split(")")[0].split(",")
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

    sec, code = string.split("#asm ", 1)[1].split(maxsplit=1)
    if sec == ".text":
        translator.write_to_text(code)
    elif sec == ".data":
        translator.write_to_data(code)
    elif sec == ".bss":
        translator.write_to_bss(code)
    else:
        raise SyntaxError((string, "unknown section"))

def _clean_asm_text(string, translator, c):
    """
        writes raw asm string in text section
    """
    translator.write_to_text(f"; [{c}]: {string}")
    
    translator.write_to_text(string)




def _syntax_if(string, translator, c):
    """
        if value1 (==|!=|>|<|>=|<=) value2: dest

        compares 2 values and jump into point

        if float value1 (==|!=|>|<|>=|<=) float value2: dest
    """
    translator.write_to_text(f"; [{c}]: {string}")

    value1 = string.split("if ")[1]
    for k in conditions.keys():
        if k in string:
            value1 = value1.split(k)[0]
            value2 = string.split(k)[1].split(":")[0]
            con = k
            break

    dest = string.split(": ")[1]
    sfc = [syntax_float_conv.fullmatch(x) for x in [value1, value2]]

    if not any(sfc):
        jump = conditions[con]
        translator.write_to_text(f"cmp {value1}, {value2}\n{jump} {dest}")
    else:
        jump = fconditions[con]
        translator.write_to_text(f"fld {value1.split('float ')[1]}" if syntax_float_conv.fullmatch(value1) else f"fild {value1}")
        translator.write_to_text(f"fld {value2.split('float ')[1]}" if syntax_float_conv.fullmatch(value2) else f"fild {value2}")
        translator.write_to_text(f"fcomi\n{jump} {dest}")



def _syntax_defundef(string, translator, c):
    """
        define something
    """

    translator.write_to_text(f"; [{c}]: {string}")

    translator.write_to_text(string.replace("#", "%", 1))


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



syntax = {
    #data
    syntax_int_data : _syntax_int_data,
    syntax_int_data_no_args : _syntax_int_data_no_args,
    syntax_res_int_data : _syntax_res_int_data,
    syntax_string : _syntax_string,
    syntax_const : _syntax_const,
    syntax_list : _syntax_list,
    syntax_float : _syntax_float,

    #instructions
    syntax_mov : _syntax_mov,
    syntax_int : _clean_asm_text,
    syntax_call : _clean_asm_text,
    syntax_push : _clean_asm_text,
    syntax_pop : _clean_asm_text,
    syntax_jmp : _clean_asm_text,
    syntax_ret : _clean_asm_text,
    syntax_syscall : _clean_asm_text,

    #macros
    syntax_global : _syntax_global,
    syntax_extern : _syntax_extern,
    syntax_append : _syntax_append,
    syntax_syntax : _syntax_syntax,
    syntax_call_with_args : _syntax_call_with_args,
    syntax_asm : _syntax_asm,
    syntax_if : _syntax_if,
    syntax_point : _syntax_point,
    syntax_def : _syntax_defundef,
    syntax_undef : _syntax_defundef,

    #math
    syntax_add : _clean_asm_text,
    syntax_sub : _clean_asm_text,
    syntax_div : _clean_asm_text,
    syntax_mul : _clean_asm_text,
    syntax_inc : _syntax_incdec,
    syntax_dec : _syntax_incdec,

    #fmath
    syntax_float_to_int : _syntax_float_to_int,

    syntax_fadd : _syntax_fadd,
    syntax_fsub : _syntax_fsub,
    syntax_fmul : _syntax_fmul,
    syntax_fdiv : _syntax_fdiv,
}

def rep_spec_chars(value):
    for x in spec_char.finditer(value):
        g = x.group()
        if (len(g.split("\\"))-1) % 2 != 0:
            a = g[-2:]
            print(a)
            value = value.replace(a, f"\", {hex(spec_char_to_num[a[1:]])}, \"")
    
    for x in numbyte.finditer(value):
        g = x.group()
        if (len(g.split("\\"))-1) % 2 != 0:
            a = g[-4:]
            value = value.replace(a, f"\", 0x{a[2:]}, \"")
    value = value.replace("\\\\", "\\")

    return value