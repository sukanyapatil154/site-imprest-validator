import pdfplumber
import re

def extract_main_sheet_data(pdf_path):

    data = {}

    with pdfplumber.open(pdf_path) as pdf:

        text = pdf.pages[0].extract_text()

        data["project_name"] = re.search(
            r'Project Name:\s*(.*)',
            text
        ).group(1)

        data["site_name"] = re.search(
            r'Site Name:\s*(.*)',
            text
        ).group(1)

        data["emp_id"] = re.search(
            r'Emp ID:\s*(\d+)',
            text
        ).group(1)

        categories = {}

        for line in text.split("\n"):

            amount_match = re.findall(r'(\d+\.\d+)', line)

            if amount_match:

                amount = float(amount_match[-1])

                if "Food" in line:
                    categories["Food"] = amount

                elif "Stationery" in line:
                    categories["Stationery"] = amount

                elif "Printing" in line:
                    categories["Printing"] = amount

                elif "Courier" in line:
                    categories["Courier"] = amount

                elif "Repairs" in line:
                    categories["Repairs"] = amount

                elif "Other Expense" in line:
                    categories["Other Expense"] = amount

        data["categories"] = categories

    return data
