import pandas as pd

from services.renewal_term_service import RenewalTerm

def test_count_group_by():
    # Data
    data = pd.DataFrame({
        'Document Name': ['Contract 1', 'Contract 2', 'Contract 3'],
        'Renewal Term (days)': [20, 60, 20]
    })
    renewal_term = RenewalTerm(data, ['Document Name', 'Renewal Term (days)'])

    # Test
    assert renewal_term.count_group_by('Renewal Term (days)').to_dict() == {
        'Renewal Term (days)': {0: 20, 1: 60},
        'Count': {0: 2, 1: 1}
    }