# Matrix Representation and Relaxation Tool for Process Mining

This repository provides a Python command-line tool for interactively manipulating a matrix representation of activities and their relationships, as commonly used in process mining and workflow analysis. The tool supports a variety of relaxation and transformation operations on the activity matrix, and can generate declarative constraints from the resulting relationships.

## Features

- **Allow self-loop:** Add a self-loop (`||`) to a specified activity.
- **Remove activity:** Remove an activity (row and column) from the matrix.
- **Remove direct relationship:** Remove a direct relationship (`→`) between two activities.
- **Remove all relationships:** Remove all relationships/activities between two specified activities.
- **Direct to concurrent relationship:** Change a direct (`→`) relationship to concurrent (`||`).
- **Exclusive to direct relationship:** Change an exclusive (`-`) relationship to direct (`→`).
- **Exclusive to concurrent relationship:** Change an exclusive (`-`) relationship to concurrent (`||`).
- **Show Matrix:** Display the current state of the matrix.
- **Reset to Original Matrix:** Restore the matrix to its original state.
- **Generate Declarative Constraints:** Generate and export declarative constraints from the current matrix.
- **Exit:** Quit the program.

## Getting Started

### Prerequisites

- Python 3.x
- pandas

### Installation

Install the required Python package:

```bash
pip install pandas
```

### Usage

1. **Clone this repository** and ensure all the following files are in the same directory:
    - `matrix-representation.py`
    - `allow_self_loop.py`
    - `remove_activity.py`
    - `remove_direct_relationship.py`
    - `remove_all_relationships.py`
    - `direct_to_concurrent_relationship.py`
    - `exclusive_to_direct_relationship.py`
    - `exclusive_to_concurrent_relationship.py`
    - `generate_declarative_constraints.py`

2. **Run the main script:**

    ```bash
    python matrix-representation.py
    ```

3. **Follow the on-screen prompts** to perform operations on the matrix.

### Example Session

```
Choose a relaxation operation:
1. Allow self-loop
2. Remove activity
3. Remove direct relationship
4. Remove all relationships/activties between two activities
5. From direct(→) to concurrent(||) relationship
6. From exclusive(-) to direct(→) relationship
7. From exclusive(-) to concurrent(||) relationship
8. Show Matrix
9. Reset to Original Matrix
10. Generate Declarative Constraints
0. Exit
Enter your choice (0-10): 1
Enter activity for self-loop: CPO
```

## Matrix Representation

The matrix is a pandas DataFrame where:
- **Rows and columns** represent activities.
- **Cell values** represent relationships:
    - `→` : Directly follows
    - `||` : Concurrent
    - `-`  : Exclusive 
    - `~>` : Eventually follows

You can modify the initial `matrix` variable in `matrix-representation.py` to represent your own process model.

## Academic Reference

The included example is based on a procurement process model from BPIC 2019:
> Diba, K., Remy, S., & Pufahl, L. (2019, June). Compliance and performance analysis of procurement processes using process mining. In International conference on process mining.

## License

This project is provided for academic and educational purposes. Please cite appropriately if used in research.

---
```# Matrix Representation and Relaxation Tool for Process Mining

This repository provides a Python command-line tool for interactively manipulating a matrix representation of activities and their relationships, as commonly used in process mining and workflow analysis. The tool supports a variety of relaxation and transformation operations on the activity matrix, and can generate declarative constraints from the resulting relationships.

## Features

- **Allow self-loop:** Add a self-loop (`||`) to a specified activity.
- **Remove activity:** Remove an activity (row and column) from the matrix.
- **Remove direct relationship:** Remove a direct relationship (`→`) between two activities.
- **Remove all relationships:** Remove all relationships/activities between two specified activities.
- **Direct to concurrent relationship:** Change a direct (`→`) relationship to concurrent (`||`).
- **Exclusive to direct relationship:** Change an exclusive (`-`) relationship to direct (`→`).
- **Exclusive to concurrent relationship:** Change an exclusive (`-`) relationship to concurrent (`||`).
- **Show Matrix:** Display the current state of the matrix.
- **Reset to Original Matrix:** Restore the matrix to its original state.
- **Generate Declarative Constraints:** Generate and export declarative constraints from the current matrix.
- **Exit:** Quit the program.

## Getting Started

### Prerequisites

- Python 3.x
- pandas

### Installation

Install the required Python package:

```bash
pip install pandas
```

### Usage

1. **Clone this repository** and ensure all the following files are in the same directory:
    - `matrix-representation.py`
    - `allow_self_loop.py`
    - `remove_activity.py`
    - `remove_direct_relationship.py`
    - `remove_all_relationships.py`
    - `direct_to_concurrent_relationship.py`
    - `exclusive_to_direct_relationship.py`
    - `exclusive_to_concurrent_relationship.py`
    - `generate_declarative_constraints.py`

2. **Run the main script:**

    ```bash
    python matrix-representation.py
    ```

3. **Follow the on-screen prompts** to perform operations on the matrix.

### Example Session

```
Choose a relaxation operation:
1. Allow self-loop
2. Remove activity
3. Remove direct relationship
4. Remove all relationships/activties between two activities
5. From direct(→) to concurrent(||) relationship
6. From exclusive(-) to direct(→) relationship
7. From exclusive(-) to concurrent(||) relationship
8. Show Matrix
9. Reset to Original Matrix
10. Generate Declarative Constraints
0. Exit
Enter your choice (0-10): 1
Enter activity for self-loop: CPO
```

## Matrix Representation

The matrix is a pandas DataFrame where:
- **Rows and columns** represent activities.
- **Cell values** represent relationships:
    - `→` : Directly follows
    - `||` : Concurrent
    - `-`  : Exclusive
    - `~>` : Eventually follows

You can modify the initial `matrix` variable in `matrix-representation.py` to represent your own process model.

## License

This project is provided for academic and educational purposes. Please cite appropriately if used in research.

---
