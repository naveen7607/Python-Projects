import mysql.connector
from datetime import date

# ---------------- Database Class ----------------
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",password="1475369",database="student_management")
        self.cursor = self.connection.cursor()

    def execute(self, query, values=None):
        self.cursor.execute(query, values or ())
        self.connection.commit()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchone()

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

db = Database()

# ---------------- Developer (Table Setup) ----------------
class Developer:
    def create_tables(self):
        db.execute("CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(20) PRIMARY KEY, password VARCHAR(20), role VARCHAR(20))")
        db.execute("CREATE TABLE IF NOT EXISTS marks (student_id VARCHAR(20), subject VARCHAR(20), marks INT)")
        db.execute("CREATE TABLE IF NOT EXISTS attendance (student_id VARCHAR(20), subject VARCHAR(20), att_date DATE, status VARCHAR(10))")

Developer().create_tables()
# ---------------- User Class ----------------
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def update_password(self):
        old_pass = input("Old Password: ")
        new_pass = input("New Password: ")

        user = db.fetch_one("SELECT * FROM users WHERE user_id=%s AND password=%s",(self.user_id, old_pass))
        if not user:
            raise Exception("Old password incorrect")

        db.execute("UPDATE users SET password=%s WHERE user_id=%s",(new_pass, self.user_id))
        print("✔ Password updated successfully")

# ---------------- Student Class ----------------
class Student(User):
    def view_marks(self):
        records = db.fetch_all(
            "SELECT subject, marks FROM marks WHERE student_id=%s",
            (self.user_id,)
        )
        print("\n--- MARKS ---")
        print("Subject\tMarks")
        print("-" * 20)
        for r in records:
            print(f"{r[0]}\t{r[1]}")

    def view_attendance(self):
        records = db.fetch_all("SELECT subject, att_date, status FROM attendance WHERE student_id=%s",(self.user_id,))
        print("\n--- ATTENDANCE ---")
        print("Subject\tDate\t\tStatus")
        print("-" * 35)
        for r in records:
            print(f"{r[0]}\t{r[1]}\t{r[2]}")

# ---------------- Professor Class ----------------
class Professor(User):
    def update_marks(self):
        student_id = input("Student ID: ")
        subject = input("Subject: ")
        marks = int(input("Marks: "))

        record = db.fetch_one("SELECT * FROM marks WHERE student_id=%s AND subject=%s",(student_id, subject))
        if record:
            db.execute(
                "UPDATE marks SET marks=%s WHERE student_id=%s AND subject=%s",(marks, student_id, subject))
        else:
            db.execute(
                "INSERT INTO marks VALUES (%s, %s, %s)",
                (student_id, subject, marks)
            )
        print("✔ Marks updated")

    def update_attendance(self):
        student_id = input("Student ID: ")
        subject = input("Subject: ")
        status = input("Status (Present/Absent): ").capitalize()
        today = date.today()

        record = db.fetch_one("SELECT * FROM attendance WHERE student_id=%s AND subject=%s AND att_date=%s",(student_id, subject, today))
        if record:
            db.execute("UPDATE attendance SET status=%s WHERE student_id=%s AND subject=%s AND att_date=%s",(status, student_id, subject, today))
        else:
            db.execute("INSERT INTO attendance VALUES (%s, %s, %s, %s)",(student_id, subject, today, status))
        print("✔ Attendance recorded")

# ---------------- Admin Class ----------------
class Admin(User):
    def add_user(self):
        uid = input("New User ID: ")
        pwd = input("Password: ")
        role = input("Role (student/professor/admin): ")
        db.execute("INSERT INTO users VALUES (%s, %s, %s)", (uid, pwd, role))
        print("✔ User added")

    def update_user_role(self):
        uid = input("User ID: ")
        role = input("New Role: ")
        db.execute("UPDATE users SET role=%s WHERE user_id=%s", (role, uid))
        print("✔ Role updated")

# ---------------- Main Program ----------------
while True:
    try:
        print("\n" + "=" * 50)
        print(" STUDENT MANAGEMENT SYSTEM ")
        print("=" * 50)
        print("1) Student\n2) Professor\n3) Admin\n4) Exit")

        role_choice = input("Choose Role: ")

        if role_choice == "4":
            break

        role_map = {"1": "student", "2": "professor", "3": "admin"}
        role = role_map.get(role_choice)

        if not role:
            raise Exception("Invalid role selection")

        user_id = input("User ID: ")
        password = input("Password: ")

        valid = db.fetch_one(
            "SELECT * FROM users WHERE user_id=%s AND password=%s AND role=%s",
            (user_id, password, role)
        )
        if not valid:
            raise Exception("Invalid login credentials")

        print(f"\n✔ Logged in as {role.upper()}")

        # -------- ROLE MENUS (LOOP UNTIL LOGOUT) --------
        while True:
            print("\n1) Change Password")

            if role == "student":
                print("2) View Marks\n3) View Attendance\n4) Logout")
                student = Student(user_id)
                choice = input("Choose option: ")

                if choice == "1":
                    student.update_password()
                elif choice == "2":
                    student.view_marks()
                elif choice == "3":
                    student.view_attendance()
                elif choice == "4":
                    break

            elif role == "professor":
                print("2) Update Marks\n3) Update Attendance\n4) Logout")
                professor = Professor(user_id)
                choice = input("Choose option: ")

                if choice == "1":
                    professor.update_password()
                elif choice == "2":
                    professor.update_marks()
                elif choice == "3":
                    professor.update_attendance()
                elif choice == "4":
                    break

            elif role == "admin":
                print("2) Add User\n3) Update User Role\n4) Logout")
                admin = Admin(user_id)
                choice = input("Choose option: ")

                if choice == "1":
                    admin.update_password()
                elif choice == "2":
                    admin.add_user()
                elif choice == "3":
                    admin.update_user_role()
                elif choice == "4":
                    break

    except Exception as e:
        print("✖ Error:", e)
        continue