🛡️ AI Risk Manager

An AI-powered transaction risk detection system that analyzes transaction behavior, predicts fraud probability, calculates a risk score, and provides explainable decisions.

🚀 Features

- 🤖 Machine Learning-based fraud detection
- 📊 Transaction risk scoring (0–100)
- 🟢 APPROVE low-risk transactions
- 🟡 REVIEW suspicious transactions
- 🔴 BLOCK high-risk transactions
- 🔍 Explainable risk factors
- ⚡ Transaction velocity analysis
- 🌍 International transaction detection
- 📱 New device risk detection
- 📝 SQLite audit logging
- 🌐 FastAPI REST API
- 📈 Streamlit dashboard

🏗️ Architecture

Transaction Input
       │
       ▼
Feature Engineering
       │
       ▼
Machine Learning Model
       │
       ├───────────────┐
       ▼               ▼
ML Risk Score      Rule-Based Signals
       │               │
       └───────┬───────┘
               ▼
        Risk Decision Engine
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    APPROVE  REVIEW   BLOCK
               │
               ▼
        Audit Database
               │
               ▼
         Analytics Dashboard

📁 Project Structure

ai-risk-manager/
│
├── app.py
├── generate_data.py
├── train_model.py
├── requirements.txt
│
├── data/
│   └── transactions.csv
│
├── models/
│   └── fraud_model.pkl
│
├── utils/
│   ├── risk_engine.py
│   ├── explainer.py
│   └── audit_logger.py
│
└── api/
    └── main.py

🧠 Risk Factors

The system analyzes multiple transaction signals:

- Transaction amount
- Transaction hour
- Transaction frequency
- New device detection
- International transaction status
- Failed authentication attempts

⚙️ Installation

Clone the repository:

git clone https://github.com/Adeshsoni/ai-risk-manager.git
cd ai-risk-manager

Install dependencies:

pip install -r requirements.txt

▶️ Run the Project

Generate synthetic transaction data:

python generate_data.py

Train the machine learning model:

python train_model.py

Run the Streamlit dashboard:

streamlit run app.py

Run the FastAPI server:

uvicorn api.main:app --reload

📊 Decision Logic

Risk Score| Decision
0–29| APPROVE
30–69| REVIEW
70–100| BLOCK

🔮 Future Improvements

- Real-time streaming risk analysis
- Model drift detection
- SHAP-based explainability
- User behavior profiling
- Graph-based fraud detection
- Docker deployment
- Cloud deployment

👨‍💻 Author

Adesh Soni

Built as an AI/ML project focused on intelligent transaction risk management and explainable fraud detection.
