import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modules import add_face, face_attendance, COL, get_today_date, load_attendances

# default webcam
WEBCAM = 0


class FaceAttendanceSystem:
    def __init__(self, root):
        self.attendance_list = []
        
        self.root = root
        self.root.title("Face Attendance System")

        # Creating tabs for different sections
        self.tabControl = ttk.Notebook(self.root)

        # Dashboard Tab
        self.dashboard_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.dashboard_tab, text="Dashboard")
        self.create_dashboard()

        # Student Management Tab
        self.student_management_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.student_management_tab,
                            text="Student Management")
        self.create_student_management()

        # Attendance View Tab
        self.attendance_view_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.attendance_view_tab, text="Attendance View")
        self.create_attendance_view()

        self.tabControl.pack(expand=1, fill="both")

    def create_dashboard(self):
        ttk.Label(self.dashboard_tab,
                  text="Welcome to the Dashboard").pack(pady=10)
        ttk.Button(self.dashboard_tab, text="Register Students",
                   command=self.open_add_students).pack(pady=5)
        ttk.Button(self.dashboard_tab, text="Attendance View",
                   command=self.open_attendance_view).pack(pady=5)
        ttk.Button(self.dashboard_tab, text="Take Attendance",
                   command=self.face_attendance).pack(pady=5)

    def create_class_management(self):
        # Class Creation Form
        ttk.Label(self.class_management_tab,
                  text="Class Creation Form").pack(pady=10)

        ttk.Label(self.class_management_tab, text="Class Name:").pack()
        self.class_name_entry = ttk.Entry(self.class_management_tab)
        self.class_name_entry.pack(pady=5)

        ttk.Label(self.class_management_tab, text="Date:").pack()
        self.date_entry = ttk.Entry(self.class_management_tab)
        self.date_entry.pack(pady=5)

        ttk.Label(self.class_management_tab, text="Time Slot:").pack()
        self.time_slot_entry = ttk.Entry(self.class_management_tab)
        self.time_slot_entry.pack(pady=5)

        ttk.Button(self.class_management_tab, text="Create Class",
                   command=self.create_class).pack(pady=10)

    def create_student_management(self):
        # Add Students Page
        ttk.Label(self.student_management_tab,
                  text="Add Students Page").pack(pady=10)

        ttk.Label(self.student_management_tab, text="Student Name:").pack()
        self.student_name_entry = ttk.Entry(self.student_management_tab)
        self.student_name_entry.pack(pady=5)

        ttk.Label(self.student_management_tab, text="Student ID:").pack()
        self.student_id_entry = ttk.Entry(self.student_management_tab)
        self.student_id_entry.pack(pady=5)

        ttk.Button(self.student_management_tab, text="Capture Face",
                   command=self.add_face).pack(pady=10)

    def create_attendance_view(self):
        # Attendance View Page
        ttk.Label(self.attendance_view_tab,
                  text="Attendance View Page").pack(pady=10)

        ttk.Label(self.attendance_view_tab,
                  text="Select Attendance Date:").pack(pady=5)
        self.attendance_date_var = tk.StringVar()
        self.attendance_date_dropdown = ttk.Combobox(
            self.attendance_view_tab, textvariable=self.attendance_date_var)
        self.attendance_date_dropdown.pack(pady=5)

        # Display attendance records
        ttk.Label(self.attendance_view_tab,
                  text="Attendance Records:").pack(pady=5)
        self.attendance_text = tk.Text(
            self.attendance_view_tab, height=15, width=80)
        self.attendance_text.pack(pady=5)

        ttk.Button(self.attendance_view_tab, text="Refresh",
                   command=self.refresh_attendance).pack(pady=10)
        
        # bind on change for combobox
        self.attendance_date_dropdown.bind("<<ComboboxSelected>>", self.on_select_attendance_date)
        
        self.all_attendance_dates()

    def add_face(self):
        student_name = self.student_name_entry.get()
        student_id = self.student_id_entry.get()
        student_added = add_face(student_name, student_id, WEBCAM)
        if student_added:
            messagebox.showinfo("Success", "Student has been added to the system!")
        else:
            messagebox.showerror("Error", "Failed to add student!")

    def open_add_students(self):
        self.tabControl.select(self.student_management_tab)

    def open_attendance_view(self):
        # Refresh the attendance records before opening the tab
        self.on_select_attendance_date(None)
        self.tabControl.select(self.attendance_view_tab)

    def face_attendance(self):
        can_take_attendance = face_attendance(WEBCAM)
        if not can_take_attendance:
            messagebox.showerror("Error", "Failed to take attendance!")
            
    def attendance_records_by_date(self, date):
        records = load_attendances(date)
        
        if len(records) == 0:
            return self.attendance_list.clear()
        
        for record in records.itertuples():
            record = record._asdict()
            self.attendance_list.append(f"ID: {record[COL[0]]} Name: {record[COL[1]]} Date: {record[COL[2]]} Time: {record[COL[3]]}")
        
    def refresh_attendance(self):
        # Functionality to refresh and display attendance records
        self.attendance_text.delete(1.0, tk.END)  # Clear previous records
        if self.attendance_list:
            for record in self.attendance_list:
                self.attendance_text.insert(tk.END, f"{record}\n")
        else:
            self.attendance_text.insert(tk.END, "No attendance records.")

    def all_attendance_dates(self):
        files = os.listdir('attendances')
        attendance_dates = [file.split('.')[0] for file in files if file.endswith('.csv')]
        default_select = f"attendance_{get_today_date()}"

        if default_select not in attendance_dates:
            attendance_dates.append(default_select)

        self.attendance_date_dropdown['values'] = attendance_dates
        self.attendance_date_var.set(default_select)
        self.attendance_records_by_date(default_select.split('_')[1])
        self.refresh_attendance()

    def on_select_attendance_date(self, event):
        date = self.attendance_date_var.get().split('_')[1]
        self.attendance_list.clear()
        self.attendance_records_by_date(date)
        self.refresh_attendance()

def main():
    root = tk.Tk()
    app = FaceAttendanceSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
