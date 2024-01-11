import kindiast as ast

state = {}

def evaluate(state, action):
    if isinstance(action, ast.Literal):
        literal = action
        return literal.value

    elif isinstance(action, ast.Block):
        block = action
        new_state = evaluate(state, action.command)
        if action.next_block != None:
            evaluate(new_state, action.next_block)

    elif isinstance(action, ast.Assign):
        state[action.name] = action.value
        return (state, None)
    elif isinstance(action, ast.BinOp):
        left, right = evaluate(state, action.left), evaluate(state, action.right)
        if left.type != right.type:
            raise SyntaxError("tipos incompatives na operacao binop")
        elif action.optype == "+":
            return (state, left + right)
        elif action.optype == "-":
            return (state, left - right)
        elif action.optype == "*":
            return (state, left * right)
    elif isinstance(action, ast.Conditional):
        if evaluate(state, action.condition)[1]:
            evaluate(state, action.on_true)


evaluate(state, output_parser)