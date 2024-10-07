import pandas as pd
from services.providers_service import Providers

# Providers
def test_count_parties():
    # Data
    data = pd.DataFrame({
        'Parties': [['Party 1', 'Party 2'], ['Party 3', 'Party 4'], ['Party 1', 'Party 2']]
    })
    providers = Providers(data)

    # Test
    assert providers.count_parties().to_dict() == {
        'Party': {0: 'Party 1', 1: 'Party 2', 2: 'Party 3', 3: 'Party 4'},
        'Count': {0: 2, 1: 2, 2: 1, 3: 1}
   }