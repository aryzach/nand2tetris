@256
D=A
@SP
M=D
// push constant 3030 
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0 
@SP
D=M-1
M=D
@SP
A=M
D=M
@THIS
M=D
// push constant 3040 
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1 
@SP
D=M-1
M=D
@SP
A=M
D=M
@THAT
M=D
// push constant 32 
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2 
@THIS
D=M
@2
D=D+A
@R15
M=D
@SP
D=M-1
M=D
@SP
A=M
D=M
@R15
A=M
M=D
// push constant 46 
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 6 
@THAT
D=M
@6
D=D+A
@R15
M=D
@SP
D=M-1
M=D
@SP
A=M
D=M
@R15
A=M
M=D
// push pointer 0 
@THIS
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// push pointer 1 
@THAT
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
// push this 2 
@THIS
D=M
@2
D=D+A
A=D
D=M
@R15
M=D
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
// push that 6 
@THAT
D=M
@6
D=D+A
A=D
D=M
@R15
M=D
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
