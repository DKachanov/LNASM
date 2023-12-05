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
math.ctg(QWORD (float) radians) -> QWORD (float) value
## Functions stringf.StrToNum and string.NumToStr now checks for sign (signed int)

## While
while(*condition*) {<br/>
	...<br/>
}<br/>

Check for example in examples/while.lnasm
