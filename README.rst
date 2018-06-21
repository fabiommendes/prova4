Lispy
=====

Vamos implementar um parser completo para uma variante simples da venerável 
linguagem LISP. LISP é uma linguagem funcional criada no final dos anos 50 que 
possui uma das sintaxes mais simples e flexíveis dentre todas as linguagens de
programação.

Em LISP, todo código é representado por uma lista de argumentos que é 
interpretada como uma chamada de função::

    (+ 1 2)

No código acima, avaliamos a função "+" (primeiro argumento da lista) com os 
argumentos 1 e 2. Nosso compilador irá converter uma versão simplificada de 
LISP para Python.

Tipos básicos
-------------

Números tipo float: ``1.0, +1.0, 42, -42``
Strings: ``"foo", "", "foo bar", "*#&(&@@#@)"``
Nomes de variáveis: ``foo, bar, foo-bar, foo_bar, FooBar, foobar42``


Funções
-------

Aceita operadores matemáticos básicos (+, -, *, /) e operadores 
lógicos (<, >, <=, >=, =, !=), funções matemáticas (sqrt, sin, cos, ...). Estas 
funções estão definidas no dicionário "symbols" no arquivo lispy.py.


Comandos especiais
------------------

Todo comando LISP tem a estrutura de uma lista de argumentos (arg1 arg2 arg3 ...),
onde interpretamos o primeiro argumento como uma função e os valores seguintes
como sendo seus argumentos. Existem alguns comandos reservados, no entanto, que
precisam de um tratamento especial do compilador. Em Lispy temos dois deles::

    (let <varname> <value> <expr>) -- (let x (+ 1 2) (+ x 1))

No comando let, definimos uma variável no escopo global e depois avaliamos uma 
expressão que possivelmente pode utilizar a variável recém definida. Na expressão
do exemplo acima definimos x como (+ 1 2), ou seja 1 + 2 = 3, e depois avaliamos 
a expressão (+ x 1), ou seja x + 1, resultando em 4.

O outro comando é a avaliação condicional::

    (if <cond> <then> <else>) -- (if (= 0 (% x 2)) "par" "impar")

Neste caso, o primeiro argumento é uma condição (booleano), o segundo argumento
é executado em caso de sucesso (then) e o terceiro no caso de falha (else).


Rodando os testes
-----------------

Rode os testes com ``pytest tests.py``. A nota é o número de testes 
que passarem.

Dicas
.....

Se o Python padrão for o Python 2:
  ``python3 -m pytest tests.py``
Para limitar a saída do pytest ao primeiro erro: 
  ``pytest tests.py --maxfail=1``
Iniciar shell interativo: 
  ``python3 calculadora.py ARQUIVO``
Instalar dependências:
  ``pip3 install ox-parser pytest --user -U``

**Atenção:** Não funciona em Python 3.5.

Use o PPA para atualizar::

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.6
