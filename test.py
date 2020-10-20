# -*- coding:utf-8 -*-
import base64
# print(base64.b64decode("N0NDRTc5OEUtNjkyMC00NjI2LUE4RDctMzUyQUUyQUMyODk5").decode())


from parse import *
a = findall(">{}<", "<p>the <b>bold</b> text</p>")
print(findall(">{}<", "<p>the <b>bold</b> text</p>"))

print(''.join(r[0] for r in findall(">{}<", "<p>the <b>bold</b> text</p>")))