import sys
import os
try:
    1/0
except Exception as e:
    print("SystemExit caught") 
    os._exit(1)
finally:
    print("finally")