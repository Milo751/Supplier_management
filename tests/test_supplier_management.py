import pandas as pd

from services.normalize import PreprocessData
from services.providers_service import Providers
from services.renewal_term_service import RenewalTerm
from services.effective_dates_service import EffectiveDates
from services.governing_law_service import GoverningLaw

def test_supplier_management():
    # Data
    data = {
        "Filename": [
            "CybergyHoldingsInc_20140520_10-Q_EX-10.27_8605784_EX-10.27_Affiliate Agreement.pdf",
            "EuromediaHoldingsCorp_20070215_10SB12G_EX-10.B(01)_525118_EX-10.B(01)_Content License Agreement.pdf"
        ],
        "Document Name": [
            "['MARKETING AFFILIATE AGREEMENT']",
            "['VIDEO-ON-DEMAND CONTENT LICENSE AGREEMENT']"
        ],
        "Document Name-Answer": [
            "MARKETING AFFILIATE AGREEMENT",
            "VIDEO-ON-DEMAND CONTENT LICENSE AGREEMENT"
        ],
        "Parties": [
            "['BIRCH FIRST GLOBAL INVESTMENTS INC.', 'MA', 'Marketing Affiliate', 'MOUNT KNOWLEDGE HOLDINGS INC.', 'Company']",
            "['EuroMedia Holdings Corp.', 'Rogers', 'Rogers Cable Communications Inc.', 'Licensor']"
        ],
        "Parties-Answer": [
            'Birch First Global Investments Inc. ("Company"); Mount Kowledge Holdings Inc. ("Marketing Affiliate", "MA")',
            'Rogers Cable Communications Inc. ("Rogers"); EuroMedia Holdings Corp. ("Licensor")'
        ],
        "Agreement Date": [
            "['8th day of May 2014', 'May 8, 2014']",
            "['July 11 , 2006']"
        ],
        "Agreement Date-Answer": [
            "5/8/14",
            "7/11/06"
        ],
        "Effective Date": [
            "['This in writing by Company']",
            "['July 11 , 2006']"
        ],
        "Effective Date-Answer": [
            "",
            "7/11/06"
        ],
        "Expiration Date": [
            "['This agreement shall begin upon 18 of this Agreement.']",
            "['The term of terminate on June 30, 2010.']"
        ],
        "Expiration Date-Answer": [
            "12/31/14",
            "6/30/10"
        ],
        "Renewal Term": [
            "['This agreement contained in paragraph 18 of this Agreement.']",
            "['At Rogers\'  herein (the \"Renewal Term\").']"
        ],
        "Renewal Term-Answer": [
            "successive 1 year",
            "2 years"
        ],
        "Notice Period To Terminate Renewal": [
            "['This Agreementr party.']",
            "['Notwithstanding the foregoing, ']"
        ],
        "Notice Period To Terminate Renewal- Answer": [
            "30 days",
            "60 days"
        ],
        "Governing Law": [
            "[oupaiu]",
            "[wowdibpwbdp]"
        ],
        "Governing Law-Answer": [
            "Nevada",
            "Ontario, Canada"
        ],
        "Exclusivity": [
            "[]",
            "[]"
        ],
        "Exclusivity-Answer": [
            "No",
            "No"
        ]
    }

    df = pd.DataFrame(data)
    preprocess = PreprocessData(df)
    df_preprocessed = preprocess.preprocess_data()

    # Test PreprocessData
    assert df_preprocessed.to_dict() == {
        "Document Name": {
            1: "Video-on-demand content license"
        },
        "Parties": {
            1: ['Rogers cable communications inc.','Euromedia holdings corp.']
        },
        "Agreement Date": {
            1: pd.to_datetime("7/11/06")
        },
        "Effective Date": {
            1: pd.to_datetime("7/11/06")
        },
        "Expiration Date": {
            1: pd.to_datetime("6/30/10")
        },
        "Renewal Term (days)": {
            1: 730
        },
        "Notification Renewal (days)": {
            1: 60
        },
        "Governing Law": {
            1: ["Ontario"]
        },
        "Exclusivity": {
            1: "No"
        }
    }

    # Test Providers
    providers = Providers(df_preprocessed)
    assert providers.count_parties().to_dict() == {
        'Party': {0: 'Rogers cable communications inc.', 1: 'Euromedia holdings corp.'},
        'Count': {0: 1, 1: 1}
    }

    # Test RenewalTerm
    renewal_term = RenewalTerm(df_preprocessed, ['Document Name', 'Renewal Term (days)'])
    assert renewal_term.count_group_by('Renewal Term (days)').to_dict() == {
        'Renewal Term (days)': {0: 730},
        'Count': {0: 1}
    }

    # Test EffectiveDates
    effective_dates = EffectiveDates(df_preprocessed, ['Document Name', 'Effective Date'])
    effective_dates.data['Effective Date'] = pd.to_datetime(effective_dates.data['Effective Date'], errors='coerce')

    min_date, min_name = effective_dates.get_min_date_index('Effective Date')
    assert min_date == '11-07-2006'
    assert min_name == 'Video-on-demand content license'

    max_date, max_name = effective_dates.get_max_date_index('Effective Date')
    assert max_date == '11-07-2006'
    assert max_name == 'Video-on-demand content license'

    # Test GoverningLaw
    governing_law = GoverningLaw(df_preprocessed)
    unique_laws = governing_law.unique_governing_laws()
    assert unique_laws == {'Ontario'}
    
    expected_df = pd.DataFrame({
        'Ciudad': ['Ontario'],
        'Pais': ['Canada'],
        'Latitud': [43.7417],
        'Longitud': [-79.3733]
    })
    countries_df = governing_law._get_countries(unique_laws)

    assert countries_df.sort_values(by=['Ciudad']).reset_index(drop=True).equals(
        expected_df.sort_values(by=['Ciudad']).reset_index(drop=True)
    ), "The returned DataFrame does not match the expected values."


    expected_df = pd.DataFrame({
        'Ciudad': ['Ontario'],
        'Pais': ['Canada'],
        'Latitud': [43.7417],
        'Longitud': [-79.3733],
        'Continent': ['NA']
    })
    result_df = governing_law._get_continents(countries_df)

    result_df[['Latitud', 'Longitud']] = result_df[['Latitud', 'Longitud']].round(4)
    expected_df[['Latitud', 'Longitud']] = expected_df[['Latitud', 'Longitud']].round(4)

    for column in expected_df.columns:
        assert result_df[column].sort_values().reset_index(drop=True).equals(
            expected_df[column].sort_values().reset_index(drop=True)
        ), f"Mismatch found in column: {column}"

