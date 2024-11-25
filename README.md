# Loan Calculator Application

This Python application provides a graphical user interface (GUI) for calculating loan amortization schedules.  It uses PyQt5 for the GUI, NumPy for numerical computations, Pandas for data manipulation, Matplotlib for charting, and fpdf for PDF report generation.

## Features

* **Loan Amortization Calculation:** Calculates monthly payments, total payments, and a detailed amortization schedule.
* **User-Friendly Interface:**  A PyQt5-based GUI makes it easy to input loan details and view results.
* **Input Validation:** Checks for invalid or missing input data.
* **Progress Indication:** Displays a progress bar during calculation (currently shows a simple representation).
* **Currency Support:** Allows selection of currency from USD, EUR and CAD. Currency symbol is updated dynamically based on the selection.
* **Result Presentation:** Displays monthly and total payments.
* **Amortization Table:** Presents the detailed amortization schedule in a separate window.
* **Amortization Graph:** Shows a graph visualizing principal and interest payments over time.
* **Data Export:** Allows saving the amortization schedule to a CSV file or a PDF report.
* **Error Handling:** Includes custom exception classes and error messages for better user experience.
* **Multithreading:** Performs the loan calculation in a separate thread to prevent the GUI from freezing.


### Installing Dependencies
You can install the required libraries using pip:

```bash
pip install PyQt5 numpy pandas matplotlib fpdf
```

## Usage Instructions

1. **Launch the Application:** Run the `main.py` script.  This will open the main application window.

2. **Input Loan Details:**  Enter the necessary loan information into the designated fields:

    * **Annual Interest Rate (%):** Enter the annual interest rate as a percentage (e.g., 5.25 for 5.25%).
    * **Loan Term (Years):** Specify the loan's duration in years (e.g., 30).
    * **Loan Amount:** Input the total principal loan amount (e.g., 250000).
    * **Currency:** Select the desired currency from the dropdown menu: USD, EUR, or CAD.

3. **Compute:** Click the "Compute" button to begin the calculation. A progress bar will be displayed to show the calculation's progress.  This step may take a few seconds depending on the loan parameters.

4. **View Results:** Once the calculation is complete, the application will display the calculated:
    * **Monthly Payment:** The amount due each month.
    * **Total Payment:** The total amount paid over the loan's lifetime.  These values will be displayed in the selected currency.

5. **View Amortization Table:** Click the "Table" button to open a new window showing a detailed amortization schedule. This table provides a month-by-month breakdown of your loan payments, including principal, interest, and the remaining balance.

6. **View Amortization Graph:** Click the "Graph" button to generate a visual representation of your loan's amortization. This graph will clearly show the principal and interest components of your payments over time.

7. **Save Results:** Click the "Save" button to save your amortization schedule. You will then be prompted to choose between saving the data as a CSV (Comma Separated Values) file or a PDF (Portable Document Format) file. Select your preferred file type and specify a location to save the file.


## Screenshots

## Technical Details

The application leverages several powerful Python libraries:

* **GUI Framework:** PyQt5 provides the user-friendly graphical interface.
* **Numerical Computation:** NumPy is used for efficient numerical calculations.
* **Data Manipulation:** Pandas handles data organization and manipulation of the amortization schedule.
* **Charting:** Matplotlib creates the visual representation of the amortization graph.
* **PDF Generation:** The fpdf library generates the downloadable PDF reports.
* **Error Handling:** Custom exception handling ensures robustness and provides informative error messages to the user.
* **Multithreading:**  The application uses multithreading to perform calculations in the background, preventing the GUI from freezing during processing.


## Contributing

I welcome contributions to improve the Loan Calculator application! Here's how you can get involved:

### Setting up the Development Environment

1. **Fork the Repository:** Create your own copy of the project by forking the main repository on GitHub.  You can find the "Fork" button on the repository's main page.

2. **Clone Your Fork:** Clone your forked repository to your local machine:

   ```bash
   git clone <https://github.com/Afnanmohamed99/loan-calculator>`
   ```

3. **Create a Virtual Environment (Recommended):**  This isolates the project's dependencies:

   ```bash
   python3 -m venv venv  # Create a virtual environment
   source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
   venv\Scripts\activate  # Activate the virtual environment (Windows)
   ```

4. **Install Dependencies:** Install the required Python packages.  A `requirements.txt` file (if you have one) lists them; otherwise, install the packages manually.

   ```bash
   pip install -r requirements.txt  # Or install manually if needed
   ```


### Making Changes

1. **Create a New Branch:** Before making changes, create a new branch to keep your work separate:

   ```bash
   git checkout -b feature/<your-feature-name>  # or bugfix/<bug-number>
   ```

2. **Develop Your Changes:** Implement your feature or bug fix, adhering to the project's coding style and conventions.  Ensure your code is well-documented and easy to understand.

3. **Test Thoroughly:** Test your changes extensively.  Write unit tests to confirm your code works as expected and doesn't introduce new problems.

4. **Commit Your Changes:** Commit your changes with descriptive commit messages:

   ```bash
   git add .  # Stage changes
   git commit -m "Your descriptive commit message"
   ```


### Submitting a Pull Request

1. **Push Your Branch:** Push your branch to your forked repository on GitHub:

   ```bash
   git push origin feature/<your-feature-name>  # or bugfix/<bug-number>
   ```
   
2. **Create a Pull Request:** Go to the original repository on GitHub and create a pull request from your branch to the main branch (usually `main` or `master`). Write a clear description of your changes and address any comments or feedback from the maintainers.


### Code Style and Conventions

* Follow PEP 8 style guidelines for Python code.
* Use clear, concise commit messages.
* Write meaningful variable and function names.
* Add comprehensive tests for any new functionality.


### Communication

Feel free to open issues on the issue tracker to report bugs, suggest features, or ask questions.  Engage in discussions on pull requests to provide feedback and address any reviewer comments.


I appreciate your contributions!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
