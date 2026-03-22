
import streamlit as st
import requests
import re
import io

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

st.set_page_config(
    page_title="Study Buddy",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CSS — Complete Dark Green Redesign

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:           #050c06;
    --bg-1:         #091210;
    --bg-2:         #0c1a0e;
    --bg-3:         #102214;
    --bg-4:         #142a18;
    --b0:           #1c3822;
    --b1:           #245230;
    --b2:           #2d6e3c;
    --b3:           #3a8c4c;
    --g1:           #4ade80;
    --g2:           #86efac;
    --g3:           #bbf7d0;
    --neon:         #39ff6e;
    --teal:         #2dd4bf;
    --lime:         #a3e635;
    --t0:           #d4fce4;
    --t1:           #86c896;
    --t2:           #4d7a58;
    --t3:           #2a4a30;
    --red:          #f87171;
    --yellow:       #fbbf24;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--t0);
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 4rem; max-width: 1100px; }

/* Subtle noise grain over everything */
.stApp::after {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 9999; opacity: 0.4;
}

/* ── HERO ────────────────────────────────────────── */
.hero {
    position: relative;
    padding: 3.5rem 3rem 2.5rem;
    margin-bottom: 0;
    overflow: hidden;
    border-bottom: 1px solid var(--b0);
    background: linear-gradient(160deg, #050c06 0%, #091a0c 55%, #050c06 100%);
}
.hero-glow-a {
    position:absolute; top:-100px; right:-60px;
    width:400px; height:400px; border-radius:50%;
    background: radial-gradient(circle, rgba(74,222,128,0.09) 0%, transparent 60%);
    pointer-events:none;
}
.hero-glow-b {
    position:absolute; bottom:-80px; left:80px;
    width:280px; height:280px; border-radius:50%;
    background: radial-gradient(circle, rgba(45,212,191,0.06) 0%, transparent 60%);
    pointer-events:none;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.25em;
    color: var(--neon); opacity: 0.75;
    text-transform: uppercase; margin-bottom: 1rem;
}
.hero-h1 {
    font-size: 3.4rem; font-weight: 800;
    letter-spacing: -0.04em; line-height: 1;
    color: var(--t0); margin-bottom: 0.7rem;
}
.hero-h1 em { font-style:normal; color: var(--g1);
    text-shadow: 0 0 40px rgba(74,222,128,0.45); }
.hero-sub {
    font-size: 1rem; font-weight: 300; color: var(--t2);
    max-width: 560px; line-height: 1.7;
}
.hero-chips {
    display: flex; gap: 8px; margin-top: 1.4rem; flex-wrap: wrap;
}
.chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.12em;
    padding: 4px 12px; border-radius: 999px;
    text-transform: uppercase;
    border: 1px solid var(--b1); color: var(--t2);
    background: rgba(74,222,128,0.04);
}
.chip-active {
    border-color: var(--g1); color: var(--g1);
    background: rgba(74,222,128,0.08);
    box-shadow: 0 0 12px rgba(74,222,128,0.12);
}

/* ── INPUT AREA ──────────────────────────────────── */
.input-card {
    background: var(--bg-2);
    border: 1px solid var(--b0);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin: 1.6rem 0 1rem 0;
    transition: border-color 0.2s;
}
.input-card:hover { border-color: var(--b1); }
.input-label {
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--t2); margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 8px;
}
.input-label span {
    display:inline-block; width:4px; height:4px;
    background: var(--neon); border-radius: 50%;
    box-shadow: 0 0 6px var(--neon);
}

/* PDF drop zone */
.pdf-zone {
    border: 1.5px dashed var(--b1);
    border-radius: 14px;
    padding: 2rem 1.5rem;
    text-align: center;
    background: rgba(74,222,128,0.02);
    transition: all 0.2s;
    cursor: pointer;
}
.pdf-zone:hover {
    border-color: var(--g1);
    background: rgba(74,222,128,0.05);
}
.pdf-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
.pdf-label { font-size: 0.85rem; color: var(--t2); }
.pdf-sub { font-size: 0.72rem; color: var(--t3); margin-top: 0.3rem;
    font-family: 'Space Mono', monospace; }

