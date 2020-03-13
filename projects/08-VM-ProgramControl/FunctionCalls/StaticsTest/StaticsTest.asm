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
// function Class1.set 0 
(Class1.set)
@0
D=A
@R14
M=D
(Class1.set$AddMoreLocVars)
@R14
D=M
@Class1.set$NoMoreLocVars
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
@Class1.set$AddMoreLocVars
0;JMP
(Class1.set$NoMoreLocVars)
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
// pop static 0 
@SP
D=M-1
M=D
@SP
A=M
D=M
@Class1.0
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
// pop static 1 
@SP
D=M-1
M=D
@SP
A=M
D=M
@Class1.1
M=D
// push constant 0 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// function Class1.get 0 
(Class1.get)
@0
D=A
@R14
M=D
(Class1.get$AddMoreLocVars)
@R14
D=M
@Class1.get$NoMoreLocVars
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
@Class1.get$AddMoreLocVars
0;JMP
(Class1.get$NoMoreLocVars)
// push static 0 
@Class1.0
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// push static 1 
@Class1.1
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
// function Class2.set 0 
(Class2.set)
@0
D=A
@R14
M=D
(Class2.set$AddMoreLocVars)
@R14
D=M
@Class2.set$NoMoreLocVars
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
@Class2.set$AddMoreLocVars
0;JMP
(Class2.set$NoMoreLocVars)
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
// pop static 0 
@SP
D=M-1
M=D
@SP
A=M
D=M
@Class2.0
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
// pop static 1 
@SP
D=M-1
M=D
@SP
A=M
D=M
@Class2.1
M=D
// push constant 0 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// function Class2.get 0 
(Class2.get)
@0
D=A
@R14
M=D
(Class2.get$AddMoreLocVars)
@R14
D=M
@Class2.get$NoMoreLocVars
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
@Class2.get$AddMoreLocVars
0;JMP
(Class2.get$NoMoreLocVars)
// push static 0 
@Class2.0
D=M
@SP
A=M
M=D
@SP
D=M+1
M=D
// push static 1 
@Class2.1
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
// push constant 6 
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8 
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2 
// push return-address
@return-Class1.set-2-2
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
@2
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
@Class1.set
0;JMP
// (return-address)
(return-Class1.set-2-2)
// pop temp 0 // Dumps the return value 
@R5
D=A
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
// push constant 23 
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15 
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2 
// push return-address
@return-Class2.set-2-3
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
@2
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
@Class2.set
0;JMP
// (return-address)
(return-Class2.set-2-3)
// pop temp 0 // Dumps the return value 
@R5
D=A
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
// call Class1.get 0 
// push return-address
@return-Class1.get-0-4
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
@Class1.get
0;JMP
// (return-address)
(return-Class1.get-0-4)
// call Class2.get 0 
// push return-address
@return-Class2.get-0-5
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
@Class2.get
0;JMP
// (return-address)
(return-Class2.get-0-5)
// label WHILE 
(WHILE)
// goto WHILE 
@WHILE
0;JMP
