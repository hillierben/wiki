from markdown2 import Markdown

markdowner = Markdown()

markdowner.convert("*boo!*")
'<p><em>boo!</em></p>\n'
markdowner.convert("**boom!**")
'<p><strong>boom!</strong></p>\n'

with open("CSS.md", "r") as file:
    lines = file.readlines()

    list = []
    for line in lines: 
        converted = markdowner.convert(line)
        list.append(line)
    print(list)

    """
    with open("tmp.html", "w") as wfile:
        writer = wfile.writelines()
        for row in writer:
            writer.
    """
        