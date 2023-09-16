; examples:
;     file.open  -> file_write.lnasm, file_read.lnasm
;     file.close -> file_write.lnasm, file_read.lnasm
;     file.write -> file_write.lnasm
;     file.read  -> file_read.lnasm


section .text


file.open:
	; file.open(QWORD PTR (string) filename, QWORD (int) mode)

	mov rax, 2

	mov rdi, [rsp+8]
	mov rsi, 102o
	mov rdx, [rsp+16]

	syscall
	ret

file.close:
	; file.close(QWORD (fd) fd)
	mov rax, 3

	mov rdi, [rsp+8]

	syscall
	ret

file.write:
    ; file.write(QWORD (fd) fd, QWORD PTR (string) addr, QWORD length)
    
    lea rdx, 0

    mov rax, 1
    mov rdi, qword [rsp+8]
    mov rsi, qword [rsp+16]
    mov rdx, qword [rsp+24]
    
    syscall
    ret

file.read:
    ; file.read(QWORD (fd) fd, QWORD PTR addr, QWORD len)
    
    lea rdx, 0

    mov rax, 0
    mov rdi, qword [rsp+8]
    mov rsi, qword [rsp+16]
    mov rdx, qword [rsp+24]

    syscall
    ret


file.stat:
    ;file.stat(QWORD PTR (string) filename, QWORD PTR (array) statbuf)

    mov rax, 4
    mov rdi, [rsp+8]
    mov rsi, [rsp+16]
    syscall
    ret