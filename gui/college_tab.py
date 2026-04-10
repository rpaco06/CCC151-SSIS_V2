import tkinter as tk
from tkinter import messagebox, StringVar, Toplevel
import ttkbootstrap as tb
from database import (load_colleges, save_college, update_college,
                      delete_college, get_college_codes, college_in_use)
from validator import validate_college

NAV   = "#0d1b2a"
ACCENT = "#1b4f72"
BG    = "#f5f7fa"
WHITE = "#ffffff"
TEXT  = "#1a1a2a"
GREY  = "#6c757d"


def styled_entry(parent, textvariable, width=24):
    e = tk.Entry(parent, textvariable=textvariable,
                 font=("Segoe UI", 10), width=width,
                 relief="flat", bd=0, bg="#eef1f7",
                 fg=TEXT, insertbackground=TEXT)
    e.config(highlightthickness=2,
             highlightbackground="#dde3ee",
             highlightcolor=ACCENT)
    return e


class CollegeTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=BG)
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Title
        tk.Label(self.parent, text="Colleges",
                 font=("Georgia", 20, "bold"),
                 bg=BG, fg=NAV).pack(anchor="w", padx=25, pady=(20, 5))

        # Toolbar
        toolbar = tk.Frame(self.parent, bg=BG)
        toolbar.pack(fill="x", padx=25, pady=(0, 8))

        tk.Label(toolbar, text="Search",
                 font=("Segoe UI", 10), bg=BG, fg=GREY).pack(side="left")
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())
        se = styled_entry(toolbar, self.search_var, width=26)
        se.pack(side="left", padx=(6, 20), ipady=5)

        tk.Label(toolbar, text="Sort by",
                 font=("Segoe UI", 10), bg=BG, fg=GREY).pack(side="left")
        self.sort_var = StringVar(value="code")
        sort_cb = tb.Combobox(toolbar, textvariable=self.sort_var,
                              values=["Code", "Name"],
                              width=10, state="readonly", bootstyle="secondary")
        sort_cb.pack(side="left", padx=6)
        sort_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Frame(toolbar, bg=BG).pack(side="left", expand=True)
        tb.Button(toolbar, text="🗑  Delete",
                  bootstyle="secondary", command=self.delete,
                  width=10).pack(side="right", padx=(5, 0))
        tb.Button(toolbar, text="＋  Add College",
                  bootstyle="dark", command=self.open_add_dialog,
                  width=14).pack(side="right")

        # Table
        table_frame = tk.Frame(self.parent, bg=BG)
        table_frame.pack(fill="both", expand=True, padx=25, pady=5)

        cols = ("code", "name")
        self.tree = tb.Treeview(table_frame, columns=cols,
                                show="headings", height=14,
                                bootstyle="primary")
        self.tree.heading("code", text="CODE")
        self.tree.heading("name", text="NAME")
        self.tree.column("code", width=160, anchor="w")
        self.tree.column("name", width=500, anchor="w")

        scroll = tb.Scrollbar(table_frame, orient="vertical",
                              command=self.tree.yview,
                              bootstyle="secondary-round")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.tag_configure("odd",  background="#f0f4fb")
        self.tree.tag_configure("even", background=WHITE)
        self.tree.bind("<ButtonRelease-1>", self.on_click)

    def refresh(self):
        q = self.search_var.get().lower()
        sort = self.sort_var.get().lower()

        rows = load_colleges()

        if q:
            rows = [r for r in rows
                    if q in r["code"].lower() or q in r["name"].lower()]

        rows.sort(key=lambda r: r.get(sort, ""))

        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end",
                             values=(r["code"], r["name"]),
                             tags=(tag,))

    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        row    = self.tree.identify_row(event.y)
        if region == "cell" and row:
            vals = self.tree.item(row)["values"]
            self.open_edit_dialog(vals[0], vals[1])

    def open_add_dialog(self):
        self.open_dialog("Add College", "", "")

    def open_edit_dialog(self, code, name):
        self.open_dialog("Edit College", code, name)

    def open_dialog(self, title, code, name):
        win = Toplevel()
        win.title(title)
        win.geometry("400x230")
        win.configure(bg=WHITE)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=title, font=("Georgia", 14, "bold"),
                 bg=WHITE, fg=NAV).pack(anchor="w", padx=20, pady=(18, 10))

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill="x", padx=20)
        form.columnconfigure(0, weight=1)

        code_var = StringVar(value=code)
        name_var = StringVar(value=name)
        is_edit  = bool(code)

        tk.Label(form, text="Code", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=0, column=0, sticky="w", pady=(0, 2))
        code_entry = styled_entry(form, code_var, width=36)
        code_entry.grid(row=1, column=0, pady=(0, 10), ipady=5, sticky="ew")
        if is_edit:
            code_entry.configure(state="disabled", bg="#e8ecf3")

        tk.Label(form, text="Name", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=2, column=0, sticky="w", pady=(0, 2))
        styled_entry(form, name_var, width=36).grid(
            row=3, column=0, pady=(0, 15), ipady=5, sticky="ew")

        def save():
            data = {
                "code": code_var.get().strip(),
                "name": name_var.get().strip()
            }
            error = validate_college(data)
            if error:
                return messagebox.showwarning("Warning", error, parent=win)
            try:
                if is_edit:
                    update_college(data)
                else:
                    save_college(data)
                self.refresh()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        tb.Button(win, text="Save", bootstyle="dark",
                  command=save, width=12).pack()

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a college first.")
        code = self.tree.item(sel[0])["values"][0]
        if college_in_use(code):
            return messagebox.showerror("Error",
                f"Cannot delete '{code}' — programs are still using it.")
        if not messagebox.askyesno("Confirm", f"Delete college '{code}'?"):
            return
        delete_college(code)
        self.refresh()