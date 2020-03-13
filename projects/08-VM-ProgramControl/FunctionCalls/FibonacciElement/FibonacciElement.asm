@256
D=A
@SP
M=D
// push return-address
@return-Sys.init-0-1
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Sys.init
0;JMP
// (return-address)
(return-Sys.init-0-1)
// function Main.fibonacci 0 
(Main.fibonacci)
@0
D=A
@R14
M=D
(Main.fibonacci$AddMoreLocVars)
@R14
D=M
@Main.fibonacci$NoMoreLocVars
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
@Main.fibonacci$AddMoreLocVars
0;JMP
(Main.fibonacci$NoMoreLocVars)
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
// push return-address
@return-Main.fibonacci-1-2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Main.fibonacci
0;JMP
// (return-address)
(return-Main.fibonacci-1-2)
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
// push constant 1 
@1
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
// call Main.fibonacci 1  // computes fib(n-1) 
// push return-address
@return-Main.fibonacci-1-3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Main.fibonacci
0;JMP
// (return-address)
(return-Main.fibonacci-1-3)
// add                    // returns fib(n-1) + fib(n-2) 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D+M
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
// function Sys.init 0 
(Sys.init)
@0
D=A
@R14
M=D
(Sys.init$AddMoreLocVars)
@R14
D=M
@Sys.init$NoMoreLocVars
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
@Sys.init$AddMoreLocVars
0;JMP
(Sys.init$NoMoreLocVars)
// push constant 4 
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1   // computes the 4'th fibonacci element 
// push return-address
@return-Main.fibonacci-1-4
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Main.fibonacci
0;JMP
// (return-address)
(return-Main.fibonacci-1-4)
// label WHILE 
(WHILE)
// goto WHILE              // loops infinitely 
@WHILE
0;JMP
