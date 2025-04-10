# Automatically Generating Programming Exercises with Open-Source LLMs: Integrating Lecture Slides and Learning Objectives

## ⚙️ Setup

### 1. Required Software

- **Python & pip:**
    Make sure that Python (>= 3.8) and pip are installed on your system. You can verify their installation by running:

    ```bash
  python --version
  pip --version
  ```

- **Ollama:**
    We use Ollama to work locally with Large Language Models. Download and install Ollama from the official website <https://ollama.com/download>. After installation, verify that Ollama is installed by running:

    ```bash
  ollama --version
  ```

- **Pull Required Models:**
    To use models locally, they must first be downloaded via the Ollama API. In this work, we used the **Qwen2.5 Coder** and **Gemma3** models. Open a terminal and execute:

    ```bash
    ollama pull qwen2.5-coder:7b
    ollama pull gemma3:4b
    ```

### 2. Create and Activate a Virtual Environment

After cloning this project, create a virtual environment by executing the following in the project root:

```bash
python -m venv venv
source venv/bin/activate     # for macOS/Linux
venv\Scripts\activate        # for Windows
```

### 4. Install dependencies

All dependencies are listed in the requirements.txt file. Install them via pip:

```bash
pip install -r requirements.txt
```

### 3. Start the Application

From the project root directory, run:

```bash
python -m streamlit run app/app.py
```
