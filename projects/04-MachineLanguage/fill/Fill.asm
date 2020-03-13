// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
@SCREEN
D=A
@currscreen
M=D   //cs = 16000 ish

@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ

(BLACK)
@currscreen
D=M
@KBD
D=A-D
D=D-1
@LOOP
D;JEQ  // if all black, ask if key is pressed again
@currscreen
A=M
M=-1 // ram[cs]= -1
@currscreen
M=M+1
@BLACK
0;JMP

/////

(WHITE)
@currscreen
D=M
@KBD
D=A-D
D=D-1
@LOOP
D;JEQ  // if all black, ask if key is pressed again
@currscreen
A=M
M=0 // ram[cs]= 0
@currscreen
M=M+1
@WHITE
0;JMP

