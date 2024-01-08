; examples:
;     socket.socket  -> socket.lnasm, socket_bind.lnasm, socket_connect.lnasm
;     socket.bind    -> socket_bind.lnasm
;     socket.listen  -> socket_bind.lnasm
;     socket.connect -> socket_connect.lnasm
;     socket.accept  -> socket_bind.lnasm
;     socket.close   -> socket.lnasm, socket_bind.lnasm, socket_connect.lnasm
;     socket.listen  -> socket_bind.lnasm
;     socket.sendto  -> socket.lnasm
;     socket.send    -> socket_connect.lnasm
;     socket.recv    -> socket_bind.lnasm

section .data
    socket.SOCK_STREAM equ 1
    socket.SOCK_DGRAM equ 2
    socket.SOCK_RAW equ 3
    socket.SOCK_RDM equ 4
    socket.SOCK_SEQPACKET equ 5
    socket.SOCK_DCCP equ 6
    socket.PACKET equ 10

    socket.PF_UNSPEC equ 0
    socket.PF_LOCAL equ 1
    socket.PF_UNIX equ socket.PF_LOCAL
    socket.PF_FILE equ socket.PF_LOCAL
    socket.PF_INET equ 2
    socket.PF_AX25 equ 3
    socket.PF_IPX equ 4
    socket.PF_APPLETALK equ 5
    socket.PF_NETROM equ 6
    socket.PF_BRIDGE equ 7
    socket.PF_ATMPVC equ 8
    socket.PF_X25 equ 9
    socket.PF_INET6 equ 10
    socket.PF_ROSE equ 11
    socket.PF_DECnet equ 12
    socket.PF_NETBEUI equ 13
    socket.PF_SECURITY equ 14
    socket.PF_KEY equ 15
    socket.PF_NETLINK equ 16
    socket.PF_ROUTE equ socket.PF_NETLINK
    socket.PF_PACKET equ 17
    socket.PF_ASH equ 18
    socket.PF_ECONET equ 19
    socket.PF_ATMSVC equ 20
    socket.PF_RDS equ 21
    socket.PF_SNA equ 22
    socket.PF_IRDA equ 23
    socket.PF_PPPOX equ 24
    socket.PF_WANPIPE equ 25
    socket.PF_LLC equ 26
    socket.PF_CAN equ 29
    socket.PF_TIPC equ 30
    socket.PF_BLUETOOTH equ 31
    socket.PF_IUCV equ 32
    socket.PF_RXRPC equ 33
    socket.PF_ISDN equ 34
    socket.PF_PHONET equ 35
    socket.PF_IEEE802154 equ 36
    socket.PF_MAX equ 37

    socket.AF_UNSPEC equ socket.PF_UNSPEC
    socket.AF_LOCAL equ socket.PF_LOCAL
    socket.AF_UNIX equ socket.PF_UNIX
    socket.AF_FILE equ socket.PF_FILE
    socket.AF_INET equ socket.PF_INET
    socket.AF_AX25 equ socket.PF_AX25
    socket.AF_IPX equ socket.PF_IPX
    socket.AF_APPLETALK equ socket.PF_APPLETALK
    socket.AF_NETROM equ socket.PF_NETROM
    socket.AF_BRIDGE equ socket.PF_BRIDGE
    socket.AF_ATMPVC equ socket.PF_ATMPVC
    socket.AF_X25 equ socket.PF_X25
    socket.AF_INET6 equ socket.PF_INET6
    socket.AF_ROSE equ socket.PF_ROSE
    socket.AF_DECnet equ socket.PF_DECnet
    socket.AF_NETBEUI equ socket.PF_NETBEUI
    socket.AF_SECURITY equ socket.PF_SECURITY
    socket.AF_KEY equ socket.PF_KEY
    socket.AF_NETLINK equ socket.PF_NETLINK
    socket.AF_ROUTE equ socket.PF_ROUTE
    socket.AF_PACKET equ socket.PF_PACKET
    socket.AF_ASH equ socket.PF_ASH
    socket.AF_ECONET equ socket.PF_ECONET
    socket.AF_ATMSVC equ socket.PF_ATMSVC
    socket.AF_RDS equ socket.PF_RDS
    socket.AF_SNA equ socket.PF_SNA
    socket.AF_IRDA equ socket.PF_IRDA
    socket.AF_PPPOX equ socket.PF_PPPOX
    socket.AF_WANPIPE equ socket.PF_WANPIPE
    socket.AF_LLC equ socket.PF_LLC
    socket.AF_CAN equ socket.PF_CAN
    socket.AF_TIPC equ socket.PF_TIPC
    socket.AF_BLUETOOTH equ socket.PF_BLUETOOTH
    socket.AF_IUCV equ socket.PF_IUCV
    socket.AF_RXRPC equ socket.PF_RXRPC
    socket.AF_ISDN equ socket.PF_ISDN
    socket.AF_PHONET equ socket.PF_PHONET
    socket.AF_IEEE802154 equ socket.PF_IEEE802154
    socket.AF_MAX equ socket.PF_MAX

    socket.SOL_RAW equ 255
    socket.SOL_DECNET equ 261
    socket.SOL_X25 equ 262
    socket.SOL_PACKET equ 263
    socket.SOL_ATM equ 264
    socket.SOL_AAL equ 265
    socket.SOL_IRDA equ 266

    socket.SHUT_RD equ 0
    socket.SHUT_WR equ 1
    socket.SHUT_RDWR equ 2

    socket.ADDR_REUSE equ 2