/* Tab row */
.tab-row {
    display: flex; gap: 6px; margin-bottom: 1.2rem;
}
.tab-btn {
    font-size: 0.78rem; font-weight: 600;
    padding: 6px 16px; border-radius: 8px; cursor: pointer;
    border: 1px solid var(--b0); color: var(--t2);
    background: var(--bg-3); transition: all 0.15s;
}
.tab-btn-active {
    background: rgba(74,222,128,0.1);
    border-color: var(--g1); color: var(--g1);
}

/* ── SECTION HEADERS ─────────────────────────────── */
.sec-row {
    display: flex; align-items: center; gap: 14px;
    margin: 2.2rem 0 1.2rem;
}
.sec-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.18em;
    color: var(--neon); background: rgba(57,255,110,0.07);
    border: 1px solid rgba(57,255,110,0.18);
    border-radius: 6px; padding: 3px 10px;
}
.sec-title {
    font-size: 1.2rem; font-weight: 700;
    letter-spacing: -0.02em; color: var(--t0);
}
.sec-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--b0), transparent);
}

/* ── WEAK TOPICS BOX ─────────────────────────────── */
.topics-box {
    background: linear-gradient(135deg, var(--bg-3), var(--bg-2));
    border: 1px solid var(--b0);
    border-left: 3px solid var(--g1);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
}
.topics-box-head {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--g1);
    margin-bottom: 0.9rem; display: flex; align-items: center; gap: 8px;
}
.topics-box-head::before {
    content: ''; display:inline-block;
    width: 6px; height: 6px; border-radius: 2px;
    background: var(--g1);
    box-shadow: 0 0 8px var(--g1);
}
.topics-body {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem; line-height: 1.9;
    color: var(--t1); white-space: pre-wrap;
}

/* ── QUESTION CARD ───────────────────────────────── */
.q-wrap {
    background: var(--bg-2);
    border: 1px solid var(--b0);
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.2rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.q-wrap:hover {
    border-color: var(--b1);
    box-shadow: 0 4px 30px rgba(74,222,128,0.05);
}
.q-wrap::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, var(--neon), var(--teal), transparent 70%);
}
.q-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.2em;
    color: var(--neon); opacity: 0.6;
    text-transform: uppercase; margin-bottom: 0.7rem;
}
.q-body {
    font-size: 1.02rem; font-weight: 600;
    color: var(--t0); line-height: 1.65;
    margin-bottom: 1.2rem;
}
.q-progress {
    display: flex; gap: 4px; margin-bottom: 1rem;
}
.q-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--b0);
}
.q-dot-done { background: var(--g1); box-shadow: 0 0 6px var(--g1); }

/* option buttons */
.stButton > button {
    background: var(--bg-3) !important;
    color: var(--t1) !important;
    border: 1px solid var(--b0) !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 1.1rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.005em !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    border-color: var(--b2) !important;
    color: var(--g2) !important;
    background: rgba(74,222,128,0.06) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(74,222,128,0.07) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

.sel-pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem; color: var(--g1);
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 8px; padding: 4px 12px;
    margin: 0.4rem 0 1rem;
}
.sel-pill::before { content: '▶'; font-size: 0.55rem; }
.no-sel {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem; color: var(--t3);
    margin: 0.4rem 0 1rem 2px;
}

/* ── SUBMIT BAR ──────────────────────────────────── */
.submit-bar {
    background: linear-gradient(135deg, var(--bg-3), var(--bg-4));
    border: 1px solid var(--b0);
    border-radius: 16px;
    padding: 1.2rem 1.6rem;
    display: flex; align-items: center;
    justify-content: space-between; gap: 1rem;
    margin: 1.2rem 0;
}
.submit-progress {
    font-size: 0.82rem; color: var(--t2);
}
.submit-progress b { color: var(--g1); }

