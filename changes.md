# Changes
## Fixed call with args
## Changed #asm
...<br />
#asm .text {<br />
	cmp ...;<br />
	je ...;<br />
	...;<br />
	test ...;<br />
};<br />
...<br />
## New function math.ctg
## Functions stringf.StrToNum and string.NumToStr now checks for sign (signed int)
math.ctg(QWORD (float) radians) -> QWORD (float) value

## While
while(*condition*) {<br/>
	...<br/>
}<br/>

Check for example in examples/while.lnasm

syntax.py
main.py
translator.py
base syntax.txt
NASMLibs/math64.asm
NASMLibs/stringf64.asm
examples/log.lnasm
examples/while.lnasm