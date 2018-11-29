import base64
open_icon = open("header.gif","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = ("header = '%s'"%b64str.decode())
f = open("header.py","w+")
f.write(write_data)
f.close()