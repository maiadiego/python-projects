from yacc import Class, Method, Attr, Id, Int, Str, Block, Assign, \
        Dispatch, StaticDispatch, Plus, Sub, Mult, Div, Lt, Le, Eq, \
        If, While, Let, Case, New, Isvoid, Neg, Not, Bool
from collections import defaultdict
import warnings
from copy import deepcopy


"""
# Análise Semântica

## Verificações
  1. Todos os identificadores são declarados
  2. Tipos
  3. Relações de herança
  4. Classes definidas apenas uma vez (não pode mais de uma vez)
  5. Métodos em uma classe definida apenas uma vez (não pode mais de uma vez)
  6. Os identificadores reservados não são usados ​​indevidamente

## Passos de Análise Semântica
  1. Reunir todos os nomes de classe
  2. Reunir todos os nomes de identificadores.
  3. Certificar de que nenhum identificador não declarado seja referenciado
  4. Certificar de que nenhuma classe não declarada seja referenciada
  3. Certificar de que todas as Regras de Escopo sejam atendidas 
  4. Realizar o Type Checking
"""

# geradores de erros 

class SemantError(Exception):
    pass


class SemantWarning(Warning):
    pass


def constroi_classes_base(ast):
    """ Inicializa todas as classe internas de COOL: Object, IO, Int, Bool and String.
        Pág 13 manual """

    objclass = Class(name="Object", parent=None, feature_list=[
        # aborta o programa com uma mensagem de erro
        Method('abort', [], 'Object', None),
        # retorna uma string com o nome da classe do objeto
        Method('type_name', [], 'String', None),
        # faz uma cópia superficial do objeto
        Method('copy', [], 'SELF_TYPE', None),
    ])
    ioclass = Class(name="IO", parent="Object", feature_list=[
        Method('out_string', [('arg', 'String')],
               'SELF_TYPE', None),  # printa o argumento
        Method('out_int', [('arg', 'Int')],
               'SELF_TYPE', None),  # printa um inteiro
        # lê uma string de uma entrada padrão (stdio)
        Method('in_string', [], 'String', None),
        Method('in_int', [], 'Int', None),  # lê um inteiro de stdio
    ])
    intclass = Class(name="Int", parent="Object", feature_list=[
        # não há métodos especiais. Inicialização default é 0 (not void)
        Attr('_val', '_prim_slot', None)
    ])
    stringclass = Class(name="String", parent="Object", feature_list=[
        # inicialização default é string vazia "" (not void)
        Attr('_val', 'Int', None),
        Attr('_str_field', '_prim_slot', None),
        Method('length', [], 'Int', None),  # retorna o tamanho da string
        # retorna string concatenada com um arg
        Method('concat', [('arg', 'String')], 'String', None),
        Method('substr', [('arg1', 'Int'), ('arg2', 'Int')],
               'String', None),  # subseleção de strings
    ])
    boolclass = Class("Bool", "Object", [
        # não há métodos especiais. Inicialização default é true ou false (not void)
        Attr('_val', '_prim_slot', None)
    ])
    ast += [objclass, ioclass, intclass, boolclass, stringclass]
    return ast 


def constroi_arvore_de_heranca(ast):
    """ Construção da tabela de símbolos e do gráfico de heranças """

    global classes_dict, inheritance_tree  # dicionários que vão ser usados por todas as funções
    classes_dict = {}
    inheritance_tree = defaultdict(set)  # formato {'classname': {'childclass1', 'childclass2'}}
    for cl in ast:
        if cl.name in classes_dict:
            raise SemantError("classe '%s' já definida" % cl.name)
        
        classes_dict[cl.name] = cl
        
        if cl.name == "Object":
            continue                                # classe Object não tem uma classe mãe
        
        inheritance_tree[cl.parent].add(cl.name)
    
    #print(classes_dict)
    #print("\n\n")
    #print(inheritance_tree)

  
