"""
محاسب الذكاء الاصطناعي | AI Accountant KSA
Bilingual Arabic-English AI Accountant powered by Claude API
KSA-specific: SOCPA · IFRS · GAZT · Zakat · VAT 15% · Vision 2030
"""

import streamlit as st
import anthropic
import json
import re
import math
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="محاسب الذكاء الاصطناعي | AI Accountant KSA",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: Islamic Geometric Luxury Theme ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=IBM+Plex+Mono:wght@400;600&family=Cormorant+Garamond:wght@300;400;600;700&display=swap');

:root {
    --emerald:  #1A6B4A;
    --emerald2: #0F4A33;
    --emerald3: #0A2E20;
    --gold:     #C9A84C;
    --gold-lt:  #E8C97A;
    --cream:    #F5F0E8;
    --cream2:   #EDE6D4;
    --ink:      #1A1208;
    --ink2:     #2D2010;
    --muted:    #7A6E5A;
    --border:   rgba(201,168,76,0.25);
    --red:      #C0392B;
    --blue:     #1A4A7A;
    --white:    #FDFAF4;
}
html, body, [class*="css"] {
    font-family: 'Cormorant Garamond', serif;
    background-color: var(--cream);
    color: var(--ink);
}
.stApp { background: var(--cream); }
.main  { background: var(--cream); }

/* Geometric background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        repeating-linear-gradient(45deg, transparent, transparent 28px, rgba(201,168,76,0.035) 28px, rgba(201,168,76,0.035) 30px),
        repeating-linear-gradient(-45deg, transparent, transparent 28px, rgba(201,168,76,0.035) 28px, rgba(201,168,76,0.035) 30px);
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--emerald3) 0%, var(--emerald2) 60%, #071C12 100%);
    border-right: 2px solid var(--gold);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stTextArea > div > div > textarea {
    background: rgba(201,168,76,0.08) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: var(--cream) !important;
    border-radius: 3px !important;
}

/* Hero */
.hero-wrap {
    background: linear-gradient(135deg, var(--emerald3) 0%, var(--emerald2) 50%, var(--emerald3) 100%);
    border: 1px solid var(--gold);
    border-top: 4px solid var(--gold);
    border-radius: 6px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-arabic {
    font-family: 'Amiri', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--gold);
    direction: rtl;
    text-align: right;
    line-height: 1.2;
    text-shadow: 0 2px 20px rgba(201,168,76,0.3);
}
.hero-english {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    font-weight: 300;
    color: rgba(245,240,232,0.65);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); margin: 1rem 0; }
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border: 1px solid rgba(201,168,76,0.4);
    color: var(--gold-lt);
    background: rgba(201,168,76,0.08);
    border-radius: 2px;
    margin: 2px 3px;
}

/* Chat messages */
.msg-user {
    background: var(--emerald2);
    border: 1px solid var(--emerald);
    border-radius: 12px 12px 4px 12px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    margin-left: 10%;
    color: var(--cream);
    font-size: 0.95rem;
}
.msg-ai {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 12px 12px 12px 4px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    margin-right: 5%;
    color: var(--ink);
    font-size: 0.93rem;
    line-height: 1.75;
}
.msg-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

/* Cards */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    border-radius: 4px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--emerald);
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* KPI row */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap:1rem; margin-bottom:1.5rem; }
.kpi {
    background: var(--white);
    border: 1px solid var(--border);
    border-bottom: 3px solid var(--gold);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.kpi-val { font-family: 'Cormorant Garamond',serif; font-size:2rem; font-weight:700; color:var(--emerald); line-height:1; }
.kpi-lbl { font-family: 'IBM Plex Mono',monospace; font-size:0.58rem; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-top:0.3rem; }
.kpi-ar  { font-family: 'Amiri',serif; font-size:0.85rem; color:var(--gold); }

/* Zakat box */
.zakat-box {
    background: linear-gradient(135deg, #FFF9EE, #FFF3D4);
    border: 1px solid var(--gold);
    border-right: 4px solid var(--gold);
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    direction: rtl;
    font-family: 'Amiri', serif;
    font-size: 0.95rem;
    color: var(--ink2);
    line-height: 1.9;
}
.zakat-title { font-family:'Amiri',serif; font-size:1.2rem; font-weight:700; color:var(--emerald); margin-bottom:0.8rem; }

/* Journal entry table */
.je-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
.je-table th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 8px 12px;
    border-bottom: 2px solid var(--gold);
    background: var(--cream2);
    text-align: right;
}
.je-table td { padding: 9px 12px; border-bottom: 1px solid rgba(201,168,76,0.1); text-align:right; }
.dr { color: var(--emerald); font-weight:600; }
.cr { color: var(--blue); font-weight:600; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--emerald), var(--emerald2)) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.2rem !important;
    border-radius: 2px !important;
}
.stButton > button:hover { opacity: 0.87 !important; }

.stTextArea > div > div > textarea {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    color: var(--ink) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1rem !important;
    border-radius: 3px !important;
}
.stSelectbox > div > div { background: var(--white) !important; border: 1px solid var(--border) !important; }
.stNumberInput > div > div > input { background: var(--white) !important; border: 1px solid var(--border) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 2px solid var(--border); gap:0; }
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.7rem 1.1rem !important;
}
.stTabs [aria-selected="true"] { color: var(--emerald) !important; border-bottom: 2px solid var(--gold) !important; }

