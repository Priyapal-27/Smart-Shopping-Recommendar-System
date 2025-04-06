import pandas as pd

# --------------------------
# STEP 1: Load and Clean Datasets
# --------------------------
customers = pd.read_csv("customer_data_collection.csv")
products = pd.read_csv("product_recommendation_data.csv")

# Remove 'Unnamed' columns
customers = customers.loc[:, ~customers.columns.str.contains('^Unnamed')]
products = products.loc[:, ~products.columns.str.contains('^Unnamed')]

# Show first few rows
print("Customers Data:\n", customers.head())
print("\nProducts Data:\n", products.head())

# --------------------------
# STEP 2: Clean and Normalize Data
# --------------------------
# Clean and format Purchase_History (remove brackets, quotes, spaces)
customers['Purchase_History'] = customers['Purchase_History'].astype(str)
customers['Purchase_History'] = customers['Purchase_History'].str.replace(r"[\[\]']", "", regex=True)
customers['Purchase_History'] = customers['Purchase_History'].str.lower().str.strip()

# Convert to list
customers['Purchase_History'] = customers['Purchase_History'].apply(lambda x: [item.strip() for item in x.split(',') if item.strip()])

# Normalize product subcategory for better matching
products['Subcategory'] = products['Subcategory'].astype(str).str.lower().str.strip()

# --------------------------
# STEP 3: Recommendation Function
# --------------------------
def recommend_products(purchase_history):
    recommendations = []
    for item in purchase_history:
        matches = products[products['Subcategory'].str.contains(item, na=False)]
        if not matches.empty:
            top_match = matches.sort_values(by='Probability_of_Recommendation', ascending=False).head(1)
            recommendations.append(top_match)
    if recommendations:
        return pd.concat(recommendations)
    else:
        return pd.DataFrame(columns=products.columns)

# --------------------------
# STEP 4: Show Recommendations for First 5 Customers
# --------------------------
for index, row in customers.head(5).iterrows():
    print(f"\nCustomer ID: {row['Customer_ID']}")
    print(f"Purchase History: {row['Purchase_History']}")
    recommended = recommend_products(row['Purchase_History'])
    if not recommended.empty:
        print("Recommended Products:")
        print(recommended[['Product_ID', 'Category', 'Subcategory', 'Probability_of_Recommendation']])
    else:
        print("No suitable product found based on purchase history.")

print("\n--- Final Top 3 Recommendations ---\n")

# Step 5: Final Top 3 Recommendations
final_recommendations = []

for index, row in customers.head(10).iterrows():
    customer_id = row['Customer_ID']
    purchase_history = row['Purchase_History']
    matched_products = products[products['Subcategory'].isin([item.lower() for item in purchase_history])]
    sorted_recommendations = matched_products.sort_values(by='Probability_of_Recommendation', ascending=False)
    top_3 = sorted_recommendations.head(3)
    for _, product in top_3.iterrows():
        final_recommendations.append({
            "Customer_ID": customer_id,
            "Product_ID": product["Product_ID"],
            "Category": product["Category"],
            "Subcategory": product["Subcategory"],
            "Probability": product["Probability_of_Recommendation"]
        })

# Create DataFrame and print
final_df = pd.DataFrame(final_recommendations)
print(final_df.head(10))

# Step 6: Segment-based Filtering
print("\n--- Final Personalized Recommendations Based on Segment ---\n")

for index, row in customers.head(10).iterrows():

    customer_id = row['Customer_ID']
    purchase_history = row['Purchase_History']
    segment = row['Customer_Segment']

    recommended_products = products[products['Subcategory'].isin([item.lower() for item in purchase_history])]
    recommended_products = recommended_products[recommended_products['Probability_of_Recommendation'] > 0.5]

    # Segment-specific thresholds
    if segment == 'New Visitor':
        threshold = 0.7
    elif segment == 'Occasional Shopper':
        threshold = 0.6
    else:
        threshold = 0.5

    recommended_products = recommended_products[recommended_products['Probability_of_Recommendation'] >= threshold]

    print(f"Customer ID: {customer_id} | Segment: {segment}")
    print("Personalized Recommendations:")
    print(recommended_products[['Product_ID', 'Category', 'Subcategory', 'Probability_of_Recommendation']])
    print("-" * 50)

# Step 7: Save to CSV
final_df.to_csv("top_3_recommendations.csv", index=False)
print("\n✅ Final Top 3 recommendations saved to 'top_3_recommendations.csv'")

# Optional: Save to Excel with formatting
excel_path = "top_3_recommendations.xlsx"
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    final_df.to_excel(writer, sheet_name='Recommendations', index=False)

print(f"📄 Excel file also saved to: {excel_path}")

import matplotlib.pyplot as plt

# Count how many times each subcategory was recommended
subcategory_counts = final_df['Subcategory'].value_counts()

# Plotting
plt.figure(figsize=(10, 6))
subcategory_counts.plot(kind='bar', color='skyblue')
plt.title('Top Recommended Subcategories')
plt.xlabel('Subcategory')
plt.ylabel('Number of Recommendations')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save chart
plt.savefig("recommendation_chart.png")
print("\n📊 Bar chart saved as 'recommendation_chart.png'")

# ----------------------------
# STEP 8: Command-Line Input for Dynamic Recommendations
# ----------------------------

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()
cli_results = []  # To store results
invalid_tries = 0  # Counter for wrong inputs

while True:
    user_input = Prompt.ask("\n🎯 Enter a Customer ID for recommendations (or type 'exit' to quit)").strip()

    if user_input.lower() == 'exit':
        console.print("✅ Exiting Smart Recommendation CLI.", style="bold green")
        break

    if user_input in customers['Customer_ID'].values:
        invalid_tries = 0  # Reset counter

        row = customers[customers['Customer_ID'] == user_input].iloc[0]
        purchase_history = [item.lower() for item in row['Purchase_History']]
        segment = row['Customer_Segment']

        matched = products[products['Subcategory'].str.lower().isin(purchase_history)]

        # Apply segment-based threshold
        threshold = 0.7 if segment == 'New Visitor' else 0.6 if segment == 'Occasional Shopper' else 0.5
        filtered = matched[matched['Probability_of_Recommendation'] >= threshold]
        top3 = filtered.sort_values(by='Probability_of_Recommendation', ascending=False).head(3)

        if not top3.empty:
            table = Table(title=f"Top 3 Recommendations for {user_input} ({segment})")

            table.add_column("Product ID", style="cyan")
            table.add_column("Category", style="magenta")
            table.add_column("Subcategory", style="green")
            table.add_column("Probability", style="yellow")

            for _, row in top3.iterrows():
                table.add_row(str(row['Product_ID']), row['Category'], row['Subcategory'], str(row['Probability_of_Recommendation']))
                cli_results.append({
                    "Customer_ID": user_input,
                    "Product_ID": row['Product_ID'],
                    "Category": row['Category'],
                    "Subcategory": row['Subcategory'],
                    "Probability": row['Probability_of_Recommendation']
                })

            console.print(table)
        else:
            console.print("⚠️ No recommendations found for this user segment and history.", style="bold red")

    else:
        invalid_tries += 1
        console.print("❌ Customer ID not found. Try again.", style="bold red")
        if invalid_tries >= 3:
            console.print("🔒 Too many invalid attempts. Exiting...", style="bold yellow")
            break

# Save CLI recommendations to CSV if any
if cli_results:
    pd.DataFrame(cli_results).to_csv("cli_recommendations.csv", index=False)
    console.print("\n✅ All CLI recommendations saved to 'cli_recommendations.csv'", style="bold green")
