# Changes
## New errors
## fixed undefined strings
## functions
### function func(qword arg1, ...) {...}
example:<br/>
RES byte res\[20\];<br/><br />
function inputNum() {<br />
	stdio.input(res, 20);<br/>
	stringf.StrToNum(res, rax);<br/>
};
### void function func(qword arg1, ...) {...}
RES byte res\[20\];<br/><br />
void function printNum(qword num) {<br/>
    stringf.NumToStr(a, res);<br/>
    stringf.len(res);<br/>
    stdio.print(res, rax);<br/>
};
### function func(qword arg1, ...) nosave {...}
nosave -> registers wont be pushed and poped<br />
(registers' data will not be saved)

### function ret
qword \[a\] = test();<br />
is the same as<br />
test();<br />
rax -> qword \[a\];<br />

## data
Now allowed to write qword a, b, c;<br />
instead of qword a; qword b; qword c

## syntax/snippets
Added .sublime-syntax/.sublime-snippet for sublime text

## new if
if (...) {<br />
    ...;<br />
} else if (...) {<br />
    ...;<br />
} else {<br />
    ...;<br />
};<br />
