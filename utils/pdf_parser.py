import pdfplumber
import re


def extract_pdf_data(pdf_path):

    data = {
        "project_details": {},
        "main_categories": {},
        "subsheet_categories": {}
    }

    with pdfplumber.open(pdf_path) as pdf:

        # ======================
        # PAGE 1 = MAIN SHEET
        # ======================

        main_text = pdf.pages[0].extract_text()

        data["project_details"] = {
            "Project Name": re.search(r'Project Name:\s*(.*?)\s*Account number', main_text).group(1),
            "Account Number": re.search(r'Account number\s*(\d+)', main_text).group(1),
            "Name": re.search(r'NAME:\s*(.*?)\s*IFSC CODE', main_text).group(1),
            "IFSC": re.search(r'IFSC CODE\s*([A-Z0-9]+)', main_text).group(1),
            "Employee ID": re.search(r'Emp ID:\s*(\d+)', main_text).group(1),
            "Email": re.search(r'Email\s*-\s*ID\s*(.*?)\s*Site Name', main_text).group(1),
            "Site Name": re.search(r'Site Name:\s*(.*?)\s*Phone Number', main_text).group(1),
            "Phone": re.search(r'Phone Number\s*(\d+)', main_text).group(1),
            "Statement No": re.search(r'Statement No\.\s*(\d+)', main_text).group(1)
        }

        category_patterns = [
            "Food",
            "Stationery Expenses",
            "Printing Charges",
            "Subscription Charges",
            "Cleaning Charges",
            "Courier Charges",
            "Repairs & Maintenance",
            "Other Expense"
        ]

        for line in main_text.split("\n"):

            for category in category_patterns:

                if category in line:

                    amounts = re.findall(r'(\d+\.\d+)', line)

                    if amounts:

                        data["main_categories"][category] = float(amounts[-1])

        adv = re.search(r'Advance Total\s*([\d,]+\.\d+)', main_text)
        exp = re.search(r'Expenses total\s*([\d,]+\.\d+)', main_text)
        bal = re.search(r'Balance on hand\s*(-?\d+)', main_text)

        data["project_details"]["Advance Total"] = adv.group(1) if adv else ""
        data["project_details"]["Expenses Total"] = exp.group(1) if exp else ""
        data["project_details"]["Balance On Hand"] = bal.group(1) if bal else ""

        # ======================
        # SUB SHEETS
        # ======================

        for page_num in range(1, len(pdf.pages)):

            page_text = pdf.pages[page_num].extract_text()

            if not page_text:
                continue

            if "Stationary" in page_text or "Stationery" in page_text:

                amounts = re.findall(r'(\d+\.\d+)', page_text)

                if amounts:

                    data["subsheet_categories"]["Stationery Expenses"] = float(amounts[-1])

    return data
