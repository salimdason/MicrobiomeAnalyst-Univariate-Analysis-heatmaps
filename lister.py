import os

filePool = [
            filename
            for filename in os.listdir("ad_data")
            if filename.endswith(".csv")
            and filename.__contains__("_AD_versus_")
        ]

for file in filePool:
    splits = file.split("_")
    period = splits[0].split('m')[0] + splits[3].split('m')[0]
    # print(period)
    pass


heads2mVersus6m = [
            "Species",
            "2AD-2m_S6",
            "4AD-2m_S2",
            "5AD-2m_S7",
            "8AD-2m_S8",
            "9AD-2m_S9",
            "10AD-2m_S10",
            "2AD-6m_S5",
            "4AD-6m_S7",
            "5AD-6m_S6",
            "8AD-6m_S8",
            "9AD-6m_S9",
            "10AD-6m_S10",
        ]

heads2mVersus12m = [
            "Species",
            "2AD-2m_S6",
            "4AD-2m_S2",
            "5AD-2m_S7",
            "8AD-2m_S8",
            "9AD-2m_S9",
            "10AD-2m_S10",
            "2AD-12m_S7",
            "5AD-12m_S8",
            "6AD-12m_S9",
            "8AD-12m_S10",
            "9AD-12m_S11",
            "10AD-12m_S12",
        ]

heads6MVersus12m = [
            "Species",
            "2AD-6m_S5",
            "4AD-6m_S7",
            "5AD-6m_S6",
            "8AD-6m_S8",
            "9AD-6m_S9",
            "10AD-6m_S10",
            "2AD-12m_S7",
            "5AD-12m_S8",
            "6AD-12m_S9",
            "8AD-12m_S10",
            "9AD-12m_S11",
            "10AD-12m_S12",
        ]




with open('data/metaphlan_matrix.csv') as mf:
    h = [x.strip() for x in mf.readlines()[0].split('\t')]



# print(h)
for x, y in enumerate(h):
    # if y == '5AD-6m_S6':
    print(x, y, sep='------->')

    # t = h[19:25] + h[31:]
    # print(len(t))
    # print(t)