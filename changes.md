# Changes
## Default definitions
At the start of file (after "append" comments) defines: <br />
name of file\*<br />
version\*\*<br />
true (1)<br />
false (0)<br />
NULL (0)<br /><br />
\* \_\_file\_\_ = --outfile without extension (test.asm => test)<br />

\*\* \_\_version\_\_ = version of LNASM (\_\_version\_\_ = "\*.\*.\*", 0)<br /><br />


_check examples/default_defines.lnasm_
## Fixed spec constructions in _string_ and _undefined_ macros
"\\\\x23 abc"   -> "\\x23 abc"<br />
"\\\\\\x31 abc" -> "\\\\1 abc"<br /><br />

"\\\\n abc" -> "\\n abc"<br />
"\\\\\\n abc" -> "\\\\<br />
 abc"
## Added "section .text" to **NASMLibs/array64.asm**
To avoid errors

## New function in **NASMLIBS/stringf64.asm**
stringf.replace(<br />
	QWORD PTR (string) str,<br />
	QWORD (byte) char_to_replace,<br />
	QWORD (byte) replace_with_char,<br />
	QWORD (int) len)<br />
	replace a char (char_to_replace) with another char (replace_with_char) in string (str)<br /><br />
_check examples/stringf_replace.lnasm_