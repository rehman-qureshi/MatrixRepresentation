# Matrix Representation for Activity Relationship Manipulation

This Python script provides a simple command-line interface to manipulate a matrix representation of activities and their relationships, commonly used in process mining and workflow analysis. The matrix is managed as a pandas DataFrame, and users can interactively perform various relaxation operations.

## Features

- **Allow self-loop:** Add a self-loop to a specified activity.
- **Remove activity:** Remove an activity (row and column) from the matrix.
- **Remove specific relationship:** Remove a direct relationship between two activities.
- **Remove all relationships:** Remove all relationships/activities between two specified activities.
- **Show Matrix:** Display the current state of the matrix.
- **Reset to Original Matrix:** Restore the matrix to its original state.
- **Exit:** Quit the program.

## Usage

1. **Clone the repository** and ensure you have Python 3.x installed.
2. **Install dependencies:**
    ```bash
    pip install pandas
    ```
3. **Ensure the following files are present in the same directory:**
    - `matrix-representation.py`
    - `allow_self_loop.py`
    - `remove_activity.py`
    - `remove_specific_relationship.py`
    - `remove_all_relationships.py`

4. **Run the script:**
    ```bash
    python matrix-representation.py
    ```

5. **Follow the on-screen prompts** to perform operations on the matrix.

## Example

```
Choose a relaxation operation:
1. Allow self-loop
2. Remove activity
3. Remove specific relationship
4. Remove all relationships/activities between two activities
5. Show Matrix
6. Reset to Original Matrix
0. Exit
Enter your choice (0-6): 1
Enter activity for self-loop: A
```

## Code Structure

- **matrix-representation.py**: Main script with the user interface and matrix logic.
- **allow_self_loop.py**: Function to add self-loops.
- **remove_activity.py**: Function to remove an activity.
- **remove_specific_relationship.py**: Function to remove a specific relationship.
- **remove_all_relationships.py**: Function to remove all relationships between two activities.

## Customization

You can modify the initial `matrix` variable in `matrix-representation.py` to represent your own set of activities and relationships.

## License

This project is provided for academic and educational purposes. Please cite appropriately if used in research.

---
```# Matrix Representation for Activity Relationship Manipulation

This Python script provides a simple command-line interface to manipulate a matrix representation of activities and their relationships, commonly used in process mining and workflow analysis. The matrix is managed as a pandas DataFrame, and users can interactively perform various relaxation operations.
