# Changes
## Fixed stringf.compare
## Fixed **nosave** in function
## New macros for int math
### +=\|-=\|\*=\|/=\|//=\|%=
+=  add<br />
-=  sub<br />
\*=  mul<br />
/= 	div (returns float)<br />
//= div (returns int)<br />
%=  div (returns remainder)<br /><br />
Also, add *float* before value, to use float functions<br />
Examples:<br />
	dword \[a\] += dword \[b\] (returns int)<br />
	float dword \[a\] -= dword \[b\] (returns float)
<br />
	dword \[a\] /= dword \[b\] (returns float)<br />
	dword \[a\] //= dword \[b\] (returns int)<br />
	dword \[a\] %= dword \[b\] (returns remainder)<br />
**BUT**<br />
Using floats with %= is forbidden

## New function stringf.findString
## New Checker for name in file
It checks if variable's name is already used in file (or appended asm files)
## undefined replaced with notdef
keyword "undefined" replaced with keyword "notdef"
### notdef arrays:
undefined \[...\]<br />
Can contain undefined strings BUT cannot contain other undefined arrays
## BITS
.lnasm: #BITS *64/32/16*;<br />
-><br />
.asm:   BITS *64/32/16*