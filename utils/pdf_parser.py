import pdfplumber
import re


def safe_search(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


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

        print("========== PAGE 1 ==========")
        print(main_text)
        print("============================")

        if not main_text:
            return data

        # Debug (remove later if needed)
        print(main_text)

        data["project_details"] = {
            "Project Name": safe_search(
                r'Project Name:\s*(.*?)\s*Account',
                main_text
            ),
            "Account Number": safe_search(
                r'Account\s*number\s*(\d+)',
                main_text
            ),
            "Name": safe_search(
                r'NAME:\s*(.*?)\s*IFSC',
                main_text
            ),
            "IFSC": safe_search(
                r'IFSC\s*CODE\s*([A-Z0-9]+)',
                main_text
            ),
            "Employee ID": safe_search(
                r'Emp\s*ID:\s*(\d+)',
                main_text
            ),
            "Email": safe_search(
                r'Email\s*-\s*ID\s*(.*?)\s*Site Name',
                main_text
            ),
            "Site Name": safe_search(
                r'Site Name:\s*(.*?)\s*Phone Number',
                main_text
            ),
            "Phone": safe_search(
                r'Phone Number\s*(\d+)',
                main_text
            ),
            "Statement No": safe_search(
                r'Statement No\.?\s*(\d+)',
                main_text
            )
        }

        # Totals

        adv = re.search(
            r'Advance Total\s*([\d,]+\.\d+)',
            main_text
        )

        exp = re.search(
            r'Expenses total\s*([\d,]+\.\d+)',
            main_text,
            re.IGNORECASE
        )

        bal = re.search(
            r'Balance on hand\s*(-?\d+)',
            main_text,
            re.IGNORECASE
        )

        data["project_details"]["Advance Total"] = (
            adv.group(1) if adv else ""
        )

        data["project_details"]["Expenses Total"] = (
            exp.group(1) if exp else ""
        )

        data["project_details"]["Balance On Hand"] = (
            bal.group(1) if bal else ""
        )

        # ======================
        # MAIN SHEET CATEGORIES
        # ======================

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

                if category.lower() in line.lower():

                    amounts = re.findall(
                        r'(\d+\.\d+)',
                        line
                    )

                    if amounts:

                        data["main_categories"][category] = float(
                            amounts[-1]
                        )

        # ======================
        # SUB SHEETS
        # ======================

        for page_num in range(1, len(pdf.pages)):

            page_text = pdf.pages[page_num].extract_text()

            if not page_text:
                continue

            print(f"\nPAGE {page_num+1}\n")
            print(page_text)

            if (
                "Stationary" in page_text
                or
                "Stationery" in page_text
            ):

                amounts = re.findall(
                    r'(\d+\.\d+)',
                    page_text
                )

                if amounts:

                    data["subsheet_categories"][
                        "Stationery Expenses"
                    ] = float(amounts[-1])
        # DEBUG
        data["debug_page1"] = main_text
        return data
