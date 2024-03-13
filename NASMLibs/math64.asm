; examples:
;     math.factorial -> factorial.lnasm
;     math.ipower    -> ipower.lnasm 

section .data
        math.piOn180 dq __float64__(0.017453292519943295)

section .text

;;required

math.factorial:
        ; math.factorial(QWORD (int) number) -> QWORD (int) value
        push  rbx
        push  rbp
        mov  rbp,rsp

        mov  rax, [rbp+24]
        
        .loop:
        cmp  rax,1
        je .end_factorial
        
        dec  rax
        
        push  rax
        
        call math.factorial.loop
        
        mov  rbx, [rbp+24]
        imul  rax,rbx


.end_factorial: 
        mov  rsp,rbp
        pop  rbp
        pop  rbx
        ret 8

;;endfunc

math.sqrt:
        ;math.sqrt(QWORD (double) value) -> QWORD (double) value
        fld qword [rsp+8]
        fsqrt
        fstp qword [rsp+8]
        mov rax, [rsp+8]
        ret 8

;;endfunc

math.radians:
        ; math.radians(QWORD (double) angle) -> QWORD (double) radians
        fld qword [math.piOn180]
        fmul qword [rsp+8]
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.sin:
        ; math.sin(QWORD (double) radians) -> QWORD (double) value
        fld qword [rsp+8]
        fsin
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.cos:
        ; math.cos(QWORD (double) radians) -> QWORD (double) value
        fld qword [rsp+8]
        fcos
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.tan:
        ; math.tan(QWORD (double) radians) -> QWORD (double) value
        fld qword [rsp+8]
        fptan
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc
math.ctg:
        ; math.ctg(QWORD (double) radians) -> QWORD (double) value
        mov rdx, [rsp+8]
        push rdx
        call math.cos
        push rax
        push rdx
        call math.sin
        fld qword [rsp+8]
        fld qword [rsp]
        fdiv
        fstp qword [rsp]
        mov rax, qword [rsp]
        add rsp, 24
        ret 8
;;endfunc

math.abs:
        ;math.abs(QWORD (int) number) -> QWORD (int) absolute of number
        push rbx
        mov rax, [rsp+8]
        mov rbx, 0x7fffffffffffffff
        cmp rax, rbx
        jl .c
        jmp .ret
        .c:
        neg rax
        .ret:
        pop rbx
        ret 8

;;endfunc

math.ipower:
        ; math.ipower(QWORD (int) number, QWORD (int) power) -> QWORD (int) value
        push rcx
        mov rax, [rsp+16]
        mov rcx, [rsp+24]

        cmp rcx, 1
        je math.ipower.end

        cmp rcx, 0
        je math.ipower.p0

        push rbx
        mov rbx, rax

        math.ipower.loop:
                dec rcx
                cmp rcx, 0
                je math.ipower.end
                mul rbx
                jmp math.ipower.loop


        math.ipower.p0:
                mov rax, 1
                pop rcx
                ret 16

        math.ipower.end:
                pop rbx
                pop rcx
                ret 16

;;endfunc

math.log:
        ; math.log(QWORD (double) base, QWORD (double) num) -> QWORD (double) result
        ; Log(2)(num)/Log(2)(base)  to get Log(base)(num)
        push 1
        fld qword [rsp] ;y 
        fld qword [rsp+16] ;x
        fyl2x
        fstp qword [rsp+16]

        fld qword [rsp]
        fld qword [rsp+24]
        fyl2x
        fstp QWORD [RSP+24];Pop the result from the logarithm to the stack

        fld qword [rsp+24]
        fld qword [rsp+16]
        fdiv
        fstp qword [rsp+16]
        mov rax, qword [rsp+16]
        add rsp, 8
        ret 16
;;endfunc

section .data
        math.res dq 0

math.round:
        ; math.round(QWORD (double) num, QWORD (int) after_dot) -> QWORD (double) result

        push rbp
        mov rbp, rsp

        push qword [rbp+24]
        push 10
        call math.ipower
        
        mov [math.res], rax
        push rax

        fld qword [rbp+16]
        fild qword [rsp]
        fmul
        fistp qword [rsp]

        fild qword [rsp]
        fild qword [math.res]
        fdiv
        fstp qword [rsp]
        
        mov rax, qword [rsp]

        mov rsp, rbp
        pop rbp

        ret 16


;;endfunc
math.sumq:
        ; math.sumq(array[qword int], len) -> int
        push rbp
        mov rbp, rsp
        push rcx
        push rsi

        mov rax,        0
        mov rcx,        qword [rbp+24]
        mov rsi,        qword [rbp+16]
        
        .loop:
        add             rax ,  qword [rsi]
        add             rsi ,  8
        dec             rcx
        cmp rcx ,  0
        jg .loop

        pop rsi
        pop rcx
        mov rsp, rbp
        pop rbp
        ret 8*2

;;endfunc
sumd:
        ; math.sumd(array[dword int], len) -> int
        push rbp
        mov rbp, rsp
        push rcx
        push rsi

        mov eax,        0
        mov rcx,        qword [rbp+24]
        mov rsi,        qword [rbp+16]

        .loop:
        add             eax ,  dword [rsi]
        add             rsi ,  4
        dec             rcx
        cmp rcx ,  0
        jg .loop

        pop rsi
        pop rcx
        mov rsp, rbp
        pop rbp
        ret 8*2

;;endfunc
math.avgq:
        ; math.avgq(array[qword int], len) -> qword float
        push rbp
        mov rbp, rsp
        push rcx
        push rsi

        mov rax,        0
        mov rcx,        qword [rbp+24]
        mov rsi,        qword [rbp+16]

        .loop:
        add             rax ,  qword [rsi]
        add             rsi ,  8
        dec             rcx
        cmp rcx ,  0
        jg .loop

        mov rcx,        qword [rbp+24]
        mov qword [__used_for_nums],    rax 
        fild qword [__used_for_nums]
        mov qword [__used_for_nums],  rcx
        fild qword [__used_for_nums]
        fdiv
        fstp qword [__used_for_nums]
        mov     rax , qword [__used_for_nums]
        
        pop rsi
        pop rcx
        mov rsp, rbp
        pop rbp
        ret 8*2

;;endfunc
avgd:
        ; math.avgd(array[dword int], len) -> dword float
        push rbp
        mov rbp, rsp
        push rcx
        push rsi

        mov rax,        0
        mov rcx,        qword [rbp+24]
        mov rsi,        qword [rbp+16]

        .loop:
        add             eax ,  dword [rsi]
        add             rsi ,  4
        dec             rcx
        cmp rcx ,  0
        jg .loop

        mov rcx,        qword [rbp+24]
        mov qword [__used_for_nums],    rax 
        fild qword [__used_for_nums]
        mov dword [__used_for_nums],  ecx
        fild dword [__used_for_nums]
        fdiv
        fstp qword [__used_for_nums]
        mov     rax , qword [__used_for_nums]
        
        pop rsi
        pop rcx
        mov rsp, rbp
        pop rbp
        ret 8*2
