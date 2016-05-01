#!/usr/bin/env python
# -*- coding : utf-8 -*-

import re,sys

INDENT_STR="    "
indent_more_re=re.compile("^\s*(while|for|if|function|sub|do|private|public)(?!.*\sthen\s+\S+).*",re.I)
indent_less_re=re.compile("^\s*(wend|loop|end|next).*",re.I)

def vb_indent(src_code):
    indent_num = 0
    result_code = ""
    for line in src_code.splitlines():
        if indent_less_re.match(line) and indent_num > 0:
            indent_num -= 1
        result_code += "{indent}{line}\n".format(indent=indent_num*INDENT_STR,line=line.strip())
        if indent_more_re.match(line):
            indent_num += 1
    return result_code

def main():
    if len(sys.argv) != 3:
        print("usage: {self_name} source target\nauto_indent for Visual BASIC".format(self_name=sys.argv[0]))
    try:
        source=open(sys.argv[1],"r")
        target=open(sys.argv[2],"w")

        target.write(vb_indent(source.read()))
    except IOError:
        print("file open failed.")
if __name__ == "__main__":
    main()
