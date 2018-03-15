import sys
from multiprocessing import Process

import web_server
import pc_side

PORT = 17828
    
def main():
    p = Process(target=web_server.server_main, 
                args=(PORT,),
                daemon=True)
    p.start()
    
    pc_side.pc_main('http://127.0.0.1:' + str(PORT))
    
if __name__ == '__main__':
    main()