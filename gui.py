import tkinter as tk
from tkinter import ttk
from judge import run_judge, run_sample
from database import save_submission, get_problem, get_submissions, get_submission_by_id

problem_id = 1

# Functions

def clear_results():
    verdict_label.config(text="")
    execution_time_label.config(text="")

    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)
    details_box.config(state="disabled")

def load_problems(problem_id):
    
    problem = get_problem(problem_id)

    problem_label.config(
        text=f"Problem {problem_id}:\n{problem[0]}"
    )

    description_label.config(
        text=problem[1]
    )

    input_format.config(
        text=f"Input Format:\n{problem[2]}"
    )

    output_format.config(
        text=f"Output Format:\n{problem[3]}"
    )

    sample_input.config(
        text=f"Sample Input:\n{problem[4]}"
    )

    sample_output.config(
        text=f"Sample Output:\n{problem[5]}"
    )

def change_problem(event):

    global problem_id

    selected = problem_dropdown.get()

    problem_id = int(selected.split(" - ")[0])

    load_problems(problem_id)

    clear_results()

    code_editor.delete("1.0", tk.END)


def run_code():

    clear_results()

    source_code = code_editor.get("1.0", tk.END).rstrip()

    if not source_code:
        verdict_label.config(text="Please enter code.")
        return

    problem = get_problem(problem_id)

    sample_input_data = problem[4] 
    sample_output_data = problem[5] 

    result = run_sample(
        source_code,
        sample_input_data
    )

    execution_time_label.config(
        text=f"Execution Time: {result['Execution Time']} sec"
    )

    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)

    if result["Status"] == "Success":

        if result["Output"] == sample_output_data:
            run_verdict = "Passed Sample Testcase ✅"
        else:
            run_verdict = "Failed Sample Testcase ❌"
        
        verdict_label.config(
            text=run_verdict
        )
        

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

        details_box.insert(
            tk.END,
            f"Runtime Error:\n\n{result['Error']}"
        )

    else:

        details_box.insert(
            tk.END,
            "Time Limit Exceed"
        )

    details_box.config(state="disabled")


def submit_code():

    clear_results()

    source_code = code_editor.get("1.0",tk.END).rstrip()

    if not source_code:
        verdict_label.config(text="Please enter code.")
        return

    result = run_judge(
        problem_id,
        source_code
    )

    save_submission(
        problem_id,
        source_code,
        result["Status"]
    )

    if result["Status"] == "Accepted!":
        text=f"{result['Status']} ({result['Passed']}/{result['Total']})"

    else:
        text=f"{result['Status']} (Testcase {result['Failed Testcase']}/{result['Total']})"
    
    verdict_label.config(
        text=text
    )

    execution_time_label.config(
        text=f"Execution Time: {result['Execution Time']} sec"
    )

    if result['Status'] == "Runtime Error!":
        details_box.config(state="normal")

        details_box.delete("1.0", tk.END)

        details_box.insert(
            tk.END,
            f"Runtime Error:\n\n{result['Error']}"
        )

        details_box.config(state="disabled")

    elif result['Status'] == "Wrong Answer!":
        details_box.config(state="normal")

        details_box.delete("1.0", tk.END)

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
    
    else:
        details_box.config(state="normal")
        details_box.delete("1.0", tk.END)
        details_box.config(state="disabled")

