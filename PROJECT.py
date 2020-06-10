import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3


class StudentApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self):
        # __init__ function for class Tk
        tk.Tk.__init__(self)
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, Student, Mark, Grade):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)
        self.current_id = 0

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        username_label = ttk.Label(self, text="User Name")
        username_label.grid(row=1, column=4, padx=10, pady=10)

        username = StringVar()
        username_entry = ttk.Entry(self, textvariable=username)
        username_entry.grid(row=1, column=5, padx=10, pady=10)

        password_label = ttk.Label(self, text="Password")
        password_label.grid(row=2, column=4, padx=10, pady=10)

        password = StringVar()
        password_entry = ttk.Entry(self, textvariable=password, show='*')
        password_entry.grid(row=2, column=5, padx=10, pady=10)

        login_button = ttk.Button(self, text="Submit",
                                  command=lambda: self.do_login(username, password))

        # putting the button in its place by
        # using grid
        login_button.grid(row=3, column=5, padx=10, pady=10)

    def do_login(self, username, password):
        inp_username = username.get()
        inp_password = password.get()
        if inp_username == "":
            messagebox.showerror("Error", "Enter User Name")
            return
        if inp_password == "":
            messagebox.showerror("Error", "Enter Password")
            return
        print (inp_username)
        print (inp_password)
        # check DB
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        user_list = cur.execute("SELECT username,password FROM user WHERE username=?", (inp_username,))
        user_data = user_list.fetchone()
        if user_data == None:
            messagebox.showerror("Error", "User not found")
            return
        db_password = user_data[1]
        print (db_password)
        if inp_password != db_password:
            messagebox.showerror("Error", "Invalid password")
            return
        conn.close()
        app.show_frame(Student)


# second window frame page1
class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        name_label = ttk.Label(self, text="Student Name")
        name_label.grid(row=1, column=4, padx=10, pady=10)

        name = StringVar()
        name_entry = ttk.Entry(self, textvariable=name)
        name_entry.grid(row=1, column=5, padx=10, pady=10)

        branch_label = ttk.Label(self, text="Branch")
        branch_label.grid(row=2, column=4, padx=10, pady=10)

        branch = StringVar()
        branch_entry = ttk.Entry(self, textvariable=branch)
        branch_entry.grid(row=2, column=5, padx=10, pady=10)

        reg_label = ttk.Label(self, text="Registration Number")
        reg_label.grid(row=3, column=4, padx=10, pady=10)

        registration_number = StringVar()
        reg_entry = ttk.Entry(self, textvariable=registration_number)
        reg_entry.grid(row=3, column=5, padx=10, pady=10)

        create_button = ttk.Button(self, text="Submit",
                                   command=lambda: self.create_student(name, branch, registration_number))

        # putting the button in its place
        # by using grid
        create_button.grid(row=4, column=5, padx=10, pady=10)

    def create_student(self, name, branch, registration_number):
        inp_name = name.get()
        inp_branch = branch.get()
        inp_registration_number = registration_number.get()
        print(inp_name)
        print(inp_branch)
        print(inp_registration_number)
        if inp_name == "" or inp_branch == "" or inp_registration_number == "":
            messagebox.showerror("Error", "Enter all input data")
            return
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        ins_sql = "INSERT INTO student_details (name,branch,registration_number) values(?,?,?) "
        cur.execute(ins_sql, (inp_name, inp_branch, inp_registration_number))
        row_id = cur.lastrowid
        conn.commit()
        print (row_id)
        app.current_id = row_id
        conn.close()
        app.show_frame(Mark)


