id: 691784590dc7cd32d7afe90a_user_guide
summary: Assessing Risks and Impacts of AI User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Navigating AI Validity Risk: A CoRIx Tree Explorer Codelab

## Introduction to the CoRIx Tree Explorer
Duration: 00:05
This codelab introduces you to the ARIA CoRIx Tree Explorer, a powerful interactive Streamlit application designed to demystify the Contextual Robustness Index (CoRIx) measurement trees. As AI systems become more prevalent, assessing their validity and reliability is paramount. The CoRIx framework, detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1], provides a structured way to quantify the validity risk of AI applications.

This application offers a transparent and intuitive way to visualize how different factors contribute to an AI system's overall validity risk score. By engaging with this explorer, you will gain a deeper understanding of the hierarchical structure of CoRIx, the aggregation logic behind the scores, and how to interpret these scores to identify potential risks in AI deployments.

<aside class="positive">
<b>Important Context:</b> Understanding CoRIx is crucial for anyone involved in developing, deploying, or evaluating AI systems, as it provides a standardized method for assessing validity risk, thereby promoting more trustworthy and reliable AI.
</aside>

Upon completing this codelab, you will be able to:
*   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
*   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
*   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
*   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.

## Understanding the Data: Inputs for CoRIx
Duration: 00:05
The CoRIx Tree Explorer operates on a synthetic dataset, meticulously crafted to align with "Table 8. Example CoRIx output scores" from the NIST ARIA 0.1 Pilot Evaluation Report. This dataset is not real-world data but mimics the structure and content of actual CoRIx evaluations across various AI applications and scenarios.

The dataset includes pre-computed CoRIx scores for different AI applications (e.g., "Application A - Pathfinder", "Application B - TV Spoilers", "Application C - Meal Planner"). Each row in this dataset represents a specific `Construct` within the CoRIx hierarchy, at a given `Level`, ranging from Level 2 (high-level risks) down to Level 5 (specific assessment items). The scores themselves are scaled from 0 to 10, indicating the magnitude of risk.

The key columns in this dataset are:
*   `Level`: Indicates the hierarchical level of the construct (e.g., 2 for overall risk, 5 for specific assessment items).
*   `Construct`: The name of the specific component being assessed (e.g., 'Validity/Reliability (V/R)', 'Model Testing (MT)', 'MT RA 1').
*   `Application X - Scenario Y`: Columns containing the CoRIx scores for each application and scenario combination.

Let's look at a snippet of the raw data:

```
Level,Construct,Application A - Pathfinder,Application B - TV Spoilers,Application C - Meal Planner
2,Validity/Reliability (V/R),2.88,4.29,6.3
3,Model Testing (MT),0.72,2.29,6.3
3,Red Teaming (RT),2.88,3.55,3.39
3,Field Testing (FT),2.36,4.29,2.8
4,MT Annotator Label,0.72,2.29,6.3
```

<aside class="positive">
<b>Interpretation:</b> This tabular data serves as the foundation for our interactive visualizations. It presents raw, unaggregated scores at various levels of detail. A quick glance already shows differing scores across applications and constructs, hinting at varying levels of AI validity risk. The goal of the explorer is to transform this flat table into an interactive, hierarchical tree that reveals the relationships and aggregation logic.
</aside>

## The CoRIx Framework: Aggregation Logic
Duration: 00:10
The Contextual Robustness Index (CoRIx) is a multidimensional framework designed to assess the technical and contextual robustness of AI systems. A CoRIx tree visually represents how various assessment items and testing layers contribute to an overall validity risk score for a specific AI application and scenario.

<aside class="negative">
<b>Critical Insight:</b> A higher numeric CoRIx score indicates greater negative risk to the AI system's validity. All scores are normalized to a scale of 0 to 10.
</aside>

The tree structure progresses through several levels, moving from broad categories to specific details:
*   **Level 2: Risks**: Represents the highest-level risk, such as 'Validity/Reliability'. This is the root of our tree.
*   **Level 3: Testing Level**: Breaks down the overall risk by the type of testing conducted, including 'Model Testing', 'Red Teaming', and 'Field Testing'.
*   **Level 4: Annotator Responses & User Perception**: Further differentiates risks within each testing level based on whether they were identified by expert 'Annotator Labels' or through 'User Perception'.
*   **Level 5: Response Collation**: Comprises specific assessment items or questionnaire questions (e.g., 'RA 1', 'DD 3', 'CC 5', 'QQ 1.1') that are direct inputs contributing to Level 4 scores.

