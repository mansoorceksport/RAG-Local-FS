# 🏟️ FC Barcelona HR RAG - Local Files, No Database

*A lightweight Retrieval-Augmented Generation system using Markdown files as knowledge base.*

Welcome to the **FC Barcelona HR RAG System** - a simple, self-contained Retrieval-Augmented Generation (RAG) project that loads Markdown-based HR/player records directly from the filesystem into memory.

No database.
No vector DB.
No embeddings.
Just pure **local markdown → dictionary → context injection → LLM**.

Perfect for small projects, demo apps, or experimenting with RAG fundamentals.

---

## 🚀 Features

### ✔ Local File-Based Knowledge Store

* HR/player records stored as `.md` files
* Loaded automatically into a Python `dict`
* Easy to modify, easy to version-control

### ✔ Context-Injection RAG

* User query analyzed for keyword matches
* Relevant markdown snippets injected into system prompt
* LLM answers with higher accuracy using only local data

### ✔ OpenAI API Integration

* Uses `gpt-4.1-nano` for fast + cheap responses
* System prompt built specifically around **FC Barcelona** employees

### ✔ Simple Gradio Chat UI

* Full chat interface
* Local browser launch
* Debug logs enabled

### ✔ Fully Offline Knowledge

* No vectors
* No external DB
* No third-party storage
* Everything lives inside `data/employees/*.md`

---

## 📁 Project Structure

```
/
├── data/
│   └── employees/
│       ├── <employee1>.md
│       ├── <employee2>.md
│       └── ...
│
├── synthetic_data_generator.py   (optional, if you generate fake players)
├── main.py                       (your main RAG chat app)
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

### 1️⃣ Load all `.md` files into memory

```python
knowledge = load_markdown_files()
```

Each employee record becomes a key-value entry:

```
{name: markdown_content}
```

### 2️⃣ Detect keywords in user query

```python
get_relevant_context(message)
```

If words from the question match employee names → relevant markdown is returned.

### 3️⃣ Inject context into system prompt

```python
system_message = SYSTEM_PREFIX + additional_context(message)
```

### 4️⃣ Chat model replies with improved accuracy

```python
openai.chat.completions.create(...)
```

### 5️⃣ All wrapped in a clean Gradio UI

```python
gr.ChatInterface(...).launch(inbrowser=True)
```

---

## ▶️ Running the Project

### **1. Install dependencies**

```bash
pip install -r requirements.txt
```

### **2. Add your OpenAI API key**

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

### **3. Put employee/player files into**

```
data/employees/*.md
```

### **4. Run the app**

```bash
python main.py
```

This opens the Gradio chat UI in your browser.

---

## ✍️ Example Query

> "What is the salary of Pedri?"
> "How did João Félix perform in 2022?"
> "Tell me about the injuries of Ansu Fati."

The system will automatically:
✔ extract keywords
✔ search local markdown files
✔ inject only relevant context
✔ respond like an FC Barcelona HR expert

---

## 🛠 Tech Stack

* **Python 3.10+**
* **OpenAI API**
* **Gradio**
* **dotenv**
* **Local markdown RAG** (no vector DB)

---

## 💡 Future Enhancements

If you want to expand the project, here are natural next steps:

* Add embeddings + semantic search
* Add synthetic player generator (already done!)
* Add evaluation for RAG accuracy
* Add API endpoint (FastAPI)
* Add frontend widget for websites
* Add player stats parser (goals/assists/etc.)

---

## ⚽ Final Words

This project is intentionally **simple**, **transparent**, and **educational** - but powerful enough to answer structured questions about FC Barcelona players using only local markdown files.

If the club ever needs a *personal AI sporting director*, you’re already halfway there. 😄
