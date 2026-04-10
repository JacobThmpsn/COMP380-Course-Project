import streamlit as st
from responder import build_report

#Page setup
st.set_page_config(
    page_title="Accessibility Text Difficulty Indicator",
    layout="wide"
)

def score_color(score):
    #Display colours based on difficulty score
    if score < 20:
        return "#2e7d32"   
    if score < 40:
        return "#558b2f"  
    if score < 60:
        return "#f9a825"  
    if score < 80:
        return "#ef6c00"  
    return "#c62828"    


def score_description(score):
    #Quick readability description
    if score < 20:
        return "Easy to read"
    if score < 40:
        return "Mostly accessible"
    if score < 60:
        return "Moderate difficulty"
    if score < 80:
        return "Challenging to read"
    return "High reading difficulty"


#Webpage Styling

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }

    .score-box {
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    .score-number {
        font-size: 2.5rem;
        line-height: 1.2;
    }

    .score-label {
        font-size: 1.1rem;
        margin-top: 0.4rem;
    }

    .section-card {
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: #fafafa;
    }

    .metric-label {
        font-weight: 600;
    }

    .small-note {
        color: #666666;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

#Header

st.markdown('<div class="main-title">Accessibility Text Difficulty Indicator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Paste text from an article, post, or document to estimate how difficult it will be to read.</div>',
    unsafe_allow_html=True
)

#Text input area

st.subheader("Text Input")

text = st.text_area(
    "Paste text to analyze",
    height=220,
    placeholder="Paste the text you want to evaluate here..."
)

analyze = st.button("Analyze Text", use_container_width=True)

#Results return

if analyze:
    if not text.strip():
        st.error("Please paste text first.")
    else:
        report = build_report(text)
        score = report["score"]
        band = report["band"]
        color = score_color(score)

        left_col, right_col = st.columns([1, 2])

        #Left column, score summary
        with left_col:
            st.markdown(
                f"""
                <div class="score-box" style="background-color: {color};">
                    <div class="score-number">{score}</div>
                    <div class="score-label">{band}</div>
                    <div class="score-label">{score_description(score)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Reading Expectations")
            for item in report["reading_expectations"]:
                st.write(f"• {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        #Detailed results
        with right_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Why This Score Was Given")
            for reason in report["reasons"]:
                st.write(f"• {reason}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Text Metrics")

            m = report["metrics"]

            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:
                st.write(f"**Word count:** {m['word_count']}")
                st.write(f"**Sentence count:** {m['sentence_count']}")
                st.write(f"**Average sentence length:** {m['avg_sentence_len']}")
                st.write(f"**Average word length:** {m['avg_word_len']}")

            with metric_col2:
                st.write(f"**Syllables per word:** {m['syllables_per_word']}")
                st.write(f"**Long word rate:** {m['long_word_rate']}")
                st.write(f"**Uncommon word rate:** {m['uncommon_word_rate']}")
                st.write(f"**Rare word rate:** {m['rare_word_rate']}")

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Complex Word Definitions")
            if report["complex_words"]:
                for item in report["complex_words"]:
                    st.write(f"**{item['word']}**: {item['definition']}")
            else:
                st.write("No complex words were flagged.")
            st.markdown("</div>", unsafe_allow_html=True)

#Description

st.markdown("---")
st.markdown(
    '<div class="small-note">This tool estimates reading difficulty using sentence length, syllables, vocabulary frequency, and AI-generated explanation.</div>',
    unsafe_allow_html=True
)