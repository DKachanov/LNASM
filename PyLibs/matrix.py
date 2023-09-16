from re import compile

syntax_matrix = compile(r"[ \t]*matrix(8|16|32|64)[ \t]+[a-z|A-Z|_]\w*\[(0x){0,1}[0-9.abcde]+(h){0,1},[ ]+(0x){0,1}[0-9.abcde]+(h){0,1}\]")
matrix_type = {
	"8" : "db",
	"16" : "dw",
	"32" : "dd",
	"64" : "dq"
}

def _syntax_matrix(string, translator, c):
	"""
		creates 2d matrix:
		matrix(8/16/32/64 bit) name[block_size, num_of_blocks]
	"""

	translator.write_to_data(f"; [{c}]: {string}")

	global matrix_type

	var, size = string.split("[")
	size = size.split("]")[0].replace(" ", "").replace("\t", "").split(",")
	s = 1
	for a in size:
		if "0x" in a or "h" in a:
			s *= int(a.replace("h", ""), 16)
		else:
			s *= int(a)
	x = var.find("matrix") + 6
	type = var[x:x+2].replace(" ", "").replace("\t", "")
	type = matrix_type[type]
	name = var.split("matrix")[1].split()[1].replace(" ", "").replace("\t", "")
	translator.write_to_data(f'{name}: TIMES {s} {type} 0')


syntax.update(
	{syntax_matrix : _syntax_matrix})