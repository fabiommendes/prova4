import ox
from ox.helpers import identity, cons, singleton, clean_string
from ox.backend.python import as_expr, var, cond, OrExpr
import operator as op
import math


# Parser -----------------------------------------------------------------------
def make_parser():
    return ox.make_parser([
        ("expr : NUMBER", lambda x: as_expr(float(x))),
        ("expr : STRING", lambda x: as_expr(clean_string(x))),
        ("expr : NAME", var),
        ("expr : SYMBOL", var.read),
        ("expr : 'if'", handle_if),
        ("expr : 'let'", handle_let),
        ("expr : '(' 'items' ')'", handle_eval),
    ])


def handle_if(test, then, other):
    raise NotImplementedError

def handle_eval(items):
    raise NotImplementedError

def handle_let(name, value, expr):
    raise NotImplementedError


# Lexer ------------------------------------------------------------------------
def make_lexer():
    return ox.make_lexer([
        ('CONTROL', r'[()]'),
        ('NUMBER', r'[-+]?\d+(\.\d+)?'),
        ('SYMBOL', r'[-+*/!~@#$%&=?<>.,^]+'),
        ('NAME', r'[a-z]+'),
        ('STRING', r'"..."'),
        ('_COMMENT', r';...'),

        # Palavras reservadas
        ('r_IF', 'if'),
        ('r_LET', 'let'),   
    ])


# Converte para Python ---------------------------------------------------------
lexer = make_lexer()
parser = make_parser()


def compile(src, debug=False):
    tokens = lexer(src)
    ast = parser(tokens)
    py_code = ast.source()
    if debug:
        print('PYTHON:', py_code)
    return py_code


# Runtime ----------------------------------------------------------------------
symbols = {
    # Aritméticos
    '+': op.add, '*': op.mul, '-': op.sub, '/': op.truediv, '**': op.pow,

    # Lógicos
    '<': op.lt, '>': op.gt, '<=': op.ge, '>=': op.le, '=': op.eq, '!=': op.ne,

    # Todos os símbolos do módulo math
    **vars(math),
}


def evaluate(src, debug=False):
    # Lê variável do dicionário de contexto
    #
    # Dica: não implemente a função no escopo global pois ela precisa ter 
    # acesso à variável de contexto criada localmente. Isto é conhecido em 
    # programação como uma "closure".
    def read(x):
        raise NotImplementedError('implemente a função read!')
    
    # Salva variável no dicionário de contexto
    def let(name, value):
        context[name] = value

    # Cria código Python
    py_src = compile(src, debug)
    
    # Cria dicionário com variáveis globais do runtime do Lispy.
    # Aqui devemos registrar todos os operadores e nomes disponíveis globalmente
    # em Lispy (ex.:, as funções read e let definidas acima)
    context = {}
    # ...

    # Avalia o resultado
    result = eval(py_src, context)
    
    # Retorna resultado
    if debug:
        print('RESULT:', result, end='\n\n')
    return result


# Main -------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        src = input('$ ')
        if not src:  
            if input('Sair (s/n)? ') == 's':
                raise SystemExit(0)
        else:
            ctx = evaluate(src, debug=True)
