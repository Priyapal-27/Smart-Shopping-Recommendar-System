# 🛍️ Smart Shopping: Data and AI for Personalized E-Commerce

### 🚀 Hack the Future: A Gen AI Sprint Powered by Data

Smart Shopping is an intelligent recommendation system designed to revolutionize e-commerce using the power of **Generative AI** and **Data Analytics**. It delivers hyper-personalized product suggestions based on customer segments, seasonal trends, and behavioral patterns.

---

## 📌 Key Features

- 🎯 **Segment-Based Filtering**: Personalized recommendations for students, professionals, and parents.
- ❄️ **Seasonal Offers**: Smart suggestions tailored to festivals, weather, or occasions (e.g., Diwali, Winter).
- 🧠 **Gen AI Chatbot**: Understands natural language queries like "I want a summer bag under ₹500".
- 📊 **Data-Driven Insights**: Highlights trending products, top picks, and personalized bundles.
- 🖼️ **Visual Recommendations** _(Optional)_: Gen AI-generated outfit/product mockups.

---

## 💡 How It Works

1. **Customer Data Input**: Via CLI, GUI, or chatbot.
2. **Recommendation Engine**:
   - Matches customer ID with historical and simulated purchase data.
   - Filters by segment and season.
3. **Smart Suggestions**:
   - Top 3 high-probability product recommendations.
   - Displayed in terminal, GUI (Tkinter), and optionally exported to CSV/Excel.

---

## 🧰 Tech Stack

| Layer         | Tech Used                                        |
| ------------- | ------------------------------------------------ |
| Frontend      | Tkinter GUI / CLI                                |
| Backend       | Python, Pandas                                   |
| Data          | CSV (Simulated data for customers & products)    |
| AI Features   | OpenAI API (optional), Prompt design             |
| Visualization | Excel / Matplotlib / Future: Streamlit Dashboard |

---

## 🧪 How to Run

### ▶️ CLI Version

```bash
python cli_recommendation.py

🖥️ GUI Version (Tkinter)
python gui_recommendation.py

🧬 Data Structure (Sample)
cli_recommendation.csv

Customer_ID,Product_ID,Category,Subcategory,Probability
C1007,P2360,Home Decor,wall art,0.99
...

📦 Future Enhancements
🧠 Gen AI chatbot integration (text-to-recommendation)

🌐 Web UI with React and Express backend

🧺 Smart cart suggestions with bundling logic

🕵️‍♂️ Behavior tracking with real-time analytics

🎨 Gen AI product image generation
```
