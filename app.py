
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
This Streamlit application, the ARIA CoRIx Tree Explorer, provides an interactive environment for users to visualize and understand the Contextual Robustness Index (CoRIx) measurement trees. It aims to demystify the hierarchical structure and aggregation logic of CoRIx scores, which are crucial for assessing the validity risk of AI applications as detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].
""")
st.subheader("Learning Goals")
st.markdown("""
Upon using this application, users will be able to:
-   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
-   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
-   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
-   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.
""")

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Data Overview", "CoRIx Tree Explorer", "Interpretation and Conclusion"])

if page == "Data Overview":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "CoRIx Tree Explorer":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Interpretation and Conclusion":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
