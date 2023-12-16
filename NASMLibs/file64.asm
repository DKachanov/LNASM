; examples:
;     file.open  -> file_write.lnasm, file_read.lnasm
;     file.close -> file_write.lnasm, file_read.lnasm
;     file.write -> file_write.lnasm
;     file.read  -> file_read.lnasm


section .text


file.open:
	; file.open(QWORD PTR (string) filename, QWORD (int) mode)
    push rax
    push rdi
    push rsi
    push rdx

	mov rax, 2

	mov rdi, [rsp+40]
	mov rsi, 102o
	mov rdx, [rsp+48]

	syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
	ret 16

file.close:
	; file.close(QWORD (fd) fd)
    push rax
    push rdi
	mov rax, 3

	mov rdi, [rsp+24]

	syscall
    pop rdx
    pop rax
	ret 8

file.write:
    ; file.write(QWORD (fd) fd, QWORD PTR (string) addr, QWORD length)
    push rax
    push rdi
    push rsi
    push rdx

    mov rax, 1
    mov rdi, qword [rsp+40]
    mov rsi, qword [rsp+48]
    mov rdx, qword [rsp+56]
    
    syscall

    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24

file.read:
    ; file.read(QWORD (fd) fd, QWORD PTR addr, QWORD len)
    push rax
    push rdi
    push rsi
    push rdx

    mov rax, 0
    mov rdi, qword [rsp+40]
    mov rsi, qword [rsp+48]
    mov rdx, qword [rsp+56]

    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24


file.stat:
    ;file.stat(QWORD PTR (string) filename, QWORD PTR (array) statbuf)
    push rax
    push rdi
    push rsi
    mov rax, 4
    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    syscall
    pop rsi
    pop rdi
    pop rax
    ret 16