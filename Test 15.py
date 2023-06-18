from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox


def set_background_image(root, image_path):
    image = Image.open(image_path)
    background_image = ImageTk.PhotoImage(image)
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image


# Define color palette
bg_color = "#FFFFFF"  # White background
fg_color = "#555555"  # Dark gray text
btn_color = "#87B9FF"  # Blue buttons
success_color = "#A5D6A7"  # Light green for success messages
txt_color = "#333333"  # Dark gray text

# Create a connection to the database
connect = sqlite3.connect('student_database.db')
cursor = connect.cursor()

# Create the student table with indexing and unique constraint
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    roll_no INTEGER UNIQUE,
    other_attributes TEXT
)
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON students (name)")
connect.commit()


class Footer(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Creating a style
        style = ttk.Style(self)
        style.configure("Footer.TFrame", background="blue")  # Change the background color of the footer to blue
        style.configure("Footer.TLabel",
                        background="blue",  # Change the background color of the label to blue
                        foreground="white",  # Text color
                        font=("Century Gothic", 10),  # Font and size
                        anchor="center")  # Text alignment

        self.configure(style="Footer.TFrame")

        self.footer_label = ttk.Label(self, text="© 2023 All rights reserved | Developed by: Abhishek Shah",
                                      style="Footer.TLabel")
        self.footer_label.pack(pady=5, padx=10, anchor="center")


import tkinter as tk
from tkinter import ttk
import datetime


class StudentDB(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Creating a style
        style = ttk.Style(self)
        style.configure("StudentDB.TFrame", background="white")  # Background color of the frame
        style.configure("DateLabel.TLabel",
                        background="white",  # Background color of the label
                        foreground="black",  # Text color
                        font=("Century Gothic", 10),  # Font and size
                        anchor="w")  # Text alignment
        style.configure("GreetingLabel.TLabel",
                        background="White",
                        foreground="black",
                        font=("Century Gothic", 14, "bold"),
                        anchor="center")
        style.configure("ModernButton.TButton",
                        font=("Century Gothic", 12),
                        foreground="black")

        self.configure(style="StudentDB.TFrame")

        self.date_label = ttk.Label(self, text=datetime.datetime.now().strftime("%Y-%m-%d"),
                                    style="DateLabel.TLabel")
        self.date_label.pack(pady=15)

        self.greeting_label = ttk.Label(self, text=self.get_greeting(), style="GreetingLabel.TLabel")
        self.greeting_label.pack(pady=25)

        self.student_button = ttk.Button(self, text="Student", command=self.raise_student_window,
                                         style="ModernButton.TButton")
        self.student_button.pack(pady=15)

        self.footer = Footer(self)
        self.footer.pack(side="bottom", fill="x")

    def get_greeting(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return "Good morning"
        elif 12 <= current_hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def raise_student_window(self):
        self.master.master.frames[StudentWindow].tkraise()


class StudentWindow(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, style="StudentWindow.TFrame")

        # Top buttons frame
        top_buttons_frame = ttk.Frame(self, style="TopButtonsFrame.TFrame")
        top_buttons_frame.pack(pady=20)

        self.view_button = ttk.Button(top_buttons_frame, text="View Student Database", command=self.view_db,
                                      style="ActionButton.TButton")
        self.view_button.pack(side="left", padx=10)

        self.add_button = ttk.Button(top_buttons_frame, text="Add Student", command=self.raise_add_student_window,
                                     style="ActionButton.TButton")
        self.add_button.pack(side="left", padx=10)

        self.home_button = ttk.Button(top_buttons_frame, text="Home", command=self.raise_home,
                                      style="ActionButton.TButton")
        self.home_button.pack(side="left", padx=10)

        search_frame = ttk.Frame(self, style="SearchFrame.TFrame")
        search_frame.pack(pady=10)

        self.search_entry = ttk.Entry(search_frame, style="SearchEntry.TEntry")
        self.search_entry.pack(side="left", padx=(0, 10))

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_db,
                                        style="ActionButton.TButton")
        self.search_button.pack(side="left")

        self.footer = Footer(self)
        self.footer.pack(side="bottom", fill="x")

        self.canvas = Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw", tags="frame")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Bind the MouseWheel event

        # Center the frame within the window
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def refresh_db(self):
        self.view_db()

    def view_db(self):
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        for row in rows:
            box_frame = ttk.Frame(self.canvas_frame, style="BoxFrame.TFrame", padding=10)
            box_frame.pack(fill="x", padx=10, pady=10)

            id_label = ttk.Label(box_frame, text="ID: " + str(row[0]), style="RecordLabel.TLabel")
            id_label.pack(anchor="w")

            roll_no_label = ttk.Label(box_frame, text="Roll No: " + str(row[2]), style="RecordLabel.TLabel")
            roll_no_label.pack(anchor="w")

            name_label = ttk.Label(box_frame, text="Name: " + row[1], style="RecordLabel.TLabel")
            name_label.pack(anchor="w")

            other_attributes_label = ttk.Label(box_frame, text="Other Attributes: " + row[3],
                                               style="RecordLabel.TLabel")
            other_attributes_label.pack(anchor="w")

            button_frame = ttk.Frame(box_frame)
            button_frame.pack(anchor="e", pady=5)

            delete_button = ttk.Button(button_frame, text="Delete", command=lambda r=row: self.delete_record(r),
                                       style="ActionButton.TButton")
            delete_button.pack(side="left")

            modify_button = ttk.Button(button_frame, text="Modify", command=lambda r=row: self.modify_record(r),
                                       style="ActionButton.TButton")
            modify_button.pack(side="left", padx=(10, 0))

            # Configure circular border for box_frame
            box_frame.bind("<Configure>", lambda event, frame=box_frame: self.rounded_corners(event, frame))

    def rounded_corners(self, event, frame):
        x1, y1, x2, y2 = frame.winfo_geometry().split('+')[1:5]
        frame.place(bordermode='outside', x=x1, y=y1, width=int(x2) - int(x1), height=int(y2) - int(y1))

    def delete_record(self, record):
        result = messagebox.askquestion("Delete Record", "Are you sure you want to delete this record?")
        if result == "yes":
            try:
                cursor.execute("DELETE FROM students WHERE id=?", (record[0],))
                connect.commit()
                messagebox.showinfo("Success", "Record deleted successfully!")

                # Remove the record from the canvas if it matches the record being deleted
                for widget in self.canvas_frame.winfo_children():
                    id_label = widget.winfo_children()[0]
                    id_text = id_label.cget("text")
                    if id_text == "ID: " + str(record[0]):
                        widget.destroy()
                        break
            except:
                messagebox.showerror("Error", "Failed to delete record.")

    def modify_record(self, record):
        self.master.master.frames[ModifyStudentWindow].set_record(record)
        self.master.master.frames[ModifyStudentWindow].tkraise()

    def search_db(self):
        query = self.search_entry.get().strip()
        if query:
            cursor.execute("SELECT * FROM students WHERE id=? OR roll_no=?", (query, query))
        else:
            cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        for row in rows:
            box_frame = ttk.Frame(self.canvas_frame, style="BoxFrame.TFrame", padding=10)
            box_frame.pack(fill="x", padx=10, pady=10)

            id_label = ttk.Label(box_frame, text="ID: " + str(row[0]), style="RecordLabel.TLabel")
            id_label.pack(anchor="w")

            roll_no_label = ttk.Label(box_frame, text="Roll No: " + str(row[2]), style="RecordLabel.TLabel")
            roll_no_label.pack(anchor="w")

            name_label = ttk.Label(box_frame, text="Name: " + row[1], style="RecordLabel.TLabel")
            name_label.pack(anchor="w")

            other_attributes_label = ttk.Label(box_frame, text="Other Attributes: " + row[3],
                                               style="RecordLabel.TLabel")
            other_attributes_label.pack(anchor="w")

            button_frame = ttk.Frame(box_frame)
            button_frame.pack(anchor="e", pady=5)

            delete_button = ttk.Button(button_frame, text="Delete", command=lambda r=row: self.delete_record(r),
                                       style="ActionButton.TButton")
            delete_button.pack(side="left")

            modify_button = ttk.Button(button_frame, text="Modify", command=lambda r=row: self.modify_record(r),
                                       style="ActionButton.TButton")
            modify_button.pack(side="left", padx=(10, 0))

            # Configure circular border for box_frame
            box_frame.bind("<Configure>", lambda event, frame=box_frame: self.rounded_corners(event, frame))

    def raise_add_student_window(self):
        self.master.master.frames[AddStudentWindow].clear_fields()
        self.master.master.frames[AddStudentWindow].tkraise()

    def raise_home(self):
        self.master.master.frames[StudentDB].tkraise()


class ModifyStudentWindow(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, style="AddStudentWindow.TFrame")

        self.footer = Footer(self)
        self.footer.pack(side="bottom", fill="x")

        self.label_id = ttk.Label(self, text="ID:", style="Label.TLabel")
        self.label_id.pack(pady=(50, 10))

        self.entry_id = ttk.Entry(self, style="Entry.TEntry", state="disabled")
        self.entry_id.pack(pady=(0, 10))

        self.label_roll_no = ttk.Label(self, text="Roll No:", style="Label.TLabel")
        self.label_roll_no.pack(pady=(0, 10))

        self.entry_roll_no = ttk.Entry(self, style="Entry.TEntry")
        self.entry_roll_no.pack(pady=(0, 10))

        self.label_name = ttk.Label(self, text="Name:", style="Label.TLabel")
        self.label_name.pack(pady=(0, 10))

        self.entry_name = ttk.Entry(self, style="Entry.TEntry")
        self.entry_name.pack(pady=(0, 10))

        self.label_other_attributes = ttk.Label(self, text="Other attributes:", style="Label.TLabel")
        self.label_other_attributes.pack(pady=(0, 10))

        self.entry_other_attributes = ttk.Entry(self, style="Entry.TEntry")
        self.entry_other_attributes.pack(pady=(0, 10))

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_changes,
                                        style="ModernButton.TButton")
        self.submit_button.pack(pady=(0, 10))

        self.back_button = ttk.Button(self, text="Back", command=self.raise_student_window,
                                      style="ModernButton.TButton")
        self.back_button.pack(pady=(0, 10))

        self.home_button = ttk.Button(self, text="Home", command=self.raise_home, style="ModernButton.TButton")
        self.home_button.pack(pady=(0, 30))

        self.record = None

    def set_record(self, record):
        self.record = record
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, END)
        self.entry_id.insert(0, record[0])
        self.entry_id.config(state="disabled")

        self.entry_roll_no.delete(0, END)
        self.entry_roll_no.insert(0, record[2])

        self.entry_name.delete(0, END)
        self.entry_name.insert(0, record[1])

        self.entry_other_attributes.delete(0, END)
        self.entry_other_attributes.insert(0, record[3])

    def submit_changes(self):
        roll_no = self.entry_roll_no.get()
        name = self.entry_name.get()
        other_attributes = self.entry_other_attributes.get()

        try:
            cursor.execute("UPDATE students SET roll_no=?, name=?, other_attributes=? WHERE id=?",
                           (roll_no, name, other_attributes, self.record[0]))
            connect.commit()
            messagebox.showinfo("Success", "Record modified successfully!")
        except:
            messagebox.showerror("Error", "Failed to modify record.")

    def raise_student_window(self):
        self.master.master.frames[StudentWindow].tkraise()

    def raise_home(self):
        self.master.master.frames[StudentDB].tkraise()


