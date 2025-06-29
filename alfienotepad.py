import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time
import os
import math

AUTO_SAVE_INTERVAL = 60  # seconds
SAVE_DIR = "versions"
session_start_time = time.time()

# Start Root Window 
root = ttk.Window(themename="darkly")
root.title("📝 Alfie Notepad Pro")
root.geometry("700x700")
default_font = ("Verdana", 10)

# Now safe to create BooleanVar
show_line_numbers = tk.BooleanVar(value=True)

# Login System 
def launch_notepad():
    login_frame.destroy()
    main_app()

def verify_login():
    if username_entry.get() == "admin" and password_entry.get() == "1234":
        launch_notepad()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

# Login Frame 
login_frame = ttk.Frame(root, padding=30)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

login_title = ttk.Label(login_frame, text="alfie's notepad pro", font=("Verdana", 16, "bold"))
login_title.pack(pady=20)

username_entry = ttk.Entry(login_frame, font=default_font, width=30)
username_entry.insert(0, "Username")
username_entry.pack(pady=10)

password_entry = ttk.Entry(login_frame, font=default_font, width=30, show="*")
password_entry.insert(0, "1234")
password_entry.pack(pady=10)

login_btn = ttk.Button(login_frame, text="Login", command=verify_login, bootstyle="success")
login_btn.pack(pady=20)

# === Rainbow Bar ===
def add_rainbow_gradient_bar(parent):
    canvas = tk.Canvas(parent, height=3, highlightthickness=0, bd=0)
    canvas.pack(fill="x")
    width = parent.winfo_screenwidth()
    gradient = tk.PhotoImage(width=width, height=3)
    for x in range(width):
        r = int(127.5 * (1 + math.sin(x * 0.02)))
        g = int(127.5 * (1 + math.sin(x * 0.02 + 2)))
        b = int(127.5 * (1 + math.sin(x * 0.02 + 4)))
        color = f"#{r:02x}{g:02x}{b:02x}"
        gradient.put(color, to=(x, 0, x+1, 3))
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

add_rainbow_gradient_bar(root)

