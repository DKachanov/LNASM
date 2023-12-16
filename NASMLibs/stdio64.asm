; examples:
;    stdio.print -> almost all *.lnasm (print.lnasm) 
;    stdio.input -> add_to_input_char.lnasm

section .text

stdio.print:
    ; stdio.print(QWORD PTR (string) addr, QWORD (int) len)
    push rax
    push rdi
    push rsi
    push rdx

    mov rax, 1
    mov rdi, 1
    mov rsi, qword [rsp+40]
    mov rdx, qword [rsp+48]
    syscall
    
    pop rdx
    pop rsi
    pop rdi
    pop rax

    ret 16

;;endfunc

stdio.input:
    ; stdio.input(QWORD PTR (string) addr, QWORD (int) len) -> QWORD (int) length

    push rdi
    push rsi
    push rdx
    
    mov rax, 0
    mov rdi, 1
    mov rsi, qword [rsp+32]
    mov rdx, qword [rsp+40]
    syscall

    pop rdx
    pop rsi
    pop rdi

    ret 16