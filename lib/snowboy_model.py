import platform

if platform.system() == "Darwin":
    from osx.snowboy import *
else:
    from ubuntu64.snowboy import *