;;required

section .text

socket.socket:
    ; socket.socket(QWORD (int) family, QWORD (int) type, QWORD (int) protocol) -> QWORD (fd) socket
    push rdi
    push rsi
    push rdx    
    mov     rax, 41
    
    mov     rdi, [rsp+32]   ; family
    mov     rsi, [rsp+40]  ; type
    mov     rdx, [rsp+48]  ; protocol
    
    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc

socket.connect:
    ; socket.connect(QWORD PTR (fd) socket, QWORD PTR (sockaddr struct) addr, QWORD (int) length)
    push rdi
    push rsi
    push rdx
    mov rax, 42

    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    mov rdx, [rsp+48]

    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc

socket.accept:
    ; socket.accept(QWORD (fd) socket, QWORD PTR (upeer_sockaddr struct) addr, QWORD PTR (int) length) -> QWORD (fd) socket_a
    push rdi
    push rsi
    push rdx
    mov rax, 43
    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    mov rdx, [rsp+48]

    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc

socket.sendto: 
    ; socket.sendto(
    ;   QWORD (fd)                  socket, 
    ;   QWORD PTR (array)           data,
    ;   QWORD (int)                 length,
    ;   QWORD PTR (sockaddr struct) addr,
    ;   QWORD (int)                 sockaddr_len
    ;   QWORD (int)                 flags,
    ;)


    push rax
    push rdi
    push rdx
    push r8
    push r9
    push r10

    mov rax, 44

    mov rdi, [rsp+56]
    mov rsi, [rsp+64]
    mov rdx, [rsp+72]
    mov r8,  [rsp+80]
    mov r9,  [rsp+88]
    mov r10, [rsp+96]

    syscall
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rdi
    pop rax
    ret 48

;;endfunc

socket.recvfrom:
    ; socket.recvfrom(
    ;   QWORD (fd)                  socket, 
    ;   QWORD PTR (array)           buffer,
    ;   QWORD (int)                 length,
    ;   QWORD PTR (sockaddr struct) addr,
    ;   QWORD (int)                 sockaddr_len
    ;   QWORD (int)                 flags,
    ;)

    push rax
    push rdi
    push rdx
    push r8
    push r9
    push r10

    mov rax, 45

    mov rdi, [rsp+56]
    mov rsi, [rsp+64]
    mov rdx, [rsp+72]
    mov r8,  [rsp+80]
    mov r9,  [rsp+88]
    mov r10, [rsp+96]

    syscall
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rdi
    pop rax
    ret 48

;;endfunc

socket.sendmsg:
    ; socket.sendmsg(QWORD (fd) socket, QWORD PTR (msghdr struct) msg, QWORD (int) flags)

    push rax
    push rdi
    push rsi
    push rdx

    mov rax, 46

    mov rdi, [rsp+40]
    mov rsi, [rsp+48]
    mov rdx, [rsp+56]

    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24

;;endfunc

socket.recvmsg:
    ; socket.recvmsg(QWORD (fd) socket, QWORD PTR (msghdr struct) msg, QWORD (int) flags)

    push rax
    push rdi
    push rsi
    push rdx
    mov rax, 47

    mov rdi, [rsp+40]
    mov rsi, [rsp+48]
    mov rdx, [rsp+56]

    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24

;;endfunc

socket.close:
    ; socket.close(QWORD (fd) socket, QWORD (int) how) -> QWORD (int) error
    push rdi
    push rsi
    mov rax, 48

    mov rdi, [rsp+24]
    mov rsi, [rsp+32]

    syscall
    pop rsi
    pop rdi
    ret 16

