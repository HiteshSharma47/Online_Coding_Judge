import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from judge import run_judge, run_sample
from database import save_submission, get_problem, get_submissions, get_submission_by_id, get_all_problems

problem_id = 1

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=kwargs.get("bg", "#1a1a1a"), highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self, bg=kwargs.get("bg", "#1a1a1a"))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        w = event.widget
        while w:
            if w == self:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                break
            try:
                w = w.master
            except AttributeError:
                break


class TextEditor(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, bg="#1e1e1e")
        self.line_numbers = tk.Canvas(self, width=35, bg="#1a1a1a", bd=0, highlightthickness=0)
        self.line_numbers.pack(side="left", fill="y", padx=(2, 2))
        
        self.text = tk.Text(self, *args, **kwargs)
        self.text.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.scroll_both)
        self.scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.on_scroll)
        
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<Button-1>", self.on_key_release)
        self.text.bind("<Configure>", self.on_key_release)
        
    def scroll_both(self, *args):
        self.text.yview(*args)
        self.redraw()
        
    def on_scroll(self, *args):
        self.scrollbar.set(*args)
        self.redraw()
        
    def on_key_release(self, event=None):
        self.redraw()
        
    def redraw(self):
        self.line_numbers.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(25, y + 2, anchor="ne", text=linenum, fill="#858585", font=("Consolas", 10))
            i = self.text.index(f"{i}+1line")


# Functions

def clear_results():
    verdict_label.config(text="Ready", fg="#8f9091")
    execution_time_label.config(text="")
    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)
    details_box.config(state="disabled")

def load_problems(pid):
    try:
        problem = get_problem(pid)
    except Exception as e:
        verdict_label.config(text="Database Error", fg="#ef4743")
        return

    if not problem:
        return

    problem_label.config(text=f"{pid}. {problem[0]}")
    current_problem_title.config(text=f"Problem {pid}: {problem[0]}")

    if pid in [1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
        difficulty_label.config(text="Easy", fg="#2db55d")
    else:
        difficulty_label.config(text="Medium", fg="#ffa116")

    description_label.config(text=problem[1])
    input_format.config(text=problem[2])
    output_format.config(text=problem[3])

    sample_input.config(state="normal")
    sample_input.delete("1.0", tk.END)
    sample_input.insert(tk.END, problem[4].strip())
    sample_input.config(state="disabled")

    sample_output.config(state="normal")
    sample_output.delete("1.0", tk.END)
    sample_output.insert(tk.END, problem[5].strip())
    sample_output.config(state="disabled")


def select_problem(pid):
    global problem_id
    problem_id = pid
    load_problems(problem_id)
    clear_results()
    code_editor.delete("1.0", tk.END)
    toggle_drawer()

def run_code():
    clear_results()
    source_code = code_editor.get("1.0", tk.END).rstrip()

    if not source_code:
        verdict_label.config(text="Please enter code.", fg="#ef4743")
        return

    try:
        problem = get_problem(problem_id)
    except Exception as e:
        verdict_label.config(text="Database Error", fg="#ef4743")
        return

    sample_input_data = problem[4] 
    sample_output_data = problem[5] 

    result = run_sample(source_code, sample_input_data)

    execution_time_label.config(text=f"Execution Time: {result['Execution Time']} sec")
    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)

    if result["Status"] == "Success":
        if result["Output"] == sample_output_data:
            run_verdict = "Passed Sample Testcase ✅"
            verdict_label.config(text=run_verdict, fg="#2db55d")
        else:
            run_verdict = "Failed Sample Testcase ❌"
            verdict_label.config(text=run_verdict, fg="#ef4743")
        
        details_box.insert(
            tk.END,
            f"{run_verdict}\n\n"
            f"Sample Input:\n"
            f"{sample_input_data}\n\n"
            f"Your Output:\n"
            f"{result['Output']}\n\n"
            f"Expected Output:\n"
            f"{sample_output_data}"
        )
    elif result["Status"] == "Runtime Error!":
        verdict_label.config(text="Runtime Error! ❌", fg="#ef4743")
        details_box.insert(tk.END, f"Runtime Error:\n\n{result['Error']}")
    else:
        verdict_label.config(text="Time Limit Exceeded ❌", fg="#ef4743")
        details_box.insert(tk.END, "Time Limit Exceed")

    details_box.config(state="disabled")

