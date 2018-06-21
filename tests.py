import os
import pytest
from datetime import date
from ox.backend.python import as_expr, var, cond, OrExpr

mod = __import__(os.environ.get('TESTMOD', 'lispy'))

#
# Lexer
#
def test_comments_are_ignored():
    """
    Comentários comecam com um ponto e vírgula (";")
    """
    assert mod.evaluate(
        ';comentário\n'
        '42 ; mais comentário'
    ) == 42


def test_valid_variable_names():
    """
    Nomes de variáveis: letra ou underscore seguida sequência de letras, 
    underscores ou números
    """
    valid = ['x', '_', 'x1', 'Y', 'a_b_c', '_1']
    for name in valid:
        assert_good_tok(name, 'NAME')
        
    invalid = ['1x', 'x-y', '--x', 'x y']
    for name in invalid:
        assert_bad_tok(name, 'NAME')
        

def test_valid_strings():
    """
    Strings utilizam aspas duplas e não possuem caracter de escape.
    """
    valid = ['"foo"', '""', '"foo bar"', '" "']
    for name in valid:
        assert_good_tok(name, 'STRING')
        
    invalid = ['"""', '"\n"', '"']
    for name in invalid:
        assert_bad_tok(name, 'STRING')


#
# Parser
#
def test_evaluate_atomic_types():
    assert mod.evaluate('()') is None
    assert mod.evaluate('42') == 42.0
    assert mod.evaluate('"foo"') == "foo"


def test_list_of_items():
    """
    Comando do tipo (func arg1 arg2 ...)
    """
    assert mod.compile('(sqrt 4)') == "sqrt(4.0)"
    assert mod.compile('(+ 1 2)') == "read('+')(1.0, 2.0)"
    assert mod.parser(mod.lexer('(sqrt 4)')) == var.sqrt(4)
    assert mod.parser(mod.lexer('(+ 1 2)')) == var.read('+')(1, 2)


def test_let_command_parser():
    """
    Commando let é da forma (let <name> <expr1> <expr2>) e atribui o valor 
    da expr1 na expr2 utilizando o nome dado. A função "let" definida em Python
    será responsável por salvar o valor do segundo argumento em uma variável
    com o nome igual ao da variável passada como primeiro argumento.

    Exemplos: (let x 1 (+ 1 x))
    """
    assert mod.compile('(let x 1 x)') == "let('x', 1.0) or x"
    assert mod.parser(mod.lexer('(let x 1 x)')) == OrExpr(var.let('x', 1), var.x)


def test_if_command_parser():
    """
    Commando if é da forma (if <cond> <then> <else>). Cria uma expressão do
    tipo (<then> if <cond> else <else>)
    """
    assert mod.compile('(if x y z)') == "(y if x else z)"
    assert mod.parser(mod.lexer('(if x y z)')) == cond(var.y, if_=var.x, else_=var.z)


#
# Runtime
#
def test_read_function_in_runtime():
    """
    A função read() deve estar disponivel no dicionário de contexto dentro da
    função evaluate do runtime. Esta função recebe o valor dado como string e 
    retorna o valor da variável correspondente.
    """
    assert mod.evaluate('(let x 1 x)') == 1.0
    assert mod.evaluate('(let foo (+ 40 1) (+ foo 1))') == 42.0


#
# Testes de integração
#
def test_examples_1():
    assert mod.evaluate('(+ 1 (* 2 3))') == 7.0
    assert mod.evaluate('(if (< 1 2) "ok" "bad")') == "ok"


def test_examples_2():
    assert mod.evaluate('(let x 1 (+ x 1))') == 2.0
    assert mod.evaluate('(let x 1 (if (< x 2) "ok" "bad"))') == "ok"


#
# Helpers
#
def assert_good_tok(src, type, value=None):
    tk = mod.lexer(src)[0]
    assert tk.type == type
    assert tk.value == (src if value is None else value)


def assert_bad_tok(src, type):
    with pytest.raises((SyntaxError, AssertionError)):
        toks = mod.lexer(src)
        assert len(toks) == 1
        tok = toks[0]
        assert tok.type != type
    