### Mathematical Foundation of CoRIx Aggregation

CoRIx scores are aggregated hierarchically, meaning scores from lower levels combine to form scores at higher levels. The specific mathematical operation for this aggregation depends on the level:

*   **Level 2 (Risks)**: The score for a parent node at this level is the **maximum** of its children's scores. This means the highest risk from any underlying testing layer dictates the overall risk.
    $$ S_P = \max(S_1, S_2, \ldots, S_N) $$

*   **Level 3 (Testing Level)**: The score for a parent node at this level is the **mean (average)** of its children's scores. This averages the contributions from annotator labels and user perceptions within a specific testing level.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

*   **Level 4 (Annotator Responses & User Perception)**: Similar to Level 3, the parent node score is the **mean (average)** of its children's scores. This averages the specific assessment items or questionnaire questions that fall under a perception or annotation category.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

*   **Level 5 (Response Collation)**: These scores represent direct aggregated measures from raw annotator labels or questionnaire responses (Level 6, which are the hypothetical leaf nodes and not explicitly visualized in this application). For visualization purposes, Level 5 nodes are treated as direct inputs to their Level 4 parents, and their "scores" are assumed to be pre-aggregated from these raw responses, typically also via a mean aggregation.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

These aggregation rules are fundamental to the CoRIx framework, ensuring that risks are accurately propagated and combined across different evaluation layers to provide a robust measure for AI system validity risk.

## Building the CoRIx Tree: From Table to Hierarchy
Duration: 00:05
To visualize the CoRIx framework, the flat tabular data from the previous step must be transformed into a tree-like data structure. This process involves identifying parent-child relationships between constructs based on their `Level` and `Construct` names, and then applying the aggregation rules to calculate scores at each level.

The application uses an internal function, `build_corix_tree_data`, to perform this transformation. This function takes the raw data and a selected application/scenario, then constructs a dictionary where each "node" represents a construct in the CoRIx tree. Each node contains its ID, name, parent's ID, its level, its aggregated score, and a list of its children. This structured representation is essential for rendering the interactive tree visualization.

### Formulae for CoRIx Aggregation (Recap)

As a reminder, here are the aggregation rules applied during the tree construction:
*   **Level 2 (Risks)**: The parent node score is the **maximum** of its children's scores.
    $$ S_P = \max(S_1, S_2, \ldots, S_N) $$
*   **Levels 3, 4, 5**: The parent node score is the **mean (average)** of its children's scores.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

<aside class="positive">
<b>Interpretation:</b> The `build_corix_tree_data` function is the engine that converts our raw data into an understandable hierarchical structure. By correctly applying the aggregation logic, it ensures that the scores displayed at each level of the tree accurately reflect the underlying contributions, allowing for meaningful analysis of AI validity risk.
</aside>

## Interacting with the Tree: Node Details
Duration: 00:03
A crucial feature of the CoRIx Tree Explorer is its ability to provide detailed insights into any specific node within the visualized tree. When you click on a node in the interactive plot, the application invokes a function called `display_node_details`.

This function dynamically retrieves and presents a clear breakdown of the information associated with the selected node. This includes:
*   The node's `Level` and `Construct` name.
*   Its `Aggregated Score` (out of 10).
*   If the node is a parent (Levels 2-4), it will list its **direct children** and their respective scores, showing how they contribute to the parent's aggregation.
*   If the node is at Level 5 (a leaf node in our visualization), it will list the **specific assessment items** or questionnaire questions that constitute its score, providing the most granular view of the contributing factors.

This feature is vital for understanding the granular elements that drive the overall risk assessment at each level, tying back directly to actionable insights for AI system improvement.

<aside class="positive">
<b>Key Benefit:</b> By drilling down into node details, you can uncover the specific factors responsible for high CoRIx scores. For instance, a high score at 'Red Teaming' could be further investigated to see if 'Annotator Label' or 'User Perception' was the primary driver, and then down to specific assessment items like 'RT RA 2.1' (guardrail violation).
</aside>

## Visualizing the CoRIx Tree: Interactive Exploration
Duration: 00:05
The core of this application is its interactive visualization of the CoRIx tree, powered by the `create_interactive_corix_tree_plot` function. This function uses the `plotly.graph_objects` library to render a dynamic and visually engaging node-link diagram.