# === Game ===
def launch_game():
    game_window = ttk.Toplevel(root)
    game_window.geometry("400x450")
    game_window.resizable(False, False)
    current_player = ["X"]
    board = ["" for _ in range(9)]

    def check_winner():
        win = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in win:
            if board[a] == board[b] == board[c] != "":
                return board[a]
        return "Draw" if "" not in board else None

    def handle_click(i):
        if board[i] == "" and not check_winner():
            board[i] = current_player[0]
            buttons[i].config(text=current_player[0], state="disabled")
            winner = check_winner()
            if winner:
                result_label.config(text=f"Winner: {winner}" if winner != "Draw" else "Draw")
            else:
                current_player[0] = "O" if current_player[0] == "X" else "X"

    def reset_game():
        for i in range(9):
            board[i] = ""
            buttons[i].config(text="", state="normal")
        current_player[0] = "X"
        result_label.config(text="")

    board_frame = ttk.Frame(game_window, padding=10)
    board_frame.pack()
    buttons = []
    for i in range(9):
        btn = ttk.Button(board_frame, text="", width=6, command=lambda i=i: handle_click(i), bootstyle="secondary")
        btn.grid(row=i//3, column=i%3, padx=5, pady=5, ipadx=10, ipady=10)
        buttons.append(btn)

    result_label = ttk.Label(game_window, text="", font=("Verdana", 12))
    result_label.pack(pady=10)
    reset_btn = ttk.Button(game_window, text="Reset", command=reset_game, bootstyle="warning")
    reset_btn.pack()

# === Main App ===
def main_app():
    def new_tab():
        frame = create_tab()
        tab_control.add(frame, text="Untitled")
        tab_control.select(frame)

    def open_file():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return
        with open(path, "r") as file:
            content = file.read()
        frame = create_tab()
        get_text_widget(frame).insert(tk.END, content)
        tab_control.add(frame, text=os.path.basename(path))
        tab_control.select(frame)

    def save_file():
        current_tab = tab_control.select()
        if not current_tab:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            content = get_text_widget(tab_control.nametowidget(current_tab)).get("1.0", tk.END)
            with open(path, "w") as file:
                file.write(content)
            tab_control.tab(current_tab, text=os.path.basename(path))

    def exit_app():
        root.quit()

    def show_about():
        messagebox.showinfo("About", "📝 Alfie Notepad Pro\nAdvanced features enabled\nMade for the people")

    def change_theme(theme):
        root.style.theme_use(theme)

    def auto_save():
        os.makedirs(SAVE_DIR, exist_ok=True)
        for tab_id in tab_control.tabs():
            frame = tab_control.nametowidget(tab_id)
            text = get_text_widget(frame).get("1.0", tk.END)
            filename = tab_control.tab(tab_id, option="text").replace(" ", "_") or "Untitled"
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            with open(f"{SAVE_DIR}/{filename}_{timestamp}.txt", "w") as f:
                f.write(text)
        root.after(AUTO_SAVE_INTERVAL * 1000, auto_save)

    menubar = tk.Menu(root, font=default_font)
    file_menu = tk.Menu(menubar, tearoff=0, font=default_font)
    file_menu.add_command(label="New Tab", command=new_tab)
    file_menu.add_command(label="Open File", command=open_file)
    file_menu.add_command(label="Save As", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)
    menubar.add_cascade(label="File", menu=file_menu)

    theme_menu = tk.Menu(menubar, tearoff=0, font=default_font)
    for theme in ["darkly", "superhero", "solar", "flatly", "minty", "journal"]:
        theme_menu.add_command(label=theme.capitalize(), command=lambda t=theme: change_theme(t))
    menubar.add_cascade(label="Themes", menu=theme_menu)

    help_menu = tk.Menu(menubar, tearoff=0, font=default_font)
    help_menu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=help_menu)

    extras_menu = tk.Menu(menubar, tearoff=0, font=default_font)
    extras_menu.add_command(label="Naughts & Crosses", command=launch_game)
    menubar.add_cascade(label="Games", menu=extras_menu)

    view_menu = tk.Menu(menubar, tearoff=0, font=default_font)
    view_menu.add_checkbutton(label="Show Line Numbers", variable=show_line_numbers, command=lambda: update_all_line_numbers(force=True))
    menubar.add_cascade(label="View", menu=view_menu)

    root.config(menu=menubar)

    global tab_control
    tab_control = ttk.Notebook(root)
    tab_control.pack(fill="both", expand=True)

    def update_stats(text_widget, stats_label):
        content = text_widget.get("1.0", tk.END)
        words = len(content.split())
        characters = len(content) - content.count("\n")
        stats_label.config(text=f"Words: {words} | Characters: {characters}")

    def update_all_line_numbers(force=False):
        for tab_id in tab_control.tabs():
            frame = tab_control.nametowidget(tab_id)
            update_line_numbers_in_frame(frame, force=force)

    def update_line_numbers_in_frame(frame, force=False):
        text_widget = None
        line_widget = None
        for widget in frame.winfo_children():
            for sub in widget.winfo_children():
                if isinstance(sub, tk.Text) and sub.cget("width") == 4:
                    line_widget = sub
                elif isinstance(sub, tk.Text):
                    text_widget = sub
        if text_widget and line_widget:
            if not show_line_numbers.get() and not force:
                line_widget.config(state="normal")
                line_widget.delete("1.0", tk.END)
                line_widget.config(state="disabled")
                return
            line_widget.config(state="normal")
            line_widget.delete("1.0", tk.END)
            lines = int(text_widget.index("end-1c").split(".")[0])
            line_widget.insert("1.0", "\n".join(str(i) for i in range(1, lines + 1)))
            line_widget.config(state="disabled")

    def update_session_duration(label):
        elapsed = int(time.time() - session_start_time)
        label.config(text=f"Session: {elapsed//60:02}:{elapsed%60:02}")
        label.after(1000, lambda: update_session_duration(label))

    def create_tab():
        frame = ttk.Frame(tab_control)

        toolbar = ttk.Frame(frame, padding=5)
        toolbar.pack(fill="x")

        search_entry = ttk.Entry(toolbar, font=default_font, width=30)
        search_entry.pack(side="left", padx=5)

        search_result_label = ttk.Label(toolbar, text="", font=("Verdana", 9))
        search_result_label.pack(side="left", padx=5)

        def search():
            text = get_text_widget(frame)
            query = search_entry.get()
            text.tag_remove("highlight", "1.0", tk.END)
            if query:
                matches = 0
                start = "1.0"
                while True:
                    start = text.search(query, start, nocase=True, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(query)}c"
                    text.tag_add("highlight", start, end)
                    matches += 1
                    start = end
                text.tag_config("highlight", background="#444444", foreground="#FF0000")
                search_result_label.config(text=f"{matches} matches" if matches else "No match")
            else:
                search_result_label.config(text="")

        def clear_text():
            get_text_widget(frame).delete("1.0", tk.END)

        ttk.Button(toolbar, text="Search", command=search).pack(side="left")
        ttk.Button(toolbar, text="Clear", command=clear_text, bootstyle="danger-outline").pack(side="right")

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True)

        line_numbers = tk.Text(content_frame, width=4, padx=4, takefocus=0, border=0,
                               background="#2b2b2b", fg="gray", font=default_font)
        line_numbers.pack(side="left", fill="y")
        line_numbers.config(state="disabled")

        text = tk.Text(content_frame, wrap="word", font=default_font, bg="#1b1e23", fg="white",
                       insertbackground="white", undo=True)
        text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(content_frame, command=text.yview)
        scroll.pack(side="right", fill="y")
        text.config(yscrollcommand=scroll.set)

        bottom_bar = ttk.Frame(frame)
        bottom_bar.pack(fill="x", side="bottom", padx=5, pady=(0, 2))

        stats_label = ttk.Label(bottom_bar, text="Words: 0 | Characters: 0", font=("Verdana", 8), anchor="w")
        stats_label.pack(side="left")

        session_label = ttk.Label(bottom_bar, text="Session: 00:00", font=("Verdana", 8), anchor="e")
        session_label.pack(side="right")
        update_session_duration(session_label)

        def on_key(event=None):
            highlight_syntax(text)
            update_stats(text, stats_label)
            update_line_numbers_in_frame(frame)

        text.bind("<KeyRelease>", on_key)
        update_line_numbers_in_frame(frame)

        return frame

    def get_text_widget(frame):
        for child in frame.winfo_children():
            for subchild in child.winfo_children():
                if isinstance(subchild, tk.Text) and subchild.cget("width") != 4:
                    return subchild

    def highlight_syntax(text_widget):
        keywords = ["def", "return", "if", "else", "for", "while", "import", "from", "as", "class", "try", "except"]
        text_widget.tag_remove("keyword", "1.0", tk.END)
        content = text_widget.get("1.0", tk.END)
        for keyword in keywords:
            idx = "1.0"
            while True:
                idx = text_widget.search(rf"\\b{keyword}\\b", idx, stopindex=tk.END, nocase=False, regexp=True)
                if not idx:
                    break
                end = f"{idx}+{len(keyword)}c"
                text_widget.tag_add("keyword", idx, end)
                idx = end
        text_widget.tag_config("keyword", foreground="#00BFFF")

    new_tab()
    auto_save()

root.mainloop()
