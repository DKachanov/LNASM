; examples:
;     stdf.exit         -> *.lnasm
;     stdf.allocate_mem -> allocate_memory.lnasm

section .text

stdf.exit:
	;stdf.exit(QWORD (integer) code)
	
	mov rax, 60
	mov rbx, [rsp+8]
	
	syscall

stdf.exec:
	;stdf.exec(QWORD PTR (string) filename, QWORD PTR (QWORD array) args)

	mov rax, 59
	mov rdi, [rsp+8]
	mov rsi, [rsp+16]
	mov rdx, 0
	
	syscall

	ret

stdf.allocate_mem:
	;stdf.allocate_mem(QWORD (int) size) -> QWORD PTR (int) pointer
	;    errors -> rbx

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
	ret

	.error:
		mov rbx, 1
		ret