def checa_classes_indefinidas():
    initial_parents = list(inheritance_tree.keys())
    for parentc in initial_parents:
        if parentc not in classes_dict and parentc != "Object":
            warnings.warn("classes '%s' herdam de uma classe pai indefinida '%s'" % (inheritance_tree[parentc], parentc), SemantWarning)
            inheritance_tree['Object'] |= inheritance_tree[parentc]  # classe intermediária não existe, então faça com que essas classes herdem de Object
            del inheritance_tree[parentc]


def impede_heranca_de_classes_base():
    for parent in ['String', 'Int', 'Bool']:
        for cl_name in inheritance_tree[parent]:
            raise SemantError("classe '%s' não pode herdar de uma classe base '%s'" % (cl_name, parent))


def visita_arvore_de_heranca(start_class, visited):
    visited[start_class] = True

    if start_class not in inheritance_tree.keys():
        return True

    for childc in inheritance_tree[start_class]:
        visita_arvore_de_heranca(childc, visited)

    return True


def checa_ciclos_de_heranca():
    visited = {}    # dicionário para marcar as classes visitadas
    for parent_name in inheritance_tree.keys():
        visited[parent_name] = False
        for cl_name in inheritance_tree[parent_name]:
            visited[cl_name] = False
    
    #print(visited)
    # Executa uma travessia em profundidade do gráfico de herança, altera o dict à medida que avança
    visita_arvore_de_heranca("Object", visited)
    
    #print(visited)

    for class_name,v in visited.items():
        if not v:
            raise SemantError("classe '%s' envolvida em um ciclo de herança" % class_name)


def checa_escopos_e_infere_tipos_de_retorno(cl):  # pega os valores de cada chave no dict
        # checa para cada classe de classes_dict(dicionário de classes do código fonte)
    """ Essa função faz checagem de escopo e inferência de tipo juntos, 
        porque o último é dependente do primeiro.
        
        Em COOL, métodos não estão no mesmo escopo de variável, o que 
        significa que nós podemos ter métodos com o mesmo nome de variáveis."""
    
    variable_scopes = [dict()]  # [{'attr':'tipo_attr'}]
    attr_seen = set()
    method_seen = set()
    
    for feature in cl.feature_list:     # cl é valor no dict
        if isinstance(feature, Attr):   # resgata os atributos dentro da lista de features de cada classe
            if feature.name in attr_seen:
                raise SemantError("atributo '%s' já está definido" % feature.name)
            
            attr_seen.add(feature.name)

            if feature.type == "SELF_TYPE":
                variable_scopes[-1][feature.name] = cl.name
            else:
                variable_scopes[-1][feature.name] = feature.type  # [-1] é o último escopo
    
    #print(variable_scopes)
    #print(attr_seen)
    #print(method_seen)
    
    # for feature in cl.feature_list:
    #     if isinstance(feature, Attr):
    #         #analisa_expressao(feature.body, variable_scopes, cl)  
    #         print("\n")
    
    for feature in cl.feature_list:     # cl é valor no dict
        if isinstance(feature, Method):   # varre os métodos e checa os parâmetros formais
            if feature.name in method_seen:
                raise SemantError("método '%s' já está definido" % feature.name)
            
            method_seen.add(feature.name)
            variable_scopes.append(dict())   # alterado - adicionando novo escopo como um dicio
            formals_seen = set()

            for formal in feature.formal_list:  # formal é uma tupla representado um parametro de um método
                if formal in formals_seen:
                    raise SemantError("formal '%s' no método '%s' já está definido" % (formal[0], feature.name))
                
                formals_seen.add(formal)
                variable_scopes[-1][formal[0]] = formal[1]  # {nome_attr: tipo_attr}         talvez mudar  

            analisa_expressao(feature.body, variable_scopes, cl)  
            #variable_scopes.destroy_scope() # tem que mudar 
            del variable_scopes[-1] # alterado - deleta a última chave do dicio
            #print(formals_seen)
        elif isinstance(feature, Attr):
            analisa_expressao(feature.body, variable_scopes, cl)  
    
    #print(method_seen)
    #print(attr_seen)
    #print(variable_scopes)


