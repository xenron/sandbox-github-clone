INDENT = ' '*2

def print_with_indent(message, repeat):
    print('{nest}{message}'.format(nest=INDENT*repeat, message=message))