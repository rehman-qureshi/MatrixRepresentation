# Bridging Imperative Process Models and Process Data Queries—Translation and Relaxation


This repository provides a Python command-line tool for interactively manipulating a matrix representation of activities and their relationships, as commonly used in process mining and workflow analysis. The tool supports a variety of relaxation and transformation operations on the activity matrix, can generate declarative constraints, and supports visualization of PNML models.

## Features

- **Matrix generation from PNML:** Automatically generate the activity matrix from a PNML file.
- **Allow self-loop:** Add a self-loop (`||`) to a specified activity.
- **Remove activity:** Remove an activity (row and column) from the matrix.
- **Remove direct relationship:** Remove a direct relationship (`→`) between two activities.
- **Remove all relationships:** Remove all relationships/activities between two specified activities.
- **Direct to concurrent relationship:** Change a direct (`→`) relationship to concurrent (`||`).
- **Add true exclusion relationships:** Add true exclusion relationships to the matrix (`#`).
- **Show Matrix:** Display the current state of the matrix.
- **Reset to Original Matrix:** Restore the matrix to its original state.
- **Generate Declarative Constraints:** Generate and export declarative constraints from the current matrix.
- **Visualize PNML Model:** Visualize the process model from a PNML file.
- **Exclusive to direct relationship:** Change an exclusive (`#`) relationship to direct (`→`).
- **Exit:** Quit the program.

## Getting Started

### Prerequisites

- Python 3.x
- pandas
- pm4py

### Installation

Install the required Python packages:

```bash
pip install pandas pm4py
```

### Usage

1. **Clone this repository** and ensure all the following files are in the same directory:
    - `driver.py`
    - `create_alpha_relations_matrix.py`
    - `allow_self_loop.py`
    - `remove_activity.py`
    - `remove_direct_relationship.py`
    - `remove_all_relationships.py`
    - `direct_to_concurrent_relationship.py`
    - `exclusive_to_direct_relationship.py`
    - `exclusive_to_concurrent_relationship.py`
    - `generate_declarative_constraints.py`
    - `add_true_exclusion_relationships.py`
    - `visualize_pnml_model.py`

2. **Run the main script with a PNML file:**

    ```bash
    python driver.py <path_to_pnml_file>
    ```

The tool will display the matrix and provide an interactive menu for relaxation and transformation operations.