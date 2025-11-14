
import streamlit as st

def run_page3():
    st.subheader("Section 10: Displaying the Interactive CoRIx Tree for Application A / Pathfinder")
    st.markdown("""
    Let's begin by examining "Application A / Pathfinder". The report indicates an overall CoRIx score of $2.88$, suggesting lower validity risks for this combination. We will generate and interpret the interactive tree visualization for this initial selection. This demonstration highlights how the tool immediately surfaces AI validity risk insights.

    **Interpretation:** The visualization for "Application A / Pathfinder" shows an overall CoRIx score of $2.88$. This relatively low score suggests a lower observed risk to validity for this application and scenario combination. Tracing down to Level 3, Red Teaming (score of $2.88$) contributes the most to the overall risk compared to Model Testing ($0.72$) and Field Testing ($2.36$). Further investigation at Level 4 reveals that Annotator Labels (score of $3.52$) identified higher risks during Red Teaming than User Perceptions (score of $2.24$). Delving into Level 5 reveals specific constructs like `RT DD 4` (Red Teaming Dialogue Dynamics 4, unnatural dialogue) with a score of $4.98$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) with a score of $7.41$ contributed to higher individual risks. This granular view allows us to pinpoint specific areas of concern.
    """)

    st.subheader("Section 11: Exploring Application B / TV Spoilers")
    st.markdown("""
    Next, we explore "Application B / TV Spoilers". The report notes an overall score of $4.29$ for this application-scenario, signaling a moderate potential for validity risk. Observe how the tree structure and score distribution differ from Application A. This comparison helps in understanding varying risk profiles across different AI applications and scenarios.

    **Interpretation:** For "Application B / TV Spoilers", the overall CoRIx score is $4.29$, indicating a moderate validity risk. Field Testing (score of $4.29$) contributes most significantly at Level 3, followed by Red Teaming ($3.55$) and Model Testing ($2.29$). At Level 4, Field Tester Perceptions (score of $5.00$) were the primary source of risk compared to Annotator Labels ($3.58$) during field testing. Level 5 reveals high scores from `RT RA 2.1` (Red Teaming Risk Assessment 2.1, guardrail violation) at $5.40$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This suggests that for this application, field testers perceived more issues, potentially related to guardrail violations and the presence of superfluous information, offering targeted areas for improvement.
    """)

    st.subheader("Section 12: Exploring Application C / Meal Planner")
    st.markdown("""
    Finally, we will analyze "Application C / Meal Planner". This application-scenario combination exhibited the highest overall CoRIx score of $6.30$ in the pilot, suggesting a higher level of validity risk. This analysis demonstrates how the explorer can highlight critical risk areas, enabling proactive mitigation strategies.

    **Interpretation:** "Application C / Meal Planner" shows the highest overall CoRIx score of $6.30$, indicating the greatest validity risk among the pilot examples. Notably, Model Testing (score of $6.30$) shows the highest risk at Level 3, with Red Teaming ($3.39$) and Field Testing ($2.80$) contributing less. At Level 4, Model Testing Annotator Labels ($6.30$) scored highest. Further breakdown in Level 5 reveals extremely high scores for `MT RA 1` (Model Testing Risk Assessment 1, general functionality) at $9.00$ and `MT RA 2` (Model Testing Risk Assessment 2, response quality) at $7.00$, along with `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This indicates significant issues with basic functionality and response quality observed during model testing, along with superfluous information in field testing. These findings provide clear guidance for developers to address fundamental AI system shortcomings.
    """)

    st.subheader("Section 13: Interpreting CoRIx Scores and Hierarchical Contribution")
    st.markdown("""
    Throughout this exploration, remember that **a higher numeric CoRIx score signifies greater negative risk to validity**.

    The hierarchical structure of the CoRIx trees allows for a nuanced understanding of AI system validity risk:
    -   **Overall Score (Level 2)**: Provides a high-level summary of the validity risk.
    -   **Testing Layers (Level 3)**: Breaks down the overall risk into contributions from different testing methodologies (Model Testing, Red Teaming, Field Testing). This helps identify *where* the risks are most apparent.
    -   **Perception Layers (Level 4)**: Differentiates between risks identified by expert annotators (`Annotator Label`) and those perceived by human users (`User Perception`), offering insights into different perspectives on AI performance.
    -   **Specific Constructs (Level 5)**: Pinpoints the exact assessment items or questionnaire questions that are driving the risks, enabling developers to target specific areas for improvement.

    By interactively navigating these trees, users can gain a deeper understanding of how various factors contribute to the overall trustworthiness and validity of AI systems. This empowers stakeholders to make informed decisions about AI deployment and risk mitigation.
    """)

    st.subheader("Section 14: Conclusion and References")
    st.markdown("""
    This Streamlit application has provided an interactive tool to explore CoRIx measurement trees, enhancing the understanding of how AI validity risk is assessed through various testing layers and aggregation logic. By visualizing and interpreting CoRIx scores, we gain insights into the contextual robustness of AI systems as defined by NIST. This transparent approach facilitates the identification of specific areas for AI system improvement.

    **References:**

    [1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
    """)
