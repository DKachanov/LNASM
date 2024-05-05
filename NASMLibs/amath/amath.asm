section .text
;;required

amath.expf:
	; amath.expf(double n) -> double e^x
	fld qword [rsp+8]
	fldl2e
	fmulp
	fst qword [rsp+8]
	fld1
	fld qword [rsp+8]
	fprem
	f2xm1
	faddp
	fscale
	sub rsp, 8
	fstp qword [rsp]
	pop rax
	ret 8