The interactive plot offers several key features:
*   **Node-Link Diagram**: Each node in the diagram represents a `Construct` in the CoRIx hierarchy, clearly displaying its name and aggregated score.
*   **Hover Information**: When you hover your mouse over a node, a tooltip appears, providing additional details such as the node's ID, full name, score, and level.
*   **Visual Cues**: Selected nodes are highlighted (e.g., in red) and slightly enlarged, making it easy to see which node's details are currently being displayed.
*   **Depth Control**: A slider allows you to control the `Max Tree Depth`, enabling you to view either a high-level overview (e.g., Depth 2 or 3) or a detailed breakdown (Depth 5), managing the complexity of the visualization.

The plot is designed to be intuitive, allowing you to trace the flow of risk from the detailed assessment items at Level 5 up to the overall validity risk at Level 2.

<aside class="positive">
<b>User Experience:</b> This interactive visualization is central to the application's learning goals. It transforms complex hierarchical data into an easily digestible format, allowing for intuitive exploration and comparison of AI validity risks across various contexts.
</aside>

## Hands-on Exploration: Using the Controls
Duration: 00:05
Now, let's put it all together and start interacting with the CoRIx Tree Explorer.

On the left sidebar of the application, you'll find the main controls:

1.  **Select Application/Scenario:**
    *   This dropdown menu allows you to choose which AI application and scenario combination you want to analyze. Options include "Application A - Pathfinder", "Application B - TV Spoilers", and "Application C - Meal Planner".
    *   **Action:** Select "Application A - Pathfinder" for our first exploration.

2.  **Max Tree Depth:**
    *   This slider controls how many levels of the CoRIx tree are displayed. You can set it from 2 (showing only the overall risk and direct children) up to 5 (showing the full detail down to individual assessment items).
    *   **Action:** Set the slider to `5` to view the complete hierarchical structure.

Once you've made your selections, the interactive CoRIx tree plot will update to reflect your choices.

### Interacting with the Tree Plot:
*   **Hover**: Move your mouse over any node in the tree. You'll see a small tooltip appear with basic information about that node (ID, Name, Score, Level).
*   **Click**: Click on any node in the tree.
    *   When you click a node, it will be highlighted in red.
    *   More importantly, a dedicated "Node Details" section below the plot will populate with comprehensive information about that specific node, including its direct children's scores or the contributing assessment items.

<aside class="positive">
<b>Tip:</b> Experiment with the `Max Tree Depth` slider. Start with a lower depth (e.g., 3) to get a high-level overview, and then increase it to 5 to dive into the specific details driving the scores.
</aside>

## Case Study 1: Application A / Pathfinder
Duration: 00:05
Let's begin by examining "Application A / Pathfinder". Ensure this selection is active in the sidebar and the `Max Tree Depth` slider is set to `5`.

Observe the overall structure and scores in the displayed tree.
The main "Validity/Reliability (V/R)" node (Level 2) should show a score. Click on it to see its details.

<aside class="positive">
<b>Interpretation:</b> For "Application A / Pathfinder", the overall CoRIx score displayed for the `Validity/Reliability (V/R)` node is $\mathbf{2.88}$. This relatively low score suggests a lower observed risk to validity for this specific application and scenario combination.

By clicking and tracing down the tree:
*   At **Level 3**, you'll see how Model Testing ($\mathbf{0.72}$), Red Teaming ($\mathbf{2.88}$), and Field Testing ($\mathbf{2.36}$) contribute. Red Teaming contributes the most to the overall risk in this case.
*   Drilling into **Red Teaming (RT)** at **Level 4**, you can see that `RT Annotator Label` (score of $\mathbf{3.52}$) identified higher risks compared to `RT User Perception` (score of $\mathbf{2.24}$).
*   Further delving into **Level 5** (by clicking `RT Annotator Label`), you might find specific constructs like `RT DD 4` (Red Teaming Dialogue Dynamics 4, related to unnatural dialogue) with a score of $\mathbf{4.98}$, or within `FT Annotator Label`, `FT CC 3` (Field Testing Content Characterization 3, related to superfluous information) with a score of $\mathbf{7.41}$ (if present as a child for the respective branch). This granular view allows us to pinpoint specific areas of concern.
</aside>

## Case Study 2: Application B / TV Spoilers
Duration: 00:05
Now, go to the sidebar and change the "Select Application/Scenario" to "Application B - TV Spoilers". Keep the `Max Tree Depth` at `5`.

Observe how the tree structure and score distribution change compared to Application A.

<aside class="positive">
<b>Interpretation:</b> For "Application B / TV Spoilers", the overall CoRIx score shown is $\mathbf{4.29}$, indicating a moderate validity risk, higher than Application A.