;;endfunc

socket.bind:
    ; socket.bind(QWORD (fd) socket, QWORD PTR (sockAddr struct) addr, QWORD (int) length) -> QWORD (int) error

    push rdi
    push rsi
    push rdx

    mov rax, 49

    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    mov rdx, [rsp+48]

    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc

socket.listen:
    ; socket.listen(QWORD (fd) socket, QWORD (int) max_connections)

    push rax
    push rdi
    push rsi
    mov rax, 50

    mov rdi, [rsp+32]
    mov rsi, [rsp+40]

    syscall
    pop rsi
    pop rdi
    pop rax
    ret 16

;;endfunc

socket.getsockname:
    ; socket.getsockname(QWORD (fd) socket, QWORD PTR (usockaddr struct) addr, QWORD PTR (int) len)
    push rax
    push rdi
    push rsi
    push rdx
    mov rax, 51

    mov rdi, [rsp+40]
    mov rsi, [rsp+48]
    mov rdx, [rsp+56]

    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24

;;endfunc

socket.getpeername:
    ; socket.getpeername(QWORD (fd) socket, QWORD PTR (usockaddr struct) addr, QWORD PTR (int) len)

    push rax
    push rdi
    push rsi
    push rdx
    mov rax, 52

    mov rdi, [rsp+40]
    mov rsi, [rsp+48]
    mov rdx, [rsp+56]

    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 24

;;endfunc

socket.socketpair:
    ; socket.socketpair(QWORD (int) family, QWORD (int) type, QWORD (int) protocol, QWORD PTR (int) usockvec)

    push rax
    push rdi
    push rsi
    push rdx
    push r10
    mov rax, 53

    mov rdi, [rsp+48]
    mov rsi, [rsp+56]
    mov rdx, [rsp+64]
    mov r10, [rsp+72]

    syscall
    pop r10
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 32

;;endfunc

socket.setsockopt:
    ; socket.setsockopt(
    ;   QWORD (fd)         socket, 
    ;   QWORD (int)        level,
    ;   QWORD (int)        optname
    ;   QWORD PTR (string) optval
    ;   QWORD (int)        optlen
    ;)
    push rax
    push rdi
    push rsi
    push rdx
    push r10
    push r8
    mov rax, 54

    mov rdi, [rsp+56]
    mov rsi, [rsp+64]
    mov rdx, [rsp+72]
    mov r10, [rsp+80]
    mov r8,  [rsp+88]

    syscall
    pop r8
    pop r10
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 40

;;endfunc

socket.getsockopt:
    ; socket.getsockopt(
    ;   QWORD (fd)         socket, 
    ;   QWORD (int)        level,
    ;   QWORD (int)        optname
    ;   QWORD PTR (string) optval
    ;   QWORD (int)        optlen
    ;)
    push rax
    push rdi
    push rsi
    push rdx
    push r10
    push r8
    mov rax, 55

    mov rdi, [rsp+56]
    mov rsi, [rsp+64]
    mov rdx, [rsp+72]
    mov r10, [rsp+80]
    mov r8,  [rsp+88]

    syscall
    pop r8
    pop r10
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret 40

;;endfunc


socket.send:
    ; socket.send(QWORD (fd) connection, QWORD PTR data, QWORD (int) length) -> QWORD (int) length
    push rdi
    push rsi
    push rdx
    mov rax, 1

    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    mov rdx, [rsp+48]

    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc


socket.recv:
    ; socket.recv(QWORD (fd) connection, QWORD PTR buffer, QWORD (int) length) -> QWORD (int) length

    push rdi
    push rsi
    push rdx
    mov rax, 0

    mov rdi, [rsp+32]
    mov rsi, [rsp+40]
    mov rdx, [rsp+48]

    syscall
    pop rdx
    pop rsi
    pop rdi
    ret 24

;;endfunc

socket.StrToAddr:
      ;socket.StrToAddr(QWORD PTR (string) str, QWORD (int) length)
      push rdx
      push rsi
      push rax
      push rcx

      mov rdx, [rsp+32] ; our string
      mov rsi, [rsp+40]
      xor rax, rax ; zero a "result so far"
      .top:
      movzx rcx, byte [rdx] ; get a character

      inc rdx ; ready for next one

      cmp rcx, '.'
      je .done

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
      pop rcx
      pop rax
      pop rsi
      pop rcx
      ret 16