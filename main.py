import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP
import threading
import locale  # For currency formatting
import csv
from fpdf import FPDF

# Constants
MONTHS_IN_YEAR = 12

# Custom Exception Classes
class InvalidInputError(Exception):
    """Custom exception raised for invalid user input."""
    pass

class CalculationError(Exception):
    """Custom exception raised for errors during calculations."""
    pass


class LoanCalculator(QMainWindow):
    """
    Main class for the loan calculator application.
    Handles UI creation, calculation logic, and result display.
    """
    calculation_finished = pyqtSignal(float, float)

    def __init__(self):
        """Initializes the LoanCalculator application."""
        super().__init__()
        self.setWindowTitle("Loan Calculator")
        self.setGeometry(200, 200, 700, 700)
        self.setMinimumSize(700, 700)
        self.setStyleSheet(self.get_stylesheet())
        self.create_ui_components()
        self.show()
        self.amortization_data = None
        self.progress_dialog = None
        self.currency_symbol = "$"  
        self.currency.currentIndexChanged.connect(self.update_currency_symbol)
        locale.setlocale(locale.LC_ALL, '') 

    def get_stylesheet(self):
        """Returns the stylesheet for the application."""
        return """
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 12px;
                color: #333;
                background-color: #f0f0f0;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QPushButton {
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                border-radius: 5px;
                cursor: pointer;
            }
            QPushButton#computeButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#computeButton:hover {
                background-color: #45a049;
            }
            QPushButton#clearButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton#clearButton:hover {
                background-color: #d32f2f;
            }
            QPushButton#saveButton {
                background-color: #2196F3;
                color: white;
            }
            QPushButton#saveButton:hover {
                background-color: #1976D2;
            }

            QPushButton#graphButton {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#graphButton:hover {
                background-color: #FFC107;
            }
            QPushButton#tableButton {
                background-color: #9C27B0;
                color: white;
            }
            QPushButton#tableButton:hover {
                background-color: #BA68C8;
            }

        """

    def clear_fields(self):
        """Clears all input and output fields."""
        self.rate.clear()
        self.years.clear()
        self.amount.clear()
        self.currency.setCurrentIndex(0)
        self.monthly_payment.clear()
        self.total_payment.clear()
        self.progress_bar.reset()  
        self.amortization_data = None 
        if self.progress_dialog:
            self.progress_dialog.close()
        

    def create_ui_components(self):
        """Creates and arranges the UI components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(self.create_title_section())
        input_group_box = self.create_input_section()
        main_layout.addWidget(input_group_box)
        output_group_box = self.create_output_section()
        main_layout.addWidget(output_group_box)
        main_layout.addSpacing(20)
        main_layout.addLayout(self.create_button_section())
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_title_section(self):
        """Creates the title section of the UI."""
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        title_label = self._create_label("Loan Calculator", font=('Times', 18, QFont.Bold), style="color: darkblue;")
        bank_label = self._create_label("XYZ Bank", font=('Times', 14), style="color: gray;")
        title_layout.addWidget(title_label)
        title_layout.addWidget(bank_label)
        return title_layout

    def _create_label(self, text, font=None, style=None):
        """Creates a QLabel with optional font and style."""
        label = QLabel(text)
        if font: label.setFont(QFont(*font))  
        if style: label.setStyleSheet(style)
        return label

    def _create_line_edit(self, validator, fixed_width=180, placeholder=""):
        """Creates a QLineEdit with a validator."""
        line_edit = QLineEdit()
        line_edit.setFont(QFont('Arial', 10))
        line_edit.setValidator(validator)
        line_edit.setFixedWidth(fixed_width)
        line_edit.setPlaceholderText(placeholder)
        return line_edit  

    def create_input_section(self):
        """Creates the input section of the UI."""
        input_layout = QGridLayout()
        input_layout.setSpacing(10)
        rate_validator = QRegExpValidator(QRegExp(r"^\d+(\.\d{1,2})?$"))
        amount_validator = QRegExpValidator(QRegExp(r"^\d+(\.\d{1,2})?$")) 
        years_validator = QIntValidator(1,100)
        rate_label = self._create_label("Annual Interest Rate (%)", font=('Arial', 12, QFont.Bold))
        self.rate = self._create_line_edit(rate_validator, placeholder="E.g., 5.25")
        years_label = self._create_label("Loan Term (Years)", font=('Arial', 12, QFont.Bold))
        self.years = self._create_line_edit(years_validator, placeholder="E.g., 30")
        amount_label = self._create_label("Loan Amount", font=('Arial', 12, QFont.Bold))
        self.amount = self._create_line_edit(amount_validator, placeholder="E.g., 250000")
        currency_label = self._create_label("Currency")
        self.currency = QComboBox()
        self.currency.addItems(["USD", "EUR", "CAD"])
        self.currency.setFixedWidth(100)
        input_layout.addWidget(rate_label, 0, 0) 
        input_layout.addWidget(self.rate, 0, 1)    
        input_layout.addWidget(years_label, 1, 0)  
        input_layout.addWidget(self.years, 1, 1)   
        input_layout.addWidget(amount_label, 2, 0)
        input_layout.addWidget(self.amount, 2, 1)
        input_layout.addWidget(currency_label, 3, 0)
        input_layout.addWidget(self.currency, 3, 1)
        input_group_box = QGroupBox("Loan Details")
        input_group_box.setLayout(input_layout)
        self.currency.currentIndexChanged.connect(self.update_currency_symbol) 
        self.rate.textEdited.connect(self.clear_results_and_progress) 
        self.years.textEdited.connect(self.clear_results_and_progress)
        self.amount.textEdited.connect(self.clear_results_and_progress)
        return input_group_box

    def clear_results_and_progress(self): 
        """Clears the results and resets the progress bar."""
        self.monthly_payment.clear()
        self.total_payment.clear()
        self.progress_bar.reset()
        self.amortization_data = None 

    def _create_button(self, text, function, button_id=""):
        """Creates a QPushButton."""
        button = QPushButton(text, self)
        button.setFont(QFont('Arial', 12))
        button.setFixedHeight(45)
        button.setFixedWidth(100)
        button.clicked.connect(function)
        button.setObjectName(button_id)
        return button

    def create_button_section(self):
        """Creates the button section of the UI."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self._create_button("Compute", self.calculate_loan, "computeButton")) 
        button_layout.addWidget(self._create_button("Clear", self.clear_fields, "clearButton"))  
        button_layout.addWidget(self._create_button("Graph", self.show_graph, "graphButton"))      
        button_layout.addWidget(self._create_button("Table", self.show_amortization_table, "tableButton")) 
        button_layout.addWidget(self._create_button("Save", self.save_dialog, "saveButton")) 
        return button_layout


    def create_output_section(self):
        """Creates the output section of the UI."""
        output_layout = QGridLayout()
        output_layout.setSpacing(10)
        monthly_payment_label = self._create_label("Monthly Payment:", font=('Arial', 12, QFont.Bold))
        self.monthly_payment = self._create_output_value_label()
        total_payment_label = self._create_label("Total Payment:", font=('Arial', 12, QFont.Bold))
        self.total_payment = self._create_output_value_label()
        self.progress_bar = QProgressBar(self) 
        self.progress_bar.setGeometry(200, 80, 250, 20)
        output_layout.addWidget(self.progress_bar,2,0,1,2) 
        output_layout.addWidget(monthly_payment_label, 0, 0)
        output_layout.addWidget(self.monthly_payment, 0, 1)
        output_layout.addWidget(total_payment_label, 1, 0)
        output_layout.addWidget(self.total_payment, 1, 1)
        output_group_box = QGroupBox("Results")
        output_group_box.setLayout(output_layout)
        return output_group_box
    
    def _create_output_value_label(self):
        """Creates a QLabel for displaying output values."""
        value_label = QLabel(self)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setFont(QFont('Arial', 14, QFont.Bold))
        value_label.setStyleSheet("background-color: #e0f7fa; border: 1px solid #4CAF50; padding: 10px;")
        value_label.setFixedWidth(200)
        value_label.setFixedHeight(40)
        return value_label


    def calculate_loan(self):
        """Initiates the loan calculation process."""
        try:
            # Input validation
            if not self.rate.text() or not self.years.text() or not self.amount.text():
                raise InvalidInputError("All fields are required.")

            try:
                annual_interest_rate = float(self.rate.text())
                loan_amount = float(self.amount.text())
                number_of_years = int(self.years.text())
            except ValueError:
                raise InvalidInputError("Invalid input: Please enter valid numbers.")

            if loan_amount <= 0:
                raise InvalidInputError("Loan amount must be positive.")
            if number_of_years <= 0:
                raise InvalidInputError("Loan term must be positive.")
            if not 0 < annual_interest_rate <= 100:
                raise InvalidInputError("Interest rate must be between 0 and 100.")

            self.calculation_thread = threading.Thread(
                target=self._perform_calculation,
                args=(loan_amount, annual_interest_rate, number_of_years),
                daemon=True
            )
            self.calculation_thread.start()

        except InvalidInputError as e:
            QMessageBox.critical(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")


    def cancel_calculation(self):
        """Cancels the ongoing calculation (currently only closes the dialog)."""
        if self.progress_dialog:
            self.progress_dialog.close()
        self.clear_results_and_progress()
        QMessageBox.warning(self, "Calculation Canceled", "The calculation has been canceled.")
    

    def _perform_calculation(self, loan_amount, annual_interest_rate, number_of_years):
        """
        Performs the loan calculation in a separate thread.
        Uses QTimer.singleShot to update the UI safely from a background thread.
        """
        try:
            self.progress_bar.setRange(0, 0)  
            self.progress_bar.show() 

            self.amortization_data = self.calculate_amortization(loan_amount, annual_interest_rate, number_of_years)
            self.calculation_finished.emit(self.amortization_data['monthly_payment'], self.amortization_data['total_payment']) 

            self.progress_bar.setRange(0, 1) 
            self.progress_bar.setValue(1) 

        except Exception as e:
            # Use QTimer.singleShot for thread-safe UI updates
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Calculation Error", f"An error occurred during calculation: {e}"))

    def _calculate_monthly_payment(self, loan_amount, monthly_interest_rate, number_of_months):
        """Calculates the monthly loan payment."""
        if monthly_interest_rate == 0:
            return loan_amount / number_of_months
        factor = (1 + monthly_interest_rate) ** number_of_months
        monthly_payment = (loan_amount * monthly_interest_rate * factor) / (factor - 1)
        return Decimal(monthly_payment).quantize(Decimal("0.00"), ROUND_HALF_UP)

    def _create_amortization_data(self, monthly_payment, total_payment, interest_rates, amortization_schedule):
        """Creates a dictionary containing amortization data."""
        return {
            "monthly_payment": float(monthly_payment),
            "total_payment": float(total_payment),
            "interest_rates": interest_rates,
            "amortization_schedule": amortization_schedule
        }
    
    def calculate_amortization(self, loan_amount, annual_interest_rate, number_of_years):
        """Calculates the full amortization schedule."""

        number_of_months = number_of_years * MONTHS_IN_YEAR
        monthly_interest_rate = annual_interest_rate / (MONTHS_IN_YEAR * 100)  # Calculate this once

        try:
            monthly_payment = self._calculate_monthly_payment(loan_amount, monthly_interest_rate, number_of_months)
        except CalculationError as e:
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Calculation Error", str(e))) # Handle error from _calculate_monthly_payment
            return None  # Return None to indicate failure


        interest_rates = np.full(number_of_months, float(annual_interest_rate))
        monthly_payments = np.full(number_of_months, float(monthly_payment))
        amortization_schedule_df = self.create_amortization_schedule(loan_amount, monthly_payments, interest_rates)

        if amortization_schedule_df is not None:  # Check if the schedule was created successfully
            return {  # Return the data directly as a dictionary
                "monthly_payment": float(monthly_payment),
                "total_payment": float(monthly_payment * number_of_months),
                "interest_rates": interest_rates,
                "amortization_schedule": amortization_schedule_df
            }
        else:
            return None # If schedule creation fails

    def update_currency_symbol(self, index):
        """Updates the currency symbol based on the selected currency."""
        currencies = {"USD": "$", "EUR": "€", "CAD": "CA$"}
        self.currency_symbol = currencies.get(self.currency.currentText(), "$") 

    def update_output_fields(self, monthly_payment, total_payment):
        """Updates the output fields with formatted values."""
        monthly_payment_str = f"{self.currency_symbol} {monthly_payment:,.2f}"
        total_payment_str = f"{self.currency_symbol} {total_payment:,.2f}"
        self.monthly_payment.setText(monthly_payment_str)
        self.total_payment.setText(total_payment_str)

    def create_amortization_schedule(self, loan_amount, monthly_payments, interest_rates):
        """
        Creates a Pandas DataFrame representing the amortization schedule.
        Handles the last payment to ensure a zero remaining balance.
        """
        total_months = len(interest_rates)
        amortization_data = {  
            "Month": np.arange(1, total_months + 1),
            "Interest Rate (%)": interest_rates,
            "Current Payment": monthly_payments,  
            "Interest": np.zeros(total_months),
            "Principal": np.zeros(total_months),
            "Remaining Balance": np.zeros(total_months)
        }
        amortization_data["Remaining Balance"][0] = loan_amount

        for i in range(total_months):
            monthly_interest_rate = float(Decimal(interest_rates[i]) / (MONTHS_IN_YEAR * Decimal(100)))
            amortization_data["Interest"][i] = amortization_data["Remaining Balance"][i] * monthly_interest_rate

            if i < total_months - 1:
                principal_payment = monthly_payments[i] - amortization_data["Interest"][i]
                principal_payment = min(principal_payment, amortization_data["Remaining Balance"][i])  
                amortization_data["Principal"][i] = principal_payment
                amortization_data["Remaining Balance"][i+1] = amortization_data["Remaining Balance"][i] - principal_payment

            else: # Handle the last payment to ensure zero remaining balance
                amortization_data["Principal"][i] = amortization_data["Remaining Balance"][i]
                amortization_data["Remaining Balance"][i] = 0  

        return pd.DataFrame(amortization_data)

    def save_results(self):
        """Saves the amortization schedule data."""
        try:
            if self.amortization_data is None:
                raise ValueError("Please calculate the payment before saving results.")

            return self.amortization_data['amortization_schedule'].copy() 

        except (ValueError, KeyError) as e:
            QMessageBox.warning(self, "Invalid Input", f"Error: {e}")
            return None
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred during saving: {e}")
            return None
        
    def show_amortization_table(self):
        """Displays the amortization schedule in a QTableWidget."""
        try:
            if self.amortization_data is None:
                raise ValueError("Please calculate the payment before showing the amortization table.")

            df = self.amortization_data['amortization_schedule'] 

            table_widget = QTableWidget(self)
            table_widget.setRowCount(df.shape[0])
            table_widget.setColumnCount(df.shape[1])
            table_widget.setHorizontalHeaderLabels(df.columns)

            for i in range(table_widget.columnCount()):
                table_widget.setColumnWidth(i, 120)

            for row in df.itertuples():
                for col, value in enumerate(row[1:]):
                    table_widget.setItem(row.Index, col, QTableWidgetItem(f"{value:,.2f}"))

            table_dialog = QDialog(self)
            table_layout = QVBoxLayout(table_dialog)
            table_layout.addWidget(table_widget)
            table_dialog.setWindowTitle("Amortization Table")
            table_dialog.setWindowModality(Qt.WindowModality.WindowModal)

            total_width = sum(table_widget.columnWidth(i) for i in range(table_widget.columnCount()))
            table_dialog.resize(total_width + 40, 600)
            table_dialog.exec_()

        except (ValueError, KeyError) as e:
            QMessageBox.warning(self, "Invalid Input", f"Error: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")

    def show_graph(self):
        """Displays a graph of the amortization schedule."""
        try:
            if self.amortization_data is None:
                raise ValueError("No data to graph. Please perform a calculation.") 

            self.create_graph(self.amortization_data['amortization_schedule']).show()  

        except (ValueError, KeyError) as e:
            QMessageBox.critical(self, "Graph Error", str(e))  
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")

    def create_graph(self, amortization_data):
        """Creates a Matplotlib graph of principal and interest payments."""
        plt.figure(figsize=(10, 6))
        plt.plot(amortization_data['Principal'], label='Principal', color='blue')
        plt.plot(amortization_data['Interest'], label='Interest', color='red')
        plt.ylabel('Amount') 
        plt.xlabel('Months')
        plt.title('Loan Payment Breakdown: Principal vs Interest')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        return plt 

    def save_dialog(self):
        """Opens a dialog to choose the file type and save the results."""
        df = self.save_results()
        if df is None:
            return

        save_type, ok = QInputDialog.getItem(self, "Save As", "Choose file type:", ["PDF", "CSV"], 0, False)

        if ok:
            if save_type == "PDF":
                self.save_pdf(df)
            elif save_type == "CSV":
                self.save_csv(df)

    def save_csv(self, df):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Amortization Table", "", "CSV Files (*.csv)")
        if filename:
            try:
                df = df.round(2)  # Round all numerical columns to two decimal places
                df.to_csv(filename, index=False, float_format='%.2f') #Format all float numbers to two decimal places

                QMessageBox.information(self, "Success", f"Amortization schedule saved to {filename}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving CSV: {e}")

    def save_pdf(self, df):
        """Saves the amortization schedule to a PDF file with dynamically adjusted column widths and formatted numbers."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Amortization Schedule", ln=1, align="C")

        col_widths = []
        line_height = pdf.font_size * 2.5

        # Calculate maximum column widths, formatting numerical values to two decimal places
        for col in df.columns:
            max_width = pdf.get_string_width(str(col))  # Use column names for width calculation
            for value in df[col]:
                formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value) #  Limit numbers to 2 decimal places
                max_width = max(max_width, pdf.get_string_width(formatted_value))
            col_widths.append(max_width + 6)

        # Write header row
        x_pos = 10  # Start x position
        for i, col in enumerate(df.columns):
            pdf.cell(col_widths[i], line_height, txt=col, border=1)
            x_pos += col_widths[i]
        pdf.ln(line_height)

        # Write data rows, formatting numerical values to two decimal places
        x_pos = 10
        for row in df.itertuples(index=False):
            for i, datum in enumerate(row):
                formatted_datum = f"{datum:.2f}" if isinstance(datum, (int, float)) else str(datum)  # Format numerical values to 2 decimal places if number.
                pdf.cell(col_widths[i], line_height, txt=formatted_datum, border=1)  # Use the formatted value
                x_pos += col_widths[i]
            pdf.ln(line_height)
            x_pos = 10

        pdf_filename, _ = QFileDialog.getSaveFileName(self, "Save Amortization Table as PDF", "", "PDF Files (*.pdf)")
        if pdf_filename:
            try:
                pdf.output(pdf_filename)
                QMessageBox.information(self, "Success", f"Amortization schedule saved to {pdf_filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving PDF: {e}")

app = QApplication(sys.argv)
window = LoanCalculator()
window.calculation_finished.connect(window.update_output_fields)  
sys.exit(app.exec_())