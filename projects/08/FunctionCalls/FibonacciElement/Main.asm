@256
D=A
@SP
M=D
// function Main.fibonacci 0 
@0
D=A
@R14
M=D
(AddMoreLocVars)
@R14
D=M
@NoMoreLocVars
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
D=M+1
M=D
@R14
D=M-1
M=D
@AddMoreLocVars
0;JMP
(NoMoreLocVars)
// push argument 0 
@ARG
D=M
@0
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
// push constant 2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt                     // checks if n<2 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M-D
@GOTO3
D;JLT
@SP
A=M-1
M=0
@GOTO5
0;JMP
(GOTO3)
@SP
A=M-1
M=-1
(GOTO5)
// if-goto IF_TRUE 
@SP
M=M-1
@SP
A=M
D=M
@IF_TRUE
D;JNE
// goto IF_FALSE 
@IF_FALSE
0;JMP
// label IF_TRUE          // if n<2, return n 
(IF_TRUE)
// push argument 0 
@ARG
D=M
@0
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
// return 
// frame = LCL
@LCL
D=M
@FRAME
M=D
// ret = *(frame-5)
@FRAME
D=M
@5
D=D-A
A=D
D=M
@RET
M=D
// *arg = pop()
@ARG
D=M
@0
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
// sp = arg+1
@ARG
D=M+1
@SP
M=D
// that = *(frame-1)
@FRAME
A=M-1
D=M
@THAT
M=D
// this = *(frame-2)
@2
D=A
@FRAME
A=M-D
D=M
@THIS
M=D
// arg = *(frame-3)
@3
D=A
@FRAME
A=M-D
D=M
@ARG
M=D
// lcl = *(frame-4)
@4
D=A
@FRAME
A=M-D
D=M
@LCL
M=D
// goto ret
@RET
A=M
0;JMP
// label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1) 
(IF_FALSE)
// push argument 0 
@ARG
D=M
@0
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
// push constant 2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// call Main.fibonacci 1  // computes fib(n-2) 