class AddStudentWindow(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, style="AddStudentWindow.TFrame")
        self.footer = Footer(self)
        self.footer.pack(side="bottom", fill="x")

        self.label_id = ttk.Label(self, text="ID:", style="Label.TLabel")
        self.label_id.pack(pady=(50, 10))

        self.entry_id = ttk.Entry(self, style="Entry.TEntry")
        self.entry_id.pack(pady=(0, 10))

        self.label_roll_no = ttk.Label(self, text="Roll No:", style="Label.TLabel")
        self.label_roll_no.pack(pady=(0, 10))

        self.entry_roll_no = ttk.Entry(self, style="Entry.TEntry")
        self.entry_roll_no.pack(pady=(0, 10))

        self.label_name = ttk.Label(self, text="Name:", style="Label.TLabel")
        self.label_name.pack(pady=(0, 10))

        self.entry_name = ttk.Entry(self, style="Entry.TEntry")
        self.entry_name.pack(pady=(0, 10))

        self.label_other_attributes = ttk.Label(self, text="Other attributes:", style="Label.TLabel")
        self.label_other_attributes.pack(pady=(0, 10))

        self.entry_other_attributes = ttk.Entry(self, style="Entry.TEntry")
        self.entry_other_attributes.pack(pady=(0, 10))

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_student,
                                        style="ModernButton.TButton")
        self.submit_button.pack(pady=(0, 10))

        self.back_button = ttk.Button(self, text="Back", command=self.raise_student_window,
                                      style="ModernButton.TButton")
        self.back_button.pack(pady=(0, 10))

        self.home_button = ttk.Button(self, text="Home", command=self.raise_home, style="ModernButton.TButton")
        self.home_button.pack(pady=(0, 30))

    def clear_fields(self):
        self.entry_id.delete(0, END)
        self.entry_roll_no.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_other_attributes.delete(0, END)

    def submit_student(self):
        id = self.entry_id.get()
        roll_no = self.entry_roll_no.get()
        name = self.entry_name.get()
        other_attributes = self.entry_other_attributes.get()

        try:
            cursor.execute("INSERT INTO students (id, roll_no, name, other_attributes) VALUES (?, ?, ?, ?)",
                           (id, roll_no, name, other_attributes))
            connect.commit()

            self.entry_id.delete(0, 'end')
            self.entry_roll_no.delete(0, 'end')
            self.entry_name.delete(0, 'end')
            self.entry_other_attributes.delete(0, 'end')

            messagebox.showinfo("Success", "Student added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Entered Id already exists!")

    def raise_student_window(self):
        self.master.master.frames[StudentWindow].tkraise()

    def raise_home(self):
        self.master.master.frames[StudentDB].tkraise()


