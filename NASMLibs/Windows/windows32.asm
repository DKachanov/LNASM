
section .data
    win32.kernel32_base dd 0
    win32.table dd 0

section .text

    win32.kernel32_dll:
    ; win32.kernel32_dll()
    ; find the kernel32.dll base address
        xor edx,edx
        mov eax, [fs: edx + 0x30]  ; EAX = PEB
        ; mov eax, fs:[edx + 0x30]  ; EAX = PEB
        mov eax, [eax + 0xc]      ; EAX = PEB->Ldr
        mov esi, [eax + 0x14]     ; ESI = PEB->Ldr.InMemoryOrderModuleList
        lodsd                     ; EAX = Second module (ntdll.dll) or like that mov eax,[esi]
        xchg eax, esi             ; EAX = ESI, ESI = EAX
        lodsd                     ; EAX = Third Module (kernel32)
        mov ebx, [eax + 0x10]     ; EBX = Base address of kernel32.dll
        mov [win32.kernel32_base], ebx
        mov eax, ebx
    ret

    win32.export_table:
    ; win32.export_table()
    ; find the export table of kernel32.dll
        mov ebx, [win32.kernel32_base]
        mov edx, [ebx + 0x3c] ; EDX = DOS->e_lfanew
        add edx, ebx          ; EDX = PE Header
        mov edx, [edx + 0x78] ; EDX = Offset export table
        add edx, ebx          ; EDX = Export table
        mov esi, [edx + 0x20] ; ESI = Offset names table
        add esi, ebx          ; ESI = Names table (address of AddressOfNames)
        xor ecx, ecx          ; ecx = 0
        mov [win32.table], esi ;table

    ret


    ; get the GetProcAddress funcation name 
    win32.get_function:
        ; win32.get_functionName(QWORD PTR (string) name, QWORD (int) length) -> QWORD PTR (function) func
        mov esi, [win32.table]
        mov edx, esi
        mov ebx, [win32.kernel32_base]
        inc ecx                              ; Increment the ordinal
        lodsd                                ; Get name offset (remember lodsd will load to eax the content of the address point by esi and add to esi 0x4)
        add eax, ebx                         ; Get function name (remember ebx contains the address of kernel32.dll)
        
        push esi
        push edi
        push ecx
        mov esi, [esp+16]
        mov ecx, [esp+20]
        mov edi, eax
        repe cmpsb
        pop ecx
        pop edi
        pop esi

        jne win32.get_functionName
        ; now eax contains the address to the string 'GetProcAddress'

        ; find the address of GetProcAddress 
        mov esi, [edx + 0x24]    ; ESI = Offset ordinals (remember edx contains the export table offset)
        add esi, ebx             ; ESI = Ordinals table (remember ebx contains the address of kernel32.dll)
        mov cx, [esi + ecx * 2]  ; CX = Number of function
        dec ecx
        mov esi, [edx + 0x1c]    ; ESI = Offset address table
        add esi, ebx             ; ESI = Address table
        mov edx, [esi + ecx * 4] ; EDX = Pointer(offset)
        add edx, ebx             ; EDX = GetProcAddress

        mov eax, edx ; esi at offset 0x4 will now hold the address of GetProcAddress

        ret