def analisa_expressao(expression, variable_scopes, cl):
    if isinstance(expression, Isvoid):
        analisa_expressao(expression.body, variable_scopes, cl)
        expression.return_type = "Bool"
    
    elif any(isinstance(expression, X) for X in [Eq, Lt, Le]):
        analisa_expressao(expression.first, variable_scopes, cl)
        analisa_expressao(expression.second, variable_scopes, cl)
        expression.return_type = "Bool"
    
    elif isinstance(expression, Neg):
        analisa_expressao(expression.body, variable_scopes, cl)
        expression.return_type = "Int"
    
    elif isinstance(expression, Not):
        analisa_expressao(expression.body, variable_scopes, cl)
        expression.return_type = "Bool"
    
    elif any(isinstance(expression, X) for X in [Plus, Sub, Mult, Div]):
        analisa_expressao(expression.first, variable_scopes, cl)
        analisa_expressao(expression.second, variable_scopes, cl)
        expression.return_type = "Int"
    
    elif isinstance(expression, While):
        analisa_expressao(expression.predicate, variable_scopes, cl)
        analisa_expressao(expression.body, variable_scopes, cl)
    
    elif isinstance(expression, Let):
        # # LET cria um novo escopo
        # #variable_scopes.new_scope() # alterar aqui
        # variable_scopes.append(dict())   # alterado - adicionando novo escopo 
        # variable_scopes[expression.object] = expression.type
        # analisa_expressao(expression.init, variable_scopes, cl)
        # analisa_expressao(expression.body, variable_scopes, cl)
        # #variable_scopes.destroy_scope() 
        # del variable_scopes[-1] # alterado
        # expression.return_type = expression.body.return_type
        pass
    
    elif isinstance(expression, Block):
        last_type = None
        for expr in expression.body:
            analisa_expressao(expr, variable_scopes, cl)
            last_type = getattr(expr, 'return_type', None)
        expression.return_type = last_type
    
    elif isinstance(expression, Assign):
        analisa_expressao(expression.body, variable_scopes, cl)
        analisa_expressao(expression.name, variable_scopes, cl)
        expression.return_type = expression.name.return_type  
    
    elif isinstance(expression, Dispatch) or isinstance(expression, StaticDispatch):
        # analisa_expressao(expression.body, variable_scopes, cl)
        # for expr in expression.expr_list:
        #     analisa_expressao(expr, variable_scopes, cl)

        # # código redundante copiado de type_check, porque é preciso inferir o tipo
        # # de retorno dispatch do tipo de chamada do método

        # if expression.body == "self":
        #     bodycln = cl.name
        # else:
        #     bodycln = expression.body.return_type

        # called_method = None
        
        # if bodycln in classes_dict:
        #     bodycl = classes_dict[bodycln]
        #     for feature in bodycl.feature_list:
        #         if isinstance(feature, Method) and feature.name == expression.method:
        #             called_method = feature
        # if not called_method:
        #     raise SemantError("tentativa de chamar um método indefinido '%s' na classe '%s'" % (expression.method, bodycl.name))

        # if called_method.return_type == "SELF_TYPE":
        #     method_type = bodycl.name
        # else:
        #     method_type = called_method.return_type

        # expression.return_type = method_type
        pass
    
    elif isinstance(expression, If):
        # analisa_expressao(expression.predicate, variable_scopes, cl)
        # analisa_expressao(expression.then_body, variable_scopes, cl)
        # analisa_expressao(expression.else_body, variable_scopes, cl)
        # then_type = classes_dict[expression.then_body.return_type]
        # else_type = classes_dict[expression.else_body.return_type]
        # ret_type = menor_parente_comum(then_type, else_type)  
        # expression.return_type = ret_type
        pass

    elif isinstance(expression, Case):
        # analisa_expressao(expression.expr, variable_scopes, cl)
        # branch_types = []
        # for case in expression.case_list:
        #     #variable_scopes.new_scope()  
        #     variable_scopes.append(dict()) # alterado - cada branch de case tem seu próprio escopo
        #     variable_scopes[case[0]] = case[1]
        #     analisa_expressao(case[2], variable_scopes, cl)
        #     branch_types.append(classes_dict[case[2].return_type])
        # expression.return_type = menor_parente_comum(*branch_types)
        pass

    elif isinstance(expression, Id):
        # if expression.name == "self":
        #     expression.return_type = cl.name
        #     return
        # if expression.name not in variable_scopes:
        #     raise SemantError("variável '%s' não está no escopo" % expression.name)
        # expression.return_type = variable_scopes[expression.name]

        for scope in variable_scopes[::-1]:
            if expression.name == "self":
                expression.return_type = cl.name
                return
            if expression.name in scope:
                expression.return_type = scope[expression.name]
                return
        raise SemantError("variável '%s' não está no escopo" % expression.name)
    
    elif isinstance(expression, New):
        if expression.type == "SELF_TYPE":
            expression.return_type = cl.name
            return
        expression.return_type = expression.type
    
    elif isinstance(expression, Int):
        expression.return_type = "Int"
    
    elif isinstance(expression, Bool):
        expression.return_type = "Bool"
    
    elif isinstance(expression, Str):
        expression.return_type = "String"


