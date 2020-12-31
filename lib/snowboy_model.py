import platform

if platform.system() == "Darwin":
    from osx.pmdl.snowboy import *
elif platform.linux_distribution()[0] == "Ubuntu" and platform.linux_distribution()[1] == "16.04":
    from ubuntu64.pmdl.snowboy import *
else:
    raise ImportError("pmdl generator only runs on OSX or Ubuntu 16.04.")
