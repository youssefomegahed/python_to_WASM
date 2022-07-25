.globl main
main:
pushl %ebp
movl %esp, %ebp
subl $4, %esp
pushl %edi
pushl %esi
pushl %ebx

pushl $1
call inject_int
addl $4, %esp
movl %eax, %ebx
pushl $2
call inject_int
addl $4, %esp
movl %eax, %esi
pushl $3
call inject_int
addl $4, %esp
movl %eax, -4(%ebp)
movl $3, %eax
shl $2, %eax
pushl %eax
call create_list
addl $4, %esp
orl $3, %eax
movl %eax, %edi
pushl %ebx
movl $0, %eax
shl $2, %eax
pushl %eax
pushl %edi
call set_subscript
addl $12, %esp
pushl %esi
movl $1, %eax
shl $2, %eax
pushl %eax
pushl %edi
call set_subscript
addl $12, %esp
pushl -4(%ebp)
movl $2, %eax
shl $2, %eax
pushl %eax
pushl %edi
call set_subscript
addl $12, %esp
movl %edi, %eax
pushl %eax
call print_any
addl $4, %esp
movl $0, %eax

popl %ebx
popl %esi
popl %edi
addl $4, %esp
leave
ret

