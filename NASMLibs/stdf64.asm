; examples:
;     stdf.exit         -> *.lnasm
;     stdf.allocate_mem -> allocate_memory.lnasm
;     stdf.signal       -> compiled/web/server.lnasm

section .text

stdf.exit:
	;stdf.exit(QWORD (integer) code)
	
	mov rax, 60
	mov rbx, [rsp+8]
	
	syscall

;;endfunc

stdf.exec:
	;stdf.exec(QWORD PTR (string) filename, QWORD PTR (QWORD array) args, QWORD PTR (QWORD array) envp, QWORD (int))

    push rdx
    push rsi
    push rdi

    mov rax, 56
    syscall
    cmp rax, 0
    jnz .parent

	mov rax, 59
	mov rdi, [rsp+32]
	mov rsi, [rsp+40]
	mov rdx, [rsp+48]
	syscall

	.parent:
	push 0
	mov rdi, rsp
	mov rdx, 0
	pop rax
	syscall
    pop rdx
    pop rsi
    pop rdi
	

	ret 16

;;endfunc

stdf.allocate_mem:
	;stdf.allocate_mem(QWORD (int) size) -> QWORD PTR (int) pointer
	;    errors -> rbx

	push rdi

	mov rax, 12
	mov rdi, 0
	syscall

	add rax, [rsp+16]
	mov rdi, rax
	mov rax, 12
	syscall
	
	cmp rax, 0
	je .error
	mov rbx, 0

	pop rdi

	ret 8

	.error:
		mov rbx, 1
		pop rdi
		ret 8

;;endfunc

stdf.signal:
	; stdf.signal(QWORD (int) signal, QWORD (addr) function) -> QWORD (int) error

	push rbp
	mov rbp, rsp
	
	push rdi
	push rsi
	push rdx
	push r10

	mov rax, 13
	mov rdi, [rbp+16]

	push 0
	push stdf.signal.restorer
	push 0x04000000
	push qword [rbp+24]
	mov rsi, rsp
	
	mov rdx, 0
	mov r10, 8
	syscall

	pop r10
	pop rdx
	pop rsi
	pop rdi

	mov rsp, rbp
	pop rbp
	ret 16

;    .sa_handler  = [rbp+24]
;    .sa_flags    = 0x04000000
;    .sa_restorer = stdf.signal.restorer
;    .sa_mask     = 0

stdf.signal.restorer:
	mov rax, 15
	syscall
	ret