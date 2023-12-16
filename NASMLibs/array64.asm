section .text

; examples:
;     array.reverse -> reverse.lnasm
;     array.get     -> array_get.lnasm
;     array.in      -> array_in.lnasm
;     array.copyto  -> matrix.lnasm
;     array.bubble_sort    -> sort.lnasm
;	  array.qsort   -> qsort.lnasm

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

	push rsi
	push rcx
	push rdx
	push rbx

	mov rsi, [rsp+40] ; PTR array
	mov rcx, [rsp+48];length
	mov rdx, rcx; saving it
	mov rbx, [rsp+56];size
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
	pop rbx
	pop rdx
	pop rcx
	pop rsi

	ret 24

	.error:
	mov rax, 1
	pop rbx
	pop rdx
	pop rcx
	pop rsi
	ret 24


array.in:
	; array.in(QWORD PTR (array) addr, QWORD (int) type, QWORD (int) len, QWORD PTR (value) smth)
	; errors -> rbx
	push rsi
	push rdx
	push rcx
	push rbx

	mov rsi, [rsp+40]  ; addr
	mov rdx, [rsp+48] ; type
	mov rcx, [rsp+56] ; len
	mov rbx, [rsp+64] ; smth


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
		jmp .ret

	.false:
		mov rbx, 0
		mov rax, 0
		jmp .ret


	.error:
		mov rbx, -1
		jmp .ret

	.ret:
	pop rbx
	pop rcx
	pop rdx
	pop rsi
	ret 32

array.copyto:
	; array.copyto(QWORD PTR (array) array1, QWORD PTR (array) array2, QWORD (int) type, QWORD (int) length)
	; errors -> rbx

	push rsi
	push rdi
	push rdx
	push rcx
	push rbx

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
    	jmp .ret
    .word:
    	cld
    	rep movsw
    	jmp .ret
    .dword:
    	cld
    	rep movsd
    	jmp .ret
    .qword:
    	cld
    	rep movsq
    	jmp .ret

	.error:
		mov rbx, 1
	
	.ret:
	pop rbx
	pop rcx
	pop rdx
	pop rdi
	pop rsi
	ret 32

;;endfunc

array.bubble_sort:
	; array.bubble_sort(QWORD PTR (int array) input, QWORD (int) len, QWORD (int) type)
	; type error -> rbx (-1)

	push rsi
	push rdx
	push r9
	push rdi
	push rcx
	push rax
	push rbx

	mov rsi, [rsp+64]
	mov rdx, [rsp+72]
	mov r9, rsi
	mov rdi, rdx
	mov rcx, 0

	mov rax, [rsp+80]

	push rbp
	mov rbp, rsp
	
	cmp rax, 0
	push .loopb
	je .loopb

	cmp rax, 1
	push .loopw
	je .loopw

	cmp rax, 2
	push .loopd
	je .loopd

	cmp rax, 3
	push .loopq
	je .loopq
	jmp .terror

	;byte

	.loopb:
		mov al, [rsi]
		mov bl, [rsi+1]
		cmp al, bl
		jg .swapb
		.continueb:
		inc rsi
		dec rdx
		cmp rdx, 1
		je .end
		jmp .loopb

	.swapb:
		mov rcx, 1
		mov [rsi], bl
		mov [rsi+1], al
		jmp .continueb

	;word

	.loopw:
		mov ax, [rsi]
		mov bx, [rsi+2]
		cmp ax, bx
		jg .swapw
		.continuew:
		add rsi, 2
		dec rdx
		cmp rdx, 1
		je .end
		jmp .loopw

	.swapw:
		mov rcx, 1
		mov [rsi], bx
		mov [rsi+2], ax
		jmp .continuew

	;dword

	.loopd:
		mov eax, [rsi]
		mov ebx, [rsi+4]
		cmp eax, ebx
		jg .swapd
		.continued:
		add rsi, 4
		dec rdx
		cmp rdx, 1
		je .end
		jmp .loopd

	.swapd:
		mov rcx, 1
		mov [rsi], ebx
		mov [rsi+4], eax
		jmp .continued

	;qword

	.loopq:
		mov rax, [rsi]
		mov rbx, [rsi+8]
		cmp rax, rbx
		jg .swapq
		.continueq:
		add rsi, 8
		dec rdx
		cmp rdx, 1
		je .end
		jmp .loopq


	.swapq:
		mov rcx, 1
		mov [rsi], rbx
		mov [rsi+8], rax
		jmp .continueq

	.end:
		cmp rcx, 0
		je .ret
		mov rsi, r9
		mov rdx, rdi
		mov rcx, 0
		jmp qword [rsp]
	.ret:

		mov rsp, rbp
		pop rbp
		pop rbx
		pop rax
		pop rcx
		pop rdi
		pop r9
		pop rdx
		pop rsi
		ret 24

	.terror:
		mov rbx, -1
		mov rsp, rbp
		pop rbp
		pop rbx
		pop rax
		pop rcx
		pop rdi
		pop r9
		pop rdx
		pop rsi
		ret 24

section .data
    array_ptr      dq 0
    outer_boundary dq 0  ; boundary for the outer loop
    inner_boundary dq 0  ; boundary for the inner loop

section .text

array.qsort:
	push rax
	push rbx
	push rsi
	push rdi
	push rdx
	push r8
	push r9
	push r10
	push r11
	;array.qsort(QWORD (array) array, QWORD (int) length)
   	mov rsi, [rsp+80]
   	mov rdx, [rsp+88] 
    mov [array_ptr],  rsi			; Save the pointer
    
    ;; for (i < size - 1)
    mov [outer_boundary], rdx			; Save and set the value of outer loop's bounds
    sub qword [outer_boundary], 8

    ;; for (j < size)
    mov [inner_boundary], rdx			; Save and set the value of inner loop's bounds

    ;; r8 will be used as 'i'
    xor r8, r8 
    .outer_loop:
        mov rsi, [array_ptr]			; Bring the array into RSI
        add rsi, r8      			; Take the pointer to the element to be processed
        mov rdx, rsi				; RDX will be used as the pointer to the smallest element in the array
        
        ;; r9 will be used as 'j'
        mov r9, r8
        add r9, 8			; Bring R9 to one element ahead of the R8
        
        ;; rdi is pointer at 'j'
        .inner_loop:
            mov rdi, [array_ptr]
            add rdi, r9     			; (array + j) - a pointer

            mov rax, [rdi]  			; array[j] - the element
            mov rbx, [rdx]  			; array[rdx] - the current minimum element

            cmp rax, rbx
            jl .if_less
            jmp .cont
            
            .if_less:
               mov rdx, rdi			; Change the minimum pointer in RDX to the newly found smaller element
            .cont:
                add r9, 8		; Take the R9 (j) to the next element
                cmp r9, [inner_boundary]
        jl .inner_loop

        ;; Swap the values
        mov r10, [rsi]				; RSI is pointing to the array[i]
        mov r11, [rdx]				; RDX is pointing to the smallest element in the array that's left
        
        mov [rsi], r11
        mov [rdx], r10

        add r8, 8
        cmp r8, [outer_boundary]
    jl .outer_loop
   	pop r11
   	pop r10
   	pop r9
   	pop r8
   	pop rdx
   	pop rdi
   	pop rsi
   	pop rbx
   	pop rax

ret 16