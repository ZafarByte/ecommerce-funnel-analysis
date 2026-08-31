# 🛒 E-commerce Funnel & Customer Behavior Analytics

<p align="center">
  <img src="https://img.shields.io/badge/Python-Data%20Analysis-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-SQL-316192?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black" />
  <img src="https://img.shields.io/badge/Pandas-Analysis-150458?logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-In%20Progress-orange" />
</p>

<p align="center">
  <b>End-to-End E-commerce Analytics Project</b>
</p>

<p align="center">
  Turning millions of customer interaction events into actionable business insights.
</p>

---

## 📊 Project at a Glance

> **How can an e-commerce business understand where customers drop off, which products have conversion problems, and what customer behaviors indicate purchase intent?**

This project analyzes the **RetailRocket E-commerce Dataset** containing over **2.7 million user events**.

The analysis combines:

**Python → PostgreSQL → Power BI**

to build an end-to-end data analytics solution.

---
</p>

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Data preparation, EDA and behavioral analysis |
| 🐼 **Pandas** | Data manipulation and aggregation |
| 🐘 **PostgreSQL** | SQL analytics and business metrics |
| 📊 **Power BI** | Interactive dashboard and storytelling |
| 📝 **Git & GitHub** | Version control and portfolio documentation |

---

# 🏗️ Project Architecture

```text
                    RETAILROCKET DATASET
                           │
                           ▼
                  ┌─────────────────┐
                  │   Raw Events    │
                  │    2.7M+ rows   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     Python      │
                  │                 │
                  │ Data Cleaning   │
                  │ EDA             │
                  │ Feature Eng.    │
                  │ Funnel Analysis │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   PostgreSQL    │
                  │                 │
                  │ Data Validation │
                  │ SQL Analytics   │
                  │ Funnel Queries  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Power BI     │
                  │                 │
                  │ KPI Dashboard   │
                  │ Funnel Charts   │
                  │ Product Analysis│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    BUSINESS     │
                  │    INSIGHTS     │
                  └─────────────────┘
