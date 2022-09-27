import ply.yacc as yacc
from calclex import tokens  


precedence = (
    ('right', 'ARROW'),
    ('right', 'NOT'),
    ('nonassoc', 'LE', 'LT', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ISVOID'),
    ('right', 'COMPLEMENT'),
    ('left', 'AT'),
    ('left', 'DOT'),
)

def p_inherits(p):
    """inherits : INHERITS TYPE
                | empty"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[2]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_assign(p):
    """assign : ARROW expr"""
    p[0] = p[2]



# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)