/* ── SCORE BOX ───────────────────────────────────── */
.score-wrap {
    position: relative;
    background: linear-gradient(160deg, var(--bg-3) 0%, var(--bg-2) 100%);
    border: 1px solid var(--b1);
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1rem 0 1.5rem;
    overflow: hidden;
}
.score-wrap::before {
    content: '';
    position: absolute; top: -60px; left: 50%; transform: translateX(-50%);
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(74,222,128,0.10) 0%, transparent 65%);
    pointer-events: none;
}
.score-big {
    font-size: 5rem; font-weight: 800;
    letter-spacing: -0.06em; line-height: 1;
    color: var(--g1);
    text-shadow: 0 0 60px rgba(74,222,128,0.5);
}
.score-denom {
    font-size: 2rem; color: var(--t3); font-weight: 300;
}
.score-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem; letter-spacing: 0.1em;
    color: var(--t2); margin-top: 0.6rem;
}
.score-msg {
    font-size: 1.1rem; font-weight: 600;
    color: var(--t0); margin-top: 0.4rem;
}
/* progress bar */
.bar-track {
    width: 200px; height: 4px;
    background: var(--b0); border-radius: 999px;
    margin: 1rem auto 0; overflow: hidden;
}
.bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--g1), var(--teal));
    box-shadow: 0 0 8px rgba(74,222,128,0.5);
    transition: width 0.8s ease;
}

/* ── RESULT CARDS ────────────────────────────────── */
.res-card {
    background: var(--bg-2);
    border: 1px solid var(--b0);
    border-radius: 16px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.res-correct { border-left: 3px solid var(--g1); }
.res-wrong   { border-left: 3px solid var(--red); }
.res-card:hover { border-color: var(--b1); }
.res-head {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-bottom: 0.7rem;
}
.res-status-ok  { font-size:0.78rem; font-weight:700; color:var(--g1); }
.res-status-bad { font-size:0.78rem; font-weight:700; color:var(--red); }
.res-qnum {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem; color: var(--t3); letter-spacing: 0.1em;
}
.res-q { font-size:0.9rem; font-weight:500; color:var(--t1); margin-bottom:0.7rem; line-height:1.5; }
.res-answers {
    display: grid; grid-template-columns: 1fr 1fr; gap: 6px;
}
.res-ans-box {
    background: var(--bg-3); border-radius: 10px;
    padding: 0.5rem 0.8rem;
    font-family: 'Space Mono', monospace; font-size: 0.72rem;
}
.res-ans-label { color: var(--t3); font-size: 0.6rem; letter-spacing: 0.1em; margin-bottom: 3px; }
.res-ans-val-ok  { color: var(--g2); }
.res-ans-val-bad { color: var(--red); }
.res-ans-val-correct { color: var(--g1); }

/* ── TIPS BOX ────────────────────────────────────── */
.tips-box {
    background: linear-gradient(135deg, var(--bg-3), var(--bg-2));
    border: 1px solid var(--b0);
    border-left: 3px solid var(--teal);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
}
.tips-head {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--teal);
    margin-bottom: 0.9rem; display: flex; align-items: center; gap: 8px;
}
.tips-head::before {
    content: ''; display:inline-block;
    width:6px; height:6px; border-radius:2px;
    background: var(--teal); box-shadow: 0 0 8px var(--teal);
}
.tips-body {
    font-size: 0.9rem; line-height: 1.85;
    color: var(--t1); white-space: pre-wrap;
}

/* ── STREAMLIT OVERRIDES ─────────────────────────── */
.stTextArea textarea {
    background: var(--bg-3) !important;
    border: 1px solid var(--b0) !important;
    border-radius: 14px !important;
    color: var(--t0) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.8 !important;
    caret-color: var(--neon) !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--b2) !important;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.08) !important;
}
.stTextArea label { display: none !important; }

/* file uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-3) !important;
    border: 1.5px dashed var(--b1) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--g1) !important;
    background: rgba(74,222,128,0.03) !important;
}
[data-testid="stFileUploader"] * { color: var(--t2) !important; }
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
}

/* alerts */
.stAlert {
    background: rgba(74,222,128,0.04) !important;
    border: 1px solid var(--b1) !important;
    border-radius: 12px !important;
    color: var(--t1) !important;
}

