; examples:
;     stringf.len           -> NumToStr.lnasm
;     stringf.NumToStr      -> NumToStr.lnasm
;     stringf.T_convert     -> time_convert.lnasm
;     stringf.FloatToString -> stringf_float.lnasm
;     stringf.StringToFloat -> stringf_float.lnasm

section .text

stringf.len:
      ; stringf.len(QWORD PTR (string) addr) -> QWORD (integer) len
      push rbx
      mov rbx, [rsp+16]
      mov  rax, rbx

stringf.lp:
        
        cmp byte [rax], 0
        jz  stringf.lpend
        
        inc rax
        
        jmp stringf.lp

stringf.lpend:
      
      sub rax, rbx
      pop rbx
      ret 8

;;endfunc

stringf.StrToNum:
      ;stringf.StrToNum(QWORD PTR (string) str, QWORD (int) length) -> QWORD (int) num

      push rdx
      push rsi
      push rcx

      mov rdx, [rsp+32] ; our string
      mov rsi, [rsp+40]
      xor rax, rax ; zero a "result so far"

      cmp byte [rdx], "-"
      jne .c

      inc rdx
      dec rsi
      
      .c:

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
      mov rdx, [rsp+32]
      
      cmp byte [rdx], "-"
      jne .ret
      neg rax

      .ret:
      pop rcx
      pop rsi
      pop rdx
      ret 16

;;endfunc

    section .data
    stringf.counter db 0
    stringf.length db 0
    stringf.string dq 0

    section .text



stringf.NumToStr:
      ;stringf.NumToStr(QWORD (int) number, QWORD PTR (string) string) -> QWORD (int) result
      ;write value in QWORD PTR string

      push rax
      push rbx
      push rcx
      push rdx
      push rdi
      mov rax, qword [rsp+48] ; QWORD (int) number
      mov rbx, qword [rsp+56] ; QWORD PTR (str) String
      mov rcx, 0x7fffffffffffffff
      cmp rax, rcx
      jl .c
      neg rax
      mov byte [rbx], "-"
      inc rbx
      
      .c:
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
    pop rdi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret 16

;;endfunc

stringf.compare:
            ; array.compare(QWORD PTR (string) addr1, QWORD PTR (string) addr2, QWORD (integer) length) -> QWORD (integer) [0,1]
        push rdx
        push rcx
        push rsi
        push rdi
        mov rdx, 0
        mov rcx, [rsp+56]
        mov rsi, [rsp+48]
        mov rdi, [rsp+40]
            
            cld

            repe cmpsb
        je .true   

.false:
    mov rax, 0
    pop rdx
    pop rcx
    pop rsi
    pop rdi
    ret 24

.true:
    mov rax, 1
    pop rdx
    pop rcx
    pop rsi
    pop rdi
    ret 24

;;endfunc

stringf.reset:
      ;stringf.reset(QWORD PTR (string) str, QWORD PTR (int) length)
      push rsi
      push rcx
      mov rsi, [rsp+24]
      mov rcx, [rsp+32]

      .loop:
            mov byte [rsi], 0
            dec rcx

            cmp rcx, 0
            je .end
            inc rsi
            jmp .loop

      .end:
      pop rcx
      pop rsi
      ret 16

;;endfunc

section .data
      stringf.T_STRUCT_str1: TIMES 21 db 0

      stringf.time.res1: dq 0
      stringf.time.res2: dq 0

section .text

stringf.T_convert:
      ; stringf.T_convert(QWORD PTR (array: [qword s, qword ns]) T_STRUCT, QWORD PTR (string) string)
      push rsi
      push rdi
      push rax
      push rbx
      push rcx
      push rdx
      push rbp
      mov rbp, rsp

      mov rsi, [rbp+64] ; T_STRUCT
      mov rdi, [rbp+72] ; string
      mov rax, [rsi] ; seconds
      mov rbx, [rsi+8] ; nanoseconds

      push rdi
      push rax
      call stringf.NumToStr
      ;stringf.NumToStr(rax, rdi)
      
      mov rdi, [rbp+72] ; string
      push rdi
      call stringf.len
      ;stringf.len(rdi)
      mov [stringf.time.res1], rax ;saving length of seconds

      mov rdx, [rbp+72]
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

      mov rsi, [rbp+64] ; T_STRUCT
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
      pop rdx
      pop rcx
      pop rbx
      pop rax
      pop rdi
      pop rsi
      ret 16

;;endfunc

