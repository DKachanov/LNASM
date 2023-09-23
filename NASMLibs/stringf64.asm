; examples:
;     stringf.len       -> NumToStr.lnasm
;     stringf.NumToStr  -> NumToStr.lnasm
;     stringf.T_convert -> time_convert.lnasm

section .text

stringf.len:
      ; stringf.len(QWORD PTR (string) addr) -> QWORD (integer) len
      
      mov rbx, [rsp+8]
      mov  rax, rbx

stringf.lp:
        
        cmp byte [rax], 0
        jz  stringf.lpend
        
        inc rax
        
        jmp stringf.lp

stringf.lpend:
      
      sub rax, rbx
      
      ret

stringf.StrToNum:
      ;stringf.StrToNum(QWORD PTR (string) str, QWORD (int) length)

      mov rdx, [rsp+8] ; our string
      mov rsi, [rsp+16]
      xor rax, rax ; zero a "result so far"
      .top:
      movzx rcx, byte [rdx] ; get a character

      inc rdx ; ready for next one

      cmp rcx, '0' ; valid?
      jb .done
      cmp rcx, '9'
      ja .done

      sub rcx, '0' ; "convert" character to number
      imul rax, 10 ; multiply "result so far" by ten
      add rax, rcx ; add in current digit

      dec rsi
      cmp rsi, 0
      jz .done

      jmp .top ; until done
      .done:
      ret

    section .data
    stringf.counter db 0
    stringf.length db 0
    stringf.string dq 0

    section .text

stringf.NumToStr:
      ;stringf.NumToStr(QWORD (int) number, QWORD PTR (string) string) -> QWORD (int) result
      ;write value in QWORD PTR string

      mov rax, qword [rsp+8] ; QWORD (int) number
      mov rbx, qword [rsp+16] ; QWORD PTR (str) String
      mov [stringf.string], rbx
      mov byte [stringf.counter], 0
      mov rcx, 10

      .loop:

      xor rdx, rdx
      inc byte [stringf.counter]

      div rcx
      push rdx

      test rax, rax
      je .end
      jmp .loop


.end:
      mov al, byte [stringf.counter]
      mov byte [stringf.length], al

      mov cl, al

      mov rdi, [stringf.string]
      .loop2:
            pop rbx
            add bl, 30h
            mov byte [rdi], bl

            dec cl
            inc rdi

            cmp cl, 0
            je .ret
            jmp .loop2

.ret:
    mov qword [stringf.string], 0
    mov qword [stringf.length], 0
    mov qword [stringf.counter], 0
    ret

section .text

stringf.compare:
            ; array.compare(QWORD PTR (string) addr1, QWORD PTR (string) addr2, QWORD (integer) length) -> QWORD (integer) [0,1]
        
        mov rdx, 0
        mov rcx, [rsp+24]
        mov rsi, [rsp+16]
        mov rdi, [rsp+8]
            
            cld

            repe cmpsb
        je .true   

.false:
    mov rax, 0
    
    ret

.true:
    mov rax, 1
    
    ret

stringf.reset:
      ;stringf.reset(QWORD PTR (string) str, QWORD PTR (int) length)
      mov rsi, [rsp+8]
      mov rcx, [rsp+16]

      .loop:
            mov byte [rsi], 0
            dec rcx

            cmp rcx, 0
            je .end
            inc rsi
            jmp .loop

      .end:
      ret

section .data
      stringf.T_STRUCT_str1: TIMES 21 db 0

      stringf.time.res1: dq 0
      stringf.time.res2: dq 0

section .text

stringf.T_convert:
      ; stringf.T_convert(QWORD PTR (array: [qword s, qword ns]) T_STRUCT, QWORD PTR (string) string)
      
      push rbp
      mov rbp, rsp

      mov rsi, [rbp+16] ; T_STRUCT
      mov rdi, [rbp+24] ; string
      mov rax, [rsi] ; seconds
      mov rbx, [rsi+8] ; nanoseconds

      push rdi
      push rax
      call stringf.NumToStr
      ;stringf.NumToStr(rax, rdi)
      
      mov rdi, [rbp+24] ; string
      push rdi
      call stringf.len
      ;stringf.len(rdi)
      mov [stringf.time.res1], rax ;saving length of seconds

      mov rdx, [rbp+24]
      add rdx, rax
      mov byte [rdx], "." ; putting dot after seconds
      mov [stringf.time.res1], rdx ; saving PTR after seconds & dot

      mov rcx, 8 ; 9 zeros

      .fill: ;filling string after dot with 9 zeros
            inc rdx
            dec rcx

            mov byte [rdx], "0"

            cmp rcx, 0
            je .fill.end
            jmp .fill
      .fill.end:

      mov rsi, [rbp+16] ; T_STRUCT
      mov rbx, [rsi+8] ; nanoseconds

      push stringf.T_STRUCT_str1
      push rbx
      call stringf.NumToStr ; filling stringf.T_STRUCT_str1 with str nanoseconds

      push stringf.T_STRUCT_str1
      call stringf.len
      ; rax - length

      mov rsi, stringf.T_STRUCT_str1
      mov rdi, [stringf.time.res1] ; putting ptr to rcx
      add rdi, 10
      sub rdi, rax
      mov rcx, 0 ; setting counter 0

      .fill2:


            mov bl, byte [rsi]
            mov byte [rdi], bl

            inc rsi
            inc rdi
            inc rcx

            cmp rcx, rax
            je .fill2.end
            jmp .fill2
      .fill2.end:


      mov rsp, rbp
      pop rbp
      ret

stringf.split:
      ; stringf.split(QWORD PTR (string) string, QWORD (int) len, QWORD (int) character) -> QWORD (int) index

      mov rbx, [rsp+8]
      mov rcx, [rsp+16]
      mov rdx, [rsp+24]
      mov rdi, 0

      .loop:
            mov al, [rbx+rdi]
            
            cmp al, dl
            je .splited

            inc rdi
            
            cmp rcx, rdi
            je .end
            
            jmp .loop

      .splited:
            mov rax, rdi
            ret

      .end:
            mov rax, -1
            ret

stringf.copyto:
      ; stringf.copyto(QWORD PTR (string) str1, QWORD PTR (string) str2, QWORD (int) length)

      mov rsi, [rsp+8]
      mov rdi, [rsp+16]
      mov rcx, [rsp+24]
      cld
      rep movsb
      ret

stringf.replace:
      ; stringf.replace(QWORD PTR (string) str, QWORD (byte) char_to_replace, QWORD (byte) replace_with_char, QWORD (int) len)
      mov rsi, [rsp+8]
      mov rdx, [rsp+16]
      mov rbx, [rsp+24]
      mov rcx, [rsp+32]

      .loop:
            dec rcx

            mov al, [rsi+rcx]

            cmp al, dl
            je .replace
            
            cmp rcx, 0
            je .end
            jmp .loop

      .replace:
            mov [rsi+rcx], bl
            jmp .loop

      .end:
            ret