def menor_parente_comum(*classes):
    """Retorna o parente comum mais baixo entre duas classes"""
    def ascend_tree(cl):
        yield cl.name
        if cl.parent:
            yield from ascend_tree(classes_dict[cl.parent])

    inheritance_paths = []
    for cl in classes:
        path = list(ascend_tree(cl))
        path.reverse()
        inheritance_paths.append(path)

    smallest_inheritance_path_length = min(len(x) for x in inheritance_paths)

    for step in range(smallest_inheritance_path_length):
        inheritance_points = [x[step] for x in inheritance_paths]
        if len(set(inheritance_points)) > 1:
            return inheritance_paths[0][step-1]  

    return classes[0].name          # se chegou aqui, os objetos tem o mesmo tipo


def expandir_classes_herdadas(start_class="Object"):
    """ Aplica as regras de herança através do dicionário de classes"""

    cl = classes_dict[start_class]
    
    if cl.parent:
        parentcl = classes_dict[cl.parent]

        attr_set_in_child = [i for i in cl.feature_list if isinstance(i, Attr)]
        attr_set_in_parent = [i for i in parentcl.feature_list if isinstance(i, Attr)]

        for attr in attr_set_in_child:
            for pattr in attr_set_in_parent:
                if attr.name == pattr.name:
                    raise SemantError("o atributo não pode ser redefinido na classe filha '%s'" % cl.name)

        method_set_in_child = [i for i in cl.feature_list if isinstance(i, Method)]
        method_set_in_parent = [i for i in parentcl.feature_list if isinstance(i, Method)]

        def extrai_assinaturas(method_set):
            method_signatures = {}
            for method in method_set:
                method_signatures[method.name] = {}
                for formal in method.formal_list:
                    method_signatures[method.name][formal[0]] = formal[1]
                method_signatures[method.name]['return'] = method.return_type
            return method_signatures

        method_signatures_for_child = extrai_assinaturas(method_set_in_child)
        method_signatures_for_parent = extrai_assinaturas(method_set_in_parent)

        methods_in_child = set()
        for method in method_set_in_child:
            methods_in_child.add(method.name)
            if method.name in method_signatures_for_parent:
                parent_signature = method_signatures_for_parent[method.name]
                child_signature = method_signatures_for_child[method.name]
                if parent_signature != child_signature:
                    raise SemantError("o método redefinido '%s' não pode alterar os argumentos ou o tipo de retorno do método pai" % method.name)

        # aplicar herança copiando as definições 
        # DEEPCOPY de sub-asts para evitar interferência com tipo de inferencia e
        # type checking (toda inferencia de tipo é armazenada dentro dos campos return_type
        # inserir em vez de anexar para que sejam avaliados anteriormente
        for method in method_set_in_parent:
            if method.name not in methods_in_child:
                new_method = deepcopy(method)
                new_method.inherited_from = cl.parent   # usado na geração de código, para reutilizar corpos de funções
                cl.feature_list.insert(0, new_method)
        for attr in attr_set_in_parent:
            cl.feature_list.insert(0, deepcopy(attr))

    # descer na árvore de herança aplicando a mesma função
    all_children = inheritance_tree[start_class]
    for child in all_children:
        expandir_classes_herdadas(child)


