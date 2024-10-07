# Supplier_management

This project consists of an application developed for the management and analysis of information within data sets. It uses Pandas library for efficient manipulation and organization of data, facilitating tasks such as cleaning, transforming, and aggregating information. In addition, it integrates a language model that allows users to query relevant data.

## Datasets

[Atticus Open Contract Dataset](https://www.kaggle.com/datasets/konradb/atticus-open-contract-dataset-aok-beta)

[World cities database](https://www.kaggle.com/datasets/juanmah/world-cities)

[World Countries and Continents Details](https://www.kaggle.com/datasets/folaraz/world-countries-and-continents-details)

## Main technologies

- Python
- Pandas
- Streamlit
- BERT

## Run app

> **Note:** This steps are on Windows, you should adjust them for IOS or Linux.

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

## App use

Using the side menu you can navigate through the different tabs where the relevant data for that category is displayed, as well as interactive diagrams to have a better understanding of the data.

To use the model, in the BERT option you can press the button `Preguntar` to solve the questions that are listed.

## Tests

`Pytest` library is used for testing.

1. Open command prompt and navigate to where the app was cloned.

2. Activate virtual enviroment.

3. Run the following command.

    ```CMD
    pytest
    ```
