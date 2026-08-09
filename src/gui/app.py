import tkinter as tk

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

def build_model_selection(active, frame, model_list):
    if active:
        # build "Model: "
        text = tk.Text(
            frame, 
            bg="#f3ebdd",
            bd=0,
            highlightthickness=0,
            relief="flat",
            height=3
        )
        font_style = "Helvetica Neue"
        text.insert("end", "Model:", "1")
        text.tag_configure(
            "1",
            font=(font_style, 30),
            foreground="#1f3a2e",
        )
        text.tag_configure("1", justify="center")
        text.config(state="disabled")
        text.bind("<Button-1>", lambda event: "break")
        text.bind("<Double-Button-1>", lambda event: "break")
        text.bind("<Triple-Button-1>", lambda event: "break")
        text.bind("<B1-Motion>", lambda event: "break")
        text.pack()

        # build dropdown
        selected = tk.StringVar(value=model_list[0])

        dropdown = tk.OptionMenu(
            frame,
            selected,
            *model_list
        )

        dropdown.config(
            font=("PT Mono", 18),
            width=40,
            fg="#1f3a2e",
        )
        dropdown["menu"].config(
            font=("PT Mono", 18),
            fg="#1f3a2e",
        )

        dropdown.pack()

def build_button(frame, text):
    button = tk.Button(
        frame, 
        text=text
    )
    button.config(
        font=("Helvetica Neue", 30),
        fg="#1f3a2e"
    )
    button.place(
        x=215,
        y=375,
        width=200,
        height=70,
        anchor="center"
    )

def build_hosting_info(active=False, frame=None, local_port="N/A", lan_info="N/A"):
    if active:
        # build localhost info
        text = tk.Text(
            frame, 
            bg="#f3ebdd",
            bd=0,
            highlightthickness=0,
            relief="flat",
            height=2,
            pady=20
        )
        font_style = "PT Mono"
        text.insert("end", f"Localhost Port: {local_port}", "1")
        text.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        text.tag_configure("1", justify="center")
        text.config(state="disabled")
        text.bind("<Button-1>", lambda event: "break")
        text.bind("<Double-Button-1>", lambda event: "break")
        text.bind("<Triple-Button-1>", lambda event: "break")
        text.bind("<B1-Motion>", lambda event: "break")
        text.pack()

        # build lan info
        text = tk.Text(
            frame, 
            bg="#f3ebdd",
            bd=0,
            highlightthickness=0,
            relief="flat",
            height=2
        )
        text.insert("end", f"LAN: {lan_info}", "1")
        text.tag_configure(
            "1",
            font=(font_style, 20),
            foreground="#1f3a2e",
        )
        text.tag_configure("1", justify="center")
        text.config(state="disabled")
        text.bind("<Button-1>", lambda event: "break")
        text.bind("<Double-Button-1>", lambda event: "break")
        text.bind("<Triple-Button-1>", lambda event: "break")
        text.bind("<B1-Motion>", lambda event: "break")
        text.pack()

def start_gui():
    # initial window creation
    root = tk.Tk()
    
    # high level setup
    setup(root)

    # frame setup
    frame = tk.Frame(root, bg="#f3ebdd", padx=10, pady=50)
    frame.pack(fill="both", expand=True)

    # frame contents
    build_heading(frame) # MyLM Server

    # buils dropdown when server not running
    models = ["Qwen 3.8 Max", "Llama", "Mistral"]
    build_model_selection(False, frame, models)

    # hosting info when active
    build_hosting_info(True, frame, "8000", "192.921.20.20")
    
    # usage button
    build_button(frame, "Kill Server")

    # launch gui
    root.mainloop()


if __name__ == "__main__":
    start_gui()