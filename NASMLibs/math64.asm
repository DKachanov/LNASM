; examples:
;     math.factorial -> factorial.lnasm
;     math.ipower    -> ipower.lnasm 

section .data
        math.piOn180 dq __float64__(0.017453292519943295)

;;required

section .text

math.factorial:
        ; math.factorial(QWORD (int) number) -> QWORD (int) value
        push  rbx
        push  rbp
        mov  rbp,rsp

        mov  rax, [rbp+24]
        
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
        ;math.sqrt(QWORD (float) value) -> QWORD (float) value
        fld qword [rsp+8]
        fsqrt
        fstp qword [rsp+8]
        mov rax, [rsp+8]
        ret 8

;;endfunc

math.radians:
        ; math.radians(QWORD (float) angle) -> QWORD (float) radians
        fld qword [math.piOn180]
        fmul qword [rsp+8]
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.sin:
        ; math.sin(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fsin
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.cos:
        ; math.cos(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fcos
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc

math.tan:
        ; math.tan(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fptan
        fstp qword [rsp+8]
        mov rax, qword [rsp+8]
        ret 8

;;endfunc
math.ctg:
        ; math.ctg(QWORD (float) radians) -> QWORD (float) value
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
        ; math.log(QWORD (float) base, QWORD (float) num) -> QWORD (float) result
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
        ; math.round(QWORD (float) num, QWORD (int) after_dot) -> QWORD (float) result

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