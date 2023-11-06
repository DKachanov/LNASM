from re import compile

unsafe_call = compile(r"[ \t]*[^\(]*\(.*\)[ \t]*")

syntax.update({unsafe_call : syntax[syntax_call_with_args]})