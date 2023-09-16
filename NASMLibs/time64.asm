; compare
;     time.sleep -> sleep.lnasm, time_convert.lnasm
;     time.time  -> sleep.lnasm, time_convert.lnasm
;     time.sub   -> time_convert.lnasm

section .text

	time.sleep:
	;time.sleep(QWORD (int) seconds, QWORD (int) nanoseconds)
	mov rax, 35
	mov rdi, rsp
	add rdi, 8
	xor rsi, rsi
	syscall
	ret

	time.time:
		;time.time(QWORD PTR (array: [QWORD s, QWORD ns]) addr)
		;228

		mov rax, 228
		xor rdi, rdi
		mov rsi, [rsp+8]
		syscall
		ret

	time.sub:
		;time.sub(QWORD PTR (array: [QWORD s, QWORD ns]) T_struct1, QWORD PTR (array: [QWORD s, QWORD ns]), T_struct2)
		mov rsi, [rsp+8]
		mov rdi, [rsp+16]

		mov rax, [rsi]
		mov rbx, [rdi]
		sub rax, rbx

		mov [rsi], rax

		mov rax, [rsi+8]
		mov rbx, [rdi+8]
		sub rax, rbx
		cmp rax, 0
		jl .less ; if result less then 0 

		mov [rsi+8], rax

		.end:
		ret

		.less: ; we converting it to unsigned 
		add rax, 1000000000
		mov [rsi+8], rax
		sub qword [rsi], 1
		jmp .end

