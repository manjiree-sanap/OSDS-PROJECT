# bankers_gui_multipage.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# You must have your bankers_logic.py file in the same folder
from bankers_logic import BankersAlgorithm

# --- Modern Theme & Colors ---
BG_COLOR = "#292d3e"
FG_COLOR = "#f0f0f0"
FRAME_COLOR = "#353a50"
HIGHLIGHT_COLOR = "#c3e88d"
SUCCESS_COLOR = "#89ddff"
WAIT_COLOR = "#ffcb6b"
ERROR_COLOR = "#f78c6c"
FONT_NORMAL = ("Calibri", 12)
FONT_BOLD = ("Calibri", 14, "bold")
FONT_TITLE = ("Calibri", 24, "bold")

class BankersApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Advanced Banker's Algorithm Simulator")
        self.geometry("1100x750")
        self.minsize(1000, 700)
        self.configure(bg=BG_COLOR)

        # Shared data between pages
        self.banker_instance = None

        # Container for all pages
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, SetupPage, DashboardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
             frame.on_show() # Call on_show if it exists to refresh data
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        label_title = tk.Label(self, text="Banker's Algorithm\nDeadlock Avoidance Simulator", font=FONT_TITLE, bg=BG_COLOR, fg=HIGHLIGHT_COLOR)
        label_title.pack(pady=(100, 20))

        label_subtitle = tk.Label(self, text="A project to visualize deadlock avoidance in operating systems.", font=FONT_NORMAL, bg=BG_COLOR, fg=FG_COLOR)
        label_subtitle.pack(pady=10)

        style = ttk.Style()
        style.configure("W.TButton", font=("Calibri", 16, "bold"), padding=20)
        start_button = ttk.Button(self, text="🚀 Start Simulation", style="W.TButton",
                                  command=lambda: controller.show_frame("SetupPage"))
        start_button.pack(pady=50)

        # You can add your name here
        author_label = tk.Label(self, text="Project by: [Your Name Here]", font=("Calibri", 10), bg=BG_COLOR, fg=FG_COLOR)
        author_label.pack(side="bottom", pady=20)


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="System Configuration", font=FONT_TITLE, bg=BG_COLOR, fg=HIGHLIGHT_COLOR).pack(pady=(50, 30))
        
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(pady=20)

        # --- Manual Setup ---
        manual_frame = tk.Frame(main_frame, bg=FRAME_COLOR, padx=20, pady=20)
        manual_frame.grid(row=0, column=0, padx=20)

        tk.Label(manual_frame, text="⚙️ Manual Setup", font=FONT_BOLD, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(manual_frame, text="Processes:", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky='w', pady=5)
        self.processes_entry = tk.Entry(manual_frame, font=FONT_NORMAL)
        self.processes_entry.grid(row=1, column=1)

        tk.Label(manual_frame, text="Resources:", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky='w', pady=5)
        self.resources_entry = tk.Entry(manual_frame, font=FONT_NORMAL)
        self.resources_entry.grid(row=2, column=1)
        
        ttk.Button(manual_frame, text="Configure & Launch", command=self.setup_and_launch).grid(row=3, column=0, columnspan=2, pady=20)

        # --- Sample Data ---
        sample_frame = tk.Frame(main_frame, bg=FRAME_COLOR, padx=20, pady=20)
        sample_frame.grid(row=0, column=1, padx=20)

        tk.Label(sample_frame, text="📊 Use Sample Data", font=FONT_BOLD, bg=FRAME_COLOR, fg=FG_COLOR).pack(pady=10)
        tk.Label(sample_frame, text="Load a pre-configured safe state.", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR, wraplength=200).pack()
        ttk.Button(sample_frame, text="Load Sample & Launch", command=self.load_sample_and_launch).pack(pady=20)

        back_button = ttk.Button(self, text="← Back to Welcome", command=lambda: controller.show_frame("WelcomePage"))
        back_button.pack(pady=50)

    def setup_and_launch(self):
        try:
            num_p = int(self.processes_entry.get())
            num_r = int(self.resources_entry.get())
            if num_p <= 0 or num_r <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive integers for processes and resources.")
            return

        try:
            avail_str = simpledialog.askstring("Input", f"Enter {num_r} available resources (comma-separated):")
            available = list(map(int, avail_str.split(',')))

            max_demand = []
            for i in range(num_p):
                row_str = simpledialog.askstring("Input", f"Enter Max demand for P{i} ({num_r} values):")
                max_demand.append(list(map(int, row_str.split(','))))

            allocation = [[0] * num_r for _ in range(num_p)]
            
            self.controller.banker_instance = BankersAlgorithm(available, max_demand, allocation)
            self.controller.show_frame("DashboardPage")
        except (AttributeError, ValueError):
             messagebox.showerror("Setup Cancelled", "Invalid input format. Setup was cancelled.")

    def load_sample_and_launch(self):
        self.controller.banker_instance = BankersAlgorithm(
            available=[3, 3, 2],
            max_demand=[[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
            allocation=[[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
        )
        self.controller.show_frame("DashboardPage")

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        self.treeviews = {}
        self.is_visualizing = False

        # --- Layout ---
        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(top_frame, text="Simulation Dashboard", font=FONT_TITLE, bg=BG_COLOR, fg=HIGHLIGHT_COLOR).pack(side='left')
        
        matrices_frame = tk.Frame(self, bg=BG_COLOR)
        matrices_frame.pack(fill='both', expand=True, padx=10)

        bottom_frame = tk.Frame(self, bg=BG_COLOR)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Control Panel ---
        control_panel = tk.Frame(bottom_frame, bg=FRAME_COLOR)
        control_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        control_panel.grid_rowconfigure(3, weight=1)

        tk.Label(control_panel, text="Actions", font=FONT_BOLD, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=0, columnspan=2, pady=10)
        tk.Label(control_panel, text="Process ID:", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky='w', padx=10)
        self.pid_entry = tk.Entry(control_panel, font=FONT_NORMAL)
        self.pid_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(control_panel, text="Request Vector:", font=FONT_NORMAL, bg=FRAME_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky='w', padx=10)
        self.request_entry = tk.Entry(control_panel, font=FONT_NORMAL)
        self.request_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(control_panel, text="Submit Request", command=self.submit_request).grid(row=3, columnspan=2, pady=10, sticky='n')
        
        vis_button = ttk.Button(control_panel, text="Visualize Safety Check", command=self.visualize_safety_check)
        vis_button.grid(row=4, columnspan=2, pady=10, sticky='n')
        
        reset_button = ttk.Button(control_panel, text="Reset & New Setup", command=lambda: controller.show_frame("SetupPage"))
        reset_button.grid(row=5, columnspan=2, pady=10, sticky='s')


        # --- Log Panel ---
        log_panel = tk.Frame(bottom_frame, bg=FRAME_COLOR)
        log_panel.pack(side='left', fill='both', expand=True)
        tk.Label(log_panel, text="Live Log", font=FONT_BOLD, bg=FRAME_COLOR, fg=FG_COLOR).pack(pady=5)
        self.log_text = tk.Text(log_panel, font=("Consolas", 11), bg="#202330", fg=FG_COLOR, wrap='word', state='disabled', relief='flat')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)


       # --- Treeview Tables ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=FRAME_COLOR, foreground=FG_COLOR, fieldbackground=FRAME_COLOR, rowheight=25, font=FONT_NORMAL)
        style.configure("Treeview.Heading", background=FRAME_COLOR, foreground=HIGHLIGHT_COLOR, font=FONT_BOLD, relief='flat')
        style.map("Treeview.Heading", background=[('active', BG_COLOR)])
        
        # Style for our new headers
        style.configure("Dashboard.TLabelframe", background=BG_COLOR, bordercolor=BG_COLOR)
        style.configure("Dashboard.TLabelframe.Label", font=FONT_BOLD, background=BG_COLOR, foreground=FG_COLOR)

        matrices = ["Allocation", "Max Demand", "Need", "Available"]
        for i, name in enumerate(matrices):
            # CHANGED: Use a LabelFrame which has a text title
            frame = ttk.LabelFrame(matrices_frame, text=name, style="Dashboard.TLabelframe")
            frame.grid(row=0, column=i, padx=10, pady=5, sticky='nsew')
            matrices_frame.columnconfigure(i, weight=1)
            
            tree = ttk.Treeview(frame, style="Treeview")
            self.treeviews[name] = tree
            # CHANGED: Pack inside the new LabelFrame
            tree.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Tag for highlighting rows
            tree.tag_configure('wait', background=WAIT_COLOR, foreground='black')
            tree.tag_configure('success', background=SUCCESS_COLOR, foreground='black')

    def on_show(self):
        self.refresh_data()
        self.log("Dashboard loaded. System is ready for simulation.")

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"> {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def refresh_data(self):
        banker = self.controller.banker_instance
        if not banker: return

        # Clear old data
        for tree in self.treeviews.values():
            tree.delete(*tree.get_children())

        # Resource headers (R0, R1...)
        res_headers = [f"R{i}" for i in range(banker.num_resources)]

        # --- Populate Allocation, Max, Need tables ---
        for name in ["Allocation", "Max Demand", "Need"]:
            tree = self.treeviews[name]
            tree['columns'] = res_headers
            tree.heading("#0", text="PID")
            tree.column("#0", width=50, anchor='center')
            for col in res_headers:
                tree.heading(col, text=col)
                tree.column(col, width=50, anchor='center')

            matrix = getattr(banker, name.lower().replace(" ", "_"))
            for i in range(banker.num_processes):
                tree.insert("", "end", iid=f"{name}_{i}", text=f"P{i}", values=matrix[i])

        # --- Populate Available table ---
        tree = self.treeviews["Available"]
        tree['columns'] = res_headers
        tree.heading("#0", text="Sys")
        tree.column("#0", width=50, anchor='center')
        for col in res_headers:
            tree.heading(col, text=col)
            tree.column(col, width=50, anchor='center')
        tree.insert("", "end", text="Total", values=banker.available)

    def submit_request(self):
        if self.is_visualizing: return
        try:
            pid = int(self.pid_entry.get())
            request = list(map(int, self.request_entry.get().split(',')))
            self.log(f"--- P{pid} requesting {request} ---")
            success, message = self.controller.banker_instance.request_resources(pid, request)
            self.log(message)
            if success:
                self.refresh_data()
        except (ValueError, AttributeError):
            messagebox.showerror("Invalid Request", "Please enter a valid Process ID and comma-separated request vector.")
    
    def visualize_safety_check(self):
        if self.is_visualizing: return
        self.is_visualizing = True
        self.log("--- Starting Safety Algorithm Visualization ---")
        self.refresh_data() # Reset colors

        banker = self.controller.banker_instance
        work = list(banker.available)
        finish = [False] * banker.num_processes
        safe_sequence = []
        
        self.after(500, self.visualization_step, work, finish, safe_sequence, 0)
        
    def visualization_step(self, work, finish, safe_sequence, round_num):
        banker = self.controller.banker_instance

        if len(safe_sequence) == banker.num_processes:
            self.log(f"SUCCESS! Safe sequence found: {' -> '.join(map(str, safe_sequence))}")
            self.is_visualizing = False
            return

        found_in_round = False
        for i in range(banker.num_processes):
            if not finish[i]:
                # Highlight current process being checked
                for name in ["Allocation", "Max Demand", "Need"]:
                     self.treeviews[name].item(f"{name}_{i}", tags=('wait',))

                self.log(f"Checking P{i}: Need={banker.need[i]} <= Work={work}?")
                
                if all(banker.need[i][j] <= work[j] for j in range(banker.num_resources)):
                    self.log(f"--> P{i} can execute. Releasing its resources.")
                    
                    for j in range(banker.num_resources):
                        work[j] += banker.allocation[i][j]
                    
                    finish[i] = True
                    safe_sequence.append(f"P{i}")

                    # Highlight success
                    for name in ["Allocation", "Max Demand", "Need"]:
                        self.treeviews[name].item(f"{name}_{i}", tags=('success',))
                    
                    found_in_round = True
                    # Schedule the next check after a delay
                    self.after(1500, self.visualization_step, work, finish, safe_sequence, 0)
                    return
                else:
                    self.log(f"--> P{i} must wait. Need > Work.")
                    # Remove highlight after a delay
                    self.after(750, lambda p=i: [self.treeviews[name].item(f"{name}_{p}", tags=()) for name in ["Allocation", "Max Demand", "Need"]])

        if not found_in_round:
            self.log(f"DEADLOCK DETECTED! No process can be allocated resources. System is in an UNSAFE state.")
            for i in range(banker.num_processes):
                if not finish[i]:
                     for name in ["Allocation", "Max Demand", "Need"]:
                          self.treeviews[name].item(f"{name}_{i}", tags=('wait',)) # Highlight remaining processes in red/yellow
            self.is_visualizing = False

if __name__ == "__main__":
    app = BankersApp()
    app.mainloop()
    
