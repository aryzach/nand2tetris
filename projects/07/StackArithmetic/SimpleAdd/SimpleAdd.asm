@256
D=A
@SP
M=D
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 0 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D-M
@GOTO3
D;JEQ
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
// push constant 10 
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D-M
@GOTO6
D;JLT
@SP
A=M-1
M=0
@GOTO8
0;JMP
(GOTO6)
@SP
A=M-1
M=-1
(GOTO8)
// push constant 10 
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D-M
@GOTO9
D;JGT
@SP
A=M-1
M=0
@GOTO11
0;JMP
(GOTO9)
@SP
A=M-1
M=-1
(GOTO11)
// push constant 10 
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 20 
@20
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D-M
@GOTO12
D;JLT
@SP
A=M-1
M=0
@GOTO14
0;JMP
(GOTO12)
@SP
A=M-1
M=-1
(GOTO14)
// push constant 10 
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 30 
@30
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt 
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=D-M
@GOTO15
D;JGT
@SP
A=M-1
M=0
@GOTO17
0;JMP
(GOTO15)
@SP
A=M-1
M=-1
(GOTO17)
