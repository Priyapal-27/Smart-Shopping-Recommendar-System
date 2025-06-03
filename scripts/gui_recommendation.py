import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Load the CSV file
df = pd.read_csv("cli_recommendation.csv")

# Get unique categories for dropdown
categories = ['All'] + sorted(df['Category'].dropna().unique().tolist())

# Filtered result will be stored globally to reuse during export
filtered_data = pd.DataFrame()

# Function to get filtered recommendations
def show_recommendations():
    global filtered_data
    customer_id = entry.get().strip()
    selected_category = category_var.get()

    if customer_id not in df['Customer_ID'].astype(str).values:
        messagebox.showerror("Error", f"Customer ID {customer_id} not found.")
        return

    customer_data = df[df['Customer_ID'].astype(str) == customer_id]

    # Apply category filter
    if selected_category != 'All':
        customer_data = customer_data[customer_data['Category'] == selected_category]

    if customer_data.empty:
        messagebox.showinfo("No Recommendations", f"No recommendations found for category '{selected_category}'.")
        return

    filtered_data = customer_data  # Store for export

    recs = f"Top {len(customer_data)} Recommendations for Customer {customer_id}:\n\n"
    for i, (_, row) in enumerate(customer_data.iterrows(), start=1):
        recs += f"{i}. Product ID: {row['Product_ID']}, Category: {row['Category']}, Subcategory: {row['Subcategory']}, Probability: {row['Probability']}\n"

    messagebox.showinfo("Recommendations", recs)

# Function to export to Excel
def export_to_excel():
    global filtered_data
    customer_id = entry.get().strip()
    if filtered_data.empty:
        messagebox.showerror("Error", "Please get recommendations first before exporting.")
        return
    try:
        file_name = f"filtered_recommendations_{customer_id}.xlsx"
        filtered_data.to_excel(file_name, index=False)
        messagebox.showinfo("Success", f"Exported to Excel as '{file_name}'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {e}")

# GUI setup
root = tk.Tk()
root.title("🛍️ Smart Shopping Recommender")
root.geometry("500x380")
root.configure(bg="#f0f4f7")

# Heading
tk.Label(root, text="Smart Shopping Recommender", font=("Helvetica", 16, "bold"), fg="#2a3f5f", bg="#f0f4f7").pack(pady=10)

# Customer ID input
tk.Label(root, text="Enter Customer ID:", font=("Arial", 12), bg="#f0f4f7").pack()
entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

# Dropdown for category
tk.Label(root, text="Filter by Category:", font=("Arial", 12), bg="#f0f4f7").pack()
category_var = tk.StringVar(value="All")
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.config(font=("Arial", 11), width=20)
category_menu.pack(pady=5)

# Buttons
tk.Button(root, text="Get Recommendations", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=show_recommendations).pack(pady=10)
tk.Button(root, text="Export to Excel", font=("Arial", 12, "bold"), bg="#2196f3", fg="white", command=export_to_excel).pack(pady=5)

# Run the app
root.mainloop()