/* spinner */
.stSpinner > div { border-top-color: var(--g1) !important; }

/* sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--b0) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
}

/* divider */
.gd {
    height: 1px; margin: 2rem 0;
    background: linear-gradient(90deg, transparent, var(--b1) 30%, var(--b1) 70%, transparent);
    opacity: 0.5;
}

/* success/warning overrides */
div[data-testid="stNotification"] {
    background: var(--bg-3) !important;
    border-color: var(--b1) !important;
}
</style>
""", unsafe_allow_html=True)

BACKEND = "http://localhost:8000"

# ── Session state ─────────────────────────────────────────────
defaults = {
    "weak_topics": None,
    "quiz_raw":    None,
    "questions":   [],
    "tips":        None,
    "user_answers":{},
    "submitted":   False,
    "feedback":    None,
    "score":       None,
    "last_notes":  "",
    "input_mode":  "text",   # "text" or "pdf"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helpers ───────────────────────────────────────────────────
def extract_pdf_text(uploaded_file) -> str:
    if not PDF_AVAILABLE:
        return ""
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    return "\n".join(p.extract_text() or "" for p in reader.pages)

def parse_quiz(text: str):
    questions = []
    blocks = re.split(r'(?:^|\n)\s*(?:Question\s*\d+[:\.]?|\d+[\.\)])\s*',
                      text, flags=re.IGNORECASE)
    for block in [b.strip() for b in blocks if b.strip()]:
        lines   = [l.strip() for l in block.split('\n') if l.strip()]
        options = {}; q_lines = []; answer = None
        for line in lines:
            opt = re.match(r'^([A-D])[).\:]\s*(.+)', line, re.IGNORECASE)
            ans = re.match(r'(?:correct\s*answer|answer)[:\s]+([A-D])', line, re.IGNORECASE)
            if ans:    answer = ans.group(1).upper()
            elif opt:  options[opt.group(1).upper()] = opt.group(2).strip()
            elif not re.search(r'correct\s*answer|answer\s*key', line, re.IGNORECASE):
                q_lines.append(line)
        q = re.sub(r'^[\W_]+', '', ' '.join(q_lines)).strip()
        if q and len(options) >= 2:
            questions.append({"question": q, "options": options, "answer": answer})
    return questions

def grade(questions, user_answers):
    results = []; score = 0
    for i, q in enumerate(questions):
        ua = user_answers.get(i); ca = q.get("answer")
        ok = (ua == ca) if ca else None
        if ok: score += 1
        results.append({"question": q["question"], "user_answer": ua,
                         "correct_answer": ca, "is_correct": ok, "options": q["options"]})
    return results, score

def reset_downstream():
    for k in ["quiz_raw","questions","user_answers","submitted","feedback","tips","score"]:
        st.session_state[k] = [] if k=="questions" else ({} if k=="user_answers" else (False if k=="submitted" else None))



# SIDEBAR — Animated Pipeline

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.6rem;
    letter-spacing:0.22em;color:#2d6e3c;text-transform:uppercase;
    margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid #1c3822;">
    ◈ Smart Study Buddy
    </div>""", unsafe_allow_html=True)

    # Connection test
    if st.button("⬡  Test Backend", use_container_width=True):
        try:
            r = requests.get(f"{BACKEND}/", timeout=5)
            st.success("✅ Backend online!") if r.status_code == 200 else st.error("❌ Error")
        except:
            st.error("❌ Offline — run:\nuvicorn main:app --reload")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Animated pipeline ─────────────────────────────────────
    s  = st.session_state
    d1 = bool(s.get("last_notes"))
    d2 = bool(s.get("weak_topics"))
    d3 = bool(s.get("questions"))
    d4 = bool(s.get("submitted"))
    d5 = bool(s.get("feedback"))
    d6 = bool(s.get("tips"))

    pipe_steps = [
        ("📄", "Input Notes / PDF",  "source",       d1),
        ("🔍", "Analyze Weaknesses", "POST /analyze", d2),
        ("❓", "Generate Quiz",      "POST /quiz",    d3),
        ("👆", "Answer Questions",   "A / B / C / D", d4),
        ("🏆", "Score & Feedback",   "local grading", d5),
        ("💡", "Study Tips",         "POST /tips",    d6),
    ]

    pipe_html = """
<style>
@keyframes flowDash {
  to { stroke-dashoffset: -16; }
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.4); }
  50%      { box-shadow: 0 0 0 5px rgba(74,222,128,0); }
}
.pipe-node {
    display:flex; align-items:center; gap:10px;
    padding:0.6rem 0.75rem; border-radius:12px;
    border:1px solid; margin:0; cursor:default;
    transition: all 0.3s ease;
}
.pn-done {
    background: linear-gradient(135deg,rgba(74,222,128,0.08),rgba(74,222,128,0.03));
    border-color: #2d6e3c;
}
.pn-idle {
    background: rgba(74,222,128,0.015);
    border-color: #1c3822;
}
.pn-icon {
    width:30px; height:30px; border-radius:8px;
    display:flex; align-items:center; justify-content:center;
    font-size:0.9rem; flex-shrink:0;
}
.pi-done { background:rgba(74,222,128,0.12); border:1px solid rgba(74,222,128,0.25);
    animation: pulseGlow 2.5s ease-in-out infinite; }
.pi-idle { background:rgba(74,222,128,0.02); border:1px solid #1c3822; }
.pn-info  { flex:1; min-width:0; }
.pn-label-done { font-family:'Plus Jakarta Sans',sans-serif; font-weight:600;
    font-size:0.77rem; color:#d4fce4; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pn-label-idle { font-family:'Plus Jakarta Sans',sans-serif; font-weight:400;
    font-size:0.77rem; color:#2a4a30; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pn-ep-done { font-family:'Space Mono',monospace; font-size:0.56rem;
    color:#3a8c4c; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pn-ep-idle { font-family:'Space Mono',monospace; font-size:0.56rem;
    color:#1c3822; margin-top:2px; }
.pn-tick-done { font-size:0.65rem; color:#4ade80; font-weight:800; flex-shrink:0; }
.pn-tick-idle { font-size:0.65rem; color:#1c3822; flex-shrink:0; }
.pipe-connector {
    display:flex; align-items:center; gap:6px;
    padding: 0 0 0 14px; height:22px;
}
.pc-line-done {
    width:2px; height:22px; flex-shrink:0;
    background: repeating-linear-gradient(
        to bottom, #2d6e3c 0,#2d6e3c 4px,transparent 4px,transparent 8px);
    background-size: 2px 8px;
    animation: flowDash 0.6s linear infinite;
}
.pc-line-idle {
    width:2px; height:22px; flex-shrink:0;
    background: repeating-linear-gradient(
        to bottom,#1c3822 0,#1c3822 3px,transparent 3px,transparent 7px);
}
.pc-text-done { font-family:'Space Mono',monospace; font-size:0.55rem; color:#245230; }
.pc-text-idle { font-family:'Space Mono',monospace; font-size:0.55rem; color:#1c3822; }
</style>
<div style="margin-bottom:0.5rem;">
<div style="font-family:'Space Mono',monospace;font-size:0.58rem;
letter-spacing:0.2em;color:#245230;text-transform:uppercase;margin-bottom:1rem;">
◈ LCEL Pipeline
</div>
"""
    connectors = ["→ /analyze","→ /quiz","→ interact","→ grade","→ /tips"]
    for idx, (icon, label, ep, done) in enumerate(pipe_steps):
        nc = "pn-done" if done else "pn-idle"
        ic = "pi-done" if done else "pi-idle"
        lc = "pn-label-done" if done else "pn-label-idle"
        ec = "pn-ep-done"    if done else "pn-ep-idle"
        tc = "pn-tick-done"  if done else "pn-tick-idle"
        tk = "✓" if done else "·"
        pipe_html += f"""
<div class="pipe-node {nc}">
  <div class="pn-icon {ic}">{icon}</div>
  <div class="pn-info">
    <div class="{lc}">{label}</div>
    <div class="{ec}">{ep}</div>
  </div>
  <span class="{tc}">{tk}</span>
</div>"""
        if idx < len(pipe_steps)-1:
            lc2 = "pc-line-done" if done else "pc-line-idle"
            tc2 = "pc-text-done" if done else "pc-text-idle"
            ct  = connectors[idx]
            pipe_html += f"""
<div class="pipe-connector">
  <div class="{lc2}"></div>
  <span class="{tc2}">{ct}</span>
</div>"""
    pipe_html += "</div>"
    st.markdown(pipe_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Reset Session", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

    st.markdown("""
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #1c3822;
    font-family:'Space Mono',monospace;font-size:0.56rem;color:#1c3822;
    letter-spacing:0.08em;line-height:2.2;text-align:center;">
    LCEL · GEMINI 2.5 FLASH<br>FASTAPI · STREAMLIT
    </div>""", unsafe_allow_html=True)



st.markdown("""
<div class="hero">
  <div class="hero-glow-a"></div>
  <div class="hero-glow-b"></div>
  <div class="hero-eyebrow">// AI-Powered Learning Environment v1.0</div>
  <div class="hero-h1">Smart <em>Study</em><br>Buddy 🌿</div>
  <div class="hero-sub">Upload your notes or a PDF — get a personalized quiz,
  instant feedback, and study tips powered by Gemini 2.5 Flash.</div>
  <div class="hero-chips">
    <span class="chip chip-active">LCEL Chains</span>
    <span class="chip chip-active">Gemini 2.5 Flash</span>
    <span class="chip">FastAPI</span>
    <span class="chip">PDF Support</span>
    <span class="chip">Interactive Quiz</span>
  </div>
</div>
""", unsafe_allow_html=True)



st.markdown("""
<div class="sec-row">
  <span class="sec-tag">STEP 01</span>
  <span class="sec-title">Add Your Study Material</span>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

# Mode toggle
mode_col1, mode_col2, _ = st.columns([1, 1, 4])
with mode_col1:
    if st.button("📝  Text Notes",
                 type="primary" if st.session_state.input_mode == "text" else "secondary",
                 use_container_width=True):
        st.session_state.input_mode = "text"
        st.rerun()
with mode_col2:
    if st.button("📄  Upload PDF",
                 type="primary" if st.session_state.input_mode == "pdf" else "secondary",
                 use_container_width=True):
        st.session_state.input_mode = "pdf"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

notes_content = ""

if st.session_state.input_mode == "text":
    notes_content = st.text_area(
        "notes_text",
        height=220,
        value=st.session_state.last_notes,
        placeholder="// paste your study notes here...\n//\n// e.g. Photosynthesis is the process by which plants\n// make food using sunlight and chlorophyll...",
        label_visibility="collapsed"
    )
else:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.7rem;
    color:#4d7a58;margin-bottom:0.6rem;letter-spacing:0.05em;">
    Drop a PDF — text will be extracted automatically
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if uploaded:
        if PDF_AVAILABLE:
            with st.spinner("Extracting text from PDF..."):
                notes_content = extract_pdf_text(uploaded)
            if notes_content.strip():
                st.success(f"✅ Extracted {len(notes_content.split())} words from **{uploaded.name}**")
                with st.expander("👁  Preview extracted text"):
                    st.text(notes_content[:1200] + ("..." if len(notes_content) > 1200 else ""))
            else:
                st.error("❌ Could not extract text — the PDF may be scanned/image-based.")
        else:
            st.error("❌ PyPDF2 not installed. Run: `pip install PyPDF2`")

st.markdown("<br>", unsafe_allow_html=True)

btn_col, _ = st.columns([1.5, 4])
with btn_col:
    analyze_clicked = st.button("🔍  Analyze Notes", use_container_width=True, type="primary")

if analyze_clicked:
    final_notes = notes_content.strip() if notes_content else st.session_state.last_notes.strip()
    if not final_notes:
        st.warning("⚠  Please add some notes or upload a PDF first!")
    else:
        with st.spinner("Gemini is scanning your notes for weak spots..."):
            try:
                r = requests.post(f"{BACKEND}/analyze", json={"notes": final_notes}, timeout=60)
                st.session_state.weak_topics = r.json()["weak_topics"]
                st.session_state.last_notes  = final_notes
                reset_downstream()
                st.rerun()
            except Exception as e:
                st.error(f"Backend error: {e}")

if st.session_state.weak_topics:
    st.markdown(f"""
<div class="topics-box">
  <div class="topics-box-head">Weak Topics Detected</div>
  <div class="topics-body">{st.session_state.weak_topics}</div>
</div>""", unsafe_allow_html=True)



if st.session_state.weak_topics:
    st.markdown('<div class="gd"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-row">
  <span class="sec-tag">STEP 02</span>
  <span class="sec-title">Generate Your Quiz</span>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

    if not st.session_state.quiz_raw:
        c1, _ = st.columns([1.5, 4])
        with c1:
            if st.button("🎲  Generate Quiz", use_container_width=True, type="primary"):
                with st.spinner("Crafting personalized questions..."):
                    try:
                        r = requests.post(
                            f"{BACKEND}/quiz",
                            json={"notes": st.session_state.last_notes},
                            timeout=90
                        )
                        raw = r.json().get("quiz", "")
                        st.session_state.quiz_raw  = raw
                        st.session_state.questions = parse_quiz(raw)
                        reset_downstream()
                        st.session_state.quiz_raw  = raw   # restore after reset
                        st.session_state.questions = parse_quiz(raw)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Backend error: {e}")
    else:
        st.markdown("""<div style="font-family:'Space Mono',monospace;
        font-size:0.7rem;color:#3a8c4c;margin-bottom:0.5rem;">
        ✓ Quiz generated — answer below</div>""", unsafe_allow_html=True)



if st.session_state.questions and not st.session_state.submitted:
    st.markdown('<div class="gd"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-row">
  <span class="sec-tag">STEP 03</span>
  <span class="sec-title">Answer the Questions</span>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

    total_q   = len(st.session_state.questions)
    answered  = len(st.session_state.user_answers)

    # progress dots
    dots_html = '<div class="q-progress">'
    for i in range(total_q):
        cls = "q-dot-done" if i in st.session_state.user_answers else "q-dot"
        dots_html += f'<div class="q-dot {cls}"></div>'
    dots_html += f'<span style="font-family:Space Mono,monospace;font-size:0.62rem;color:#4d7a58;margin-left:8px;">{answered}/{total_q} answered</span>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

    for i, q in enumerate(st.session_state.questions):
        selected = st.session_state.user_answers.get(i)

        st.markdown(f"""
<div class="q-wrap">
  <div class="q-num">Question {i+1} of {total_q}</div>
  <div class="q-body">{q['question']}</div>
</div>""", unsafe_allow_html=True)

        items = list(q["options"].items())
        rows  = [items[j:j+2] for j in range(0, len(items), 2)]
        for row in rows:
            cols = st.columns(len(row))
            for col, (letter, text) in zip(cols, row):
                with col:
                    tick  = "✅  " if selected == letter else f"{letter})  "
                    label = f"{tick}{text}"
                    if st.button(label, key=f"opt_{i}_{letter}"):
                        st.session_state.user_answers[i] = letter
                        st.rerun()

        if selected:
            st.markdown(
                f'<span class="sel-pill">'
                f'Selected: <b>&nbsp;{selected}</b>&nbsp;—&nbsp;'
                f'{q["options"].get(selected,"")}</span>',
                unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-sel">○  No answer selected yet</div>', unsafe_allow_html=True)

    # Submit bar
    if answered < total_q:
        st.markdown(f"""
<div class="submit-bar">
  <div class="submit-progress">
    Answer <b>{total_q - answered}</b> more question(s) to unlock submit
  </div>
</div>""", unsafe_allow_html=True)
    else:
        c1, _ = st.columns([1.5, 4])
        with c1:
            if st.button("📤  Submit & See Score", use_container_width=True, type="primary"):
                results, score = grade(st.session_state.questions, st.session_state.user_answers)
                st.session_state.feedback  = results
                st.session_state.score     = score
                st.session_state.submitted = True
                st.rerun()



if st.session_state.submitted and st.session_state.feedback:
    st.markdown('<div class="gd"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-row">
  <span class="sec-tag">STEP 04</span>
  <span class="sec-title">Your Results</span>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

    total = len(st.session_state.questions)
    score = st.session_state.score
    pct   = int((score / total) * 100) if total else 0
    msg   = "Perfect! 🌟" if score==total else "Great effort! 💪" if pct>=60 else "Keep going! 📖"

    st.markdown(f"""
<div class="score-wrap">
  <div class="score-big">{score}<span class="score-denom">/{total}</span></div>
  <div class="score-pct">{pct}%  CORRECT</div>
  <div class="score-msg">{msg}</div>
  <div class="bar-track"><div class="bar-fill" style="width:{pct}%;"></div></div>
</div>""", unsafe_allow_html=True)

    for i, res in enumerate(st.session_state.feedback):
        ok   = res["is_correct"]
        ua   = res["user_answer"]  or "—"
        ca   = res["correct_answer"] or "N/A"
        opts = res["options"]
        u_t  = f'{ua})  {opts.get(ua,"")}' if ua != "—" else "No answer"
        c_t  = f'{ca})  {opts.get(ca,"")}' if ca != "N/A" else "N/A"
        u_vc = "res-ans-val-ok" if ok else "res-ans-val-bad"
        st.markdown(f"""
<div class="res-card {'res-correct' if ok else 'res-wrong'}">
  <div class="res-head">
    <span class="{'res-status-ok' if ok else 'res-status-bad'}">
      {'✅  Correct' if ok else '❌  Incorrect'}
    </span>
    <span class="res-qnum">Q {i+1} / {total}</span>
  </div>
  <div class="res-q">{res['question']}</div>
  <div class="res-answers">
    <div class="res-ans-box">
      <div class="res-ans-label">YOUR ANSWER</div>
      <div class="{u_vc}">{u_t}</div>
    </div>
    <div class="res-ans-box">
      <div class="res-ans-label">CORRECT ANSWER</div>
      <div class="res-ans-val-correct">{c_t}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, _ = st.columns([1.5, 4])
    with c1:
        if st.button("🔁  Retake Quiz", use_container_width=True):
            st.session_state.user_answers = {}
            st.session_state.submitted    = False
            st.session_state.feedback     = None
            st.session_state.score        = None
            st.rerun()



if st.session_state.weak_topics:
    st.markdown('<div class="gd"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-row">
  <span class="sec-tag">STEP 05</span>
  <span class="sec-title">Get Study Tips</span>
  <div class="sec-line"></div>
</div>""", unsafe_allow_html=True)

    c1, _ = st.columns([1.5, 4])
    with c1:
        if st.button("💡  Generate Tips", use_container_width=True):
            with st.spinner("Crafting your personalised tips..."):
                try:
                    r = requests.post(f"{BACKEND}/tips",
                                      json={"notes": st.session_state.last_notes}, timeout=90)
                    st.session_state.tips = r.json().get("tips")
                except Exception as e:
                    st.error(f"Backend error: {e}")

    if st.session_state.tips:
        st.markdown(f"""
<div class="tips-box">
  <div class="tips-head">Personalised Study Tips</div>
  <div class="tips-body">{st.session_state.tips}</div>
</div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding:1.5rem 0;
border-top:1px solid #1c3822;">
<span style="font-family:'Space Mono',monospace;font-size:0.6rem;
color:#1c3822;letter-spacing:0.12em;">
STUDY BUDDY v2.0 &nbsp;·&nbsp; LCEL + GEMINI 2.5 FLASH + FASTAPI + STREAMLIT
</span>
</div>""", unsafe_allow_html=True)