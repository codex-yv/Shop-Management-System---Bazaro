import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

def plot_monthly_income_chart(root, months, monthly_totals):
    """Plots total income per month for the last 12 months."""
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)

    bars = ax.bar(months, monthly_totals, color='skyblue', picker=True)

    ax.set_title("Monthly Income (Last 12 Months)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Income ($)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_pick(event):
        bar = event.artist
        for i, rect in enumerate(bars):
            if rect == bar:
                month = months[i]
                total = monthly_totals[i]
                messagebox.showinfo("Monthly Income", f"Month: {month}\nTotal Income: ${total:.2f}")
                break

    fig.canvas.mpl_connect('pick_event', on_pick)

# --- Main GUI App ---
if __name__ == "__main__":
    # Example data: 12 months and corresponding incomes
    example_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    example_incomes = [2200, 2500, 2100, 2400, 2700, 3000, 2800, 2600, 3100, 2900, 3200, 3300]

    root = tk.Tk()
    root.title("Monthly Income Chart (Last 12 Months)")
    root.geometry("1000x700")

    plot_monthly_income_chart(root, example_months, example_incomes)

    root.mainloop()


# from datetime import datetime

# # Get current date and time
# now = datetime.now()

# # Get month name
# month_name = now.strftime("%B")
# year = now.year

# print(f"Current Month: {month_name}")
# print(f"Current Year: {year}")

