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


def p_class(p):
    """class : CLASS TYPE inherits LBRACE features_opt RBRACE DOTCOMMA"""
   

def p_feature(p):
    """feature : ID LPAREN formals_opt RPAREN DOUBLEDOT TYPE LBRACE expr RBRACE DOTCOMMA
               | attr_def DOTCOMMA"""


def p_formal(p):
    """formal : ID DOUBLEDOT TYPE"""


def p_formals_opt(p):
    """formals_opt : formals
                   | empty"""
    

def p_expr(p):
    """expr : ID assign                                      # ID <- expr
            | expr targettype_opt DOT function_call          # expr[@TYPE].ID( [ expr [[, expr]]∗ ] )
            | function_call                                  # ID( [ expr [[, expr]]∗ ] )
            | IF expr THEN expr ELSE expr FI                 # if expr then expr else expr fi
            | WHILE expr LOOP expr POOL                      # while expr loop expr pool
            | LBRACE expr DOTCOMMA RBRACE                    # { [[expr; ]]+ }      ** ATENÇÃO NESSA REGRA **
            | LET attr_defs IN expr                          # let ID : TYPE [ <- expr ] [[, ID : TYPE [ <- expr ]]]∗ in expr    
            | CASE expr OF typeactions ESAC                  # case expr of [[ID : TYPE => expr; ]]+ esac
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
            | LBRACE block RBRACE                       ** ATENÇÃO AQUI **
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
    """attr_def : ID COLON TYPE assign_opt"""


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