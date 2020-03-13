


@i
M=1
@sum
M=0

(LOOP)
@i
D=M
@100
D=D-A
@END
D;JGT
//else
@i
D=M
@sum
M=M+D
@i
M=M+1
@LOOP
0;JMP

(END)
@sum
D=M
@R0
M=D
@END
0;JMP