def type_check(cl):
    """Verifica se o tipo inferido coincide com o tipo declarado"""
    for feature in cl.feature_list:
        if isinstance(feature, Attr):
            if feature.type == "SELF_TYPE":
                realtype = cl.name
            else:
                realtype = feature.type

            if feature.body:
                type_check_expression(feature.body, cl)
                childcln = feature.body.return_type
                parentcln = realtype
                if not is_child(childcln, parentcln):
                    raise SemantError("tipo inferido '%s' para o atributo '%s' não coincide com o tipo declarado '%s'" % (childcln, feature.name, parentcln))
        
        elif isinstance(feature, Method):
            for formal in feature.formal_list:
                if formal[1] == "SELF_TYPE":
                    raise SemantError("formal %s não pode ter o tipo SELF_TYPE" % formal[0])
                elif formal[1] not in classes_dict:
                    raise SemantError("formal %s tem um tipo indefinido" % formal[0])

            if feature.return_type == "SELF_TYPE":
                realrettype = cl.name
            else:
                realrettype = feature.return_type

            if feature.body is None:
                # para classes internas, o corpo de alguns métodos não está definido
                # assume que eles retornam SELF_TYPE
                if feature.return_type == "SELF_TYPE":
                    returnedcln = cl.name
                else:
                    returnedcln = feature.return_type
            else:
                type_check_expression(feature.body, cl)
                returnedcln = feature.body.return_type

            declaredcln = realrettype
            if returnedcln is None:
                warnings.warn("conteúdo não digitado para o método '%s' com tipo declarado '%s'" % (feature.name, declaredcln), SemantWarning)
            else:
                if not is_child(returnedcln, declaredcln):
                    raise SemantError("tipo inferido '%s' para o método '%s' não coincide com o tipo declarado '%s'" % (returnedcln, feature.name, declaredcln))



