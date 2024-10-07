import pandas as pd
from services.normalize import PreprocessData

def test_preprocess_data():
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

