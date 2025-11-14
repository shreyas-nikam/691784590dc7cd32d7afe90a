
import streamlit as st
import pandas as pd
import os

def run_page1():
    st.subheader("Section 3: Data/Inputs Overview")
    st.markdown("""
    The CoRIx Tree Explorer uses a synthetic dataset based on "Table 8. Example CoRIx output scores" from Appendix E of the NIST ARIA 0.1 Pilot Evaluation Report [1]. This dataset contains pre-computed CoRIx scores for different AI applications (Application A, B, C) across various scenarios (Pathfinder, TV Spoilers, Meal Planner). The data is structured to reflect Levels 2 through 5 of the CoRIx tree, including constructs like 'Validity/Reliability', 'Model Testing', 'Red Teaming', 'Field Testing', 'Annotator Label', 'User Perception', and detailed assessment items (e.g., RA 1, DU 2, CC 3, QQ 1.1).

    The dataset `corix_scores.csv` will have the following columns: `Level`, `Construct`, `Application A - Pathfinder`, `Application B - TV Spoilers`, `Application C - Meal Planner`. The scores are scaled from 0 to 10. This dataset supports our business goal of transparently assessing AI validity risk by providing the foundational data for our interactive visualizations.
    """)

    @st.cache_data
    def load_corix_dataset(filepath):
        """
        Loads the CoRIx scores from a specified CSV file into a pandas DataFrame.
        Arguments: filepath (string or path-like object to the CSV file).
        Output: pandas.DataFrame containing the raw CoRIx data.
        """
        if not isinstance(filepath, (str, os.PathLike)):
            raise TypeError(f"filepath must be a string or a path-like object, got {type(filepath).__name__}")
        df = pd.read_csv(filepath)
        return df

    # Data creation and saving logic to ensure the file exists for the app.
    # This would ideally be a separate script or part of deployment setup,
    # but for a self-contained app, it can be run conditionally.
    # For production, 'corix_scores.csv' should be a pre-existing file.
    if not os.path.exists('corix_scores.csv'):
        data = {
            'Level': [2, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            'Construct': ['Validity/Reliability (V/R)', 'Model Testing (MT)', 'Red Teaming (RT)', 'Field Testing (FT)', 'MT Annotator Label', 'RT Annotator Label', 'RT User Perception', 'FT Annotator Label', 'FT User Perception', 'MT RA 1', 'MT RA 2', 'MT DD 3', 'MT CC 4', 'MT CC 5', 'RT RA 1', 'RT RA 2.1', 'RT DD 3', 'RT DD 4', 'RT CC 5', 'RT UR 1', 'RT UR 2', 'RT UR 3', 'RT UR 4', 'RT UR 5', 'FT RA 1', 'FT RA 2', 'FT DD 3', 'FT CC 4', 'FT CC 5', 'FT UR 1', 'FT UR 2', 'FT UR 3', 'FT UR 4', 'FT UR 5', 'MT QQ 1.1', 'MT QQ 2.1', 'RT QQ 1.1', 'RT QQ 2.1', 'FT QQ 1.1', 'FT QQ 2.1', 'MT Annotator Label (Overall)', 'RT Annotator Label (Overall)', 'RT User Perception (Overall)', 'FT Annotator Label (Overall)', 'FT User Perception (Overall)'],
            'Application A - Pathfinder': [2.88, 0.72, 2.88, 2.36, 0.72, 3.52, 2.24, 3.06, 1.67, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.98, 0.0, 4.98, 0.0, 0.0, 0.0, 0.0, 4.98, 0.0, 0.0, 0.0, 0.0, 0.0, 7.41, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'Application B - TV Spoilers': [4.29, 2.29, 3.55, 4.29, 2.29, 3.75, 3.34, 3.58, 5.00, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.40, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'Application C - Meal Planner': [6.30, 6.30, 3.39, 2.80, 6.30, 3.74, 3.05, 3.56, 2.03, 9.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        corix_df = pd.DataFrame(data)
        corix_df.to_csv('corix_scores.csv', index=False)

    loaded_df = load_corix_dataset('corix_scores.csv')

    st.dataframe(loaded_df.head()) # Display the first few rows
    st.markdown("""
    **Interpretation:** The table above displays the initial rows of our `corix_scores.csv` dataset. Each row represents a specific construct within the CoRIx hierarchy, at a given `Level`. The columns on the right show the CoRIx scores (scaled 0-10) for different application and scenario combinations. This tabular format is the raw input that we will transform into a hierarchical tree structure for visualization. A quick scan already reveals varying scores across applications and constructs, indicating differing levels of AI validity risk.
    """)