hr { border-color: var(--border) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# KSA ACCOUNTING KNOWLEDGE & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """أنت محاسب خبير ومتخصص في المملكة العربية السعودية. اسمك "محاسب".

You are an expert AI accountant specializing in Saudi Arabia's financial and regulatory environment.

## Core Expertise:
1. **SOCPA Standards** — Saudi Organization for Chartered and Professional Accountants (all pronouncements)
2. **IFRS as adopted in KSA** — IFRS 9 (ECL), IFRS 15 (Revenue), IFRS 16 (Leases), IAS 36/37/38/40
3. **GAZT / ZATCA** — Zakat, Tax and Customs Authority: Zakat 2.5%, VAT 15%, Excise Tax, e-invoicing (Fatoorah)
4. **Zakat Calculation** — Zakatable net worth, Nisab, Hawl, GAZT assessment methodology
5. **Transfer Pricing** — Ministerial Resolution 2019, arm's length principle for KSA related parties
6. **Vision 2030** — Giga-projects (NEOM, ROSHN, Qiddiya), NTP, government grants (IAS 20)
7. **IFRS 16 Leases** — ROU assets, lease liability, Saudi real estate specific treatments
8. **IFRS 9 ECL** — Expected Credit Loss for Saudi banks and corporates
9. **Double-Entry Bookkeeping** — Arabic and English journal entries
10. **Financial Ratio Analysis** — Liquidity, profitability, leverage, DuPont, Islamic finance ratios

## Critical Response Rules:
- **ALWAYS respond in the SAME LANGUAGE the user used.** Arabic question → Arabic answer. English question → English answer. Mixed → Arabic primary.
- For journal entries: present as Dr/Cr table with SAR amounts. Always verify Dr = Cr (balanced).
- Always cite the relevant IFRS/IAS/SOCPA standard.
- For Zakat: show formula → Zakat = Zakatable Base × 2.5% (base = Zakatable Assets − Current Liabilities).
- For VAT: always mention ZATCA Fatoorah e-invoicing requirement.
- Add خلاصة (summary) at end of long English responses.
- Use SAR currency. Mention Hijri calendar where relevant.
- Be concise, professional, and practically actionable for a Saudi accountant.
"""

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Cormorant Garamond, serif", color="#7A6E5A", size=11),
    margin=dict(l=40, r=20, t=40, b=40),
)

QUICK_PROMPTS = [
    ("🧮 حساب الزكاة", "كيف تحسب زكاة الشركات في المملكة؟ أعطني المعادلة الكاملة والوعاء الزكوي مع مثال عملي"),
    ("📒 قيد أصل ثابت", "أعطني القيد المحاسبي لشراء أصل ثابت بقيمة 500,000 ريال مع ضريبة القيمة المضافة 15%"),
    ("💰 ضريبة القيمة المضافة", "كيف تسجل الفاتورة الإلكترونية (فاتورة) في دفاتر الشركة؟ مع القيود المحاسبية"),
    ("📋 IFRS 16 إيجار", "اشرح تطبيق IFRS 16 على عقد إيجار مكتب في الرياض — القيود والعرض في الميزانية"),
    ("🏦 نموذج ECL", "How do I calculate Expected Credit Loss (IFRS 9) for a Saudi corporate loan portfolio? Step by step."),
    ("📈 رؤية 2030", "ما هي الاعتبارات المحاسبية للمنح الحكومية من برامج رؤية 2030؟ وفق IAS 20"),
    ("📊 تحليل النسب", "ما هي أهم النسب المالية لتحليل شركة سعودية؟ مع معايير القياس"),
    ("⚖️ أسعار التحويل", "What are Saudi Arabia's transfer pricing rules for intercompany transactions under GAZT regulations?"),
]

SAMPLE_ACCOUNTS = {
    "1001": ("النقدية وما في حكمها", "Cash & Equivalents"),
    "1101": ("الذمم المدينة", "Accounts Receivable"),
    "1102": ("مخصص الديون المشكوك فيها", "ECL Allowance (IFRS 9)"),
    "1201": ("المخزون", "Inventories"),
    "1501": ("الأصول الثابتة", "Property, Plant & Equipment"),
    "1502": ("مجمع الاستهلاك", "Accumulated Depreciation"),
    "1601": ("حق الاستخدام – IFRS 16", "Right-of-Use Asset"),
    "2001": ("الذمم الدائنة", "Accounts Payable"),
    "2101": ("ضريبة القيمة المضافة – ZATCA", "VAT Payable — ZATCA"),
    "2201": ("الزكاة المستحقة", "Zakat Payable"),
    "2301": ("التزام الإيجار – IFRS 16", "Lease Liability"),
    "2401": ("مخصص منافع الموظفين", "Employee Benefits Provision (IAS 19)"),
    "3001": ("رأس المال", "Share Capital"),
    "3101": ("الأرباح المحتجزة", "Retained Earnings"),
    "4001": ("الإيرادات", "Revenue (IFRS 15)"),
    "4101": ("إيرادات أخرى", "Other Income"),
    "5001": ("تكلفة الإيرادات", "Cost of Revenue"),
    "5101": ("مصاريف الرواتب والمزايا", "Salaries & Benefits (IAS 19)"),
    "5201": ("مصاريف عمومية وإدارية", "G&A Expenses"),
    "5301": ("مصاريف الاستهلاك", "Depreciation Expense"),
    "5401": ("مصاريف التمويل", "Finance Costs"),
    "5501": ("مصروف خسائر ائتمان", "Credit Loss Expense (IFRS 9)"),
}

JE_TEMPLATES = {
    "شراء أصل ثابت | Fixed Asset Purchase": lambda amt: {
        "standard": "IAS 16 — Property, Plant & Equipment",
        "entries": [
            ("Dr", "الأصول الثابتة | PPE (1501)", amt),
            ("Dr", "ضريبة القيمة المضافة – ZATCA (2101)", amt * 0.15),
            ("Cr", "النقدية / البنك | Cash (1001)", amt * 1.15),
        ],
        "narration": f"شراء أصل ثابت SAR {amt:,.2f} + ضريبة القيمة المضافة {amt*0.15:,.2f} = الإجمالي {amt*1.15:,.2f}",
    },
    "بيع بضاعة | Sale of Goods": lambda amt: {
        "standard": "IFRS 15 — Revenue from Contracts with Customers",
        "entries": [
            ("Dr", "الذمم المدينة | Accounts Receivable (1101)", amt * 1.15),
            ("Cr", "الإيرادات | Revenue (4001)", amt),
            ("Cr", "ضريبة القيمة المضافة – ZATCA (2101)", amt * 0.15),
        ],
        "narration": f"تسجيل إيراد بيع SAR {amt:,.2f} + VAT SAR {amt*0.15:,.2f}",
    },
    "صرف رواتب | Payroll": lambda amt: {
        "standard": "IAS 19 — Employee Benefits",
        "entries": [
            ("Dr", "مصاريف الرواتب | Salaries Expense (5101)", amt),
            ("Cr", "النقدية | Cash / Bank (1001)", amt * 0.90),
            ("Cr", "التأمينات الاجتماعية | GOSI (2401)", amt * 0.10),
        ],
        "narration": f"رواتب الشهر — صافي {amt*0.9:,.2f} + GOSI {amt*0.1:,.2f}",
    },
    "دفع الزكاة | Zakat Payment": lambda amt: {
        "standard": "SOCPA 7 — Zakat · هيئة الزكاة والضريبة والجمارك",
        "entries": [
            ("Dr", "الزكاة المستحقة | Zakat Payable (2201)", amt),
            ("Cr", "النقدية | Cash / Bank (1001)", amt),
        ],
        "narration": f"تسديد الزكاة السنوية لهيئة الزكاة SAR {amt:,.2f}",
    },
    "بدء عقد إيجار | IFRS 16 Lease": lambda amt: {
        "standard": "IFRS 16 — Leases (Right-of-Use Asset)",
        "entries": [
            ("Dr", "أصل حق الاستخدام | ROU Asset (1601)", amt),
            ("Cr", "التزام الإيجار | Lease Liability (2301)", amt),
        ],
        "narration": f"تسجيل عقد إيجار جديد — القيمة الحالية للمدفوعات SAR {amt:,.2f}",
    },
    "مخصص ECL | IFRS 9 Credit Loss": lambda amt: {
        "standard": "IFRS 9 — Financial Instruments (Expected Credit Loss)",
        "entries": [
            ("Dr", "مصروف خسائر ائتمان | Credit Loss Expense (5501)", amt),
            ("Cr", "مخصص خسائر ائتمان | ECL Allowance (1102)", amt),
        ],
        "narration": f"تسجيل مخصص خسائر الائتمان المتوقعة SAR {amt:,.2f} وفق IFRS 9",
    },
}


# ═══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "q_count" not in st.session_state:
    st.session_state.q_count = 0
if "uploaded_context" not in st.session_state:
    st.session_state.uploaded_context = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# ═══════════════════════════════════════════════════════════════════════
# AI CALL
# ═══════════════════════════════════════════════════════════════════════
def call_claude(user_message: str) -> str:
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)
        payload = []
        for m in st.session_state.messages[-14:]:
            payload.append({"role": m["role"], "content": m["content"]})

        full_msg = user_message
        if st.session_state.uploaded_context:
            full_msg = f"[Uploaded Document Context]\n{st.session_state.uploaded_context[:2000]}\n\n[Question]\n{user_message}"

        payload.append({"role": "user", "content": full_msg})

        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=payload,
        )
        st.session_state.total_tokens += resp.usage.input_tokens + resp.usage.output_tokens
        return resp.content[0].text
    except anthropic.AuthenticationError:
        return "❌ مفتاح API غير صحيح | Invalid API key. Please check the key in the sidebar."
    except anthropic.RateLimitError:
        return "⚠️ تجاوز حد الطلبات | Rate limit reached. Please wait a moment."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def compute_zakat(cash, receivables, inventory, investments, curr_liab):
    base = (cash + receivables * 0.9 + inventory * 0.85 + investments) - curr_liab
    base = max(base, 0)
    return base, base * 0.025


def make_gauge(value, title, lo, hi):
    color = "#1A6B4A" if lo <= value <= hi else "#C9A84C" if value < lo * 1.5 else "#C0392B"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title=dict(text=title, font=dict(size=10, color="#7A6E5A")),
        gauge=dict(
            axis=dict(range=[0, max(value * 2, hi * 2)], tickfont=dict(size=8)),
            bar=dict(color=color),
            bgcolor="rgba(201,168,76,0.04)",
            borderwidth=1, bordercolor="rgba(201,168,76,0.2)",
            steps=[dict(range=[lo, hi], color="rgba(26,107,74,0.08)")],
        ),
        number=dict(font=dict(size=22, color=color), suffix=""),
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=185, margin=dict(l=20, r=20, t=50, b=10))
    return fig


# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:0.8rem 0 1.3rem;">
        <div style="font-family:'Amiri',serif; font-size:2.2rem; color:#C9A84C; font-weight:700;">محاسب</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.55rem; letter-spacing:3px;
                    color:rgba(201,168,76,0.55); text-transform:uppercase; margin-top:0.2rem;">AI Accountant · KSA</div>
        <div style="height:1px; background:linear-gradient(90deg,transparent,#C9A84C,transparent); margin-top:0.9rem;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:rgba(201,168,76,0.6);margin-bottom:0.3rem;">Anthropic API Key</div>', unsafe_allow_html=True)
    api_input = st.text_input("", type="password", placeholder="sk-ant-...", label_visibility="collapsed", key="api_input")
    if api_input:
        st.session_state.api_key = api_input
        st.markdown('<div style="font-size:0.7rem;color:#2ECC71;font-family:IBM Plex Mono,monospace;margin-top:3px;">✓ مفتاح متصل | Key connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.7rem;color:rgba(201,168,76,0.4);font-family:IBM Plex Mono,monospace;margin-top:3px;">⬡ Enter key to activate AI</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:rgba(201,168,76,0.6);margin-bottom:0.4rem;">القطاع | Sector</div>', unsafe_allow_html=True)
    sector = st.selectbox("", [
        "شركة تجارية | Trading", "بنك / تمويل | Banking & Finance",
        "عقارات | Real Estate", "إنشاءات | Construction",
        "نفط وغاز | Oil & Gas", "صحة | Healthcare",
        "مشاريع رؤية 2030 | Vision 2030", "حكومي | Government",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:rgba(201,168,76,0.6);margin-bottom:0.4rem;margin-top:0.7rem;">السنة المالية | FY</div>', unsafe_allow_html=True)
    fy = st.selectbox("", ["2024 (1446هـ)", "2023 (1445هـ)", "2022 (1444هـ)"], label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:rgba(201,168,76,0.6);margin-bottom:0.4rem;">رفع ملف | Upload File</div>', unsafe_allow_html=True)
    up_file = st.file_uploader("", type=["csv", "txt"], label_visibility="collapsed")
    if up_file:
        try:
            if up_file.name.endswith(".csv"):
                df_up = pd.read_csv(up_file)
                st.session_state.uploaded_context = df_up.to_string(max_rows=40)
                st.markdown(f'<div style="font-size:0.7rem;color:#2ECC71;font-family:IBM Plex Mono,monospace;">✓ {len(df_up)} rows loaded</div>', unsafe_allow_html=True)
            else:
                st.session_state.uploaded_context = up_file.read().decode("utf-8", errors="ignore")[:2500]
                st.markdown('<div style="font-size:0.7rem;color:#2ECC71;font-family:IBM Plex Mono,monospace;">✓ File loaded</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(str(e))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:rgba(201,168,76,0.55);line-height:2.1;">
        💬 &nbsp;Q&A: <span style="color:#C9A84C;">{st.session_state.q_count}</span><br>
        🔢 &nbsp;Tokens: <span style="color:#C9A84C;">{st.session_state.total_tokens:,}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑 مسح المحادثة | Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.q_count = 0
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-arabic">محاسب الذكاء الاصطناعي للمملكة العربية السعودية</div>
    <div class="hero-english">AI Accountant · KSA · SOCPA · IFRS · GAZT · Zakat · Vision 2030</div>
    <div class="hero-divider"></div>
    <span class="badge">SOCPA معايير</span>
    <span class="badge">IFRS / IAS</span>
    <span class="badge">زكاة GAZT</span>
    <span class="badge">VAT 15% فاتورة</span>
    <span class="badge">رؤية 2030</span>
    <span class="badge">قيود محاسبية</span>
    <span class="badge">Claude AI</span>
    <span class="badge">ثنائي اللغة</span>
</div>
""", unsafe_allow_html=True)

