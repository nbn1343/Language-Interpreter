from Parser.project_2_classes.datalog_program import DatalogProgram
from Lexer.project1_classes.lexer_fsm import LexerFSM
from Interpreter.Interpreter import Interpreter
from Parser.project_2_classes.parser import Parser

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer: LexerFSM = LexerFSM()
    tokens = lexer.lex(input)


    parser: Parser = Parser()
    # parser.run(tokens)
    datalog_program: DatalogProgram = parser.run(tokens)

    interpreter: Interpreter = Interpreter()
    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    # input_contents = read_file_contents("./project5-passoff/80/input0.txt")
    input_contents = '''
# COPYRIGHT © BRIGHAM YOUNG UNIVERSITY CS 236
# FOR USE ONLY DURING SPRING 2021 SEMESTER
Schemes:

slide(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z)

Facts:

slide('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z').

Rules:

slide(b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a):-slide(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z).

Queries:

slide(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z)?

'''
    print(project5(input_contents))
