def validate(main_categories, subsheet_categories):

    results = []

    all_categories = set(main_categories.keys())

    for category in all_categories:

        main_amt = main_categories.get(category, 0)

        sub_amt = subsheet_categories.get(category, 0)

        status = "PASS"

        if abs(main_amt - sub_amt) > 1:

            status = "FAIL"

        results.append({
            "Category": category,
            "Main Sheet": main_amt,
            "Sub Sheet": sub_amt,
            "Status": status
        })

    return results
