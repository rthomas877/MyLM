from multiprocessing import Process
from server import start_server
import asyncio
import socket
import subprocess
import os
import socket as sock_mod

def get_wifi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable, this just forces the OS to pick the right network interface
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def port_open(port, host="127.0.0.1"):
    # returns True if we can access port, False o/w
    try:
        with sock_mod.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


# when running main, launcher is imported so this global var has its memory shared in the same process as main
server_process = None
# process for the actual llm to be run via llama.cpp
llm_process = None

async def run_server():
    global server_process
    global llm_process

    if llm_process is not None and llm_process.poll() is None:
        print("LLM already running")
    else:
        model_path = os.path.expanduser(
            "~/MyLM/models/Qwen3-8B-Q4_K_M.gguf"
        )

        llm_process = subprocess.Popen([
            "llama-server",
            "-m", model_path,
            "--port", "8080"
        ])
        

    counter = 0
    while not port_open(8080):
        if llm_process.poll() is not None:
            print("LLM process exited early")
            return None
        if counter > 30:  # give it real time, model loads can take a while
            print("LLM failed to start")
            return None
        await asyncio.sleep(2)
        counter += 1
    print("LLM running...")

    if server_process is not None and server_process.is_alive():
        print("Server already running")
        return

    # create new process to run server
    server_process = Process(target=start_server)
    server_process.start()

    print(f"Server PID: {server_process.pid}")

    counter = 0
    while not server_running():
        if counter > 5:
            break
        await asyncio.sleep(2)
        counter += 1
    if not server_running():
        print("Server failed to start")
        llm_process.terminate()
        llm_process.wait()
        return None

    return(("8000", get_wifi_ip()))


def stop_server():
    global server_process
    global llm_process

    if server_process is None and llm_process is None:
        return

    if server_process.is_alive():
        server_process.terminate()
        server_process.join()

    if llm_process.poll() is None:
        llm_process.terminate()
        llm_process.wait()

    llm_process = None


    server_process = None
    print("Server stopped")
    return


def server_running():
    return (
        server_process is not None
        and server_process.is_alive()
    )