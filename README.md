# Supplier_management

The following application was design for the management and analysis of information within a dataset, supported by a language model to simplify and improve the process.

## Dataset

[Atticus Open Contract Dataset](https://www.kaggle.com/datasets/konradb/atticus-open-contract-dataset-aok-beta)

## Technologies

- Python
- Streamlit
- GPT Neo

## Run app

> **Note:** This steps are on Windows, for IOS or Linux adjust them.

1. Clone repository and open it.

    ``` CMD
    git clone https://github.com/Milo751/Supplier_management.git
    ```

2. Create and activate virtual enviroment on command prompt.

    ``` CMD
    python -m venv venv
    cd venv/scritps
    activate
    ```

3. Install required libraries using `requirements.txt`.

    ``` CMD
    pip install -r requirements.txt
    ```

4. Run app.

    ``` CMD
    streamlit run app.py
    ```

## Tests

`Pytest` library is used for testing.

1. Open command prompt and navigate to where the app was cloned.

2. Activate virtual enviroment.

3. Run the following command.

    ```CMD
    pytest
    ```
