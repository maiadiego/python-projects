import ply.lex as lex


tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
#t_ignore = ' \t'    # especifica caracteres ignorados entre tokes, usualmente espaços em branco e tabs
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'      # docstring retém expressão regular     # casa digitos de 0 a 9? oq o '+' significa?
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()  # constrói o lexer criando uma expressão regular geral

lexer.input("x = 3 * 4 + 5 * 6")
while True: 
    tok = lex.token()
    if not tok: 
        break
    print(tok)
    #print(tok.type, tok.value, tok.lineno, tok.lexpos)


