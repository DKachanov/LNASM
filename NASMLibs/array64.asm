; examples:
;     array.reverse -> reverse.lnasm
;     array.get     -> array_get.lnasm
;     array.in      -> array_in.lnasm
;     array.copyto  -> matrix.lnasm

array.reverse:
	; array.reverse(QWORD PTR (array) array, QWORD (int) length, QWORD (int) type) -> QWORD (int) error
	; type:
	;	0 - byte
	;	1 - word
	;	2 - dword
	;	3 - qword
	; error:
	;	1 = type error
	;

	mov rsi, [rsp+8] ; PTR array
	mov rcx, [rsp+16];length
	mov rdx, rcx; saving it
	mov rbx, [rsp+24];size
	xor rax, rax

	cmp rbx, 0
	jz ._byte
	
	cmp rbx, 1
	jz ._word
	
	cmp rbx, 2
	jz ._dword

	cmp rbx, 3
	jz ._qword

	jmp .error



	._byte:
	cmp rcx, 0
	jz ._rbyte

	mov al, byte [rsi+rcx-1]
	push rax

	dec rcx
	
	jmp ._byte

	._word:
	cmp rcx, 0
	jz ._rword

	mov ax, word [rsi+rcx*2-2]
	push rax

	dec rcx
	
	jmp ._word


	._dword:
	cmp rcx, 0
	jz ._rdword

	mov eax, dword [rsi+rcx*4-4]
	push rax

	dec rcx
	
	jmp ._dword


	._qword:
	cmp rcx, 0
	jz ._rword

	mov rax, qword [rsi+rcx*8-8]
	push rax

	dec rcx
	
	jmp ._qword

	._rbyte:
		pop rax
		mov byte [rsi+rdx-1], al
		dec rdx
		cmp rdx, 0
		je .end
		jmp ._rbyte



	._rword:
		pop rax
		mov word [rsi+rdx*2-2], ax
		dec rdx
		cmp rdx, 0
		je .end
		jmp ._rword


	._rdword:
		pop rax
		mov dword [rsi+rdx*4-4], eax
		dec rdx
		cmp rdx, 0
		je .end
		jmp ._rdword


	._rqword:
		pop rax
		mov qword [rsi+rdx*8-8], rax
		dec rdx
		cmp rdx, 0
		je .end
		jmp ._rqword



	.end:
	ret

	.error:
	mov rax, 1
	ret


array.get:
	; array.get(QWORD PTR (array) addr, QWORD (int) type, QWORD (int) index) -> value
	; errors -> rbx

	mov rsi, [rsp+8]
	mov rdx, [rsp+16]
	mov rcx, [rsp+24]
	mov rbx, 0
	mov rax, 0

	cmp rdx, 0
	jz .byte
	
	cmp rdx, 1
	jz .word
	
	cmp rdx, 2
	jz .dword

	cmp rdx, 3
	jz .qword

	jmp .error

	.byte:
		mov al, [rsi+rcx]
		ret

	.word:
		mov ax, [rsi+rcx*2]
		ret

	.dword:
		mov eax, [rsi+rcx*4]
		ret

	.qword:
		mov rax, [rsi+rcx*8]
		ret

	.error:
		mov rbx, 1

array.in:
	; array.in(QWORD PTR (array) addr, QWORD (int) type, QWORD (int) len, QWORD PTR (value) smth)
	; errors -> rbx

	mov rsi, [rsp+8]  ; addr
	mov rdx, [rsp+16] ; type
	mov rcx, [rsp+24] ; len
	mov rbx, [rsp+32] ; smth


	cmp rdx, 0
	je .byte
	cmp rdx, 1
	je .word
	cmp rdx, 2
	je .dword
	cmp rdx, 3
	je .qword
	jmp .error

	.byte:
		dec rcx
		mov al, [rsi+rcx]
		cmp al, bl
		je .true
		cmp rcx, 0
		je .false
		jmp .byte

	.word:
		dec rcx
		mov ax, [rsi+rcx*2]
		cmp ax, bx
		je .true
		cmp rcx, 0
		je .false
		jmp .word

	.dword:
		dec rcx
		mov eax, [rsi+rcx*4]
		cmp eax, ebx
		je .true
		cmp rcx, 0
		je .false
		jmp .dword

	.qword:
		dec rcx
		mov rax, [rsi+rcx*8]
		cmp rax, rbx
		je .true
		cmp rcx, 0
		je .false
		jmp .qword

	.true:
		mov rbx, 0
		mov rax, 1
		ret

	.false:
		mov rbx, 0
		mov rax, 0
		ret


	.error:
		mov rbx, -1
		ret


array.copyto:
	; array.copyto(QWORD PTR (array) array1, QWORD PTR (array) array2, QWORD (int) type, QWORD (int) length)
	; errors -> rbx

	mov rsi, [rsp+8]
	mov rdi, [rsp+16]
	mov rdx, [rsp+24]
	mov rcx, [rsp+32]
	mov rbx, 0

	cmp rdx, 0
	je .byte
	cmp rdx, 1
	je .word
	cmp rdx, 2
	je .dword
	cmp rdx, 3
	je .qword
	jmp .error

	.byte:
		cld
    	rep movsb
    	ret
    .word:
    	cld
    	rep movsw
    	ret
    .dword:
    	cld
    	rep movsd
    	ret
    .qword:
    	cld
    	rep movsq
    	ret

	.error:
		mov rbx, 1
		ret