from re import compile

'''
[
qword dev, 0
qword ino, 8
dword mode, 16
dword nlink, 16
dword uid, 20
dword gid, 24
qword rdev, 28
qword __pad1, 36
qword size, 44
dword blksize, 52
dword __pad2, 56
qword blocs, 60
qword atime, 68
qword __pad3, 76
qword mtime, 84
qword __pad4, 92
qword ctime, 100
qword __pad5, 108
dword __unused4, 112
dword __unused5, 116
]
len = 132'''

syntax_statbuf_stat = compile(r"[ \t]*statbuf[ \t]+[a-z|A-Z|_]\w*[ \t]*")

def _syntax_statbuf_stat(string, translator, c):
	translator.write_to_data(f"; [{c}]: {string}")

	name = string.split("statbuf ", 1)[1].split(" ")[0]

	translator.write_to_data(f"""
{name}: TIMES 132 db 0
{name}.dev equ {name}
{name}.ino equ {name}+8
{name}.mode equ {name}+16
{name}.nlink equ {name}+20
{name}.uid equ {name}+24
{name}.gid equ {name}+28
{name}.rdev equ {name}+32
{name}.__pad1 equ {name}+40
{name}.size equ {name}+48
{name}.blksize equ {name}+56
{name}.__pad2 equ {name}+60
{name}.blocs equ {name}+64
{name}.atime equ {name}+72
{name}.__pad3 equ {name}+80
{name}.mtime equ {name}+88
{name}.__pad4 equ {name}+96
{name}.ctime equ {name}+104
{name}.__pad5 equ {name}+112
{name}.__unused4 equ {name}+120
{name}.unused5 equ {name}+128

""")

syntax.update({
	syntax_statbuf_stat : _syntax_statbuf_stat
	})