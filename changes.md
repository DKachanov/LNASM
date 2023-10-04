# Changes
## New datatype _struct_
struct x = {<br />
    str    : db "test" \\<br />
    length : dq $ - x.str<br />
};<br /><br />
Creates a structure.<br />
You can access to value in structure with keyword using \*structure\*.\*keyword\*<br /><br />
In structure values are written as a raw string (you must use db/dw/dd/dq) and keyword -> value segments are splitted by backslash
## Comments
The problems with only-line comment and semicolon in comments are solved
## New functions
### stringf.StringToFloat
    (stringf.StringToFloat(QWORD PTR (string) addr, QWORD (int) length) -> QWORD (float) num)

    Converts a string to a float
### stringf.FloatToString()
    (stringf.FloatToString(QWORD (float) num, QWORD PTR (string) str) -> QWORD (int) length)

    Converts a float to a string