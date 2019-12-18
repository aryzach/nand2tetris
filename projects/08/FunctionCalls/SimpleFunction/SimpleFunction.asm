// function SimpleFunction.test 2 
(SimpleFunction.test)
@2
D=A
@R14
M=D
(SimpleFunction.test$AddMoreLocVars)
@R14
D=M
@SimpleFunction.test$NoMoreLocVars
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
@SimpleFunction.test$AddMoreLocVars
0;JMP
(SimpleFunction.test$NoMoreLocVars)
// push local 0 
@LCL
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
// push local 1 
@LCL
D=M
@1
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
// not 
@SP
A=M-1
D=M
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
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
// push argument 1 
@ARG
D=M
@1
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
