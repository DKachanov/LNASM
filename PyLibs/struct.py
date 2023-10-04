from re import compile

syntax_struct = compile(r"[ \t]*struct[ \t]+[a-z|A-Z|_][\w|\.]*[ \t]+=[ \t]+\{(.*\,[ ]*)*.*\}[ \t]*")
by_backslash = compile(r"\\(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
by_space = compile(r"[ \t](?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
nothing = compile(r"[ \t]+")

def _syntax_struct(string, translator, c):
	"""
	creates structure
	"""
	global by_backslash, by_space, nothing
	translator.write_to_data(f"; [{c}]: {string}")

	s = string.split("struct", 1)[1]
	
	n, s = s.split("=", 1)
	n = n.replace(" ", "").replace("\t","")
	
	struct = s.split("{", 1)[1][::-1].split("}", 1)[1][::-1]
	# "{abc}" -> "abc}" -> "}cba" -> "cba" -> "abc"
	key_val = by_backslash.split(struct)

	translator.write_to_data(f"{n} equ $")

	for kv in key_val:
		if ":" in kv:
			k,v = kv.split(":", 1)
			k = ''.join(by_space.split(k)) + ":"
			translator.write_to_data(f"{n}.{k}{v}")
		else:
			if not nothing.fullmatch(kv):
				print(f"[WARNING!] ({c}): Struct {n}: in {kv} is ignored due to missed colon")


syntax.update({
	syntax_struct : _syntax_struct
	})