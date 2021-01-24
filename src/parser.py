def tokenizer(input: str) -> list:
    tokens = []
    current = ""
    i = 0
    input = input.replace('\n', ' ')
    while (i < len(input)):
        if input[i] == '(':
            if (current != ""):
                tokens.append(current)
                current = ""
            tokens.append('(')
            i += 1
        elif input[i] == ')':
            if (current != ""):
                tokens.append(current)
                current = ""
            tokens.append(')')
            i += 1
        elif input[i] == ' ':
            if (len(current) > 0):
                tokens.append(current)
                current = ""
            while input[i] == ' ':
                i += 1
        else:
            current += input[i]
            i += 1

    return tokens


def accept(tok: str, input: list):
    return (len(input) > 0 and input[0] == tok)


def is_int(s: str):
    if len(s) == 1:
        return s[0] in "0123456789"

    return (s[0] in "0123456789") and is_int(s[1:])


def parse_sexpr(level, input: list):
    content = []

    if len(input) == 0:
        return (None, "")

    if accept('(', input):
        (res, next) = parse_sexpr(level + 1, input[1:])
        while (res != None and len(next) >= 0):
            content.append(res)
            (res, next) = parse_sexpr(level + 1, next)
        if accept(')', next):
            return (content, next[1:])
        else:
            print("Closing parenthesis expected !")
            return (None, input)

    if accept(')', input):
        return (None, input)

    if is_int(input[0]):
        return (int(input[0]), input[1:])

    return (input[0], input[1:])


def eval_arith(arith, env):
    if type(arith) == int:
        return arith
    if type(arith) == list:
        if len(arith) == 0:
            return 0
        if arith[0] == '+':
            s = 0
            for v in arith[1:]:
                s += eval_arith(v, env)
            return s
        if arith[0] == '*':
            s = 1
            for v in arith[1:]:
                s *= eval_arith(v, env)
            return s
    if type(arith) == str:
        if arith in env:
            return env[arith[0]]
        else:
            print(f"Undeclared variable {arith[0]}!")
            quit()
    print(f"Invalid arithmetic expression {arith}")
    quit()


def eval_bool(prog, env):
    return (eval_arith(prog[1], env) < eval_arith(prog[2], env))


def eval(prog, env):
    for s in prog:
        if s[0] == "affect":
            env[s[1]] = eval_arith(s[2], env)
        elif s[0] == "while":
            while eval_bool(s[1], env):
                eval(s[2:], env)


prog = """
(
    (affect a  1)
    (affect b 10)
    (affect sum (* 9 (+ 1 1)))
    (while (< a b)
        (affect a (+ a 1)) 
    )
)"""

parsed, _ = parse_sexpr(0, tokenizer(prog))
env = {}
eval(
    parsed,
    env
)
print(env)