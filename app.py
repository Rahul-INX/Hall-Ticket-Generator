import tkinter as tk
from tkinter import messagebox
import cv2
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import hashlib
import os
import csv
from datetime import datetime, timedelta

# Main application class
class HallTicketGeneratorApp:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        master.title("Hall Ticket Generator")

        # Directory for storing generated PDFs
        self.storage_dir = "hall_tickets"
        os.makedirs(self.storage_dir, exist_ok=True)

        # CSV file for recording hall ticket details; stored in the default directory
        self.csv_file = "hall_tickets_record.csv"
        self.existing_hashes = set()  # Set to track unique hash codes to avoid duplicate entries

        # Load existing hashes from the CSV if it exists, to maintain uniqueness
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.existing_hashes.add(row['Hash'])
        else:
            # Create the CSV file if it doesn't exist, with headers
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Roll Number', 'Name', 'DOB', 'College Name', 'PDF Path', 'Hash', 'Date of Issue'])

        # GUI elements
        tk.Label(master, text="Roll Number").grid(row=0, column=0)
        self.roll_number = tk.Entry(master)
        self.roll_number.grid(row=0, column=1)

        tk.Label(master, text="Name").grid(row=1, column=0)
        self.name = tk.Entry(master)
        self.name.grid(row=1, column=1)

        tk.Label(master, text="Date of Birth").grid(row=2, column=0)
        self.dob = tk.Entry(master)
        self.dob.grid(row=2, column=1)

        tk.Label(master, text="College Name").grid(row=3, column=0)
        self.college_name = tk.Entry(master)
        self.college_name.grid(row=3, column=1)

        # Buttons for capturing a photo and generating the hall ticket
        tk.Button(master, text="Capture Photo", command=self.capture_photo).grid(row=4, column=0)
        tk.Button(master, text="Generate Hall Ticket", command=self.generate_hall_ticket).grid(row=4, column=1)

    # Method to capture a photo using the system's camera
    def capture_photo(self):
        photo_path = "temp_photo.jpg"  # Temporary file path for the captured photo
        cap = cv2.VideoCapture(0)  # Initialize the camera
        while True:
            ret, frame = cap.read()
            cv2.imshow("Capture - Press SPACE to capture", frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                cv2.imwrite(photo_path, frame)  # Save the captured photo
                messagebox.showinfo("Success", "Photo captured successfully!")
                break
        cap.release()
        cv2.destroyAllWindows()

    # Method to generate the hall ticket PDF
    def generate_hall_ticket(self):
        # Collect input from the GUI
        student_details = {
            'roll_number': self.roll_number.get(),
            'name': self.name.get(),
            'dob': self.dob.get(),
            'college_name': self.college_name.get(),
        }

        # Ensure all fields are filled
        if not all(student_details.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Generate a unique hash for the student details
        unique_identifier = hashlib.sha256('_'.join(student_details.values()).encode()).hexdigest()

        # Check for the uniqueness of the hash code
        if unique_identifier in self.existing_hashes:
            messagebox.showinfo("Duplicate", "A hall ticket with these details has already been generated.")
            if 
            os.remove('temp_photo.jpg')  # Remove the temporary photo if duplicate
            return

        # Define the PDF path using the unique hash
        pdf_path = os.path.join(self.storage_dir, f"{unique_identifier}.pdf")

        # Generate the PDF
        self.generate_hall_ticket_pdf(student_details, "temp_photo.jpg", pdf_path)

        # Clean up the temporary photo after adding it to the PDF
        os.remove("temp_photo.jpg")

        # Record the hall ticket details in the CSV
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                student_details['roll_number'], student_details['name'],
                student_details['dob'], student_details['college_name'],
                pdf_path, unique_identifier, datetime.now().strftime('%Y-%m-%d')
            ])
        self.existing_hashes.add(unique_identifier)  # Add the new hash to the set

        messagebox.showinfo("Success", "Hall Ticket Generated Successfully!")

    # Method to create the hall ticket PDF
    def generate_hall_ticket_pdf(self, student_details, photo_path, pdf_path):
        qr_code = qrcode.make(student_details['roll_number'])  # Generate QR code
        qr_code.save("temp_qr.png")  # Save the QR code temporarily

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Add student details to the PDF
        c.drawString(200, height - 100, f"Roll Number: {student_details['roll_number']}")
        c.drawString(200, height - 115, f"Name: {student_details['name']}")
        c.drawString(200, height - 130, f"DOB: {student_details['dob']}")
        c.drawString(200, height - 145, f"College: {student_details['college_name']}")

        # Add the photo and QR code to the PDF
        if os.path.exists(photo_path):
            c.drawImage(photo_path, 50, height - 150, width=100, height=100)
        c.drawImage("temp_qr.png", width - 150, height - 150, width=100, height=100)

        # Generate a dummy exam schedule and add it to the PDF
        schedule_start_y = height / 2 + 50
        c.drawString(width / 2 - 75, schedule_start_y, "Exam Schedule:")
        exams = [
            {"subject": "Mathematics", "code": "MTH101", "date": datetime.now() + timedelta(days=10)},
            {"subject": "Physics", "code": "PHY101", "date": datetime.now() + timedelta(days=15)},
            {"subject": "Chemistry", "code": "CHM101", "date": datetime.now() + timedelta(days=20)},
        ]
        for i, exam in enumerate(exams):
            c.drawString(width / 2 - 75, schedule_start_y - (15 * (i + 1)), f"{exam['subject']} ({exam['code']}) - {exam['date'].strftime('%Y-%m-%d')}")

        c.save()  # Save the PDF
        os.remove("temp_qr.png")  # Clean up the temporary QR code

if __name__ == "__main__":
    root = tk.Tk()
    app = HallTicketGeneratorApp(root)
    root.mainloop()
