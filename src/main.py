#runs worksheet maker functions in an interactive session
# $ python main.py    (from /Users/chris/GitHub/mathai/src directory)
import sys
import os
from makedoc import makedoc, makeset
from loadstandards import print_tree

print("running worksheet generator")
arg = input("Type anything to run: ")

standards = loadstandards()
bank = loadbank(standards)
makedoc(bank)

print("done. look for newfile.tex in out folder")

#for dir in sys.path:
#    print(dir)
