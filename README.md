# Automatically Generating Programming Exercises with Open-Source LLMs: Integrating Lecture Slides and Learning Objectives

## 1. Required Software

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
    To run the models locally, they must first be downloaded via the Ollama CLI. We used the Qwen2.5 Coder model (7 billion parameters) for exercise generation and the Gemma 3 model (4 billion parameters) for summarizing lecture slides.
    Open a terminal and execute the following commands:

    ```bash
    ollama pull qwen2.5-coder:7b
    ollama pull gemma3:4b
    ```

   The gemma3:4b model has a size of approximately 3.3 GB, and qwen2.5-coder:7b is around 4.7 GB.
   Depending on your internet connection, the download may take several minutes.

## 2. Create and Activate a Virtual Environment

After cloning the repository, create and activate a virtual environment in the project root:

```bash
python -m venv venv
source venv/bin/activate     # for macOS/Linux
venv\Scripts\activate        # for Windows
```

## 3. Install dependencies

Install all required packages listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```

## 4. Update path in config file

For the automated evaluation pipeline, generated Haskell code is compiled using the runghc executable.
To enable this feature, you need to set the correct path in config.py.

You can check the location of runghc on your system by running:

```bash
which runghc
```

Replace the value of DEFAULT_RUNGHC_PATH in config.py with the your path.

## 5. Start the Application

From the project root, run the Streamlit app:

```bash
python -m streamlit run app/app.py
```
