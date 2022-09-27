import ply.lex as lex
import sys


tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'COMPLEMENT',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'DOTCOMMA',
    'DOUBLEDOT',
    'ARROW',
    'EQ',
    'LT',
    'LE',
    'STRING'
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
   'false': 'FALSE',       
   'true':'TRUE',          
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
}

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_COMPLEMENT = r'~'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_DOTCOMMA = r';'
t_DOUBLEDOT = r':'
t_ARROW = r'<-'
t_AT = r'\@'     
t_EQ = r'='
t_LT = r'<'
t_LE = r'<='


tokens = ['LPAREN','RPAREN','NUMBER', 'PLUS', 'MINUS', 'NOT', 'TYPE', 
          'TIMES', 'DIVIDE', 'COMPLEMENT', 'COMMA', 'DOT', 'DOTCOMMA', 'DOUBLEDOT', 'ARROW', 'AT', 
          'EQ', 'LT', 'LE', 'STRING', 'ID'] + list(reserved.values())

def t_ID(t):
    r'[a-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID') 
    return t


def t_TYPE(t):
    r'[A-Z][A-Za-z0-9_]*'
    return t


def t_NUMBER(t):
    r'\d+'      # docstring retém a expressão regular   
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'("[^"\n]*")' # corresponde a quaisquer strings literais entre aspas duplas 
    return t


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
t_ignore  = ' \t'   # provides substantially better lexing performance because 
                    # it is handled as a special case and is checked in a much 
                    # more efficient manner than the normal regular expression rules.


literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',','=','<']

def t_lbrace(t):
    r'\{'
    t.type = '{'      
    return t


def t_rbrace(t):
    r'\}'
    t.type = '}'      
    return t


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