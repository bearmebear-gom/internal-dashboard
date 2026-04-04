#  K-Beauty Persona Dashboard (Apple-Style)

### 📊 Overview
This is a high-fidelity, professional analytics dashboard for **K-Beauty Persona Market Analysis**, designed strictly based on **Apple's Human Interface Guidelines (HIG)**. It features a "Liquid Glass" minimalist UI, concentric design, and a clear visual hierarchy.

### 🚀 Quick Start
To run this project locally using `uv`:
```bash
# Install dependencies
uv sync

# Run the dashboard
uv run streamlit run src/dashboard.py
```

### 🌍 Deployment
This project is configured for easy deployment via **Streamlit Cloud** or similar GitHub-integrated platforms:
1.  Push the project folder to a GitHub repository.
2.  Connect the repository to Streamlit Cloud.
3.  Set the main file path to: `src/dashboard.py`.

### 🗂️ Project Structure
-   `src/dashboard.py`: Core application code (Streamlit + Plotly).
-   `requirements.txt`: Python dependencies.
-   `pyproject.toml`: Modern Python packaging config.
-   `data/`: Raw and processed data samples.

### ✨ Key Features
-   **Apple HIG Standard**: Subtle semantic palette, SF Pro typography, and "Quiet Luxury" aesthetic.
-   **Executive Summary**: High-level progress rings for Growth, Retention, Conversion, and Loyalty.
-   **National KPI Analysis**: Granular performance comparisons across different countries.
-   **AI Lab Diagnostics**: Predictive patterns and actionable recommendation plans.
