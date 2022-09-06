import ply.lex as lex


tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    
    'COMMA',
    'DOTCOMMA',
    'DOUBLEDOT',
    'ARROW',
    'EQ',
    'NEQ',
    'GT',
    'LT',
    'GE',
    'LE'
)

reserved = {
   'class': 'CLASS',
   'fi': 'FI',
   'in': 'IN',
   'inherits':'INHERITS',
   'isvoid':'ISVOID',
   'let': 'LET',
   'loop': 'LOOP',
   'pool': 'POOL',
   'case': 'CASE',
   'esac': 'ESAC',
   'new': 'NEW',
   'of': 'OF',
   'not': 'NOT',
   'false': 'false',        ## obs: true e false são case sensitive, apenas a primeira letra precisa
   'true':'true',           # ser minúscula. Como seria isso no código?
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
}

# Regular expression rules for simple tokens
#t_ignore = ' \t'    # especifica caracteres ignorados entre tokes, usualmente espaços em branco e tabs
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_COMMA = r','
t_DOTCOMMA = r';'
t_DOUBLEDOT = r':'
t_ARROW = r'<-'     # não sei se é assim pra representar '<-'
t_EQ = r'='
t_NEQ = r'!='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='


tokens = ['LPAREN','RPAREN','NUMBER', 'PLUS', 'MINUS', 
          'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 
          'COMMA', 'DOTCOMMA', 'DOUBLEDOT', 'ARROW', 
          'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE', 'ID'] + list(reserved.values())

# A regular expression rule with some action code
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'      # docstring retém a expressão regular     # casa digitos de 0 a 9? oq o '+' significa?
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'("[^"\n]*")' # corresponde a quaisquer strings literais entre aspas duplas 
    return t


def t_COMMENT(t):
    # comentários em cool: -- e *...* 
    r'\--.*'   
    r'\**.*'   # não sei se esse padrão de reconhecer esse tipo de comentário funciona
    pass
    # No return value. Token discarded


# Define a rule so we can track line numbers
def t_newline(t):       # o que são line numbers?
    r'\n+'
    t.lexer.lineno += len(t.value)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):  # não entendi mt bem a utilidade dessa função
    line_start = input.rfind('\n', 0, token.lexpos) + 1    
    return (token.lexpos - line_start) + 1


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'   # provides substantially better lexing performance because 
                    # it is handled as a special case and is checked in a much 
                    # more efficient manner than the normal regular expression rules.


literals = [ '{', '}' ]

def t_lbrace(t):
    r'\{'
    t.type = '{'      # Set token type to the expected literal
    return t


def t_rbrace(t):
    r'\}'
    t.type = '}'      # Set token type to the expected literal
    return t


# Error handling rule: lidar com strings que não forem tokenizadas, isto é, não possuem regra de
# reconhecimento 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def test_lex():

    # aqui precisamos dar um jeito de ler um arquivo cool

    lex.input("x = 3 * 4 + (5 * 6)")

    while True: 
        tok = lex.token()
        if not tok: 
            break
        print(tok)
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)


# Build the lexer
lex.lex()  # constrói o lexer criando uma expressão regular geral


if __name__ == '__main__':
    test_lex()