import pandas as pd
from services.governing_law_service import GoverningLaw

def test_unique_governing_laws():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Governing Law': [['Ontario'], ['California', 'Hong Kong'], ['Israel']]
    })
    governing_law = GoverningLaw(data)

    # Test
    assert governing_law.unique_governing_laws() == {'Ontario', 'California', 'Hong Kong', 'Israel'}

def test_get_countries():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Governing Law': [['Ontario'], ['California', 'Hong Kong'], ['Israel']]
    })
    governing_law = GoverningLaw(data)
    unique_laws = {'Ontario', 'California', 'Hong Kong', 'Israel'}

    # Expected DataFrame
    expected_df = pd.DataFrame({
        'Ciudad': ['Israel', 'Hong Kong', 'California', 'Ontario'],
        'Pais': ['Israel', 'Hong Kong', 'United States', 'Canada'],
        'Latitud': [32.08, 22.3, 34.1141, 43.7417],
        'Longitud': [34.78, 114.2, -118.4068, -79.3733]
    })

    # Test
    result_df = governing_law._get_countries(unique_laws)

    assert result_df.sort_values(by=['Ciudad']).reset_index(drop=True).equals(
        expected_df.sort_values(by=['Ciudad']).reset_index(drop=True)
    ), "The returned DataFrame does not match the expected values."


def test_get_continents():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Governing Law': [['Ontario'], ['California', 'Hong Kong'], ['Israel']]
    })
    governing_law = GoverningLaw(data)
    
    countries = pd.DataFrame({
        'Ciudad': ['Israel', 'Hong Kong', 'California', 'Ontario'],
        'Pais': ['Israel', 'Hong Kong', 'United States', 'Canada'],
        'Latitud': [32.08, 22.3, 34.1141, 43.7417],
        'Longitud': [34.78, 114.2, -118.4068, -79.3733]
    })

    # Expected DataFrame
    expected_df = pd.DataFrame({
        'Ciudad': ['Israel', 'Hong Kong', 'California', 'Ontario'],
        'Pais': ['Israel', 'Hong Kong', 'United States', 'Canada'],
        'Latitud': [32.08, 22.3, 34.1141, 43.7417],
        'Longitud': [34.78, 114.2, -118.4068, -79.3733],
        'Continent': ['AS', 'AS', 'NA', 'NA']
    })

    # Test
    result_df = governing_law._get_continents(countries)

    result_df[['Latitud', 'Longitud']] = result_df[['Latitud', 'Longitud']].round(4)
    expected_df[['Latitud', 'Longitud']] = expected_df[['Latitud', 'Longitud']].round(4)

    for column in expected_df.columns:
        assert result_df[column].sort_values().reset_index(drop=True).equals(
            expected_df[column].sort_values().reset_index(drop=True)
        ), f"Mismatch found in column: {column}"
