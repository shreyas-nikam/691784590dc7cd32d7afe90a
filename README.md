# QuLab - ARIA CoRIx Tree Explorer: An Interactive Streamlit Application

## Project Title and Description

The **QuLab - ARIA CoRIx Tree Explorer** is an interactive Streamlit application designed to facilitate the visualization and understanding of Contextual Robustness Index (CoRIx) measurement trees. Developed as a lab project for educational purposes, it aims to demystify the hierarchical structure and aggregation logic of CoRIx scores, which are critical for assessing the validity risk of AI applications. The framework and data structure are inspired by the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].

**Learning Goals for Users:**

*   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
*   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
*   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
*   Interpret the meaning of CoRIx scores, where **higher scores indicate greater negative risk**.

## Features

The QuLab - ARIA CoRIx Tree Explorer offers the following key features:

*   **Interactive CoRIx Tree Visualization**: A dynamic node-link diagram using Plotly, allowing users to visually explore the hierarchical breakdown of CoRIx scores.
*   **Dynamic Data Loading and Processing**: Loads a synthetic dataset (`corix_scores.csv`) representing pre-computed CoRIx scores across various AI applications and scenarios.
*   **Hierarchical Aggregation Logic**: Implements the CoRIx aggregation rules:
    *   **Level 2 (Risks)**: Maximum of children's scores.
    *   **Levels 3, 4, 5**: Mean (average) of children's scores.
*   **Detailed Node Inspection**: On clicking any node in the tree, a dedicated section displays its level, construct, aggregated score, direct children's scores, and contributing raw assessment items/questionnaire questions.
*   **Application and Scenario Selection**: Users can choose different AI application and scenario combinations from a dropdown menu to dynamically update the tree visualization.
*   **Tree Depth Control**: A slider allows users to control the maximum visible depth of the tree, simplifying complex visualizations.
*   **Overview of CoRIx Methodology**: A dedicated section explains the CoRIx framework, its levels, and the mathematical foundation for aggregation.
*   **Guided Interpretation**: Provides pre-written interpretations for example AI applications (Pathfinder, TV Spoilers, Meal Planner) to guide users through understanding varying risk profiles.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quolab-corix-explorer.git
    cd quolab-corix-explorer
    ```
    *(Replace `your-username/quolab-corix-explorer` with the actual repository path if it's hosted.)*

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` doesn't exist, create it manually or generate it using `pip freeze > requirements.txt` after installing the below packages.)*

    The required packages are:
    ```
    streamlit
    pandas
    numpy
    plotly
    streamlit-plotly-events
    ```
    So, you can also install them directly:
    ```bash
    pip install streamlit pandas numpy plotly streamlit-plotly-events
    ```

## Usage

To run the Streamlit application:

1.  Ensure you are in the project's root directory (`quolab-corix-explorer/`) and your virtual environment is activated.
2.  Execute the following command:
    ```bash
    streamlit run app.py
    ```
3.  Your web browser should automatically open to the application (usually at `http://localhost:8501`). If not, copy and paste the URL from your terminal.

### Basic Usage Instructions:

*   **Navigation**: Use the "Navigation" selectbox in the left sidebar to switch between "Data Overview", "CoRIx Tree Explorer", and "Interpretation and Conclusion".
*   **Data Overview**: Provides an explanation and a preview of the synthetic dataset used.
*   **CoRIx Tree Explorer**:
    *   **Select Application/Scenario**: Use the dropdown in the left sidebar to choose an AI application and scenario combination (e.g., "Application A - Pathfinder"). The tree visualization will update dynamically.
    *   **Adjust Max Tree Depth**: Use the slider in the left sidebar to control how many levels of the CoRIx tree are displayed.
    *   **Explore Nodes**: Hover over any node in the tree to see its ID, name, score, and level.
    *   **View Node Details**: Click on a node to display a detailed breakdown of its aggregated score, direct children, and contributing assessment items in the main content area below the tree.
*   **Interpretation and Conclusion**: Offers guided insights into the different example applications and summarizes the key takeaways of the CoRIx framework.

## Project Structure

The project is organized as follows:

```
quolab-corix-explorer/
├── app.py                      # Main Streamlit application entry point
├── corix_scores.csv            # (Generated if not exists) Synthetic dataset of CoRIx scores
├── application_pages/          # Directory containing individual Streamlit page modules
│   ├── __init__.py             # Makes 'application_pages' a Python package
│   ├── page1.py                # "Data Overview" page: loads/previews data
│   ├── page2.py                # "CoRIx Tree Explorer" page: core visualization and logic
│   └── page3.py                # "Interpretation and Conclusion" page: guided analysis
└── README.md                   # This README file
└── requirements.txt            # List of Python dependencies
```

## Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: The open-source app framework used to build and deploy the web application.
*   **Pandas**: Utilized for data manipulation and analysis, particularly for handling the `corix_scores.csv` DataFrame.
*   **NumPy**: Used for numerical operations, specifically `np.max` and `np.mean` for CoRIx score aggregation.
*   **Plotly**: An interactive graphing library for creating the dynamic node-link tree visualization.
*   **streamlit-plotly-events**: A Streamlit component that enables handling click events on Plotly charts within a Streamlit app.

## Contributing

As this is a lab project, direct contributions might not be formally managed as in a large open-source project. However, if you have suggestions for improvements, bug reports, or feature ideas, please consider:

1.  **Forking the repository.**
2.  **Creating a new branch** (`git checkout -b feature/YourFeatureName` or `bugfix/FixDescription`).
3.  **Making your changes and committing them** with clear, descriptive messages.
4.  **Pushing your branch** to your forked repository.
5.  **Opening a Pull Request** against the original repository.

## License

This project is licensed under the MIT License - see the `LICENSE` file (if present) or assume MIT for typical lab projects for more details.

## Contact

For any questions or further information about this project, please reach out via:

*   **QuantUniversity**: [https://www.quantuniversity.com/](https://www.quantuniversity.com/)
*   **Email**: info@quantuniversity.com

---

### References

[1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, [https://doi.org/10.6028/NIST.AI.700-2](https://doi.org/10.6028/NIST.AI.700-2).
