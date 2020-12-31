import os
import sys
import platform

if platform.system() == "Darwin":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib/osx/pmdl"))
    from snowboy import *
elif platform.linux_distribution()[0] == "Ubuntu" and platform.linux_distribution()[1] == "16.04":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib/ubuntu64/pmdl"))
    from snowboy import *
else:
    raise ImportError("pmdl generator only runs on OSX or Ubuntu 16.04.")
