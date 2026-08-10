import asyncio
from gui.app import GUI

async def start_server():
    print("STARTING SERVER")
    await asyncio.sleep(2)
    print("STARTED")
    return(("8000", "192.193.20.30"))

async def kill_server():
    print("KILLING SERVER")
    await asyncio.sleep(2)
    print("KILLED")
    return("KILLED")

def k2():
    asyncio.run(start_server())


def main():
    models = ["Qwen 3.8 Max", "Llama"]
    gui = GUI(True, start_server, kill_server, models)
    gui.start_gui()


if __name__ == "__main__":
    main()

