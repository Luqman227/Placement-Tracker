# Placement Tracker
# A simple program to keep track of internship and placement applications.

import sqlite3

# Connect to the database file (it is created the first time you run this)
connection = sqlite3.connect("applications.db")
cursor = connection.cursor()

# Create the table if it does not exist yet
cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        status TEXT,
        deadline TEXT
    )
""")
connection.commit()

STATUSES = ["applied", "online test", "interview", "offer", "rejected"]

# The skills I have, used to check job adverts
my_skills = ["python", "java", "sql", "git", "teamwork", "communication"]


def add_application():
    company = input("Company name: ")
    role = input("Role: ")
    deadline = input("Deadline (YYYY-MM-DD) or press Enter to skip: ")
    cursor.execute(
        "INSERT INTO applications (company, role, status, deadline) VALUES (?, ?, ?, ?)",
        (company, role, "applied", deadline),
    )
    connection.commit()
    print("Application added.")


def show_applications():
    cursor.execute("SELECT id, company, role, status, deadline FROM applications")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("No applications yet.")
    for row in rows:
        print(f"#{row[0]} | {row[1]} | {row[2]} | {row[3]} | deadline: {row[4] or 'none'}")


def update_status():
    show_applications()
    app_id = input("Enter the id number to update: ")
    if not app_id.isdigit():
        print("Please enter a number.")
        return
    print("Statuses:", ", ".join(STATUSES))
    new_status = input("New status: ").lower()
    if new_status not in STATUSES:
        print("That is not a valid status.")
        return
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, int(app_id)))
    connection.commit()
    if cursor.rowcount == 0:
        print("No application with that id.")
    else:
        print("Status updated.")


def show_stats():
    cursor.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    for status, count in cursor.fetchall():
        print(f"{status}: {count}")


def check_advert():
    print("Paste the job advert as one block of text, then press Enter:")
    advert = input().lower()
    matched = []
    for skill in my_skills:
        if skill in advert:
            matched.append(skill)
    score = round(100 * len(matched) / len(my_skills))
    print(f"You match {score}% of my skills list.")
    print("Skills that match:", ", ".join(matched) or "none")


# Main menu, repeats until the user chooses to quit
while True:
    print()
    print("1. Add an application")
    print("2. Show all applications")
    print("3. Update an application's status")
    print("4. Show statistics")
    print("5. Check a job advert against my skills")
    print("6. Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        add_application()
    elif choice == "2":
        show_applications()
    elif choice == "3":
        update_status()
    elif choice == "4":
        show_stats()
    elif choice == "5":
        check_advert()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Please choose a number from 1 to 6.")

connection.close()