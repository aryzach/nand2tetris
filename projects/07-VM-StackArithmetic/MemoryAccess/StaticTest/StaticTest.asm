@256
D=A
@SP
M=D
// push constant 111 
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333 
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888 
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8 
@SP
D=M-1
M=D
@SP
A=M
D=M
@.8
M=D
// pop static 3 
@SP
D=M-1
M=D
@SP
A=M
D=M
@.3
M=D
// pop static 1 
@SP
D=M-1
M=D
@SP
A=M
D=M
@.1
M=D
// push static 3 
@.3
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// push static 1 
@.1
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// sub 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M-D
M=D
// push static 8 
@.8
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// add 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D+M
M=D
