import tkinter as tk
import asyncio

class GUI:

    def __init__(self, state, on_start, on_kill):
        self.on_start = on_start
        self.on_kill = on_kill
        self.root = tk.Tk()
        self.state = state # True = START, False = KILL
        self.busy = False
        self.root.protocol("WM_DELETE_WINDOW", self.handle_early_exit)
        self.frame = tk.Frame(self.root, bg="#f3ebdd", padx=10, pady=50)
        self.button = tk.Button(
            self.frame,
            command=self.handle_click
        )
        self.text = tk.Text(
                self.frame, 
                bg="#f3ebdd",
                bd=0,
                highlightthickness=0,
                relief="flat",
                height=3
            )
        self.localhost_textbox = tk.Text(
                self.frame, 
                bg="#f3ebdd",
                bd=0,
                highlightthickness=0,
                relief="flat",
                height=2,
                pady=20
            )
        self.lan_textbox = tk.Text(
                self.frame, 
                bg="#f3ebdd",
                bd=0,
                highlightthickness=0,
                relief="flat",
                height=2,
                pady=20
            )
        
        # high level setup
        GUI.setup(self.root)

        # frame setup
        self.frame.pack(fill="both", expand=True)

        # frame contents
        GUI.build_heading(self.frame) # MyLM Server

        # hosting info when active
        GUI.build_hosting_info(self.frame, self.localhost_textbox, "N/A", self.lan_textbox, "N/A")
        
        # usage button
        GUI.build_button(self.frame, self.state, self.button)

    def setup(root):
        root.title("MyLM")
        root.configure(bg="#f3ebdd")
        root.geometry("450x550+100+100")
        root.resizable(False, False)
        root.iconphoto(False, tk.PhotoImage(file="src/assets/logo.icns")) # change during packaging

    def build_heading(frame):
        text = tk.Text(
            frame, 
            bg="#f3ebdd",
            bd=0,
            highlightthickness=0,
            relief="flat",
            height=11
        )
        font_style = "Helvetica Neue"
        text.insert("end", "My", "1")
        text.tag_configure(
            "1",
            font=(font_style, 55, "italic"),
            foreground="#1f3a2e",
        )
        text.insert("end", "LM", "2")
        text.tag_configure(
            "2",
            font=(font_style, 55, "bold"),
            foreground="#1f3a2e",        
        )
        text.insert("end", " Server", "3")
        text.tag_configure(
            "3",
            font=(font_style, 55),
            foreground="#1f3a2e",
        )
        text.tag_configure("1", justify="center")
        text.config(state="disabled")
        text.bind("<Button-1>", lambda event: "break")
        text.bind("<Double-Button-1>", lambda event: "break")
        text.bind("<Triple-Button-1>", lambda event: "break")
        text.bind("<B1-Motion>", lambda event: "break")
        text.pack()

    def build_button(frame, state, button):
        if state:
            text = "Start Server"
        else:
            text = "Kill Server"
        button.config(
            font=("Helvetica Neue", 30),
            fg="#1f3a2e",
            text=text
        )
        button.place(
            x=215,
            y=375,
            width=200,
            height=70,
            anchor="center"
        )

    def build_hosting_info(frame, localhost_textbox, local_port, lan_textbox, lan_info):
        # build localhost info
        font_style = "PT Mono"
        localhost_textbox.insert("end", f"Localhost Port: {local_port}", "1")
        localhost_textbox.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        localhost_textbox.tag_configure("1", justify="center")
        localhost_textbox.config(state="disabled")
        localhost_textbox.pack_forget()

        # build lan info
        lan_textbox.insert("end", f"LAN: {lan_info}", "1")
        lan_textbox.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        lan_textbox.tag_configure("1", justify="center")
        lan_textbox.config(state="disabled")
        lan_textbox.pack_forget()

    def update_hosting_info(frame, localhost_textbox, local_port, lan_textbox, lan_info):
        # build localhost info
        localhost_textbox.config(state="normal")
        localhost_textbox.delete("1.0", "end")
        font_style = "PT Mono"
        localhost_textbox.insert("end", f"Port: {local_port}", "1")
        localhost_textbox.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        localhost_textbox.tag_configure("1", justify="center")
        localhost_textbox.config(state="disabled")
        localhost_textbox.pack_forget()

        # build lan info
        lan_textbox.config(state="normal")
        lan_textbox.delete("1.0", "end")
        lan_textbox.insert("end", f"LAN: {lan_info}", "1")
        lan_textbox.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        lan_textbox.tag_configure("1", justify="center")
        lan_textbox.config(state="disabled")
        lan_textbox.pack_forget()

    def start_gui(self):
        self.root.mainloop()

    def handle_click(self):
        if self.busy: # if button already clicked for same process, exit
            return
        # if waiting to start
        if self.state:
            self.busy = True # prevents double clicking button
            self.button.config(state="disabled")
            self.button.config(text="Working...")
            self.root.update()

            # run server, receive port info
            local_port, lan_info = asyncio.run(self.on_start())
            
            # update and display hosting info
            GUI.update_hosting_info(self.frame, self.localhost_textbox, local_port, self.lan_textbox, lan_info)
            self.localhost_textbox.pack()
            self.lan_textbox.pack()

            self.button.config(text="Kill Server")
            self.button.config(state="normal")
            
            self.root.update_idletasks()
            self.root.update()
            
            self.state = False # waiting to kill now
            self.busy = False # button action finished
            return
        else: # if waiting to kill
            self.busy = True
            self.button.config(state="disabled")
            self.button.config(text="Working...")
            self.root.update()
            self.on_kill()
            self.button.config(text="Start Server")
            self.button.config(state="normal")
            self.localhost_textbox.pack_forget()
            self.lan_textbox.pack_forget()
            self.root.update_idletasks()
            self.root.update()
            self.state = True
            self.busy = False
            return
        
    def handle_early_exit(self):
        if not self.state:
            self.handle_click()
        self.root.destroy()
