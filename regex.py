from parse import Lexer, Parser, Token, State, NFA, Handler

def compile(p,location, debug = False):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t.name,t.value,t.loc)

    lexer = Lexer(p,location)
    parser = Parser(lexer)
    tokens = parser.parse()

    handler = Handler()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    for t in tokens:
        handler.handlers[t.name](t, nfa_stack)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 