def main():
    root = Tk()
    window_width = 800
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    """root.geometry("800x700")
    root.title("Student Database")"""

    # Set the background image
    set_background_image(root, "background.jpg")

    # Configure ttk Style
    style = ttk.Style()
    style.configure("ModernButton.TButton",
                    foreground=fg_color,
                    background=btn_color,
                    font=("Century Gothic", 12),
                    relief="flat")

    style.configure("Footer.TFrame",
                    background=bg_color,
                    borderwidth=1,
                    relief="solid")

    style.configure("Footer.TLabel",
                    foreground=txt_color,
                    background=bg_color,
                    font=("Century Gothic", 10))

    style.configure("StudentDB.TFrame",
                    background=bg_color)

    style.configure("DateLabel.TLabel",
                    foreground=txt_color,
                    background=bg_color,
                    font=("Roboto", 14))

    style.configure("GreetingLabel.TLabel",
                    foreground=txt_color,
                    background=bg_color,
                    font=("Century Gothic", 16, "bold"))

    style.configure("StudentWindow.TFrame",
                    background=bg_color)

    style.configure("ModernButton.TButton",
                    foreground=fg_color,
                    background=btn_color,
                    font=("Century Gothic", 12),
                    relief="flat")

    style.configure("SearchEntry.TEntry",
                    foreground=txt_color,
                    background=btn_color,
                    font=("Century Gothic", 14))

    style.configure("BoxFrame.TFrame",
                    background=btn_color,
                    borderwidth=1,
                    relief="solid")

    style.configure("RecordLabel.TLabel",
                    foreground=txt_color,
                    background=btn_color,
                    font=("Century Gothic", 14))

    style.configure("DeleteButton.TButton",
                    foreground=txt_color,
                    background="#F44336",  # Red
                    font=("Century Gothic", 10),
                    relief="flat")

    style.configure("AddStudentWindow.TFrame",
                    background=bg_color)

    style.configure("Label.TLabel",
                    foreground=txt_color,
                    background=bg_color,
                    font=("Century Gothic", 14))

    style.configure("Entry.TEntry",
                    foreground=txt_color,
                    background=btn_color,
                    font=("Century Gothic", 14))

    style.configure("ActionButton.TButton",  # Add this style definition
                    foreground=txt_color,
                    background=btn_color,
                    font=("Century Gothic", 12),
                    relief="flat")

    container = ttk.Frame(root, style="StudentDB.TFrame")
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    frames = {}
    for F in (StudentDB, StudentWindow, AddStudentWindow, ModifyStudentWindow):
        frame = F(container)
        frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    root.frames = frames
    root.frames[StudentDB].tkraise()

    root.after(0, root.frames[StudentWindow].refresh_db)  # Automatically refresh the database display
    root.mainloop()


if __name__ == "__main__":
    main()
