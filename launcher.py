import os
import sys
from multiprocessing import Process

from server import web_server
from pc import pc_side

PORT = 17828

# 集成包版本
FULL_VERSION = 4

# ting_py版本
# 改变这里后，也要改变pc_side.py里的current_ver
TING_VERSION = 3

def main():
    p = Process(target = web_server.server_main, 
                args = (PORT,),
                daemon = True)
    p.start()
    
    py_path = os.path.dirname(os.path.realpath(__file__))
    py_path = os.path.join(py_path, 'py34', 'python.exe')
    
    pc_side.pc_main('http://127.0.0.1:' + str(PORT),
                    py_path, FULL_VERSION)
    
if __name__ == '__main__':
    main()