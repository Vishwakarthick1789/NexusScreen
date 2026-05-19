# 🚀 NexusScreen: AI-Powered Resume Intelligence System

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gradio](https://img.shields.io/badge/UI-Gradio-ff69b4.svg)](https://gradio.app/)
[![FAISS](https://img.shields.io/badge/Vector-FAISS-lightgrey.svg)](https://github.com/facebookresearch/faiss)

**NexusScreen** is a high-performance, enterprise-grade AI system designed to intelligently screen, rank, and visualize candidate resumes against a target job description. It hybridizes classic Data Structures (Tries, Heaps) with cutting-edge AI (Semantic Embeddings, LLMs) to provide an incredibly fast and resource-efficient recruitment tool.

---

## ✨ Key Features

1. **🚀 Trie-Based Data Layer ($O(L)$ Extraction):**
   Utilizes a highly optimized `SkillTrie` to perform instantaneous keyword and "Hard Skill" extraction across massive PDF files before touching any AI models.
2. **🧠 Semantic AI Engine:**
   Leverages `sentence-transformers` and Facebook's `FAISS` library to convert extracted resume data into dense vectors, enabling lightning-fast mathematical similarity searches against Job Descriptions.
3. **🤖 LLM Intelligence Integration:**
   Seamlessly integrates with OpenAI (GPT-4o) to evaluate semantically relevant chunks and produce structured JSON output containing a `Technical_Score`, `Soft_Skills_Analysis`, and `Red_Flags`.
4. **🛡️ Memory-Safe Efficiency (The Heap):**
   Uses a custom Min-Heap data structure to dynamically track the Top $K$ candidates across batches of hundreds of resumes, strictly bounding RAM usage to $O(K)$.
5. **📊 Interactive Candidate Cluster Map:**
   A futuristic Gradio UI featuring an interactive 2D Principal Component Analysis (PCA) plot powered by Plotly, allowing recruiters to visually map the semantic landscape of their candidate pool.

---

## 🛠️ Technology Stack

- **Backend / Core:** Python, `asyncio`
- **Machine Learning & Vectors:** `sentence-transformers`, `faiss-cpu`, `scikit-learn`, `numpy`
- **Data Parsing:** `PyMuPDF` (`fitz`) for robust PDF text extraction
- **Interface & Visualization:** `gradio`, `pandas`, `plotly`
- **LLM Provider:** `openai` (Async API)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed on your Windows machine.

### Installation & Setup

We have provided a fully automated setup script for Windows environments.

1. **Clone or Download the Repository**
2. **Run the Initialization Script:**
   Simply double-click the `start.bat` file, or run it via terminal:
   ```cmd
   start.bat
   ```
   *This script will automatically create a virtual environment, install all dependencies from `requirements.txt`, and launch the application locally.*

### Optional: Unlocking Full AI Capabilities

By default, NexusScreen will use a mock logic system to ensure it runs out-of-the-box without requiring paid API keys. To enable true LLM rationale generation:

1. Obtain an API key from OpenAI.
2. Set the environment variable before launching:
   ```cmd
   set OPENAI_API_KEY=sk-your-openai-api-key-here
   python app.py
   ```

---

## 🧪 Testing with Mock Data

If you don't have a folder of resumes handy, you can generate an instant test suite! We have included a mock data generator.

1. Ensure your virtual environment is activated.
2. Run the mock script:
   ```cmd
   python generate_mocks.py
   ```
3. A `sample_resumes` directory will be created containing 6 diverse candidate PDFs (Frontend, Backend, Data Science, DevOps, etc.) that you can drag and drop into the NexusScreen UI.

---

## 🤝 Contributing

We welcome contributions to make NexusScreen even better! If you have suggestions for improvements, new features, or bug fixes:

1. **Fork** the project.
2. **Create your Feature Branch:** `git checkout -b feature/AmazingFeature`
3. **Commit your Changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the Branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request.**

Please ensure your code adheres to standard Python styling (PEP 8) and includes appropriate exception handling.

---

## 📞 Support & Contact

If you encounter any issues, need setup assistance, or want to discuss enterprise contributions, please reach out!

- **Developer:** Vishwakarthick
- **GitHub:** [@vishwakarthick1789](https://github.com/vishwakarthick1789)
- **Issues:** Please open a ticket in the GitHub Issues tab for bug tracking.

---
*Architected for speed, built for intelligence.*
