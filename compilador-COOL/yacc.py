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

""" Each function accepts a single argument p that is a sequence containing the 
    values of each grammar symbol in the corresponding rule. 
    The values of p[i] are mapped to grammar symbols. """

# regras de acordo com a ordem do manual de cool
# Ctrl K + Ctrl C pra comentar em bloco e Ctrl K + Ctrl U para descomentar

def p_program(p):
    """program : classes"""
    p[0] = p[1] 


def p_classes(p):
    """classes : class
               | class classes"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + p[[2]]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_class(p):
    """class : CLASS TYPE inherits LBRACE features RBRACE DOTCOMMA"""
    p[0] = Class(p[2], p[3], p[5])
     

def p_features(p):
    """features : feature
                | feature features
                | empty"""
    if len(p) == 2:
        if p.slice[1].type == 'empty':
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_feature(p):
    """feature : ID LPAREN formals RPAREN DOUBLEDOT TYPE LBRACE expr RBRACE DOTCOMMA
               | attr_def DOTCOMMA"""


def p_formals(p):
    """formals : formal
               | formal COMMA formals
               | empty"""
    if len(p) == 2:
        if p.slice[1].type == 'empty':
            p[0] = tuple()
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_formal(p):
    """formal : ID DOUBLEDOT TYPE"""
    p[0] = (p[1], p[3])


def p_expr(p):
    """expr : ID ARROW expr                                      
            | expr targettype DOT function_call          
            | function_call                                  
            | IF expr THEN expr ELSE expr FI                
            | WHILE expr LOOP expr POOL      
            | LBRACE blockelements RBRACE                                
            | LET attr_defs IN expr                              
            | CASE expr OF typeactions ESAC                  
            | NEW TYPE
            | ISVOID expr
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | COMPLEMENT expr
            | expr LT expr
            | expr LE expr
            | expr EQ expr
            | NOT expr                     
            | LPAREN expr RPAREN
            | ID
            | INTEGER
            | STRING
            | BOOL
    """

    first_token = p.slice[1].type
    second_token = p.slice[2].type if len(p) > 2 else None
    third_token = p.slice[3].type if len(p) > 3 else None

    if first_token == 'ID':
        if second_token is None:
            p[0] = Id(p[1])
        elif second_token == 'assign':
            p[0] = idAssign(p[1], p[3])  # não tenho certeza
    
    # falta a segunda regra

    elif first_token == 'function_call':
        p[0] = p[1]
    elif first_token == 'IF':
        p[0] = If(p[2], p[4], p[6])
    elif first_token == 'WHILE':
        p[0] = While(p[2], p[4])
    elif first_token == 'LBRACE':
        p[0] = Block(p[2])
    elif first_token == 'LET':
        p[0] = Let(p[2], p[4])
    elif first_token == 'CASE':
        p[0] = ast.Case(p[2], p[4])
    elif first_token == 'NEW':
        p[0] = New(p[2])
    elif first_token == 'ISVOID':
        p[0] = Isvoid(p[2])
    elif first_token == 'NOT':
        p[0] = Not(p[2])
    elif first_token == 'COMPLEMENT':
        p[0] = Complement(p[2])
    elif first_token == 'LBRACE':
        p[0] = p[2]
    elif first_token == 'INTEGER':
        p[0] = Int(p[1])
    elif first_token == 'STRING':
        p[0] = Str(p[1])
    elif first_token == 'BOOL':
        p[0] = Bool(p[1])

    # binary operations
    if second_token == '+':
        p[0] = Plus(p[1], p[3])
    elif second_token == '-':
        p[0] = Sub(p[1], p[3])
    elif second_token == '*':
        p[0] = Mult(p[1], p[3])
    elif second_token == '/':
        p[0] = Div(p[1], p[3])
    elif second_token == '<':
        p[0] = Lt(p[1], p[3])
    elif second_token == '<=':
        p[0] = Le(p[1], p[3])
    elif second_token == '=':
        p[0] = Eq(p[1], p[3])
    

# regras auxiliares  
def p_targettype(p):
    """targettype : AT TYPE
                  | empty"""
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        raise SyntaxError('Número de símbolos inválido')
    

def p_function_call(p):
    """function_call : ID LPAREN params RPAREN"""


def p_attr_defs(p):
    """attr_defs : attr_def
                 | attr_def COMMA attr_defs"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_attr_def(p):
    """attr_def : ID DOUBLEDOT TYPE assign"""


def p_typeactions(p):
    """typeactions : typeaction
                   | typeaction typeactions"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_typeaction(p):
    """typeaction : ID DOUBLEDOT TYPE EL expr DOTCOMMA"""


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
    """assign : ARROW expr
              | empty"""
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_params(p):
    """params : expr
              | expr COMMA params
              | empty"""
    if len(p) == 2:
        if p.slice[1].type == 'empty':       # params opt
            p[0] = tuple()
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        raise SyntaxError('Número de símbolos inválido')


def p_blockelements(p):
    """blockelements : expr DOTCOMMA
                     | expr DOTCOMMA blockelements"""
    if len(p) == 3:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        raise SyntaxError('Número de símbolos inválido')

def p_expr_self(p):
    """expr  : SELF"""

    
def p_empty(p):
    """empty :""" 
    p[0] = None


def p_error(p):
    print('Syntax error in input at {!r}'.format(p))


# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        data = open(sys.argv[1], 'r').read()
        result = parser.parse(data)
        print(result)
    else:
        while True:
            try:
                s = input('coolp> ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            print(result)