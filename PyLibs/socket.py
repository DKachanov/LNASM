from re import compile

syntax_socketAddr = compile(
	r"[ \t]*socketAddr[ \t]+[a-z|A-Z|_]\w*\[.*,[ \t]*\d+\.\d+\.\d+\.\d+,[ \t]*(-)?(0x){0,1}[0-9.abcde]+(h){0,1},[ \t]*(-)?(0x){0,1}[0-9.abcde]+(h){0,1}\][ \t]*")

syntax_res_socketAddr = compile(
	r"[ \t]*socketAddr[ \t]+[a-z|A-Z|_]\w*\[\][ \t]*")

def _syntax_socketAddr(string, translator, c):
	"""
		creates sockaddr struct
		sockaddr:
			dw FAMILY
			db port (0, 0)
			db addr (0, 0, 0, 0)
			dq flags

		constants:
			sockaddr.family
			sockaddr.port
			sockaddr.addr
			sockaddr.flags
	"""
	translator.write_to_data(f"; [{c}]: {string}")

	var = string.split("socketAddr", 1)[1]
	var, data = var.split("[",1)
	data = data.split("]", 1)[0].split(",")
	data[1] = data[1].replace('.', ',')

	data[2] = str(hex(int(data[2].replace('h', "").replace("0x", "").replace(" ", "").replace("\t", ""))))[2:]
	if len(data[2]) < 5:
		data[2] = "0"*(4-len(data[2])) + data[2]
	data[2] = data[2][:2], data[2][2:]

	translator.write_to_data(f"""{var}:
	dw {data[0]}
	db 0x{data[2][0]}, 0x{data[2][1]}
	db {data[1]}
	dq {data[3]}
{var}.len equ $ - {var}
{var}.family equ {var}
{var}.port   equ {var}+2
{var}.addr   equ {var}+4
{var}.flags  equ {var}+8""")

def _syntax_res_socketAddr(string, translator, c):
	translator.write_to_data(f"; [{c}]: {string}")

	var = string.split("socketAddr", 1)[1]
	var = var.split(maxsplit=1)[0]
	var = var[:len(var)-2]
	translator.write_to_data(f"""{var}:
	dw 0
	db 0, 0
	db 0, 0, 0, 0
	dq 0
{var}.len equ $ - {var}
{var}.family equ {var}
{var}.port   equ {var}+2
{var}.addr   equ {var}+4
{var}.flags  equ {var}+8""")


syntax.update({syntax_socketAddr : _syntax_socketAddr,
			   syntax_res_socketAddr : _syntax_res_socketAddr
			   })