# Loan Calculator Application

This Python application provides a graphical user interface (GUI) for calculating loan amortization schedules. It uses PyQt5 for the GUI, NumPy for numerical computations, Pandas for data manipulation, Matplotlib for charting, and fpdf for PDF report generation.

## Features

* Loan Amortization Calculation: Calculates monthly payments, total payments, and a detailed amortization schedule.
* User-Friendly Interface: A PyQt5-based GUI simplifies input and result viewing.
* Input Validation: Prevents errors from invalid or missing data.
* Progress Indication: Displays a progress bar during calculation.
* Currency Support: Supports USD, EUR, and CAD with dynamic currency symbol updates.
* Result Presentation: Clearly displays monthly and total payments in the selected currency.
* Amortization Table: Presents a detailed schedule in a separate window.
* Amortization Graph: Visualizes principal and interest payments over time.
* Data Export: Allows saving the schedule to CSV or PDF files.
* Error Handling: Includes robust error handling with informative messages.
* Multithreading: Prevents GUI freezes during calculations.


## Installation

1. **Clone the Repository:** Fork the repository on GitHub, then clone *your* fork:

   ```bash
   git clone <your-fork-url>
   ```
   
2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
   
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   
   ```bash
   python main.py
   ```

## Usage Instructions

1. **Launch the Application:** Run the `main.py` script.
2. **Input Loan Details:** Enter the required information:
 * Annual Interest Rate (%): (e.g., 5.25)
 * Loan Term (Years): (e.g., 30)
 * Loan Amount: (e.g., 250000)
 * Currency: Select from USD, EUR, or CAD.
3. **Compute:** Click "Compute" to begin the calculation.
4. **View Results:** The monthly and total payments will be displayed.
5. **View Amortization Table:** Click "Table" to view the detailed schedule.
6. **View Amortization Graph:** Click "Graph" to view the principal/interest breakdown.
7. **Save Results:** Click "Save" to export to CSV or PDF.


## Screenshots

The following screenshots demonstrate the Loan Calculator application's key features:

**1. Main Window (Initial State):**

![Main Window (Empty)](main_window_initial.png)

This shows the application's main window with input fields for loan details (interest rate, loan term, amount, and currency selection).  The fields include placeholders for guidance.

**2. Main Window (Results):**

![Main Window (Results)](main_window_results.png)

This screenshot displays the main window after a loan calculation. The calculated monthly and total payments are shown, clearly formatted with the chosen currency symbol. A progress bar indicates 100% completion of the calculation.

**3. Amortization Graph:**

![Amortization Graph](amortization_graph.png)

This graph visually represents the loan's amortization schedule, showing the principal and interest payments over time.  The graph provides a quick overview of how your loan payments are allocated.

**4. & 5. Amortization Table:**

![Amortization Table](amortization_table.png)  

This detailed table provides a month-by-month breakdown of the loan's amortization.  Each row shows the month, interest rate, payment amount, interest paid, principal paid, and the remaining loan balance.

**6. Save As Dialog:**

![Save As Dialog](save_as_dialog.png)

This dialog allows users to choose between saving the amortization schedule as a PDF or CSV file. This provides flexibility for users to utilize the results as they need.

## Technical Details

* GUI Framework: PyQt5
* Numerical Computation: NumPy
* Data Manipulation: Pandas
* Charting: Matplotlib
* PDF Generation: fpdf
* Error Handling: Custom exceptions
* Multithreading: Prevents GUI freezes


## Contributing

We welcome contributions!

1. **Fork the Repository:** [https://docs.github.com/en/get-started/quickstart/fork-a-repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

2. **Clone Your Fork:**

   ```bash
   git clone <your-fork-url>
   ```

3. **Create a Virtual Environment:** This isolates the project's dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
   
4. **Install Dependencies:** Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a Branch:**

   ```bash
   git checkout -b feature/<your-feature-name>
   ```

6. **Develop, Test, and Commit:** Make changes, test thoroughly, commit with clear messages.

7. **Push and Create Pull Request:** Push your branch and create a pull request to the `main` branch.


## Code Style and Conventions

* Follow PEP 8.
* Use clear commit messages.
* Use meaningful names.
* Add comprehensive tests.


## Communication

Use the GitHub issue tracker.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


