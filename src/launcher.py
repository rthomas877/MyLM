from multiprocessing import Process
from server import start_server
import asyncio
import socket

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

server_process = None

async def run_server():
    global server_process

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
        return None

    return(("8000", get_wifi_ip()))


def stop_server():
    global server_process

    if server_process is None:
        return

    if server_process.is_alive():
        server_process.terminate()
        server_process.join()

    server_process = None
    print("Server stopped")
    return


def server_running():
    return (
        server_process is not None
        and server_process.is_alive()
    )