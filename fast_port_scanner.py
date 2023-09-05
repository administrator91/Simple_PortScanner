import socket, sys
import time, queue
import threading
import requests
import colorama
from colorama import Back, Fore, Style

colorama.init()

usage = "python3 simple_port_scanner.py TARGET START_PORT END_PORT THREADS"

print(Fore.GREEN+"*" * 66)
print(Fore.BLUE+f"Heyy Buddy!! This is a Simple Fast Port Scanner Made By {Fore.RED}_R{Fore.YELLOW}a{Fore.GREEN}j{Fore.BLUE}a{Fore.MAGENTA}r{Fore.RED}s{Fore.YELLOW}h{Fore.GREEN}i_")
print(Fore.CYAN+"Python Simple Port Scanner")
print(Fore.GREEN+"*" * 66)

target = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
thread_no = int(sys.argv[4])

result =Fore.RED+f"[+] Result:\n{Fore.GREEN}PORT\tSTATE\tSERVICE\n"

try:
    target = socket.gethostbyname(target)
except:
    print("[-] Host resolution failed.")
    exit()

print(Fore.RED+"[+] Scanning target: {}".format(target))

if not target or not str(start_port) or not end_port or not thread_no:
    print(usage)
    exit()

def get_banner(port, s):
    if (port == 80):
        response = requests.get("http://" + target)
        return response.headers['Server']
    try:
        return s.recv(1024).decode()
    except:
        return 'Not Found'

def scan_port(t_no):
    global result
    while not q.empty():
        port = q.get()
        print(Fore.BLUE+"Scanning for port {}..".format(port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            conn = s.connect_ex((target, port))
            if not conn:
                banner = get_banner(port, s)
                banner = ''.join(banner.splitlines())
                result += Fore.MAGENTA+f"{port}\tOPEN\t{banner}\n"
            s.close()
        except socket.gaierror as e:
            pass
        q.task_done()


q = queue.Queue()

start_time = time.time()

for j in range(start_port, end_port + 1):
    q.put(j)

for i in range(thread_no):
    t = threading.Thread(target= scan_port, args=(i,))
    t.start()

q.join()

end_time = time.time()
print(result)
print(Fore.YELLOW+"Time taken: {}".format(end_time - start_time))

with open("ports.txt", 'w') as file:
    file.write(f"Port scan results for target: {target}\n")
    file.write(result)
print(Fore.WHITE+"[+] Written to file ports.txt")




