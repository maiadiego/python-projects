import ply.yacc as yacc
from calclex import tokens  
from collections import namedtuple
from types import new_class


class Returnable:
    return_type = None


def returnable_namedtuple(type_name, fields):
    return new_class(type_name, (Returnable, namedtuple(type_name, fields)))


class Inheritable:
    inherited_from = None


def inheritable_namedtuple(type_name, fields):
    return new_class(type_name, (Inheritable, namedtuple(type_name, fields)))


# namedtuple é uma forma concisa para criar classes que representam os nós 
# da árvore sintática abstrata, de acordo com cada regra
# new_class cria um objeto de classe dinamicamente passando o nome e as definições do cabeçalho da classe

Class = namedtuple("Class", "name, parent, feature_list")
Method = inheritable_namedtuple("Method", "name, formal_list, return_type, body")
Attr = namedtuple("Attr", "name, type, body")
Id = returnable_namedtuple("Id", "name")
Int = returnable_namedtuple("Int", "content")
Bool = returnable_namedtuple("Bool", "content")
Str = returnable_namedtuple("Str", "content")
Block = returnable_namedtuple("Block", "body")
Assign = returnable_namedtuple("Assign", "name, body")
Dispatch = returnable_namedtuple("Dispatch", "body, method, expr_list")
StaticDispatch = returnable_namedtuple("StaticDispatch", "body, type, method, expr_list")
Plus = returnable_namedtuple("Plus", "first, second")
Sub = returnable_namedtuple("Sub", "first, second")
Mult = returnable_namedtuple("Mult", "first, second")
Div = returnable_namedtuple("Div", "first, second")
Lt = returnable_namedtuple("Lt", "first, second")
Le = returnable_namedtuple("Le", "first, second")
Eq = returnable_namedtuple("Eq", "first, second")
If = returnable_namedtuple("If", "predicate, then_body, else_body")
While = returnable_namedtuple("While", "predicate, body")
Let = returnable_namedtuple("Let", "object, type, init, body")
Case = returnable_namedtuple("Case", "expr, case_list")
New = returnable_namedtuple("New", "type")
Isvoid = returnable_namedtuple("Isvoid", "body")
Neg = returnable_namedtuple("Neg", "body")
Not = returnable_namedtuple("Not", "body")

precedence = (
    ('right', 'ARROW'),
    ('left', 'NOT'),
    ('nonassoc', 'LE', 'LT', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'ISVOID'),
    ('left', 'COMPLEMENT'),
    ('left', 'AT'),
    ('left', 'DOT'),
)

""" Each function accepts a single argument p that is a sequence containing the 
    values of each grammar symbol in the corresponding rule. 
    The values of p[i] are mapped to grammar symbols. """

# regras de acordo com a ordem do manual de cool
# Ctrl K + Ctrl C pra comentar em bloco e Ctrl K + Ctrl U para descomentar

def p_class_list_many(p):
    """class_list : class_list class DOTCOMMA"""
    p[0] = p[1] + [p[2]]

def p_class_list_single(p):
    """class_list : class DOTCOMMA"""
    p[0] = [p[1]]

def p_class(p):
    """class : CLASS TYPE LBRACE feature_list RBRACE"""
    p[0] = Class(p[2], "Object", p[4])

def p_class_inherits(p):
    """class : CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE"""
    p[0] = Class(p[2], p[4], p[6])

def p_feature_list_many(p):
    """feature_list : feature_list feature DOTCOMMA"""
    p[0] = p[1] + [p[2]]  

def p_feature_list_single(p):
    """feature_list : feature DOTCOMMA"""
    p[0] = [p[1]]

def p_feature_list_empty(p):
    """feature_list : """
    p[0] = []

def p_feature_method(p):
    """feature : ID LPAREN formal_list RPAREN DOUBLEDOT TYPE LBRACE expression RBRACE"""
    p[0] = Method(p[1], p[3], p[6], p[8])

def p_feature_method_no_formals(p):
    """feature : ID LPAREN RPAREN DOUBLEDOT TYPE LBRACE expression RBRACE"""
    p[0] = Method(p[1], [], p[5], p[7])

def p_feature_attr_initialized(p):
    """feature : ID DOUBLEDOT TYPE ARROW expression"""
    p[0] = Attr(p[1], p[3], p[5])

def p_feature_attr(p):
    """feature : ID DOUBLEDOT TYPE"""
    p[0] = Attr(p[1], p[3], None)

def p_formal_list_many(p):
    """formal_list : formal_list COMMA formal"""
    p[0] = p[1] + [p[3]]

def p_formal_list_single(p):
    """formal_list : formal"""
    p[0] = [p[1]]

def p_formal(p):
    """formal : ID DOUBLEDOT TYPE"""
    p[0] = (p[1], p[3])

def p_expression_object(p):
    """expression : ID"""
    p[0] = Id(p[1])

def p_expression_int(p):
    """expression : INTEGER"""
    p[0] = Int(p[1])

def p_expression_bool(p):
    """expression : BOOL"""
    p[0] = Bool(p[1])

