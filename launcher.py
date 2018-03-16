import sys
from multiprocessing import Process

from server import web_server
from pc import pc_side

PORT = 17828

# 集成包版本
FULL_VERSION = 1

# ting_py版本
TING_VERSION = 1
    
def main():
    p = Process(target = web_server.server_main, 
                args = (PORT,),
                daemon = True)
    p.start()
    
    pc_side.pc_main('http://127.0.0.1:' + str(PORT),
                    FULL_VERSION, True)
    
if __name__ == '__main__':
    main()