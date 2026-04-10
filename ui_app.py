import streamlit as st
from responder import build_report

st.set_page_config(page_title="Text Difficulty Indicator")

st.title("Accessibility Text Difficulty Indicator")

text = st.text_area(
    "Paste text to evaluate",
    height=200
)

run = st.button("Analyze text")

if run:

    if not text.strip():
        st.error("Please paste text first.")
    else:

        report = build_report(text)

        st.subheader("Difficulty Score")
        st.metric("Score", str(report["score"]), report["band"])

        st.subheader("Why this score")

        for r in report["reasons"]:
            st.write("- " + r)

        st.subheader("Reading expectations")

        for e in report["reading_expectations"]:
            st.write("- " + e)

        st.subheader("Metrics")

        m = report["metrics"]

        st.write("Word count:", m["word_count"])
        st.write("Sentence count:", m["sentence_count"])
        st.write("Average sentence length:", m["avg_sentence_len"])
        st.write("Average word length:", m["avg_word_len"])
        st.write("Syllables per word:", m["syllables_per_word"])
        st.write("Long word rate:", m["long_word_rate"])
        st.write("Uncommon word rate:", m["uncommon_word_rate"])

        st.subheader("Complex word definitions")

        if report["complex_words"]:
            for item in report["complex_words"]:
                st.write(item["word"] + " : " + item["definition"])
        else:
            st.write("None detected.")