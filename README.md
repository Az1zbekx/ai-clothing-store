<div align="center">
  <h1>🛍️ AI Clothing Store</h1>
  <p><strong>A fully intelligent, AI-powered e-commerce platform built with FastAPI, PostgreSQL (pgvector), and Local LLMs.</strong></p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
</div>

<br>

## 🌟 Overview

**AI Clothing Store** is a modern, next-generation e-commerce application that leverages Artificial Intelligence and Vector Search to provide an unparalleled shopping experience. Instead of traditional browsing, customers can simply chat with our intelligent AI Assistant (powered by local LLMs via Ollama) to find exactly what they are looking for in natural language.

The application also features a highly advanced **Boss Dashboard** with its own AI Business Analyst to instantly calculate revenue, track low-stock items, and provide strategic business recommendations on the fly.

## 🚀 Key Features

*   **💬 AI Customer Assistant:** Chat-based shopping experience. Customers can talk to the AI in natural language to search for products, sizes, colors, and seasons.
*   **🔍 Hybrid Search Engine:** Combines structured keyword filtering with powerful **Vector Similarity Search** (`pgvector` & `nomic-embed-text`) to find products even if the user types in slightly different words.
*   **📊 Boss Dashboard & Analytics:** A dedicated panel for store owners to monitor live sales, revenue, and product stock.
*   **👨‍💼 Boss AI Analyst:** An intelligent assistant for the owner that analyzes store data and provides immediate text-based reports (e.g., *"What is the best selling product?", "Which items are out of stock?"*).
*   **🧠 Local AI Processing:** Runs entirely using local AI models (via Ollama + Qwen) for maximum privacy and cost-efficiency.

## 🛠️ Technology Stack

### Backend
*   **Framework:** FastAPI (Python)
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Vector Database Extension:** `pgvector`
*   **AI Engine:** Ollama (`qwen2.5:1.5b` for chat generation, `nomic-embed-text` for vector embeddings)

### Frontend
*   Vanilla HTML5, CSS3, JavaScript (No heavy frameworks, blazing fast)
*   Glassmorphism UI design
*   Responsive and mobile-friendly

## ⚙️ Installation & Setup

### Prerequisites
1.  **Python 3.9+** installed.
2.  **PostgreSQL** installed and running.
3.  **Ollama** installed on your machine (Download at [ollama.com](https://ollama.com/)).

### 1. Database Setup
Create a PostgreSQL database and install the `pgvector` extension:
```sql
CREATE DATABASE ai_clothing_store;
\c ai_clothing_store
CREATE EXTENSION vector;
```

### 2. Ollama Setup
Pull the required local AI models:
```bash
ollama run qwen2.5:1.5b
ollama pull nomic-embed-text
```

### 3. Backend Setup
Clone the repository and install Python dependencies:
```bash
git clone https://github.com/Az1zbekx/ai-clothing-store.git
cd ai_clothing_store/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

Set up your `.env` file in the `backend/` directory:
```ini
DATABASE_URL=postgresql://username:password@localhost:5432/ai_clothing_store
SECRET_KEY=your_super_secret_key
```

### 4. Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

To view the frontend, simply open `frontend/customer.html` or `frontend/boss.html` in your favorite web browser!

## 🤖 Smart Chat System

The AI Assistant uses a **Hybrid Fallback Logic** to ensure 100% correct Uzbek language outputs:
1.  **Keyword Matching:** Detects intents (like "salom", "shim", "S o'lcham").
2.  **Vector Fallback:** Uses `pgvector` to find semantic similarities if keywords fail.
3.  **Smart Templating:** Instead of risking AI hallucinations, it dynamically slots the retrieved DB results into perfectly structured natural language templates.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).