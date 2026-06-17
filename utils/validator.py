def validate(main_categories, bill_totals):

    output = []

    for category in main_categories:

        main_amt = main_categories[category]

        bill_amt = bill_totals.get(category, 0)

        status = "PASS"

        if abs(main_amt - bill_amt) > 1:

            status = "FAIL"

        output.append({
            "Category": category,
            "Main Sheet": main_amt,
            "Bills Total": bill_amt,
            "Status": status
        })

    return output
