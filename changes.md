# Changes
## New PyLib unsafe_call.py
If you have some unusual "names" for function address (\[rbp + 8\], \[rbx\], etc.), use _\#syntax PyLibs/unsafe\_call.py_.<br />
It allows using unsafe names
## New function stdf.signal
Handles signals<br /><br />

example: compiled/web/server.lnasm
## New function array.bubble_sort
Sort an array with bubble sort algorithm<br /><br />

example: sort.lnasm
## Server example at compiled/web
## Fixed false = 1 -> false = 0