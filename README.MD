# 📊 BAC Analyzer

**BAC Analyzer** is a Python project designed to parse, store, and analyze data from the Romanian *Bacalaureat* exam results. The tool collects detailed student performance data across the last **three sessions** (years) of the exam and provides visual analytics for trends, distributions, and school-level performance insights.

> A project to showcase **data parsing**, **database design**, and **data analysis/visualization** skills.

---

## ⚙️ Features

- Parses and cleans *Bacalaureat* exam result data from official sources.
- Stores structured data in a **SQLite** database.
- Supports data from the **last 3 years** of exam sessions.
- `main.py` provides interactive options to generate visual plots and statistics.
- Current visualizations:
    -Student performance by high school within a selected county (liceu-level breakdown by judet)

    - Distribution of average grades (medie) across all counties

    - Categorical outcome analysis, showing counts of exam results (e.g., REUȘIT, RESPINS, NEPREZENTAT, ELIMINAT DIN EXAMEN)
- Extensible design — more plots & analyses planned.

---

## Technologies Used

| Purpose                | Technology |
|------------------------|------------|
| Data Parsing           | `BeautifulSoup`, `requests` |
| Data Storage           | `SQLite3` |
| Data Manipulation      | `pandas` |
| Data Visualization     | `matplotlib`, `seaborn` |

---

## ⚠️ In Development

This project is under active development. Upcoming features:

- [ ] More graphs for visualizing data
- [ ] Exportable reports (PDF/CSV)
- [ ] Interactive dashboards 
- [ ] More...

---

## ❓ How to Run

```bash
# # Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install . # Use '-e .' if you want to develop further

# Run the main CLI analysis tool and see help
bac-analyzer -h
```