# third window frame page2
class Mark(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        mark1_label = ttk.Label(self, text="Physics")
        mark1_label.grid(row=1, column=4, padx=10, pady=10)

        mark1 = StringVar()
        mark1_entry = ttk.Entry(self, textvariable=mark1)
        mark1_entry.grid(row=1, column=5, padx=10, pady=10)

        mark2_label = ttk.Label(self, text="Applied Mechanics")
        mark2_label.grid(row=2, column=4, padx=10, pady=10)

        mark2 = StringVar()
        mark2_entry = ttk.Entry(self, textvariable=mark2)
        mark2_entry.grid(row=2, column=5, padx=10, pady=10)

        mark3_label = ttk.Label(self, text="Chemistry")
        mark3_label.grid(row=3, column=4, padx=10, pady=10)

        mark3 = StringVar()
        mark3_entry = ttk.Entry(self, textvariable=mark3)
        mark3_entry.grid(row=3, column=5, padx=10, pady=10)

        mark_button = ttk.Button(self, text="Submit",
                                 command=lambda: self.save_mark(mark1, mark2, mark3))
        mark_button.grid(row=4, column=5, padx=10, pady=10)

    def save_mark(self, mark1, mark2, mark3):
        print("update mark")
        print (app.current_id)
        inp_mark1 = mark1.get()
        inp_mark2 = mark2.get()
        inp_mark3 = mark3.get()
        if inp_mark1.isnumeric() and inp_mark2.isnumeric() and inp_mark3.isnumeric():
            print ("Marks are all numeric")
        else:
            messagebox.showerror("Error", "Enter numeric data")
            return
        print(inp_mark1)
        print(inp_mark2)
        print(inp_mark3)
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        updt_sql = "UPDATE student_details set subject_1_mark = ? , subject_2_mark = ? , subject_3_mark = ? where id = ?"
        cur.execute(updt_sql, (inp_mark1, inp_mark2, inp_mark3, app.current_id))
        row_id = cur.lastrowid
        conn.commit()
        conn.close()
        app.show_frame(Grade)


# third window frame page2
class Grade(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        new_button = ttk.Button(self, text="CGPA",
                                command=lambda: self.show_cgpa())
        new_button.grid(row=1, column=1, padx=10, pady=10)

        new_button = ttk.Button(self, text="Grade",
                                command=lambda: self.show_grade())
        new_button.grid(row=2, column=1, padx=10, pady=10)

        new_button = ttk.Button(self, text="New Input",
                                command=lambda: controller.show_frame(Student))
        new_button.grid(row=3, column=1, padx=10, pady=10)

        close_button = ttk.Button(self, text="Close",
                                  command=lambda: app.destroy())
        close_button.grid(row=4, column=1, padx=10, pady=10)

    def show_cgpa(self):
        print ("cgpa")
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        grade_list = cur.execute("SELECT subject_1_mark,subject_2_mark,subject_3_mark FROM student_details WHERE id=?",
                                 (app.current_id,))
        grade_data = grade_list.fetchone()
        mark1 = grade_data[0]
        mark2 = grade_data[1]
        mark3 = grade_data[2]
        CGPA = int((mark1 + mark2 + mark3) / 30)
        messagebox.showerror("CGPA", CGPA)
        conn.close()

    def show_grade(self):
        print ("grade")
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        grade_list = cur.execute("SELECT subject_1_mark,subject_2_mark,subject_3_mark FROM student_details WHERE id=?",
                                 (app.current_id,))
        grade_data = grade_list.fetchone()
        mark1 = grade_data[0]
        mark2 = grade_data[1]
        mark3 = grade_data[2]
        CGPA = (mark1 + mark2 + mark3) / 3
        grade = ""
        if CGPA >= 90:
            grade = "O"
        elif CGPA >= 80:
            grade = "A"
        elif CGPA >= 70:
            grade = "B"
        elif CGPA >= 60:
            grade = "C"
        elif CGPA >= 50:
            grade = "D"
        else:
            grade = "F"
        messagebox.showerror("Grade", grade)
        conn.close()


# Main Code
if __name__ == "__main__":
    app = StudentApp()
    app.title("Student Grade Application")
    app.minsize(800, 300)
    app.mainloop()