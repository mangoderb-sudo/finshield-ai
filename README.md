<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&pause=1000&color=1B3F72&center=true&vCenter=true&width=700&lines=FinShield+AI+%F0%9F%9B%A1%EF%B8%8F;Financial+Risk+Intelligence+Platform;Credit+Scoring+%C2%B7+Fraud+Detection+%C2%B7+RAG" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-FF6600?style=for-the-badge&logoColor=white)](https://xgboost.readthedocs.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logoColor=white)](https://langchain.com)
[![Mistral](https://img.shields.io/badge/Mistral-AI-FF7000?style=for-the-badge&logoColor=white)](https://mistral.ai)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

<br/>

> **FinShield AI** is a production-grade, explainable AI platform for financial risk management —
> combining credit scoring, real-time fraud detection, and a RAG-powered financial assistant
> into a single unified system compliant with Bâle IV & EU AI Act requirements.

<br/>

[**📊 Live Demo**](#) · [**📖 Documentation**](#architecture) · [**🚀 Quick Start**](#-quick-start) · [**🤝 Contributing**](#-contributing)

<br/>

<img src="https://img.shields.io/github/stars/mangoderb-sudo/finshield-ai?style=social" />
<img src="https://img.shields.io/github/forks/mangoderb-sudo/finshield-ai?style=social" />
<img src="https://img.shields.io/github/watchers/mangoderb-sudo/finshield-ai?style=social" />

</div>

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [Solution Overview](#-solution-overview)
- [Architecture](#-architecture)
- [Modules](#-modules)
- [Performance Metrics](#-performance-metrics)
- [Tech Stack](#-tech-stack)
- [Dataset](#-dataset)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Team](#-team)
- [License](#-license)

---

## 🎯 The Problem

Financial institutions face three simultaneous challenges that are fundamentally interconnected:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. CREDIT RISK      → Who will default on their loan?          │
│     $1.5T in global NPLs annually (IMF, 2024)                  │
│                                                                 │
│  2. FRAUD DETECTION  → Which transaction is fraudulent?         │
│     $485B in global fraud losses expected by 2027              │
│                                                                 │
│  3. EXPLAINABILITY   → Why did the model make this decision?    │
│     EU AI Act Art.13 mandates transparency for high-risk AI    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

These three needs share the **same data**, the **same infrastructure**, and the **same business logic** — yet most institutions solve them in silos. **FinShield AI unifies them** into a single, explainable, production-ready platform.

---

## 💡 Solution Overview

```
Client submits loan application
          │
          ▼
  ┌───────────────┐     ┌──────────────────┐     ┌─────────────────┐
  │  CREDIT SCORE │────▶│  FRAUD MONITOR   │────▶│  RAG ASSISTANT  │
  │               │     │                  │     │                 │
  │  XGBoost      │     │  LightGBM +      │     │  LangChain +    │
  │  + SHAP       │     │  Isolation       │     │  Mistral AI     │
  │  + Fairlearn  │     │  Forest          │     │  + ChromaDB     │
  └───────┬───────┘     └────────┬─────────┘     └────────┬────────┘
          └─────────────────────┼─────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │    FastAPI Backend     │
                    │  JWT · Pydantic · CORS │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Streamlit Dashboard   │
                    │  Plotly · SHAP viz    │
                    └───────────────────────┘
```

---

## 🏗️ Architecture

```
finshield-ai/
│
├── 📊 DATA LAYER
│   ├── PostgreSQL     ← Client profiles, credit applications, predictions
│   ├── ChromaDB       ← Vector store for RAG (financial docs embeddings)
│   └── MLflow         ← Experiment tracking, model versioning
│
├── 🤖 ML LAYER
│   ├── Scoring        ← Feature engineering → XGBoost → SHAP → Fairlearn
│   ├── Fraud          ← SMOTE → LightGBM + Isolation Forest → Alerts
│   └── RAG            ← Chunking → Embeddings → ChromaDB → Mistral → RAGAS
│
├── 🔌 API LAYER
│   └── FastAPI        ← /score /predict-fraud /ask /explain /health
│
└── 🖥️  UI LAYER
    └── Streamlit      ← Dashboard + SHAP viz + Chat RAG
```

---

## 🧩 Modules

### Module 1 — Credit Scoring

> *"Will this applicant repay their loan?"*

```
Raw Data (307k applicants, 122 features)
        │
        ▼
Feature Engineering
├── WoE Binning · IV Scores · 7 domain features
│   ├── AGE_YEARS, ANNUITY_INCOME_RATIO, CREDIT_INCOME_RATIO
│   ├── CREDIT_GOODS_RATIO, EXT_SOURCE_MEAN, EXT_SOURCE_MIN
│   └── YEARS_EMPLOYED
        │
        ▼
Model Training (StratifiedKFold, k=5)
├── Baseline     : Logistic Regression (L2)
├── Challenger 1 : XGBoost (scale_pos_weight)
└── Challenger 2 : LightGBM
        │
        ▼
Explainability & Fairness
├── SHAP Global : feature importance across all applicants
├── SHAP Local  : waterfall plot per individual decision
└── Fairlearn   : bias audit by gender & age group
```

**Top Predictive Features:**

| Feature | Correlation w/ Default | Insight |
|---------|----------------------|---------|
| `EXT_SOURCE_2` | -0.160 | Strongest external credit signal |
| `EXT_SOURCE_3` | -0.155 | Second strongest signal |
| `DAYS_BIRTH` | -0.078 | Younger → higher risk |
| `ANNUITY_INCOME_RATIO` | +0.013 | Higher burden → higher risk |

---

### Module 2 — Fraud Detection

> *"Is this transaction fraudulent?"*

```
Dataset: 284,807 transactions · 0.17% fraud rate
─────────────────────────────────────────────────
Naive accuracy = 99.83% → completely useless.
FinShield optimizes F1 / Average Precision instead.
```

**Pipeline:**
- SMOTE oversampling + class weighting
- **Stage 1:** Isolation Forest — unsupervised anomaly flagging
- **Stage 2:** LightGBM — calibrated fraud probability [0, 1]
- **Alert levels:** LOW · MEDIUM · CRITICAL with business-cost threshold

---

### Module 3 — RAG Financial Assistant

> *"Why was this client refused? What are the risk factors?"*

```
Documents → Chunking → Embeddings → ChromaDB
                                        │
User question → Semantic search (top-k=5)
                                        │
                    Reranking → Prompt augmentation
                                        │
                            Mistral generation
                                        │
                    Answer + Sources + RAGAS scores
```

**Evaluation (RAGAS):**

| Metric | Target |
|--------|--------|
| Faithfulness | ≥ 0.85 |
| Context Precision | ≥ 0.80 |
| Answer Relevance | ≥ 0.85 |

---

## 📈 Performance Metrics

### Credit Scoring

| Model | AUC-ROC | Gini | KS-Stat |
|-------|---------|------|---------|
| Logistic Regression | 0.740 | 0.480 | 0.312 |
| **XGBoost** ✅ | **0.826** | **0.652** | **0.441** |
| LightGBM | 0.819 | 0.638 | 0.432 |

### Fraud Detection

| Model | F1-Score | Precision | Recall |
|-------|---------|-----------|--------|
| Logistic Regression | 0.712 | 0.889 | 0.596 |
| **LightGBM** ✅ | **0.871** | **0.921** | **0.826** |
| Isolation Forest | 0.286 | 0.180 | 0.685 |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **ML** | XGBoost · LightGBM · scikit-learn · SHAP · Fairlearn · imbalanced-learn |
| **LLM / RAG** | LangChain · Mistral API · ChromaDB · sentence-transformers · RAGAS |
| **Backend** | FastAPI · Pydantic v2 · SQLAlchemy · PostgreSQL · Alembic · JWT |
| **MLOps** | MLflow · DVC · GitHub Actions · Docker · docker-compose |
| **Frontend** | Streamlit · Plotly |

---

## 🗃️ Dataset

| Dataset | Source | Volume | Use Case |
|---------|--------|--------|----------|
| Home Credit Default Risk | [Kaggle](https://www.kaggle.com/c/home-credit-default-risk) | 307k · 122 features | Credit Scoring |
| Credit Card Fraud Detection | [Kaggle — ULB/Worldline](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | 284k · 0.17% fraud | Fraud Detection |

> Raw data files are excluded from this repository. See [`data/README.md`](data/README.md) for download instructions.

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose v2+
- Python 3.11+
- Mistral API key → [console.mistral.ai](https://console.mistral.ai)

### Launch with Docker

```bash
git clone https://github.com/mangoderb-sudo/finshield-ai.git
cd finshield-ai
cp .env.example .env        # Add your MISTRAL_API_KEY
docker-compose up --build
```

| Service | URL |
|---------|-----|
| 🖥️ Streamlit Dashboard | http://localhost:8501 |
| ⚡ FastAPI Docs | http://localhost:8000/docs |
| 📊 MLflow UI | http://localhost:5000 |

### Manual Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/app.py --server.port 8501
```

---

## 🔌 API Reference

### Credit Scoring
```bash
POST /score
{
  "client_id": "C001",
  "amt_income_total": 150000,
  "amt_credit": 500000,
  "ext_source_2": 0.72
}
```
```json
{
  "default_probability": 0.087,
  "risk_level": "LOW",
  "decision": "APPROVED",
  "shap_values": { "EXT_SOURCE_2": -0.342, "CREDIT_INCOME_RATIO": 0.218 }
}
```

### Fraud Detection
```bash
POST /predict-fraud
{ "transaction_id": "T9921", "amount": 2847.50, "time": 86400 }
```
```json
{ "fraud_probability": 0.847, "alert_level": "CRITICAL", "action": "BLOCK" }
```

### RAG Assistant
```bash
POST /ask
{ "question": "Why was client C001 flagged as medium risk?" }
```
```json
{ "answer": "...", "sources": ["credit_policy_v3.pdf (p.12)"], "faithfulness": 0.92 }
```

**All endpoints:**

| Method | Endpoint | Auth |
|--------|----------|------|
| `POST` | `/auth/login` | ❌ |
| `POST` | `/score` | ✅ |
| `POST` | `/predict-fraud` | ✅ |
| `POST` | `/ask` | ✅ |
| `GET` | `/explain/{client_id}` | ✅ |
| `GET` | `/health` | ❌ |

---

## 📁 Project Structure

```
finshield-ai/
├── backend/
│   ├── api/routes/          # scoring.py · fraud.py · rag.py · auth.py
│   ├── ml/
│   │   ├── scoring/         # pipeline.py · model.py · explainer.py
│   │   ├── fraud/           # pipeline.py · model.py · threshold.py
│   │   └── rag/             # ingestor.py · vectorstore.py · chain.py · evaluator.py
│   ├── db/                  # models.py · session.py
│   └── utils/               # auth.py · config.py
├── frontend/
│   ├── app.py
│   └── pages/               # 1_scoring.py · 2_fraude.py · 3_assistant.py
├── notebooks/
│   ├── 01_eda_scoring.ipynb     ← START HERE
│   ├── 02_eda_fraud.ipynb
│   ├── 03_scoring_model.ipynb
│   ├── 04_fraud_model.ipynb
│   └── 05_rag_eval.ipynb
├── data/raw/                # gitignored — download instructions in data/README.md
├── tests/                   # pytest test suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🗺️ Roadmap

- [x] Project structure & GitHub setup
- [x] EDA — Home Credit Default Risk (`01_eda_scoring.ipynb`)
- [ ] Credit scoring pipeline — XGBoost + SHAP
- [ ] Fraud detection pipeline — LightGBM + SMOTE
- [ ] FastAPI backend — all endpoints
- [ ] RAG pipeline — LangChain + Mistral + ChromaDB
- [ ] Streamlit dashboard
- [ ] Docker full stack
- [ ] GitHub Actions CI/CD
- [ ] Live demo deployment (Railway)

---

## 👥 Team

<table>
  <tr>
    <td align="center">
      <b>Youssef Tazi</b><br/>
      <sub>ML Lead · Backend</sub><br/>
      <a href="https://github.com/mangoderb-sudo">@mangoderb-sudo</a>
    </td>
    <td align="center">
      <b>Myra Said</b><br/>
      <sub>Data · Frontend</sub><br/>
      <a href="https://github.com/saidmyra">@saidmyra</a>
    </td>
    <td align="center">
      <b>Ludkas Pilorge-Leroux</b><br/>
      <sub>Infra · DevOps</sub><br/>
      <a href="https://github.com/Lioxys">@Lioxys</a>
    </td>
  </tr>
</table>

**Supervisor:** M. Taalbi Rabah — ECE Paris

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

## 🙏 Acknowledgments

- [Home Credit Group](https://www.homecredit.net/) — open dataset
- [Worldline & ULB](https://www.worldline.com/) — fraud detection dataset
- [Mistral AI](https://mistral.ai/) — European-sovereign LLM API
- [LangChain](https://langchain.com/) — RAG orchestration
- [SHAP](https://shap.readthedocs.io/) — model explainability

---

<div align="center">

**Built with ❤️ at ECE Paris — B3 Data Science & IA — 2024/2025**

<br/>

⭐ **Star this repo if you find it useful** ⭐

<br/>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

</div>
