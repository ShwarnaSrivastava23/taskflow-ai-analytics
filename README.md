# 📊 TaskFlow Analytics Assistant

> **Ask business questions in plain English. Get SQL-backed insights instantly.**

An AI-powered analytics assistant for SaaS business data that converts natural-language questions into SQL queries, executes them on DuckDB, and presents the results through interactive tables and charts.

<p align="center">

  <a href="https://taskflow-ai-analytics-k98f95vpxkpscfftevxtut.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge" />
  </a>

  <a href="https://github.com/ShwarnaSrivastava23/taskflow-ai-analytics">
    <img src="https://img.shields.io/badge/💻%20Source%20Code-GitHub-181717?style=for-the-badge&logo=github" />
  </a>

</p>

---

## 🎯 Why TaskFlow?

Business teams often have valuable data but don't always have the time or SQL knowledge required to analyze it.

**TaskFlow Analytics Assistant** provides a simple conversational interface where users can ask questions such as:

> 💬 *"What is the churn rate by plan tier?"*

Instead of manually writing SQL, the application generates the query, validates it, executes it, and displays the result.

---

## 🚀 Live Demo

### 👉 [Try TaskFlow Analytics Assistant](https://taskflow-ai-analytics-k98f95vpxkpscfftevxtut.streamlit.app/)

Ask questions about:

- 📈 MRR and revenue
- 👥 Users and subscriptions
- 🔄 Churn
- 🎫 Support tickets
- 🌎 Customer distribution
- 📊 Product usage

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 Natural Language Queries | Ask questions without writing SQL |
| 🤖 AI-powered SQL Generation | Groq LLM converts questions into SQL |
| 🗄️ DuckDB Analytics | Fast analytical queries on SaaS data |
| 📊 Interactive Visualizations | Automatically generated Plotly charts |
| 🔐 SQL Safety Validation | Only read-only `SELECT` queries are executed |
| 📋 Tabular Results | View the underlying query results |
| 🎲 Synthetic Dataset | Realistic SaaS data generated with Faker |
| ☁️ Cloud Deployment | Deployed using Streamlit Community Cloud |

---

## 🧠 How It Works

```text
                  ┌─────────────────┐
                  │   User Question │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Groq LLM     │
                  │  Question → SQL │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  SQL Validation │
                  │  Read-only only │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     DuckDB      │
                  │  Query Execute  │
                  └────────┬────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │     Results + Chart     │
              │  Streamlit + Plotly     │
              └─────────────────────────┘