# KPIs
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi">
        <div class="kpi-ar">معايير SOCPA/IFRS</div>
        <div class="kpi-val">20+</div>
        <div class="kpi-lbl">Standards Covered</div>
    </div>
    <div class="kpi">
        <div class="kpi-ar">ضريبة القيمة المضافة</div>
        <div class="kpi-val">15%</div>
        <div class="kpi-lbl">KSA VAT Rate</div>
    </div>
    <div class="kpi">
        <div class="kpi-ar">نسبة الزكاة</div>
        <div class="kpi-val">2.5%</div>
        <div class="kpi-lbl">Zakat Rate</div>
    </div>
    <div class="kpi">
        <div class="kpi-ar">محادثات</div>
        <div class="kpi-val">{st.session_state.q_count}</div>
        <div class="kpi-lbl">Conversations</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "💬  المحادثة الذكية | AI Chat",
    "🧮  الزكاة والضريبة | Zakat & VAT",
    "📒  القيود والحسابات | JE Builder",
    "📊  التحليل المالي | Ratios",
])


# ──────────────── TAB 1: AI CHAT ─────────────────────────────────────
with tab1:
    # Quick prompts
    st.markdown('<div class="card"><div class="card-title">أسئلة سريعة | Quick Prompts — Click to Ask</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (label, prompt) in enumerate(QUICK_PROMPTS):
        with cols[i % 4]:
            if st.button(label, key=f"qp_{i}", use_container_width=True):
                if not st.session_state.api_key:
                    st.warning("⬡ Enter your Anthropic API key in the sidebar.")
                else:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.spinner("محاسب يفكر... | Thinking..."):
                        ans = call_claude(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.session_state.q_count += 1
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat history
    if st.session_state.messages:
        st.markdown('<div class="card"><div class="card-title">المحادثة | Conversation</div>', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="msg-label" style="color:#C9A84C;text-align:right;">أنت | You</div>
                    {msg["content"]}
                </div>""", unsafe_allow_html=True)
            else:
                # Safe render: convert markdown bold and newlines
                content = msg["content"]
                content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                content = content.replace("\n", "<br>")
                st.markdown(f"""
                <div class="msg-ai">
                    <div class="msg-label" style="color:#1A6B4A;">🕌 محاسب AI</div>
                    {content}
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Export
        chat_txt = "\n\n".join([
            f"{'[أنت]' if m['role']=='user' else '[محاسب AI]'}\n{m['content']}"
            for m in st.session_state.messages
        ])
        st.download_button(
            "⬇ تصدير المحادثة | Export Chat",
            data=chat_txt.encode("utf-8"),
            file_name=f"محاسب_AI_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )

    # Input area
    st.markdown('<div class="card"><div class="card-title">اكتب سؤالك | Your Question</div>', unsafe_allow_html=True)
    col_q, col_btn = st.columns([5, 1])
    with col_q:
        user_q = st.text_area(
            "", height=90,
            placeholder="اكتب سؤالك المحاسبي هنا بالعربية أو الإنجليزية...\nAsk in Arabic or English — e.g. How do I record depreciation under IAS 16?",
            key="chat_input",
            label_visibility="collapsed",
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        send_btn = st.button("إرسال\nSend", use_container_width=True)

    if send_btn and user_q.strip():
        if not st.session_state.api_key:
            st.warning("⬡ Please enter your Anthropic API key in the sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_q.strip()})
            with st.spinner("محاسب يفكر... | Analysing..."):
                ans = call_claude(user_q.strip())
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.session_state.q_count += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────── TAB 2: ZAKAT & VAT ─────────────────────────────────
with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="card"><div class="card-title">حاسبة الزكاة | Zakat Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Amiri,serif;font-size:0.9rem;direction:rtl;color:#7A6E5A;margin-bottom:1rem;">أدخل البيانات المالية لحساب الوعاء الزكوي وفق أحكام هيئة الزكاة والضريبة والجمارك</div>', unsafe_allow_html=True)

        z_cash  = st.number_input("النقدية والبنوك (SAR)", 0.0, value=500000.0, step=10000.0, format="%.2f")
        z_rec   = st.number_input("الذمم المدينة (SAR)", 0.0, value=300000.0, step=10000.0, format="%.2f")
        z_inv   = st.number_input("المخزون (SAR)", 0.0, value=200000.0, step=10000.0, format="%.2f")
        z_inv2  = st.number_input("الاستثمارات (SAR)", 0.0, value=100000.0, step=10000.0, format="%.2f")
        z_liab  = st.number_input("الالتزامات المتداولة (SAR)", 0.0, value=150000.0, step=10000.0, format="%.2f")

        base, zakat = compute_zakat(z_cash, z_rec, z_inv, z_inv2, z_liab)

        st.markdown(f"""
        <div class="zakat-box">
            <div class="zakat-title">⬡ نتيجة حساب الزكاة</div>
            <table style="width:100%;font-family:'Amiri',serif;font-size:0.92rem;">
                <tr><td>النقدية والبنوك</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;">SAR {z_cash:,.2f}</td></tr>
                <tr><td>الذمم المدينة × 90٪</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;">SAR {z_rec*0.9:,.2f}</td></tr>
                <tr><td>المخزون × 85٪</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;">SAR {z_inv*0.85:,.2f}</td></tr>
                <tr><td>الاستثمارات</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;">SAR {z_inv2:,.2f}</td></tr>
                <tr style="border-top:1px solid #C9A84C;"><td>يطرح: الالتزامات</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#C0392B;">(SAR {z_liab:,.2f})</td></tr>
                <tr style="background:rgba(201,168,76,0.08);"><td><strong>الوعاء الزكوي</strong></td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;font-weight:700;">SAR {base:,.2f}</td></tr>
                <tr style="background:rgba(26,107,74,0.08);"><td><strong>الزكاة المستحقة ٢.٥٪</strong></td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A6B4A;font-weight:700;font-size:1.1rem;">SAR {zakat:,.2f}</td></tr>
            </table>
            <div style="margin-top:1rem;font-size:0.8rem;color:#7A6E5A;">
            الزكاة = الوعاء الزكوي × ٢.٥٪ (أو ÷ ٤٠)<br>
            المرجع: قرار وزارة المالية ٢٠٨٢ · هيئة الزكاة والضريبة والجمارك
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Zakat waterfall
        wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative","relative","relative","relative","relative","total"],
            x=["النقدية","ذمم مدينة×90%","مخزون×85%","استثمارات","(التزامات)","الوعاء"],
            y=[z_cash, z_rec*0.9, z_inv*0.85, z_inv2, -z_liab, 0],
            connector=dict(line=dict(color="#C9A84C", width=1, dash="dot")),
            increasing=dict(marker_color="#1A6B4A"),
            decreasing=dict(marker_color="#C0392B"),
            totals=dict(marker_color="#C9A84C"),
        ))
        wf.update_layout(**CHART_LAYOUT,
                          title=dict(text="الوعاء الزكوي | Zakat Base", font=dict(color="#1A6B4A", size=11), x=0),
                          height=250, showlegend=False,
                          yaxis=dict(title="SAR", gridcolor="rgba(201,168,76,0.1)"),
                          xaxis=dict(gridcolor="rgba(201,168,76,0.1)"))
        st.plotly_chart(wf, use_container_width=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">حاسبة ضريبة القيمة المضافة | VAT Calculator</div>', unsafe_allow_html=True)
        vat_mode = st.radio("", ["إضافة الضريبة | Add VAT", "استخراج الضريبة | Extract VAT"], horizontal=True, label_visibility="collapsed")
        vat_amt_in = st.number_input("المبلغ (SAR)", 0.0, value=10000.0, step=100.0, format="%.2f")
        vat_rt = st.selectbox("نسبة الضريبة", ["15٪ — قياسي | Standard", "0٪ — معفي | Zero-rated"], label_visibility="collapsed")
        rate = 0.15 if "15" in vat_rt else 0.0

        if "Add" in vat_mode:
            vat_v = vat_amt_in * rate
            total_v = vat_amt_in + vat_v
            base_v = vat_amt_in
        else:
            total_v = vat_amt_in
            vat_v = vat_amt_in * rate / (1 + rate)
            base_v = vat_amt_in - vat_v

        st.markdown(f"""
        <div class="zakat-box" style="background:linear-gradient(135deg,#F0F7FF,#E8F0FF);border-color:#1A4A7A;border-right-color:#1A4A7A;">
            <div class="zakat-title" style="color:#1A4A7A;">⬡ نتيجة ضريبة القيمة المضافة</div>
            <table style="width:100%;font-family:'Amiri',serif;font-size:0.92rem;">
                <tr><td>المبلغ قبل الضريبة</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A4A7A;">SAR {base_v:,.2f}</td></tr>
                <tr><td>نسبة الضريبة (فاتورة)</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A4A7A;">{rate*100:.0f}%</td></tr>
                <tr><td>مبلغ الضريبة</td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#C0392B;font-weight:700;">SAR {vat_v:,.2f}</td></tr>
                <tr style="background:rgba(26,74,122,0.06);"><td><strong>الإجمالي شامل الضريبة</strong></td><td style="text-align:left;font-family:'IBM Plex Mono',monospace;color:#1A4A7A;font-weight:700;font-size:1.1rem;">SAR {total_v:,.2f}</td></tr>
            </table>
            <div style="margin-top:1rem;font-size:0.8rem;color:#7A6E5A;">
            ⬡ ضريبة القيمة المضافة ١٥٪ ساري منذ يوليو ٢٠٢٠<br>
            ⬡ الفاتورة الإلكترونية (فاتورة) إلزامية لجميع المنشآت<br>
            المرجع: هيئة الزكاة والضريبة والجمارك – ZATCA
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # VAT pie
        if vat_v > 0:
            fig_pie = go.Figure(go.Pie(
                labels=["المبلغ الأساسي", "ضريبة القيمة المضافة"],
                values=[base_v, vat_v],
                marker=dict(colors=["#1A6B4A", "#C9A84C"],
                            line=dict(color="#F5F0E8", width=2)),
                textfont=dict(family="Cormorant Garamond, serif"),
            ))
            fig_pie.update_layout(**CHART_LAYOUT, height=220, showlegend=True,
                                   legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                                   title=dict(text="توزيع ضريبة القيمة المضافة | VAT Split", font=dict(color="#1A6B4A", size=11), x=0))
            st.plotly_chart(fig_pie, use_container_width=True)


# ──────────────── TAB 3: JOURNAL ENTRY BUILDER ───────────────────────
with tab3:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="card"><div class="card-title">منشئ القيود المحاسبية | Journal Entry Builder</div>', unsafe_allow_html=True)
        je_sel = st.selectbox("نوع العملية | Transaction", list(JE_TEMPLATES.keys()), label_visibility="collapsed")
        je_amt = st.number_input("المبلغ (SAR)", 100.0, value=100000.0, step=1000.0, format="%.2f")
        je_date = st.date_input("التاريخ | Date", datetime.today())

        tmpl = JE_TEMPLATES[je_sel](je_amt)
        total_dr = sum(v for t,_,v in tmpl["entries"] if t=="Dr")
        total_cr = sum(v for t,_,v in tmpl["entries"] if t=="Cr")
        balanced = abs(total_dr - total_cr) < 0.01

        rows_html = ""
        for typ, acc, val in tmpl["entries"]:
            indent = "" if typ == "Dr" else "&nbsp;&nbsp;&nbsp;&nbsp;"
            rows_html += f"<tr><td class='{typ.lower()}'>{typ}</td><td>{indent}{acc}</td><td style='text-align:left;font-family:IBM Plex Mono,monospace;' class='{typ.lower()}'>SAR {val:,.2f}</td></tr>"

        st.markdown(f"""
        <div style="background:var(--white);border:1px solid var(--border);border-top:3px solid var(--gold);border-radius:4px;padding:1.2rem;direction:rtl;">
            <div style="font-family:'Amiri',serif;font-size:1.1rem;font-weight:700;color:var(--emerald);margin-bottom:0.5rem;">{je_sel}</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--muted);margin-bottom:1rem;">
                {je_date.strftime('%d/%m/%Y')} &nbsp;|&nbsp; {tmpl['standard']}
            </div>
            <table class="je-table">
                <tr><th>نوع</th><th>الحساب</th><th style="text-align:left;">المبلغ</th></tr>
                {rows_html}
                <tr style="border-top:2px solid var(--gold);background:rgba(201,168,76,0.04);">
                    <td colspan="2" style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:var(--muted);">المجموع | Total</td>
                    <td style="font-family:'IBM Plex Mono',monospace;font-weight:700;text-align:left;color:var(--emerald);">SAR {total_dr:,.2f}</td>
                </tr>
            </table>
            <div style="margin-top:0.7rem;font-size:0.85rem;color:var(--muted);font-family:'Amiri',serif;">البيان: {tmpl['narration']}</div>
            <div style="margin-top:0.5rem;padding:0.45rem 0.8rem;background:{'rgba(26,107,74,0.06)' if balanced else 'rgba(192,57,43,0.06)'};border:1px solid {'var(--emerald)' if balanced else 'var(--red)'};border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:{'var(--emerald)' if balanced else 'var(--red)'};">
                {'✅ متوازن | Balanced — Dr = Cr = SAR ' + f'{total_dr:,.2f}' if balanced else f'❌ غير متوازن — Dr: {total_dr:,.2f} ≠ Cr: {total_cr:,.2f}'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Export JE
        je_export = f"JOURNAL ENTRY — {je_sel}\nDate: {je_date}\nStandard: {tmpl['standard']}\n\n"
        for typ, acc, val in tmpl["entries"]:
            je_export += f"  {typ}: {acc}  SAR {val:,.2f}\n"
        je_export += f"\nNarration: {tmpl['narration']}\nBalanced: {'Yes' if balanced else 'NO — ERROR'}"
        st.download_button("⬇ تصدير القيد | Export JE", je_export.encode("utf-8"),
                           f"JE_{je_date}.txt", "text/plain")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">دليل الحسابات | Chart of Accounts (SOCPA-Aligned)</div>', unsafe_allow_html=True)
        coa_rows = []
        for code, (ar, en) in SAMPLE_ACCOUNTS.items():
            t = "أصول" if code[0]=="1" else "خصوم" if code[0]=="2" else "حقوق" if code[0]=="3" else "إيرادات" if code[0]=="4" else "مصروفات"
            n = "مدين" if code[0] in ("1","5") else "دائن"
            coa_rows.append({"Code": code, "الحساب": ar, "Account": en, "Type": t, "Normal": n})
        df_coa = pd.DataFrame(coa_rows)
        st.dataframe(df_coa, use_container_width=True, hide_index=True, height=480)
        st.markdown("""
        <div style="margin-top:0.7rem;font-family:'Amiri',serif;font-size:0.85rem;direction:rtl;color:#7A6E5A;">
        ⬡ المعادلة المحاسبية: الأصول = الخصوم + حقوق الملكية<br>
        ⬡ مجموع المدين = مجموع الدائن في كل قيد<br>
        ⬡ وفق معايير SOCPA والمعايير الدولية IFRS المعتمدة في المملكة
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ──────────────── TAB 4: FINANCIAL ANALYSIS ──────────────────────────
with tab4:
    st.markdown('<div class="card"><div class="card-title">إدخال البيانات المالية | Financial Data Input (SAR Millions)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**أصول | Assets**")
        fa_ca   = st.number_input("أصول متداولة | Current Assets", 0.0, value=25.0, step=1.0)
        fa_ta   = st.number_input("إجمالي الأصول | Total Assets",  0.0, value=80.0, step=1.0)
    with c2:
        st.markdown("**خصوم وحقوق | Liab & Equity**")
        fa_cl   = st.number_input("خصوم متداولة | Current Liab",   0.0, value=12.0, step=1.0)
        fa_tl   = st.number_input("إجمالي الخصوم | Total Liab",    0.0, value=35.0, step=1.0)
        fa_eq   = st.number_input("حقوق الملكية | Equity",         0.0, value=45.0, step=1.0)
    with c3:
        st.markdown("**نتائج الأعمال | P&L**")
        fa_rev  = st.number_input("الإيرادات | Revenue",            0.0, value=60.0, step=1.0)
        fa_gp   = st.number_input("مجمل الربح | Gross Profit",      0.0, value=18.0, step=1.0)
        fa_ni   = st.number_input("صافي الربح | Net Income",        0.0, value=8.0,  step=1.0)
    st.markdown("</div>", unsafe_allow_html=True)

    cr_ratio = fa_ca / fa_cl if fa_cl else 0
    gpm = fa_gp / fa_rev * 100 if fa_rev else 0
    npm = fa_ni / fa_rev * 100 if fa_rev else 0
    roe = fa_ni / fa_eq * 100  if fa_eq else 0
    roa = fa_ni / fa_ta * 100  if fa_ta else 0
    dr  = fa_tl / fa_ta * 100  if fa_ta else 0

    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(make_gauge(cr_ratio, "Current Ratio | نسبة التداول", 1.5, 3.0), use_container_width=True)
    with g2: st.plotly_chart(make_gauge(gpm, "Gross Margin % | هامش المجمل", 20, 50),        use_container_width=True)
    with g3: st.plotly_chart(make_gauge(roe, "ROE % | العائد على حقوق الملكية", 10, 25),      use_container_width=True)

    st.markdown('<div class="card"><div class="card-title">جدول النسب المالية | Financial Ratios Dashboard</div>', unsafe_allow_html=True)
    ratios = [
        ("نسبة التداول | Current Ratio", f"{cr_ratio:.2f}x", "1.5x – 3.0x", "✅" if 1.5<=cr_ratio<=3.0 else "⚠️", "IAS 1"),
        ("هامش المجمل | Gross Margin",   f"{gpm:.1f}%",     "> 20%",         "✅" if gpm>20 else "⚠️",             "IFRS 15"),
        ("هامش الشبكة | Net Margin",     f"{npm:.1f}%",     "> 5%",          "✅" if npm>5 else "⚠️",              "IFRS 15"),
        ("العائد على حقوق | ROE",        f"{roe:.1f}%",     "> 10%",         "✅" if roe>10 else "⚠️",             "IAS 1"),
        ("العائد على الأصول | ROA",      f"{roa:.1f}%",     "> 5%",          "✅" if roa>5 else "⚠️",              "IAS 1"),
        ("نسبة الدين | Debt Ratio",      f"{dr:.1f}%",      "< 60%",         "✅" if dr<60 else "⚠️",              "IFRS 7"),
    ]
    rows = "".join([
        f"<tr><td style='font-family:Amiri,serif;'>{r[0]}</td>"
        f"<td style='font-family:IBM Plex Mono,monospace;font-weight:600;color:var(--emerald);'>{r[1]}</td>"
        f"<td style='font-family:IBM Plex Mono,monospace;color:var(--muted);font-size:0.75rem;'>{r[2]}</td>"
        f"<td>{r[3]}</td>"
        f"<td style='font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:var(--muted);'>{r[4]}</td></tr>"
        for r in ratios
    ])
    st.markdown(f"""
    <table class="je-table" style="direction:ltr;">
        <tr><th>Ratio / النسبة</th><th>Value</th><th>Benchmark</th><th>Status</th><th>Standard</th></tr>
        {rows}
    </table>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Summary bar chart
    fig_bar = go.Figure(go.Bar(
        x=["Current Assets","Total Assets","Curr. Liab","Total Liab","Equity","Revenue","Net Income"],
        y=[fa_ca, fa_ta, fa_cl, fa_tl, fa_eq, fa_rev, fa_ni],
        marker=dict(color=["#1A6B4A","#2E8B57","#C9A84C","#A88030","#1A4A7A","#C0392B","#2ECC71"],
                    line=dict(color="rgba(245,240,232,0.3)", width=1)),
        text=[f"SAR {v:.1f}M" for v in [fa_ca,fa_ta,fa_cl,fa_tl,fa_eq,fa_rev,fa_ni]],
        textposition="outside", textfont=dict(size=9, color="#7A6E5A"),
    ))
    fig_bar.update_layout(**CHART_LAYOUT,
                           title=dict(text="ملخص البيانات المالية | Financial Summary (SAR Millions)", font=dict(color="#1A6B4A",size=11),x=0),
                           xaxis=dict(gridcolor="rgba(201,168,76,0.1)"),
                           yaxis=dict(title="SAR Millions",gridcolor="rgba(201,168,76,0.1)"),
                           height=280, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:2rem;padding:1.2rem 0;border-top:1px solid rgba(201,168,76,0.2);text-align:center;">
    <div style="font-family:'Amiri',serif;font-size:1rem;color:var(--emerald);margin-bottom:0.3rem;direction:rtl;">
        محاسب الذكاء الاصطناعي للمملكة العربية السعودية
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:2px;color:rgba(201,168,76,0.45);text-transform:uppercase;">
        SOCPA · IFRS · GAZT · Zakat 2.5% · VAT 15% · Vision 2030 · Claude AI · Bilingual
    </div>
</div>
""", unsafe_allow_html=True)