def show_history():

    history_window = tk.Toplevel(root)

    history_window.title("Submission History")

    history_window.geometry("800x400")

    submissions = get_submissions(problem_id)

    scrollbar = tk.Scrollbar(
        history_window,
        orient="vertical"
    )

    tree = ttk.Treeview(
        history_window,
        columns=("ID","Problem","Verdict","Time"),
        show="headings"
    )

    scrollbar.config(
        command=tree.yview
    )

    tree.heading("ID", text="Submission ID")
    tree.heading("Problem", text="Problem ID")
    tree.heading("Verdict", text="Verdict")
    tree.heading("Time", text="Submitted At")

    tree.pack(
        side="left",
        fill="both", 
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for submission in submissions:

        tree.insert(
            "",
            "end",
            values=(
                submission[0],
                submission[1],
                submission[2],
                submission[3]
            )
        )

    def view_submission(event):
        
        selected = tree.selection()

        if not selected:
            return
        
        item = tree.item(selected[0])

        submission_id = item["values"][0]
        submission = get_submission_by_id(submission_id)

        source_code = submission[0]
        
        code_window = tk.Toplevel(history_window)

        code_window.title(
            f"Submission {submission_id}"
        )

        code_window.geometry("800x600")

        scrollbar = tk.Scrollbar(code_window)

        code_box = tk.Text(
            code_window,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=code_box.yview
        )

        code_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        code_box.insert(
            tk.END,
            source_code
        )

        code_box.config(
            state="disabled"
        )
    
    tree.bind(
        "<Double-1>",
        view_submission
    )


# GUI
root = tk.Tk()

root.title("Online Coding Judge")

root.geometry("1000x700")

problem_var = tk.StringVar()

problem_dropdown = ttk.Combobox(
    root,
    textvariable=problem_var,
    state="readonly",
    width=30
)

problem_dropdown["values"] = (
    "1 - Add Two Integers",
    "2 - Multiply Two Integers",
    "3 - Maximum of Two Numbers",
    "4 - Sum of Three Integers",
    "5 - Even or Odd"
)

problem_dropdown.current(0)

problem_dropdown.pack(pady=10)

problem_dropdown.bind(
    "<<ComboboxSelected>>",
    change_problem
)

problem_label = tk.Label(
    root,
    text = "",
    font = ('Arial', 20, 'bold')
)

problem_label.pack(pady = 10)

description_label = tk.Label(
    root,
    text ="",
    wraplength = 400,
    font=('Aerial','15','bold'),
    justify = "left"
)

description_label.pack(pady = 10)

input_format = tk.Label(
    root,
    text ="",
    justify="center"
)

input_format.pack(pady=10)

output_format = tk.Label(
    root,
    text ="",
    justify="center"
)

output_format.pack(pady=10)

sample_input = tk.Label(
    root,
    text ="",
    justify="center"
)

sample_input.pack(pady=10)

sample_output = tk.Label(
    root,
    text ="",
    justify="center"
)

sample_output.pack(pady=10)

load_problems(1)

code_editor = tk.Text(
    root,
    height = 12,
    width = 80
)

code_editor.pack(pady = 10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

run_button = tk.Button(
    root,
    text="Run",
    command=run_code
)

run_button.pack(in_=button_frame, side="left", padx=5)

submit_button = tk.Button(
    root,
    text = "Submit",
    command = submit_code
)

submit_button.pack(in_=button_frame, side="left", padx=5)

result_frame = tk.Frame(
    root,
    bd = 2,
    relief = "groove"
)

result_frame.pack(
    fill = "x",
    expand = True,
    padx = 100,
    pady = 10
)

verdict_label = tk.Label(
    result_frame,
    text = "",
    font = ('Arial', 14, 'bold')
)

verdict_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

execution_time_label = tk.Label(
    result_frame,
    text="",
    font=("Arial", 10)
)

execution_time_label.grid(
    row=1,
    column=0,
    sticky="w",
    padx=10
)

scrollbar = tk.Scrollbar(result_frame)

details_box = tk.Text(
    result_frame,
    height=8,
    width=80,
    font=("Arial",11),
    yscrollcommand=scrollbar.set,
    wrap="word"
)

details_box.config(state="disabled")

scrollbar.config(command=details_box.yview)

details_box.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
scrollbar.grid(row=2, column=1, sticky="ns")

result_frame.rowconfigure(2, weight=1)
result_frame.columnconfigure(0, weight=1)

history_button = tk.Button(
    root,
    text="History",
    command=show_history
)

history_button.pack(in_=button_frame, side="left", padx=10)

root.mainloop()