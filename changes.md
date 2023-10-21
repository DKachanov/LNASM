# Changes

## New macros
### \#from "file" append "func";
This macros requires a split word ";;endfunc"<br />
If your functions requires some definitions or variables, you can move them to the start of file and write ";;required" after to let
### syscall
Now, it can include args:<br />
syscall 1, 1, undefined "test", 4;<br />
translates to<br />
mov rax, 1<br />
mov rdi, 1<br />
mov rsi, \_\_undefined_string.n0<br />
mov rdx, 4<br />
syscall
### \#head
#head ...;<br />
Append head of file (before ";;head")
## Fixed stringf.FloatToString
## New struct syntax
The split char is changed to ',' ('\\' before)<br /><br />
To access _struct_ syntax, load _PyLibs/struct.py_
## New NASMLib "syscalls.asm"
Append a list of syscall names (defines)
<br />
For example, syscall.sys_exit, syscall.sys_write, etc.<br />

Use _#head_ to apply it properly.