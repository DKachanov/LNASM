section .data

    consts.http200:
        db      "HTTP/1.1 200 OK",                      0ah
        db      "Date: xxx, xx xxx xxxx xx:xx:xx xxx",  0ah
        db      "Server: HTTP-ASM64",                   0ah
        db      "Content-Type: text/html",              0ah,0ah,0h
    consts.http200Len  equ     $ - consts.http200

    consts.http404:     
        db      "HTTP/1.1 404 Not Found",               0ah
        db      "Date: xxx, xx xxx xxxx xx:xx:xx xxx",  0ah
        db      "Server: HTTP-ASM64",                   0ah
        db      "Content-Type: text/html",              0ah,0ah,0
    consts.http404Len  equ     $ - consts.http404