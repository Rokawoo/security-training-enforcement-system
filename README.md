<div align="center">
  <h1>Security Enforcement System</h1>
  <p>By Rokawoo</p>
  <img src="https://www.pngplay.com/wp-content/uploads/7/Cybersecurity-No-Background.png" alt="Security Logo" width="150" height="150">
</div>

> [!CAUTION]
> ⭐ If your security certificates are out of date, expect a visit. Yeah, I would start running if I were you.

**What is a Security Enforcement System?**
A Security Enforcement System is a package of scripts that you can run to log user data, certificate names, and certificate dates. After logging, the data is normalized, categorized, and then distributed to the proper record folder for safekeeping. Additionally, there's a record search function for verifying the existence or status of stored records.

**Demo**

[Demo](https://github.com/Rokawoo/security-training-enforcement-system/assets/129356996/93778193-ac08-44a1-91df-63a4412b0e87)

**Features Include:**
- Conversion of images to PDFs.
- Content-aware PDF scanning to extract dates.
- Automatic retrieval of first and last names with a switch option.
- PDF display for review if no date is found.
- A robust date-logging system that alerts you about outdated certificates. It also facilitates easy assignment of dates to certificates in DD, MM-DD, or YYYY-MM-DD formats.
- Auto-filling of missing information with the current system date.
- A file buffer to ensure files are not distributed in case of error.
- Automatic and manual modes of distribution.
- Logging of moved files for audit.

**How to Use the System**
**Security Enforcement System**:
1. Type "get" or enter a name to start.
2. Watch as specified files are normalized and sorted into corresponding folders.
3. Type "end" to flush the buffer, or repeat steps to process more files.

**Record Search**:
1. Enter the first and last name to search for a record.
2. View existing records in the search directory and subdirectories.


## 🛠 Libraries and Tools Used

The project uses the following libraries and tools:

- **pdfplumber**: For working with and extracting content from PDF files.
- **datetime**: Python's built-in module for date and time manipulations.
- **re**: Python's built-in module for regular expressions.
- **fitz**: From PyMuPDF, used to work with PDF files.
- **tkinter**: Python's built-in library for creating graphical user interfaces.
- **datefinder**: For finding dates in text.
- **PIL (Python Imaging Library)**: For image processing, accessed through `Image` and `ImageTk`.
- **os**: For interacting with the operating system, such as file operations.
- **shutil**: For high-level file operations like copying and moving files.
- **logging**: For logging messages and errors in Python.
- **subprocess**: For running subprocesses and executing system commands from Python.
- **sys**: Provides access to some system-specific parameters and functions.
- **dotenv**: For loading environment variables from `.env` files.
- **reportlab**: Specifically, `reportlab.lib.pagesizes` and `reportlab.pdfgen.canvas`, used for generating PDFs.




