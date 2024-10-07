import pandas as pd
from services.effective_dates_service import EffectiveDates

def test_get_min_date_index():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Effective Date': ['2021-01-01', '2021-02-01', '2021-03-01']
    })
    effective_dates = EffectiveDates(data, ['Document Name', 'Effective Date'])
    effective_dates.data['Effective Date'] = pd.to_datetime(effective_dates.data['Effective Date'], errors='coerce')

    # Test
    min_date, min_name = effective_dates.get_min_date_index('Effective Date')
    assert min_date == '01-01-2021'
    assert min_name == 'Contract 1'

def test_get_max_date_index():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Effective Date': ['2021-01-01', '2021-02-01', '2021-03-01']
    })
    effective_dates = EffectiveDates(data, ['Document Name', 'Effective Date'])
    effective_dates.data['Effective Date'] = pd.to_datetime(effective_dates.data['Effective Date'], errors='coerce')

    # Test
    max_date, max_name = effective_dates.get_max_date_index('Effective Date')
    assert max_date == '01-03-2021'
    assert max_name == 'Contract 3'