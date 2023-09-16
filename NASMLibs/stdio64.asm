; examples:
;    stdio.print -> almost all *.lnasm (print.lnasm) 
;    stdio.input -> add_to_input_char.lnasm

section .text

stdio.print:
    ; stdio.print(QWORD PTR (string) addr, QWORD (int) len)
    
    mov rax, 1
    mov rdi, 1
    mov rsi, qword [rsp+8]
    mov rdx, qword [rsp+16]
    
    syscall
    ret

stdio.input:
    ; stdio.input(QWORD PTR (string) addr, QWORD (int) len)
    
    mov rax, 0
    mov rdi, 1
    mov rsi, qword [rsp+8]
    mov rdx, qword [rsp+16]

    syscall
    ret
