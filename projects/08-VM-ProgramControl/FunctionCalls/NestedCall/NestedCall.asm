@256
D=A
@SP
M=D
// push return-address
@return-Sys.init-0
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
(return-Sys.init-0)
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
// push constant 4000	// test THIS and THAT context save 
@4000	//
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
// push constant 5000 
@5000
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
// call Sys.main 0 
// push return-address
@return-Sys.main-0
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
@Sys.main
0;JMP
// (return-address)
(return-Sys.main-0)
// pop temp 1 
@R5
D=A
@1
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
// label LOOP 
(LOOP)
// goto LOOP 
@LOOP
0;JMP
// function Sys.main 5 
(Sys.main)
@5
D=A
@R14
M=D
(Sys.main$AddMoreLocVars)
@R14
D=M
@Sys.main$NoMoreLocVars
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
@Sys.main$AddMoreLocVars
0;JMP
(Sys.main$NoMoreLocVars)
// push constant 4001 
@4001
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
// push constant 5001 
@5001
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
// push constant 200 
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1 
@LCL
D=M
@1
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
// push constant 40 
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2 
@LCL
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
// push constant 6 
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3 
@LCL
D=M
@3
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
// push constant 123 
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1 
// push return-address
@return-Sys.add12-1
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
@Sys.add12
0;JMP
// (return-address)
(return-Sys.add12-1)
// pop temp 0 
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
// push local 2 
@LCL
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
// push local 3 
@LCL
D=M
@3
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
// push local 4 
@LCL
D=M
@4
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
// function Sys.add12 0 
(Sys.add12)
@0
D=A
@R14
M=D
(Sys.add12$AddMoreLocVars)
@R14
D=M
@Sys.add12$NoMoreLocVars
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
@Sys.add12$AddMoreLocVars
0;JMP
(Sys.add12$NoMoreLocVars)
// push constant 4002 
@4002
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
// push constant 5002 
@5002
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
// push constant 12 
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
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
