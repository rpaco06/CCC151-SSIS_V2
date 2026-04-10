import tkinter as tk
import ttkbootstrap as tb
from gui.college_tab import CollegeTab
from gui.program_tab import ProgramTab
from gui.student_tab import StudentTab

NAV   = "#0d1b2a"
ACCENT = "#1b4f72"
BG    = "#f5f7fa"
WHITE = "#ffffff"

def main():
    app = tb.Window(themename="litera")
    app.title("Student Information System v2")
    app.geometry("1100x700")
    app.configure(bg=BG)

    import tkinter.ttk as ttk
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", font=("Segoe UI", 10), rowheight=40,
                background="white", fieldbackground="white",
                foreground="#1a1a2a")
    s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                background="#0d1b2a", foreground="white", relief="flat")
    s.map("Treeview", background=[("selected", "#1b4f72")],
          foreground=[("selected", "white")])
    
    # Sidebar
    sidebar = tk.Frame(app, bg=NAV, width=200)
    sidebar.pack(fill="y", side="left")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="SSIS",
             font=("Georgia", 24, "bold"),
             bg=NAV, fg=WHITE).pack(pady=(30, 2), padx=20, anchor="w")
    tk.Label(sidebar, text="Student Information\nSystem v2",
             font=("Segoe UI", 8),
             bg=NAV, fg="#7a9cc0").pack(padx=20, anchor="w")

    tk.Frame(sidebar, bg="#1e3a52", height=1).pack(fill="x", padx=15, pady=18)

    # Content area
    content = tk.Frame(app, bg=BG)
    content.pack(fill="both", expand=True, side="left")

    frames = {}
    for name in ["Colleges", "Programs", "Students"]:
        f = tk.Frame(content, bg=BG)
        frames[name] = f

    active_btn = {"ref": None}

    def show_tab(name, btn):
        for f in frames.values():
            f.pack_forget()
        frames[name].pack(fill="both", expand=True)
        if active_btn["ref"]:
            active_btn["ref"].configure(bg=NAV, fg="#7a9cc0")
        btn.configure(bg=ACCENT, fg=WHITE)
        active_btn["ref"] = btn

    icons = {
        "Colleges": "🏛  Colleges",
        "Programs": "📚  Programs",
        "Students": "👤  Students"
    }

    nav_buttons = {}
    for name in ["Colleges", "Programs", "Students"]:
        btn = tk.Button(sidebar, text=icons[name],
                        font=("Segoe UI", 11), bg=NAV,
                        fg="#7a9cc0", relief="flat",
                        anchor="w", padx=20, pady=12,
                        activebackground=ACCENT,
                        activeforeground=WHITE,
                        cursor="hand2", bd=0)
        btn.configure(command=lambda n=name, b=btn: show_tab(n, b))
        btn.pack(fill="x", pady=2)
        nav_buttons[name] = btn

    tk.Frame(sidebar, bg=NAV).pack(expand=True)
    tk.Label(sidebar, text="v2.0", font=("Segoe UI", 8),
             bg=NAV, fg="#3d5a73").pack(pady=10)

    CollegeTab(frames["Colleges"])
    ProgramTab(frames["Programs"])
    StudentTab(frames["Students"])

    show_tab("Students", nav_buttons["Students"])
    app.mainloop()

if __name__ == "__main__":
    main()