def submit_code():
    clear_results()
    source_code = code_editor.get("1.0", tk.END).rstrip()

    if not source_code:
        verdict_label.config(text="Please enter code.", fg="#ef4743")
        return

    try:
        result = run_judge(problem_id, source_code)
        save_submission(problem_id, source_code, result["Status"])
    except Exception as e:
        verdict_label.config(text="Database Error", fg="#ef4743")
        return

    if result["Status"] == "Accepted!":
        text = f"{result['Status']} ({result['Passed']}/{result['Total']})"
        verdict_label.config(text=text, fg="#2db55d")
    else:
        text = f"{result['Status']} (Testcase {result['Failed Testcase']}/{result['Total']})"
        verdict_label.config(text=text, fg="#ef4743")
    
    execution_time_label.config(text=f"Execution Time: {result['Execution Time']} sec")
    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)

    if result['Status'] == "Runtime Error!":
        details_box.insert(tk.END, f"Runtime Error:\n\n{result['Error']}")
    elif result['Status'] == "Wrong Answer!":
        details_text = (
            f"Input:\n"
            f"{result['Input']}\n\n"
            f"Your Output:\n"
            f"{result['Your Output']}\n\n"
            f"Expected Output:\n"
            f"{result['Expected Output']}"
        )
        details_box.insert(tk.END, details_text)
    
    details_box.config(state="disabled")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Submission History")
    history_window.geometry("800x400")
    history_window.configure(bg="#282828")
    history_window.transient(root)
    history_window.grab_set()

    title_lbl = tk.Label(history_window, text=f"Submission History (Problem {problem_id})", font=("Segoe UI", 14, "bold"), bg="#282828", fg="#ffffff")
    title_lbl.pack(pady=10)

    tree_frame = tk.Frame(history_window, bg="#282828")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    tree = ttk.Treeview(tree_frame, columns=("ID", "Problem", "Verdict", "Time"), show="headings", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)

    tree.heading("ID", text="Submission ID")
    tree.heading("Problem", text="Problem ID")
    tree.heading("Verdict", text="Verdict")
    tree.heading("Time", text="Submitted At")

    tree.column("ID", anchor="center", width=100)
    tree.column("Problem", anchor="center", width=100)
    tree.column("Verdict", anchor="center", width=150)
    tree.column("Time", anchor="center", width=250)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    try:
        submissions = get_submissions(problem_id)
        for submission in submissions:
            tree.insert("", "end", values=(submission[0], submission[1], submission[2], submission[3]))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve submissions: {e}")
        history_window.destroy()
        return

    def view_submission(event):
        selected = tree.selection()
        if not selected:
            return
        
        item = tree.item(selected[0])
        submission_id = item["values"][0]
        
        try:
            submission = get_submission_by_id(submission_id)
            if not submission:
                return
            source_code = submission[0]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load submission: {e}")
            return
        
        code_window = tk.Toplevel(history_window)
        code_window.title(f"Submission {submission_id}")
        code_window.geometry("800x600")
        code_window.configure(bg="#1e1e1e")
        code_window.transient(history_window)

        lbl = tk.Label(code_window, text=f"Submitted Code for Submission #{submission_id}", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ffffff")
        lbl.pack(pady=10)

        code_scrollbar = ttk.Scrollbar(code_window)
        code_box = tk.Text(
            code_window,
            font=("Consolas", 11),
            yscrollcommand=code_scrollbar.set,
            bg="#151515",
            fg="#eff1f5",
            insertbackground="white",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        code_scrollbar.config(command=code_box.yview)

        code_box.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        code_scrollbar.pack(side="right", fill="y", pady=(0, 15), padx=(0, 15))
        code_box.insert(tk.END, source_code)
        code_box.config(state="disabled")
    
    tree.bind("<Double-1>", view_submission)


# Drawer Animation
drawer_width = 320
drawer_x = -drawer_width
drawer_open = False

def toggle_drawer():
    global drawer_open, drawer_x
    if drawer_open:
        slide_close()
    else:
        problems_drawer.lift()
        populate_problem_list()
        slide_open()

def slide_open():
    global drawer_x, drawer_open
    if drawer_x < 0:
        drawer_x += 32
        if drawer_x > 0:
            drawer_x = 0
        problems_drawer.place(x=drawer_x, y=50, relheight=1.0, height=-50, width=drawer_width)
        root.after(10, slide_open)
    else:
        drawer_open = True

def slide_close():
    global drawer_x, drawer_open
    if drawer_x > -drawer_width:
        drawer_x -= 32
        if drawer_x < -drawer_width:
            drawer_x = -drawer_width
        problems_drawer.place(x=drawer_x, y=50, relheight=1.0, height=-50, width=drawer_width)
        root.after(10, slide_close)
    else:
        drawer_open = False
        problems_drawer.place_forget()

def populate_problem_list():
    for widget in drawer_scroll.scrollable_frame.winfo_children():
        widget.destroy()

    try:
        probs = get_all_problems()
    except Exception:
        probs = []

    for item in probs:
        pid = item[0]
        title = item[1]
        
        diff_text = "Easy" if pid in [1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] else "Medium"
        diff_color = "#2db55d" if diff_text == "Easy" else "#ffa116"

        item_frame = tk.Frame(drawer_scroll.scrollable_frame, bg="#202020", height=40)
        item_frame.pack(fill="x", pady=2)
        item_frame.pack_propagate(False)

        def make_callbacks(p_id=pid, frame=item_frame):
            def on_enter(e):
                frame.config(bg="#2d2d2d")
                for w in frame.winfo_children():
                    if w.winfo_class() == "Label" and w != diff_lbl:
                        w.config(bg="#2d2d2d")
            def on_leave(e):
                frame.config(bg="#202020")
                for w in frame.winfo_children():
                    if w.winfo_class() == "Label" and w != diff_lbl:
                        w.config(bg="#202020")
            def on_click(e):
                select_problem(p_id)
            return on_enter, on_leave, on_click

        on_enter, on_leave, on_click = make_callbacks(pid, item_frame)
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        item_frame.bind("<Button-1>", on_click)

        title_lbl = tk.Label(item_frame, text=f"{pid}. {title}", font=("Segoe UI", 10), fg="#eff1f5", bg="#202020", anchor="w")
        title_lbl.pack(side="left", padx=10, fill="y")
        title_lbl.bind("<Button-1>", on_click)

        diff_lbl = tk.Label(item_frame, text=diff_text, font=("Segoe UI", 8, "bold"), fg=diff_color, bg="#2c2c2c", padx=5, pady=1)
        diff_lbl.pack(side="right", padx=10)


# Initialize Root
root = tk.Tk()
root.title("Online Coding Judge")
root.geometry("1200x800")
root.minsize(800, 600)
root.configure(bg="#1a1a1a")


style = ttk.Style()
style.theme_use("clam")


style.configure("TScrollbar", troughcolor="#1a1a1a", background="#3e3e3e", bordercolor="#1a1a1a", arrowcolor="#eff1f5")
style.map("TScrollbar", background=[('active', '#4f4f4f')])


style.configure("Treeview", background="#1e1e1e", foreground="#eff1f5", fieldbackground="#1e1e1e", rowheight=28, bordercolor="#3e3e3e", borderwidth=1)
style.map("Treeview", background=[('selected', '#007acc')], foreground=[('selected', '#ffffff')])
style.configure("Treeview.Heading", background="#282828", foreground="#ffffff", font=("Segoe UI", 10, "bold"), bordercolor="#3e3e3e", borderwidth=1)
style.map("Treeview.Heading", background=[('active', '#3e3e3e')])


top_bar = tk.Frame(root, bg="#202020", height=50)
top_bar.pack(fill="x", side="top")
top_bar.pack_propagate(False)

problems_btn = tk.Button(top_bar, text="☰  Problems", command=toggle_drawer, bg="#3e3e3e", fg="white", activebackground="#4f4f4f", activeforeground="white", bd=0, font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2")
problems_btn.pack(side="left", padx=15, pady=10)

current_problem_title = tk.Label(top_bar, text="", font=("Segoe UI", 12, "bold"), fg="#eff1f5", bg="#202020")
current_problem_title.pack(side="left", padx=10)

# Main Workspace Layout
main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#1a1a1a", bd=0, sashwidth=4, sashrelief=tk.FLAT)
main_paned.pack(fill="both", expand=True, padx=10, pady=10)

left_pane = tk.Frame(main_paned, bg="#282828")
right_pane = tk.Frame(main_paned, bg="#1a1a1a")
main_paned.add(left_pane, width=500)
main_paned.add(right_pane, width=680)

scroll_frame = ScrollableFrame(left_pane, bg="#282828")
scroll_frame.pack(fill="both", expand=True)

problem_label = tk.Label(scroll_frame.scrollable_frame, text="", font=("Segoe UI", 18, "bold"), fg="#ffffff", bg="#282828", justify="left", anchor="w")
problem_label.pack(fill="x", padx=15, pady=(15, 5))

difficulty_frame = tk.Frame(scroll_frame.scrollable_frame, bg="#282828")
difficulty_frame.pack(fill="x", padx=15, pady=(0, 10))

difficulty_label = tk.Label(difficulty_frame, text="Easy", font=("Segoe UI", 9, "bold"), fg="#2db55d", bg="#333333", padx=8, pady=2)
difficulty_label.pack(side="left")

divider = tk.Frame(scroll_frame.scrollable_frame, height=1, bg="#3e3e3e")
divider.pack(fill="x", padx=15, pady=10)

description_label = tk.Label(scroll_frame.scrollable_frame, text="", font=("Segoe UI", 11), fg="#d4d4d4", bg="#282828", justify="left", anchor="w", wraplength=450)
description_label.pack(fill="x", padx=15, pady=10)

input_format_header = tk.Label(scroll_frame.scrollable_frame, text="Input Format", font=("Segoe UI", 12, "bold"), fg="#ffa116", bg="#282828", justify="left", anchor="w")
input_format_header.pack(fill="x", padx=15, pady=(15, 2))

input_format = tk.Label(scroll_frame.scrollable_frame, text="", font=("Segoe UI", 10), fg="#d4d4d4", bg="#282828", justify="left", anchor="w", wraplength=450)
input_format.pack(fill="x", padx=15, pady=(0, 10))

output_format_header = tk.Label(scroll_frame.scrollable_frame, text="Output Format", font=("Segoe UI", 12, "bold"), fg="#ffa116", bg="#282828", justify="left", anchor="w")
output_format_header.pack(fill="x", padx=15, pady=(15, 2))

output_format = tk.Label(scroll_frame.scrollable_frame, text="", font=("Segoe UI", 10), fg="#d4d4d4", bg="#282828", justify="left", anchor="w", wraplength=450)
output_format.pack(fill="x", padx=15, pady=(0, 10))

examples_header = tk.Label(scroll_frame.scrollable_frame, text="Examples", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#282828", justify="left", anchor="w")
examples_header.pack(fill="x", padx=15, pady=(15, 5))

example_input_lbl = tk.Label(scroll_frame.scrollable_frame, text="Sample Input:", font=("Segoe UI", 10, "bold"), fg="#eff1f5", bg="#282828", justify="left", anchor="w")
example_input_lbl.pack(fill="x", padx=15, pady=(5, 2))

sample_input = tk.Text(scroll_frame.scrollable_frame, height=3, font=("Consolas", 10), bg="#1e1e1e", fg="#e0e0e0", bd=0, highlightthickness=1, highlightbackground="#3e3e3e", highlightcolor="#3e3e3e", padx=10, pady=5, wrap="word")
sample_input.pack(fill="x", padx=15, pady=(0, 10))

example_output_lbl = tk.Label(scroll_frame.scrollable_frame, text="Sample Output:", font=("Segoe UI", 10, "bold"), fg="#eff1f5", bg="#282828", justify="left", anchor="w")
example_output_lbl.pack(fill="x", padx=15, pady=(5, 2))

sample_output = tk.Text(scroll_frame.scrollable_frame, height=3, font=("Consolas", 10), bg="#1e1e1e", fg="#e0e0e0", bd=0, highlightthickness=1, highlightbackground="#3e3e3e", highlightcolor="#3e3e3e", padx=10, pady=5, wrap="word")
sample_output.pack(fill="x", padx=15, pady=(0, 20))

# Right Pane Layout
right_paned = tk.PanedWindow(right_pane, orient=tk.VERTICAL, bg="#1a1a1a", bd=0, sashwidth=4, sashrelief=tk.FLAT)
right_paned.pack(fill="both", expand=True)

editor_frame = tk.Frame(right_paned, bg="#1e1e1e")
console_frame = tk.Frame(right_paned, bg="#282828")

right_paned.add(editor_frame, height=450)
right_paned.add(console_frame, height=280)

editor_title_bar = tk.Frame(editor_frame, bg="#2d2d2d", height=30)
editor_title_bar.pack(fill="x")
editor_title_bar.pack_propagate(False)

editor_title_lbl = tk.Label(editor_title_bar, text="Solution.py (Python 3)", font=("Segoe UI", 9, "bold"), bg="#2d2d2d", fg="#ffffff")
editor_title_lbl.pack(side="left", padx=10, pady=5)

code_editor_container = TextEditor(editor_frame, font=("Consolas", 12), bg="#1e1e1e", fg="#eff1f5", insertbackground="white", selectbackground="#264f78", selectforeground="#ffffff", undo=True, autoseparators=True)
code_editor_container.pack(fill="both", expand=True)

code_editor = code_editor_container.text

# Console Controls
actions_frame = tk.Frame(console_frame, bg="#282828", height=40)
actions_frame.pack(fill="x", side="top", pady=(5, 5))
actions_frame.pack_propagate(False)

submit_button = tk.Button(actions_frame, text="Submit", command=submit_code, bg="#2db55d", fg="white", activebackground="#24904c", activeforeground="white", bd=0, font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2")
submit_button.pack(side="right", padx=10, pady=5)

run_button = tk.Button(actions_frame, text="Run Code", command=run_code, bg="#3e3e3e", fg="white", activebackground="#4f4f4f", activeforeground="white", bd=0, font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2")
run_button.pack(side="right", padx=5, pady=5)

history_button = tk.Button(actions_frame, text="Submission History", command=show_history, bg="#007acc", fg="white", activebackground="#1f97e8", activeforeground="white", bd=0, font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2")
history_button.pack(side="left", padx=10, pady=5)

result_frame = tk.Frame(console_frame, bg="#1e1e1e", highlightthickness=1, highlightbackground="#3e3e3e")
result_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

result_labels_frame = tk.Frame(result_frame, bg="#1e1e1e")
result_labels_frame.pack(fill="x", padx=15, pady=5)

verdict_label = tk.Label(result_labels_frame, text="Ready", font=("Segoe UI", 12, "bold"), fg="#8f9091", bg="#1e1e1e")
verdict_label.pack(side="left")

execution_time_label = tk.Label(result_labels_frame, text="", font=("Segoe UI", 10), fg="#8f9091", bg="#1e1e1e")
execution_time_label.pack(side="right", padx=10)

details_scrollbar = ttk.Scrollbar(result_frame)
details_box = tk.Text(result_frame, font=("Consolas", 10), bg="#151515", fg="#e0e0e0", bd=0, yscrollcommand=details_scrollbar.set, wrap="word")
details_box.config(state="disabled")
details_scrollbar.config(command=details_box.yview)

details_box.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
details_scrollbar.pack(side="right", fill="y", pady=(0, 15), padx=(0, 15))

# Side Drawer for Problem List (initially hidden)
problems_drawer = tk.Frame(root, bg="#202020", highlightthickness=1, highlightbackground="#3e3e3e")

drawer_header = tk.Frame(problems_drawer, bg="#1a1a1a", height=50)
drawer_header.pack(fill="x")
drawer_header.pack_propagate(False)

drawer_title = tk.Label(drawer_header, text="Problems", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#1a1a1a")
drawer_title.pack(side="left", padx=15)

close_btn = tk.Button(drawer_header, text="×", command=toggle_drawer, bg="#1a1a1a", fg="#8f9091", activebackground="#2a2a2a", activeforeground="white", bd=0, font=("Segoe UI", 16, "bold"), cursor="hand2")
close_btn.pack(side="right", padx=15)

drawer_scroll = ScrollableFrame(problems_drawer, bg="#202020")
drawer_scroll.pack(fill="both", expand=True)

# Load initial problem
load_problems(problem_id)

root.mainloop()