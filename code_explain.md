### Overview

* **Tkinter** for the graphical user interface (GUI).
* **OpenCV (cv2)** to capture photos using a webcam.
* **QRCode** to generate QR codes.
* **ReportLab** to create PDF documents.
* **hashlib** to generate unique hash codes for each student.
* **os** and **csv** for file and directory operations and CSV file handling.
* **datetime** to handle dates for the dummy exam schedule.

### Class: `HallTicketGeneratorApp`

* Initializes the application window and its components.
* Manages student data input, photo capture, hall ticket generation, and CSV logging.

### Initialization `__init__(self, master)`

* Sets up the GUI layout with input fields for student details and buttons for capturing a photo and generating the hall ticket.
* Checks for an existing CSV file to log hall ticket details or creates a new one with a header row.
* Prepares a set to track unique hash codes to ensure each hall ticket is generated only once.

### Method: `capture_photo(self)`

* Invokes the webcam to capture a photo.
* Saves the photo temporarily, which later gets moved to a permanent directory with a unique name upon hall ticket generation.
* The temporary photo is removed after being embedded into the hall ticket PDF.

### Method: `generate_hall_ticket(self)`

* Gathers input data from the GUI.
* Validates the completeness of the input.
* Generates a unique hash code from the student details to check for uniqueness.
* Prevents duplicate hall tickets based on the unique hash code.
* Calls `generate_hall_ticket_pdf` to create the hall ticket.
* Logs the hall ticket details in the CSV file.
* Cleans up any temporary files used in the process.

### Method: `generate_hall_ticket_pdf(self, student_details, photo_path, pdf_path)`

* Generates a QR code specific to the student's roll number and saves it temporarily.
* Creates a PDF hall ticket embedding the student's photo, personal details, the QR code, and a dummy exam schedule.
* The layout is designed to be semantically structured like a typical hall ticket.
* Cleans up the temporary QR code image after embedding it into the PDF.

### Utility and Cleanup

* Temporary files (`temp_photo.jpg` and `temp_qr.png`) are created during the process. These are deleted after their contents are embedded into the hall ticket PDF, ensuring they don't accumulate over time.
* The hall tickets are stored in a specific directory (`hall_tickets`), and the details of each generated hall ticket are logged in a CSV file located in the default directory to maintain a record.

### Running the Application

* Instantiates the application class and starts the Tkinter event loop.
* The application is ready to accept input, capture photos, generate QR codes, create PDF hall tickets, and log the operations in a CSV file, providing a complete workflow for hall ticket generation.
