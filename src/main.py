import asyncio
from gui.app import GUI
from launcher import run_server, stop_server

def main():
    gui = GUI(True, run_server, stop_server)
    gui.start_gui()

if __name__ == "__main__":
    main()