def type_check_expression(expression, cl):
    """verificar se os tipos validam em qualquer ponto da ast"""
    if isinstance(expression, Case):
        type_check_expression(expression.expr, cl)
        for case in expression.case_list:
            type_check_expression(case[2], cl)
    
    elif isinstance(expression, Assign):
        type_check_expression(expression.body, cl)
        if not is_child(expression.body.return_type, expression.name.return_type):
            raise SemantError("o tipo inferido '%s' para '%s' não coincide com o tipo declarado '%s'" % (expression.body.return_type, expression.name.name, expression.name.return_type))
    
    elif isinstance(expression, If):
        type_check_expression(expression.predicate, cl)
        type_check_expression(expression.then_body, cl)
        type_check_expression(expression.else_body, cl)
        if expression.predicate.return_type != "Bool":
            raise SemantError("declarações IF devem ter condições booleanas")
    
    elif isinstance(expression, Let):
        type_check_expression(expression.init, cl)
        if expression.init:  # algumas expressões let auto-initializam com valores padrão
            if not is_child(expression.init.return_type, expression.type):
                raise SemantError("o tipo inferido '%s' para let init não coincide com o tipo declarado '%s'" % (expression.init.return_type, expression.type))
    
    elif isinstance(expression, Block):
        for line in expression.body:
            type_check_expression(line, cl)
    
    elif isinstance(expression, Dispatch) or isinstance(expression, StaticDispatch):
        type_check_expression(expression.body, cl)
        # despachar para a instância atual(self)
        if expression.body == "self":
            bodycln = cl.name
        else:
            bodycln = expression.body.return_type
        if isinstance(expression, StaticDispatch):
            # checagem adicional em static dispatch
            if not is_child(bodycln, expression.type):
                raise SemantError("expressão static dispatch (antes @Type) não coincide com o tipo declarado {}".format(expression.type))

        called_method = None
        if bodycln in classes_dict:
            bodycl = classes_dict[bodycln]
            for feature in bodycl.feature_list:
                if isinstance(feature, Method) and feature.name == expression.method:
                    called_method = feature
        if not called_method:
            raise SemantError("Tentativa de chamar um método indefinido %s na classe %s" % (expression.method, bodycl.name))
        if len(expression.expr_list) != len(called_method.formal_list):
            raise SemantError("Tentativa de chamar o método {} na classe {} com o número incorreto de argumentos".format(called_method.name, bodycl.name))
        else:
            # checar se os argumentos coincidem
            for expr, formal in zip(expression.expr_list, called_method.formal_list):
                if not is_child(expr.return_type, formal[1]):
                    raise SemantError("Argumento {} passado para o método {} na classe {} não coincide com sua {} declaração".format(expr.return_type, called_method.name, bodycl.name, formal[1]))
    
    elif isinstance(expression, While):
        type_check_expression(expression.predicate, cl)
        type_check_expression(expression.body, cl)
        if expression.predicate.return_type != "Bool":
            raise SemantError("Declaração While deve ter condições booleanas")
    
    elif isinstance(expression, Isvoid):
        type_check_expression(expression.body, cl)
    
    elif isinstance(expression, Not):
        type_check_expression(expression.body, cl)
        if expression.body.return_type != "Bool":
            raise SemantError("Declaração NOT requer valores booleanos")
    
    elif isinstance(expression, Lt) or isinstance(expression, Le):
            type_check_expression(expression.first, cl)
            type_check_expression(expression.second, cl)
            if expression.first.return_type != "Int" or expression.second.return_type != "Int":
                raise SemantError("Argumentos não inteiros não podem ser verificados com < == ou <=")
        
    elif isinstance(expression, Complement):
        type_check_expression(expression.body, cl)
        if expression.body.return_type != "Int":
            raise SemantError("Declaração negativa requer valores inteiros")
    
    elif any(isinstance(expression, X) for X in [Plus, Sub, Mult, Div]):
        type_check_expression(expression.first, cl)
        type_check_expression(expression.second, cl)
        if expression.first.return_type != "Int" or expression.second.return_type != "Int":
            raise SemantError("Operações aritiméticas requerem inteiros")
    
    elif isinstance(expression, Eq):
        type_check_expression(expression.first, cl)
        type_check_expression(expression.second, cl)
        type1 = expression.first.return_type
        type2 = expression.second.return_type
        if (type1 == "Int" and type2 == "Int") or \
           (type1 == "Bool" and type2 == "Bool") or \
           (type1 == "String" and type2 == "String"):
            pass  # comparar tipos básicos juntos ok 
        else:
            raise SemantError("A comparação somente é possível entre os mesmos tipos base")


def is_child(childclname, parentclname):
    """checa se childcl é um descendente de parentcl"""
    if childclname == parentclname:
        return True
    for clname in inheritance_tree[parentclname]:
        if is_child(childclname, clname):
            return True
    return False


def semant(ast):
    constroi_classes_base(ast)
    constroi_arvore_de_heranca(ast)
    checa_classes_indefinidas()
    impede_heranca_de_classes_base()
    checa_ciclos_de_heranca()
    expandir_classes_herdadas()
    
    for cl in classes_dict.values():
    #   #print(cl)
    #   print("\n\n")
        checa_escopos_e_infere_tipos_de_retorno(cl)
        #print("\n")

    #print(classes_dict)
    # print("\n\n")
    # for cl in classes_dict.values():
    #     #type_check(cl)
    #     print(cl.feature_list)
    #     print("\n")
    # #return classes_dict  
    #print(classes_dict)


if __name__ == '__main__':
    import sys
    from yacc import parser

    with open(sys.argv[1], 'r') as f:
        ast = parser.parse(f.read())

        if ast is None:
             print("Cannot parse!")
        else:
            try:
                #classes_dict = semant(ast)
                semant(ast)
            except SemantError as e:
                print("Semantic Error: %s" % str(e))
            else:
                print("Semantic sucessful!")

        