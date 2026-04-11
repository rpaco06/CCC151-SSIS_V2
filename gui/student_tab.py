import tkinter as tk
from tkinter import messagebox, StringVar, Toplevel
import ttkbootstrap as tb
from database import (load_students, save_student, update_student,
                      delete_student, get_program_codes,
                      student_exists, count_students)
from validator import validate_student

NAV    = "#0d1b2a"
ACCENT = "#1b4f72"
BG     = "#f5f7fa"
WHITE  = "#ffffff"
TEXT   = "#1a1a2a"
GREY   = "#6c757d"

PER_PAGE = 25


def styled_entry(parent, textvariable, width=24):
    e = tk.Entry(parent, textvariable=textvariable,
                 font=("Segoe UI", 10), width=width,
                 relief="flat", bd=0, bg="#eef1f7",
                 fg=TEXT, insertbackground=TEXT)
    e.config(highlightthickness=2,
             highlightbackground="#dde3ee",
             highlightcolor=ACCENT)
    return e


class StudentTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=BG)
        self.current_page = 1
        self.total_pages  = 1
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Title
        tk.Label(self.parent, text="Students",
                 font=("Georgia", 20, "bold"),
                 bg=BG, fg=NAV).pack(anchor="w", padx=25, pady=(20, 5))

        # Toolbar
        toolbar = tk.Frame(self.parent, bg=BG)
        toolbar.pack(fill="x", padx=25, pady=(0, 8))

        tk.Label(toolbar, text="Search",
                 font=("Segoe UI", 10), bg=BG, fg=GREY).pack(side="left")
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda *a: self.reset_and_refresh())
        se = styled_entry(toolbar, self.search_var, width=26)
        se.pack(side="left", padx=(6, 20), ipady=5)

        tk.Label(toolbar, text="Sort by",
                 font=("Segoe UI", 10), bg=BG, fg=GREY).pack(side="left")
        self.sort_var = StringVar(value="id")
        sort_cb = tb.Combobox(toolbar, textvariable=self.sort_var,
                              values=["Id", "Firstname", "Lastname",
                                      "Course", "Year", "Gender"],
                              width=10, state="readonly", bootstyle="secondary")
        sort_cb.pack(side="left", padx=6)
        sort_cb.bind("<<ComboboxSelected>>", lambda e: self.reset_and_refresh())

        tk.Frame(toolbar, bg=BG).pack(side="left", expand=True)
        tb.Button(toolbar, text="🗑  Delete",
                  bootstyle="secondary", command=self.delete,
                  width=10).pack(side="right", padx=(5, 0))
        tb.Button(toolbar, text="＋  Add Student",
                  bootstyle="dark", command=self.open_add_dialog,
                  width=14).pack(side="right")

        # Table
        table_frame = tk.Frame(self.parent, bg=BG)
        table_frame.pack(fill="both", expand=True, padx=25, pady=5)

        cols = ("id", "firstname", "lastname", "course", "year", "gender")
        self.tree = tb.Treeview(table_frame, columns=cols,
                                show="headings", height=12,
                                bootstyle="primary")

        col_widths = {"id": 110, "firstname": 150, "lastname": 150,
                      "course": 110, "year": 60, "gender": 90}
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=col_widths.get(c, 100), anchor="w")

        scroll = tb.Scrollbar(table_frame, orient="vertical",
                              command=self.tree.yview,
                              bootstyle="secondary-round")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.tag_configure("odd",  background="#f0f4fb")
        self.tree.tag_configure("even", background=WHITE)
        self.tree.bind("<ButtonRelease-1>", self.on_click)

        # Pagination bar
        page_bar = tk.Frame(self.parent, bg=BG)
        page_bar.pack(fill="x", padx=25, pady=6)

        tb.Button(page_bar, text="◀ Prev",
                  bootstyle="secondary-outline",
                  command=self.prev_page,
                  width=10).pack(side="left", padx=(0, 5))

        self.page_label = tk.Label(page_bar, text="Page 1 of 1",
                                   font=("Segoe UI", 10),
                                   bg=BG, fg=GREY)
        self.page_label.pack(side="left", padx=10)

        tb.Button(page_bar, text="Next ▶",
                  bootstyle="secondary-outline",
                  command=self.next_page,
                  width=10).pack(side="left", padx=(5, 0))

        self.total_label = tk.Label(page_bar, text="",
                                    font=("Segoe UI", 10),
                                    bg=BG, fg=GREY)
        self.total_label.pack(side="right")

    def reset_and_refresh(self):
        self.current_page = 1
        self.refresh()

    def refresh(self):
        q    = self.search_var.get()
        sort = self.sort_var.get().lower()

        total = count_students(search=q)
        self.total_pages = max(1, -(-total // PER_PAGE))
        self.current_page = min(self.current_page, self.total_pages)

        rows = load_students(search=q, sort=sort,
                             page=self.current_page, per_page=PER_PAGE)

        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end",
                             values=(r["id"], r["firstname"], r["lastname"],
                                     r["course"], r["year"], r["gender"]),
                             tags=(tag,))

        self.page_label.config(
            text=f"Page {self.current_page} of {self.total_pages}")
        self.total_label.config(text=f"Total: {total} students")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh()

    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        row    = self.tree.identify_row(event.y)
        if region == "cell" and row:
            vals = self.tree.item(row)["values"]
            self.open_edit_dialog(*vals)

    def open_add_dialog(self):
        self.open_dialog("Add Student", "", "", "", "", "", "")

    def open_edit_dialog(self, sid, fn, ln, course, yr, gen):
        self.open_dialog("Edit Student", sid, fn, ln, course, yr, gen)

    def open_dialog(self, title, sid, fn, ln, course, yr, gen):
        win = Toplevel()
        win.title(title)
        win.geometry("420x380")
        win.configure(bg=WHITE)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=title, font=("Georgia", 14, "bold"),
                 bg=WHITE, fg=NAV).pack(anchor="w", padx=20, pady=(18, 10))

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill="x", padx=20)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        is_edit  = bool(sid)
        id_var   = StringVar(value=sid)
        fn_var   = StringVar(value=fn)
        ln_var   = StringVar(value=ln)
        course_var = StringVar(value=course)
        yr_var   = StringVar(value=yr)
        gen_var  = StringVar(value=gen)

        # ID
        tk.Label(form, text="Student ID  (YYYY-NNNN)",
                 font=("Segoe UI", 10), bg=WHITE,
                 fg=GREY).grid(row=0, column=0, columnspan=2,
                 sticky="w", pady=(0, 2))
        id_entry = styled_entry(form, id_var, width=36)
        id_entry.grid(row=1, column=0, columnspan=2,
                      pady=(0, 10), ipady=5, sticky="ew")
        if is_edit:
            id_entry.configure(state="disabled", bg="#e8ecf3")

        # First / Last name
        tk.Label(form, text="First Name", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=2, column=0, sticky="w", pady=(0, 2))
        tk.Label(form, text="Last Name", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=2, column=1, sticky="w",
                 padx=(10, 0), pady=(0, 2))
        styled_entry(form, fn_var, width=17).grid(
            row=3, column=0, pady=(0, 10), ipady=5, sticky="ew")
        styled_entry(form, ln_var, width=17).grid(
            row=3, column=1, pady=(0, 10), ipady=5,
            padx=(10, 0), sticky="ew")

        # Course / Year / Gender
        tk.Label(form, text="Course", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=4, column=0, sticky="w", pady=(0, 2))

        bottom_row = tk.Frame(form, bg=WHITE)
        bottom_row.grid(row=5, column=0, columnspan=2,
                        sticky="ew", pady=(0, 10))
        bottom_row.columnconfigure(0, weight=3)
        bottom_row.columnconfigure(1, weight=1)
        bottom_row.columnconfigure(2, weight=1)

        tb.Combobox(bottom_row, textvariable=course_var,
                    values=get_program_codes(),
                    state="readonly",
                    bootstyle="secondary").grid(
                    row=1, column=0, sticky="ew", padx=(0, 8))

        tk.Label(bottom_row, text="Year", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=0, column=1, sticky="w")
        tb.Combobox(bottom_row, textvariable=yr_var,
                    values=["1", "2", "3", "4", "5"],
                    width=6, state="readonly",
                    bootstyle="secondary").grid(
                    row=1, column=1, sticky="ew", padx=(0, 8))

        tk.Label(bottom_row, text="Gender", font=("Segoe UI", 10),
                 bg=WHITE, fg=GREY).grid(row=0, column=2, sticky="w")
        tb.Combobox(bottom_row, textvariable=gen_var,
                    values=["Male", "Female", "Other"],
                    width=8, state="readonly",
                    bootstyle="secondary").grid(
                    row=1, column=2, sticky="ew")

        def save():
            data = {
                "id":        id_var.get().strip(),
                "firstname": fn_var.get().strip(),
                "lastname":  ln_var.get().strip(),
                "course":    course_var.get().strip(),
                "year":      yr_var.get().strip(),
                "gender":    gen_var.get().strip()
            }
            error = validate_student(data)
            if error:
                return messagebox.showwarning("Warning", error, parent=win)
            try:
                if is_edit:
                    update_student(data)
                else:
                    if student_exists(data["id"]):
                        return messagebox.showerror(
                            "Error", "Student ID already exists.", parent=win)
                    save_student(data)
                self.refresh()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        tb.Button(win, text="Save", bootstyle="dark",
                  command=save, width=12).pack(pady=8)

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a student first.")
        sid = self.tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Delete student '{sid}'?"):
            return
        delete_student(sid)
        self.refresh()