def p_expression_str(p):
    """expression : STRING"""
    p[0] = Str(p[1])

def p_expression_block(p):
    """expression : LBRACE block_list RBRACE"""
    p[0] = Block(p[2])

def p_block_list_many(p):
    """block_list : block_list expression DOTCOMMA"""
    p[0] = p[1] + [p[2]]

def p_block_list_single(p):
    """block_list : expression DOTCOMMA"""
    p[0] = [p[1]]

def p_expression_assignment(p):
    """expression : ID ARROW expression"""
    p[0] = Assign(Id(p[1]), p[3])

def p_expression_dispatch(p):
    """expression : expression DOT ID LPAREN expr_list RPAREN"""
    p[0] = Dispatch(p[1], p[3], p[5])

def p_expr_list_many(p):
    """expr_list : expr_list COMMA expression"""
    p[0] = p[1] + [p[3]]

def p_expr_list_single(p):
    """expr_list : expression"""
    p[0] = [p[1]]

def p_expr_list_empty(p):
    """expr_list : """
    p[0] = []

def p_expression_static_dispatch(p):
    """expression : expression AT TYPE DOT ID LPAREN expr_list RPAREN"""
    p[0] = StaticDispatch(p[1], p[3], p[5], p[7])

def p_expression_self_dispatch(p):
    """expression : ID LPAREN expr_list RPAREN"""
    p[0] = Dispatch("self", p[1], p[3])

def p_expression_basic_math(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    """
    if p[2] == '+':
        p[0] = Plus(p[1], p[3])
    elif p[2] == '-':
        p[0] = Sub(p[1], p[3])
    elif p[2] == '*':
        p[0] = Mult(p[1], p[3])
    elif p[2] == '/':
        p[0] = Div(p[1], p[3])

def p_expression_numerical_comparison(p):
    """
    expression : expression LT expression
               | expression LE expression
               | expression EQ expression
    """
    if p[2] == '<':
        p[0] = Lt(p[1], p[3])
    elif p[2] == '<=':
        p[0] = Le(p[1], p[3])
    elif p[2] == '=':
        p[0] = Eq(p[1], p[3])

def p_expression_with_parenthesis(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_expression_if(p):
    """expression : IF expression THEN expression ELSE expression FI"""
    p[0] = If(p[2], p[4], p[6])

def p_expression_while(p):
    """expression : WHILE expression LOOP expression POOL"""
    p[0] = While(p[2], p[4])

def p_expression_let(p):
    """expression : LET ID DOUBLEDOT TYPE IN expression
       expression : LET ID DOUBLEDOT TYPE COMMA inner_lets"""
    p[0] = Let(p[2], p[4], None, p[6])

def p_expression_let_initialized(p):
    """expression : LET ID DOUBLEDOT TYPE ARROW expression IN expression
       expression : LET ID DOUBLEDOT TYPE ARROW expression COMMA inner_lets"""
    p[0] = Let(p[2], p[4], p[6], p[8])

def p_expression_let_with_error_in_first_decl(p):
    """expression : LET error COMMA ID DOUBLEDOT TYPE IN expression
       expression : LET error COMMA ID DOUBLEDOT TYPE COMMA inner_lets"""
    p[0] = Let(p[4], p[6], None, p[8])

def p_expression_let_initialized_with_error_in_first_decl(p):
    """expression : LET error COMMA ID DOUBLEDOT TYPE ARROW expression IN expression
       expression : LET error COMMA ID DOUBLEDOT TYPE ARROW expression COMMA inner_lets"""
    p[0] = Let(p[4], p[6], p[8], p[10])

def p_inner_lets_simple(p):
    """inner_lets : ID DOUBLEDOT TYPE IN expression
       inner_lets : ID DOUBLEDOT TYPE COMMA inner_lets """
    p[0] = Let(p[1], p[3], None, p[5])

def p_inner_lets_initialized(p):
    """inner_lets : ID DOUBLEDOT TYPE ARROW expression IN expression
       inner_lets : ID DOUBLEDOT TYPE ARROW expression COMMA inner_lets"""
    p[0] = Let(p[1], p[3], p[5], p[7])

def p_expression_case(p):
    """expression : CASE expression OF case_list ESAC"""
    p[0] = Case(p[2], p[4])

def p_case_list_one(p):
    """case_list : case"""
    p[0] = [p[1]]

def p_case_list_many(p):
    """case_list : case_list case"""
    p[0] = p[1] + [p[2]]

def p_case_expr(p):
    """case : ID DOUBLEDOT TYPE EL expression DOTCOMMA"""
    p[0] = (p[1], p[3], p[5])

def p_expression_new(p):
    """expression : NEW TYPE"""
    p[0] = New(p[2])

def p_expression_isvoid(p):
    """expression : ISVOID expression"""
    p[0] = Isvoid(p[2])

def p_expression_neg(p):
    """expression : COMPLEMENT expression"""
    p[0] = Neg(p[2])

def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = Not(p[2])


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