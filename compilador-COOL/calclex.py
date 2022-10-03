import ply.lex as lex
import sys


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
   'false': 'FALSE',       
   'true':'TRUE',          
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'self' : 'SELF'
}

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',','=','<']

tokens = ['LPAREN','RPAREN', 'LBRACE', 'RBRACE', 'DOUBLEDOT', 'COMMA', 'DOT', 'DOTCOMMA', 'AT',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQ', 'LT', 'LE', 'ARROW', 'COMPLEMENT',
          'INTEGER', 'STRING', 'BOOL',
          'TYPE', 'ID',
          'EL'] + list(reserved.values())

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'       
t_RBRACE = r'\}'
t_DOUBLEDOT = r':'
t_COMMA = r','
t_DOT = r'\.'
t_DOTCOMMA = r';'
t_AT = r'@' 
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ = r'='
t_LT = r'<'
t_LE = r'<='
t_EL = r'=>'  
t_ARROW = r'<-'
t_COMPLEMENT = r'~'


def t_ID(t):
    r'[a-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID') 
    return t


def t_TYPE(t):
    r'[A-Z][A-Za-z0-9_]*'
    return t


def t_STRING(t):
    r'("[^"\n]*")' # corresponde a quaisquer strings literais entre aspas duplas 
    return t


def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return 


def t_COMMENT(t):
    r'\--.* | \(\*(.|\n)*\*\)'
    occurrencies = t.value.count('\n')
    #print(occurrencies)
    t.lexer.lineno += occurrencies
    pass


def t_NOT(t):
    r'[nN][oO][tT]'
    return t


# Define a rule so we can track line numbers
# O lex.py não sabe o que constitui uma "linha" de entrada
# Então é preciso criar uma regra para lidar com esse caso  
def t_newline(t):       
    r'\n+'
    t.lexer.lineno += len(t.value)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):  
    line_start = input.rfind('\n', 0, token.lexpos) + 1    
    return (token.lexpos - line_start) + 1


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r\f'   # provides substantially better lexing performance because 
                        # it is handled as a special case and is checked in a much 
                        # more efficient manner than the normal regular expression rules.


# Lidar com strings que não forem tokenizadas, isto é, não possuem regra de reconhecimento 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Constrói o lexer criando uma expressão regular geral
lex.lex()   

if __name__ == '__main__':
    code = open(sys.argv[1], "r").read()    
    lex.input(code)

    while True:     
        tok = lex.token()
        if not tok: 
            break
        print(tok)
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)