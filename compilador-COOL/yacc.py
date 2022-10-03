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

def p_program(p):
    """program : classes"""


def p_classes(p):
    """classes : class
               | class classes"""


def p_class(p):
    """class : CLASS TYPE inherits LBRACE features_opt RBRACE DOTCOMMA"""
     


def p_features_opt(p):
    """features_opt : features
                    | empty"""

def p_features(p):
    """features : feature
                | feature features"""
   

def p_feature(p):
    """feature : ID LPAREN formals_opt RPAREN DOUBLEDOT TYPE LBRACE expr RBRACE DOTCOMMA
               | attr_def DOTCOMMA"""


def p_formals_opt(p):
    """formals_opt : formals
                   | empty"""


def p_formals(p):
    """formals : formal
               | formal COMMA formals"""


def p_formal(p):
    """formal : ID DOUBLEDOT TYPE"""
    

def p_expr(p):
    """expr : ID assign                                      
            | expr targettype_opt DOT function_call          
            | function_call                                  
            | IF expr THEN expr ELSE expr FI                
            | WHILE expr LOOP expr POOL                                      
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
            | LBRACE block RBRACE
            | NOT expr                     
            | LPAREN expr RPAREN
            | ID
            | INTEGER
            | STRING
            | BOOL
    """

# regras auxiliares  

def p_targettype_opt(p):
    """targettype_opt : targettype
                      | empty"""


def p_targettype(p):
    """targettype : AT TYPE"""
    

def p_function_call(p):
    """function_call : ID LPAREN params_opt RPAREN"""


def p_attr_defs(p):
    """attr_defs : attr_def
                 | attr_def COMMA attr_defs"""


def p_attr_def(p):
    """attr_def : ID DOUBLEDOT TYPE assign_opt"""


def p_typeactions(p):
    """typeactions : typeaction
                   | typeaction typeactions"""


def p_typeaction(p):
    """typeaction : ID DOUBLEDOT TYPE EL expr DOTCOMMA"""


def p_inherits(p):
    """inherits : INHERITS TYPE
                | empty"""
   

def p_assign_opt(p):    
    """assign_opt : assign
                  | empty"""


def p_assign(p):
    """assign : ARROW expr"""
   

def p_params_opt(p):
    """params_opt : params
                  | empty"""


def p_params(p):
    """params : expr
              | expr COMMA params"""


def p_block(p):
    """block : blockelements"""


def p_blockelements(p):
    """blockelements : expr DOTCOMMA
                     | expr DOTCOMMA blockelements"""


def p_expr_self(p):
    """expr  : SELF"""

    
def p_empty(p):
    """empty :""" 


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