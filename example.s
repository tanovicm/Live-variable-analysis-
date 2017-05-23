	.file	"example.cpp"
	.section	.rodata
.LC0:
	.string	"%d\n"
.LC1:
	.string	"%d "
	.text
	.globl	main
	.type	main, @function
main:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$17, -8(%rbp)
	movl	-8(%rbp), %eax
	cmpl	$5, %eax
	setg	%al
	testb	%al, %al
	je	.L2
	movl	-8(%rbp), %eax
	addl	$5, %eax
	movl	%eax, -8(%rbp)
	jmp	.L3
.L2:
	movl	-8(%rbp), %eax
	subl	$5, %eax
	movl	%eax, -8(%rbp)
.L3:
	movl	-8(%rbp), %eax
	movl	%eax, %esi
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
	movl	$0, -4(%rbp)
.L5:
	movl	-8(%rbp), %eax
	cltd
	xorl	%edx, %eax
	subl	%edx, %eax
	cmpl	-4(%rbp), %eax
	setg	%al
	testb	%al, %al
	je	.L4
	movl	-8(%rbp), %edx
	movl	-4(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, %esi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	addl	$1, -4(%rbp)
	jmp	.L5
.L4:
	movl	-8(%rbp), %eax
	addl	$7, %eax
	movl	%eax, -8(%rbp)
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
