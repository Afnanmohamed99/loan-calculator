# Loan Calculator

A user-friendly loan amortization calculator built with Python and PyQt5.  This application provides a graphical interface for calculating loan payments, generating amortization schedules, and visualizing payment breakdowns.

## Features

* **Calculate Loan Payments:**  Easily calculate monthly and total loan payments based on loan amount, interest rate, and loan term.
* **Generate Amortization Schedule:**  Generate a detailed amortization schedule showing the breakdown of principal, interest, and remaining balance for each payment period.
* **Visualize Payment Breakdown:**  Visualize the principal and interest components of your loan payments over time with a clear and interactive graph.
* **Export Results:** Export the amortization schedule to PDF or CSV for record-keeping or further analysis.
* **Currency Selection:** Choose from different currencies (USD, EUR, CAD) for calculations and display.
* **User-Friendly Interface:**  Intuitive and easy-to-use graphical interface built with PyQt5.


## Installation

This application requires Python and the following libraries:

- PyQt5: For the graphical user interface.
- pandas: For creating and manipulating DataFrames (used for the amortization schedule).
- numpy: For numerical operations (array creation, calculations).
- matplotlib: For creating the graph of principal and interest payments.
- fpdf: For generating PDF output of the amortization schedule.
- decimal: This is a built in library that comes with python, but I'm including it for clarity.

You can install these libraries using pip:

pip install PyQt5 pandas numpy matplotlib fpdf

