# محاسب الذكاء الاصطناعي | AI Accountant KSA

> **The first bilingual Arabic-English AI accountant built specifically for the Saudi regulatory environment.**  
> Powered by Claude AI (Anthropic) · SOCPA · IFRS · GAZT · Zakat · VAT 15% · Vision 2030

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Claude AI](https://img.shields.io/badge/Powered_by-Claude_AI-orange)
![Arabic](https://img.shields.io/badge/Language-Arabic_%2F_English-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Why This Beats Every Generic AI Accounting Tool

| What others do | What محاسب does |
|---|---|
| Respond in English only | **Fully bilingual — answers in Arabic if you ask in Arabic** |
| Generic GAAP/IFRS knowledge | **KSA-specific: SOCPA, GAZT, Zakat 2.5%, VAT 15%, Fatoorah** |
| No sector awareness | **Tailored for Oil & Gas, Banking, Real Estate, Vision 2030 Giga-projects** |
| No calculation tools | **Live Zakat calculator, VAT calculator, ratio dashboards** |
| No journal entry builder | **6 pre-built KSA journal entry templates with balance verification** |
| Static responses | **Claude AI — real-time, context-aware, multi-turn conversation** |
| No document analysis | **Upload your GL/Trial Balance CSV and ask questions about it** |

---

## Features

### 💬 Bilingual AI Chat (Claude-Powered)
- Ask accounting questions in **Arabic or English** — it responds in the same language
- Multi-turn conversation with full context memory
- System prompt pre-loaded with KSA regulatory knowledge:
  - SOCPA standards (all core pronouncements)
  - IFRS 9 (ECL), IFRS 15 (Revenue), IFRS 16 (Leases)
  - IAS 36, 37, 38, 40
  - GAZT Zakat rules, VAT 15%, Transfer Pricing, e-invoicing (Fatoorah)
  - Vision 2030 accounting implications, government grants (IAS 20)
- 8 one-click quick prompts for the most common Saudi accounting questions
- Export full conversation as `.txt`
- Upload CSV/TXT financial files — AI analyses them in context

### 🧮 Zakat & VAT Calculator
- **Zakat Calculator**: computes zakatable base with correct haircuts (receivables 90%, inventory 85%), deducts current liabilities, applies 2.5% rate
- Waterfall chart showing Zakat base decomposition
- **VAT Calculator**: Add or extract VAT at 15%; ZATCA Fatoorah notes included
- VAT split pie chart

### 📒 Journal Entry Builder
6 pre-built Saudi-specific journal entries:
1. **شراء أصل ثابت** — Fixed asset purchase with VAT 15% (IAS 16)
2. **بيع بضاعة** — Sale of goods with VAT (IFRS 15)
3. **صرف رواتب** — Payroll with GOSI 10% (IAS 19)
4. **دفع الزكاة** — Zakat payment to GAZT (SOCPA 7)
5. **بدء عقد إيجار** — IFRS 16 lease commencement (ROU asset)
6. **مخصص ECL** — Expected Credit Loss provision (IFRS 9)

Each entry: automatically balanced (Dr = Cr), IFRS/SOCPA standard cited, downloadable.

Also includes **full Saudi Chart of Accounts** (22 accounts, Arabic + English, SOCPA-aligned).

### 📊 Financial Ratio Analysis
- Input: Current Assets, Total Assets, Liabilities, Equity, Revenue, Gross Profit, Net Income
- Gauge charts for Current Ratio, Gross Margin, ROE
- Full ratio table: Current Ratio, Gross Margin, Net Margin, ROE, ROA, Debt Ratio
- Each ratio benchmarked and flagged with IFRS/IAS reference
- Summary bar chart

---

## Tech Stack

```
Python 3.12
Streamlit    ≥ 1.32   — Web app framework
Anthropic    ≥ 0.25   — Claude AI API
Pandas       ≥ 2.0    — Data processing
NumPy        ≥ 1.26   — Calculations
Plotly       ≥ 5.18   — Interactive charts
```

**Design**: Islamic geometric aesthetic — Amiri Arabic font, Cormorant Garamond, emerald & gold palette.

---

## Quick Start

### Local
```bash
git clone https://github.com/YOUR_USERNAME/محاسب-ai-ksa.git
cd محاسب-ai-ksa
pip install -r requirements.txt
streamlit run app.py
```
Enter your [Anthropic API key](https://console.anthropic.com/) in the sidebar.

### Streamlit Cloud (Free, 2 minutes)
1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select `app.py` → Deploy
4. Enter API key in the sidebar at runtime (never stored)

> **API Key**: The app never stores your API key. It is only used per-session in memory.

---

## KSA Regulatory Coverage

| Area | Coverage |
|---|---|
| **SOCPA Standards** | All core pronouncements including SOCPA 1, 3, 7, 9, 15 |
| **IFRS** | IFRS 9, 15, 16 + IAS 2, 16, 19, 20, 36, 37, 38, 40 |
| **Zakat** | Base computation, Nisab, Hawl, GAZT assessment rules |
| **VAT** | 15% standard rate, zero-rated categories, ZATCA Fatoorah e-invoicing |
| **Transfer Pricing** | Ministerial Resolution 2019, arm's length principle |
| **Vision 2030** | Government grants (IAS 20), Giga-project accounting, NTP |
| **GOSI** | Payroll integration, Saudization (Nitaqat) |
| **Islamic Finance** | Murabaha, Ijarah, Sukuk accounting notes |

---

## AI Question Examples

### Arabic
```
كيف تحسب زكاة الشركات في المملكة العربية السعودية؟
ما هو القيد المحاسبي لعقد إيجار وفق IFRS 16؟
كيف أعالج الفاتورة الضريبية الإلكترونية في دفاتر الشركة؟
ما هي متطلبات الإفصاح عن المعاملات مع الأطراف المرتبطة وفق SOCPA 7؟
```

### English
```
How do I calculate Expected Credit Loss under IFRS 9 for a Saudi bank?
What are Saudi Arabia's transfer pricing documentation requirements?
How should government grants from Vision 2030 programs be accounted for?
Explain the IFRS 16 lease modification accounting treatment.
```

---

## CV / Interview Value

This project demonstrates to KSA hiring managers:

- **Arabic proficiency** — built an Arabic-first application
- **KSA regulatory depth** — SOCPA, GAZT, Zakat, VAT 15%, Vision 2030
- **IFRS technical knowledge** — IFRS 9/15/16, IAS 36/37, ECL models
- **AI integration skills** — Claude API, prompt engineering, multi-turn dialogue
- **Python/Streamlit** — production-ready deployment
- **Design thinking** — culturally appropriate Islamic geometric UI

Live demo link → instant credibility over candidates with only textbook knowledge.

---

## Roadmap

- [ ] Arabic PDF report generation (audit memo in Arabic)
- [ ] SAP / Oracle GL CSV parser with AI analysis
- [ ] ZATCA e-invoice XML validator
- [ ] Islamic finance instruments (Murabaha, Sukuk, Ijarah)
- [ ] GAZT Zakat return form pre-filler
- [ ] Multi-user authentication (Streamlit Community Cloud)

---

## License

MIT — free to use, fork, and extend for portfolio or commercial use.

---

*محاسب is an AI-powered educational and analytical tool. Outputs are indicative and should be validated by a licensed SOCPA Chartered Accountant before use in official filings or audit reports.*