By exploring the tree:
*   At **Level 3**, **Field Testing** (score of $\mathbf{4.29}$) stands out as the most significant contributor to the overall risk, followed by Red Teaming ($\mathbf{3.55}$) and Model Testing ($\mathbf{2.29}$).
*   Diving into **Field Testing (FT)** at **Level 4**, `FT User Perception` (score of $\mathbf{5.00}$) was the primary source of risk compared to `FT Annotator Labels` ($\mathbf{3.58}$) during field testing.
*   At **Level 5**, high scores come from `RT RA 2.1` (Red Teaming Risk Assessment 2.1, related to guardrail violation) at $\mathbf{5.40}$ and `FT CC 3` (Field Testing Content Characterization 3, related to superfluous information) at $\mathbf{7.42}$. This suggests that for this application, field testers perceived more issues, potentially related to guardrail violations and the presence of superfluous information. These findings offer targeted areas for improvement.
</aside>

## Case Study 3: Application C / Meal Planner
Duration: 00:05
Finally, let's analyze "Application C / Meal Planner". Select it from the sidebar dropdown. Keep the `Max Tree Depth` at `5`.

This application-scenario combination exhibited the highest overall CoRIx score in the pilot. Observe where the highest risks are concentrated.

<aside class="positive">
<b>Interpretation:</b> "Application C / Meal Planner" presents the highest overall CoRIx score of $\mathbf{6.30}$, indicating the greatest validity risk among our pilot examples.

Through the tree exploration:
*   Notably, **Model Testing (MT)** (score of $\mathbf{6.30}$) shows the highest risk at **Level 3**, with Red Teaming ($\mathbf{3.39}$) and Field Testing ($\mathbf{2.80}$) contributing less. This is a clear indicator that fundamental issues might be present even before deployment.
*   At **Level 4**, `MT Annotator Labels` ($\mathbf{6.30}$) scored highest.
*   Further breakdown in **Level 5** reveals extremely high scores for `MT RA 1` (Model Testing Risk Assessment 1, general functionality) at $\mathbf{9.00}$ and `MT RA 2` (Model Testing Risk Assessment 2, response quality) at $\mathbf{7.00}$. Additionally, `FT CC 3` (Field Testing Content Characterization 3, superfluous information) shows a score of $\mathbf{7.42}$. These findings point to significant issues with basic functionality and response quality observed during model testing, along with superfluous information in field testing. This provides clear guidance for developers to address fundamental AI system shortcomings.
</aside>

## Interpreting CoRIx Scores and Hierarchical Contribution
Duration: 00:03
Throughout this exploration, consistently remember the core principle: **a higher numeric CoRIx score signifies greater negative risk to the validity of the AI system.**

The hierarchical structure of the CoRIx trees allows for a nuanced and actionable understanding of AI system validity risk:
*   **Overall Score (Level 2)**: Provides a high-level, immediate summary of the AI system's validity risk for a given application and scenario.
*   **Testing Layers (Level 3)**: Breaks down the overall risk into contributions from different testing methodologies (Model Testing, Red Teaming, Field Testing). This helps identify *where* the risks are most apparent in the development and deployment lifecycle.
*   **Perception Layers (Level 4)**: Differentiates between risks identified by expert annotators (`Annotator Label`) and those perceived by human users (`User Perception`). This offers critical insights into different stakeholder perspectives on AI performance and trustworthiness.
*   **Specific Constructs (Level 5)**: Pinpoints the exact assessment items or questionnaire questions that are driving the risks. This level provides the most granular information, enabling developers and stakeholders to target specific areas for improvement, debugging, or policy adjustments.

By interactively navigating these trees and understanding the aggregation logic at each level, users can gain a profound understanding of how various factors combine and contribute to the overall trustworthiness and validity of AI systems. This empowers stakeholders to make informed decisions about AI deployment and risk mitigation strategies.

## Conclusion and References
Duration: 00:02
This Streamlit application has served as an interactive tool to explore and interpret CoRIx measurement trees. By guiding you through various case studies and explaining the underlying methodology, we've enhanced your understanding of how AI validity risk is assessed through different testing layers and aggregation logic.

The transparent visualization and intuitive controls of the CoRIx Tree Explorer facilitate the identification of specific areas for AI system improvement, contributing to the development of more robust and trustworthy AI. We encourage you to continue experimenting with different applications, scenarios, and tree depths to deepen your insights into AI validity risk.

**References:**

[1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
