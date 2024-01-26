from project1_classes.lexer_fsm import LexerFSM

# Return your program output here for grading (can treat this function as your "main")
def project1(input: str) -> str:
    i = 1
    n = -1
    token_string = ""
    lexer: LexerFSM = LexerFSM()
    tokens = lexer.lex(input)
    line_num = lexer.line_num
    for token in tokens:
        token_string += f'{token}\n'
    total_tokens = len(tokens)
    if len(tokens) > 0 and "UNDEFINED" == tokens[-1]:               
        return (f'{token_string}\nTotal Tokens = Error on line {line_num}')
    return (f'{token_string}(EOF,"",{line_num})\nTotal Tokens = {total_tokens + 1}') 

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

# Use this to run and debug code within VS Code
if __name__ == "__main__":
    input_contents = read_file_contents("./project-2-nbn1343/Parser/project2-passoff/80/input4.txt")
#     input_contents = '''# COPYRIGHT © BRIGHAM YOUNG UNIVERSITY CS 236
# # FOR USE ONLY DURING SPRING 2021 SEMESTER
# # passoffInput20     SUCCESS
# # This tests their 'success' with a few comments tokens now and then
#   #Schemes: 
# Schemes: 
#   #student(N, I, A, M)
# student(N, I, A, M)
#   #WhoMajor(N,M)
# WhoMajor(N,M)

# Facts: 
#   #Facts: 
# student('Roosevelt', '51', '10 Main', 'Econ').
#   #student('Roosevelt', '51', '10 Main', 'Econ').
# student('Reagan','52', '11 Maple', 'Econ').
#   #student('Reagan','52', '11 Maple', 'Econ').
# student('G.W.Bush','53','12 Ashton', 'AgriSci').
#   #student('G.W.Bush','53','12 Ashton', 'AgriSci').
# student('Clinton','54','', 'Lying').
#   #student('Clinton','54','', 'Lying').

#   #Rules:
# Rules:
#   #WhoMajor(N,M):-student(N,I,A,M).
# WhoMajor(N,M):-student(N,I,A,M).

# Queries:
#   #Queries:
# WhoMajor('Roosevelt',N)?WhoMajor(M,'Econ')?
#   #WhoMajor('Roosevelt',N)?WhoMajor(M,'Econ')?
# WhoMajor('George Washington','PoliSci')?
#   #WhoMajor('George Washington','PoliSci')?
# WhoMajor('Abraham Lincoln','Law')?student('John Adams', I, A, M)?
#   #WhoMajor('Abraham Lincoln','Law')?student('John Adams', I, A, M)? 
# '''
    print(project1(input_contents).rstrip())

