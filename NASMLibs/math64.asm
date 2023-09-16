; examples:
;     math.factorial -> factorial.lnasm
;     math.ipower    -> ipower.lnasm 


section .data
        math.piOn180 dq __float64__(0.017453292519943295)
        math.res dq 0

section .text

math.factorial:
        ; math.factorial(QWORD (int) number) -> QWORD (int)
        push  rbp

        mov  rbp,rsp
        mov  rax, [rbp+16]
        
        cmp  rax,1
        je .end_factorial
        
        dec  rax
        
        push  rax
        
        call math.factorial
        
        mov  rbx, [rbp+16]
        imul  rax,rbx


.end_factorial: 
        mov  rsp,rbp
        pop  rbp

        ret

math.sqrt:
        ;math.sqrt(QWORD (float) value) -> QWORD (float) value
        fld qword [rsp+8]
        fsqrt
        fstp qword [math.res]
        mov rax, [math.res]
        ret

math.radians:
        ; math.radians(QWORD (float) angle) -> QWORD (float) radians
        fld qword [math.piOn180]
        fmul qword [rsp+8]
        fstp qword [math.res]
        mov rax, qword [math.res]
        ret

math.sin:
        ; math.sin(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fsin
        fstp qword [math.res]
        mov rax, qword [math.res]
        ret

math.cos:
        ; math.cos(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fcos
        fstp qword [math.res]
        mov rax, qword [math.res]
        ret

math.tan:
        ; math.tan(QWORD (float) radians) -> QWORD (float) value
        fld qword [rsp+8]
        fptan
        fstp qword [math.res]
        mov rax, qword [math.res]
        ret

math.ipower:
        ; math.ipower(QWORD (int) number, QWORD (int) power) -> QWORD (int) value
        mov rax, [rsp+8]
        mov rcx, [rsp+16]

        cmp rcx, 1
        je math.ipower.end

        cmp rcx, 0
        je math.ipower.p0

        mov rbx, rax

        math.ipower.loop:
                dec rcx
                cmp rcx, 0
                je math.ipower.end
                mul rbx
                jmp math.ipower.loop


        math.ipower.p0:
                mov rax, 1
                ret

        math.ipower.end:
                ret