stringf.split:
      ; stringf.split(QWORD PTR (string) string, QWORD (int) len, QWORD (int) character) -> QWORD (int) index
      push rbx
      push rcx
      push rdx
      push rdi

      mov rbx, [rsp+40]
      mov rcx, [rsp+48]
      mov rdx, [rsp+56]
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
            pop rdi
            pop rdx
            pop rcx
            pop rbx
            ret 24

      .end:
            mov rax, -1
            pop rdi
            pop rdx
            pop rcx
            pop rbx
            ret 24

;;endfunc

stringf.copyto:
      ; stringf.copyto(QWORD PTR (string) str1, QWORD PTR (string) str2, QWORD (int) length)
      push rsi
      push rdi
      push rcx
      mov rsi, [rsp+32]
      mov rdi, [rsp+40]
      mov rcx, [rsp+48]
      cld
      rep movsb
      pop rcx
      pop rdi
      pop rsi
      ret 24

;;endfunc

stringf.replace:
      ; stringf.replace(QWORD PTR (string) str, QWORD (byte) char_to_replace, QWORD (byte) replace_with_char, QWORD (int) len)
      push rsi
      push rdx
      push rbx
      push rcx

      mov rsi, [rsp+40]
      mov rdx, [rsp+48]
      mov rbx, [rsp+56]
      mov rcx, [rsp+64]

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
            pop rcx
            pop rbx
            pop rdx
            pop rsi
            ret 32

;;endfunc

section .data
      stringf._1012 dq 1000000000000
      stringf._res  dq 0
      stringf._res2 dq 0
      stringf._res3 dq 0

section .text

stringf.FloatToString:
      ; stringf.FloatToString(QWORD (float) num, QWORD PTR (string) str) -> QWORD (int) length

      ;(x*?).(x*12)

      ;18446744073709551615
      push rbx
      push rdx
      push rdi

      mov rdi, [rsp+40]

      fld qword [rsp+32]
      fild qword [stringf._1012]
      fmul
      fistp qword [stringf._res]
      mov rax, qword [stringf._res]
      mov rbx, qword [stringf._1012]
      mov rdx, 0
      div rbx
      ;rax::rdx
      mov qword [stringf._res], rdx

      push rbp
      mov rbp, rsp

      push rdi
      push rax
      call stringf.NumToStr

      mov byte [rdi], "."
      inc rdi

      mov rax, qword [stringf._res]

      cmp rax, 0
      je .continue

      .loop:

            mov rbx, 10
            mul rbx

            cmp rax, qword [stringf._1012]
            jge .continue
            mov byte [rdi], "0"
            inc rdi

            jmp .loop

      .continue:

      push rdi
      push qword [stringf._res]
      call stringf.NumToStr

      sub rdi, [rbp+48]
      mov rax, rdi

      mov rsp, rbp
      pop rbp
      pop rdi
      pop rdx
      pop rbx
      ret 16

;;endfunc

stringf.StringToFloat:
      ; stringf.StringToFloat(QWORD PTR (string) addr, QWORD (int) length) -> QWORD (float) num
      push rdi
      push rcx
      push rbx
      mov rdi, [rsp+32]
      mov rcx, [rsp+40]

      push rbp
      mov rbp, rsp

      push rcx
      push qword [rbp+40]
      call stringf.StrToNum

      mov qword [stringf._res],  rdi
      ;         "***.***"
      ; addr+rdi =  ^

      mov qword [stringf._res2], rax

      mov rax, [stringf._res]
      inc rax

      mov rdi, [rbp+40]
      sub rcx, qword [stringf._res]
      add rdi, qword [stringf._res]
      push rcx
      push rdi
      call stringf.StrToNum
      


      mov qword [stringf._res3], rax
      fild qword [stringf._res3]

      mov rax, [stringf._res]
      inc rax
      mov rcx, [rbp+48]
      sub rcx, rax

      push rcx
      push 10
      call stringf.math.ipower
      mov qword [stringf._res3], rax
      fild qword [stringf._res3]
      fdiv

      fild qword [stringf._res2]
      fadd
      fstp qword [stringf._res]

      mov rsp, rbp
      pop rbp
      pop rbx
      pop rcx
      pop rdi
      mov rax, qword [stringf._res]

      ret 16


      stringf.math.ipower:
        mov rax, [rsp+8]
        mov rcx, [rsp+16]

        cmp rcx, 1
        je stringf.math.ipower.end

        cmp rcx, 0
        je stringf.math.ipower.p0

        mov rbx, rax

        stringf.math.ipower.loop:
                dec rcx
                cmp rcx, 0
                je stringf.math.ipower.end
                mul rbx
                jmp stringf.math.ipower.loop


        stringf.math.ipower.p0:
                mov rax, 1
                ret

        stringf.math.ipower.end:
                ret 16

