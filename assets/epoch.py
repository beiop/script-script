def ask_for_offset():
    import tkinter as tk
    from datetime import datetime, timedelta
    offset_seconds = 0
    def calculate_offset_seconds():
        try:
            # Get values from offset fields, default to 0 if empty
            years = int(entry_years.get() or 0)
            months = int(entry_months.get() or 0)
            days = int(entry_days.get() or 0)
            hours = int(entry_hours.get() or 0)
            minutes = int(entry_minutes.get() or 0)
            seconds = int(entry_seconds.get() or 0)

            # Use a base datetime
            base = datetime(1970, 1, 1)

            # Approximate months as 30 days and years as 365 days
            total_offset = timedelta(
                days=(years * 365 + months * 30 + days),
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )

            # Get total seconds of offset
            offset_seconds = int(total_offset.total_seconds())

            label_offset_result.config(text=f"Offset in Seconds: {offset_seconds}")
            tk.self.kill()#close the window after calculation
        except ValueError:
            label_offset_result.config(text="Error: Enter valid integers.")

    # GUI setup
    rootOffset = tk.Tk()
    rootOffset.title("Epoch Offset Calculator")

    # Offset input labels and entries
    tk.Label(rootOffset, text="Years:").grid(row=0, column=0)
    entry_years = tk.Entry(rootOffset, width=5)
    entry_years.grid(row=0, column=1)

    tk.Label(rootOffset, text="Months:").grid(row=1, column=0)
    entry_months = tk.Entry(rootOffset, width=5)
    entry_months.grid(row=1, column=1)

    tk.Label(rootOffset, text="Days:").grid(row=2, column=0)
    entry_days = tk.Entry(rootOffset, width=5)
    entry_days.grid(row=2, column=1)

    tk.Label(rootOffset, text="Hours:").grid(row=3, column=0)
    entry_hours = tk.Entry(rootOffset, width=5)
    entry_hours.grid(row=3, column=1)

    tk.Label(rootOffset, text="Minutes:").grid(row=4, column=0)
    entry_minutes = tk.Entry(rootOffset, width=5)
    entry_minutes.grid(row=4, column=1)

    tk.Label(rootOffset, text="Seconds:").grid(row=5, column=0)
    entry_seconds = tk.Entry(rootOffset, width=5)
    entry_seconds.grid(row=5, column=1)

    tk.Button(rootOffset, text="Calculate Offset (in seconds)", command=calculate_offset_seconds).grid(row=6, column=0, columnspan=2, pady=10)

    label_offset_result = tk.Label(rootOffset, text="")
    label_offset_result.grid(row=7, column=0, columnspan=2)

    rootOffset.mainloop()

    return offset_seconds