# -*- coding: utf-8 -*-


from collections import OrderedDict

from iapc.tools import getSetting, selectDialog, setSetting


# selectRegion -----------------------------------------------------------------

regions = OrderedDict(
    (
        ("DZ", "Algeria, الجزائر"),
        ("AR", "Argentina"),
        ("AU", "Australia"),
        ("AT", "Austria, Österreich"),
        ("AZ", "Azerbaijan"),
        ("BH", "Bahrain"),
        ("BD", "Bangladesh, বাংলাদেশ"),
        ("BY", "Belarus"),
        ("BE", "Belgium"),
        ("BO", "Bolivia"),
        ("BA", "Bosnia and Herzegovina"),
        ("BR", "Brazil, Brasil"),
        ("BG", "Bulgaria, България"),
        ("CA", "Canada"),
        ("CL", "Chile"),
        ("CO", "Colombia"),
        ("CR", "Costa Rica"),
        ("HR", "Croatia, Hrvatska"),
        ("CY", "Cyprus"),
        ("CZ", "Czechia, Česko"),
        ("DK", "Denmark, Danmark"),
        ("DO", "Dominican Republic, República Dominicana"),
        ("EC", "Ecuador"),
        ("EG", "Egypt, مصر"),
        ("SV", "El Salvador"),
        ("EE", "Estonia, Eesti"),
        ("FI", "Finland"),
        ("FR", "France"),
        ("GE", "Georgia, საქართველო"),
        ("DE", "Germany, Deutschland"),
        ("GH", "Ghana"),
        ("GR", "Greece, Ελλάδα"),
        ("GT", "Guatemala"),
        ("HN", "Honduras"),
        ("HK", "Hong Kong"),
        ("HU", "Hungary, Magyarország"),
        ("IS", "Iceland, Ísland"),
        ("IN", "India"),
        ("ID", "Indonesia"),
        ("IQ", "Iraq"),
        ("IE", "Ireland"),
        ("IL", "Israel"),
        ("IT", "Italy, Italia"),
        ("JM", "Jamaica"),
        ("JP", "Japan, 日本"),
        ("JO", "Jordan, الأردن"),
        ("KZ", "Kazakhstan"),
        ("KE", "Kenya"),
        ("KW", "Kuwait, الكويت"),
        ("LV", "Latvia, Latvija"),
        ("LB", "Lebanon"),
        ("LY", "Libya"),
        ("LI", "Liechtenstein"),
        ("LT", "Lithuania, Lietuva"),
        ("LU", "Luxembourg"),
        ("MY", "Malaysia"),
        ("MT", "Malta"),
        ("MX", "Mexico, México"),
        ("ME", "Montenegro, Црна Гора"),
        ("MA", "Morocco"),
        ("NP", "Nepal, नेपाल"),
        ("NL", "Netherlands, Nederland"),
        ("NZ", "New Zealand"),
        ("NI", "Nicaragua"),
        ("NG", "Nigeria"),
        ("MK", "North Macedonia, Македонија"),
        ("NO", "Norway"),
        ("OM", "Oman, عمان"),
        ("PK", "Pakistan"),
        ("PA", "Panama, Panamá"),
        ("PG", "Papua New Guinea"),
        ("PY", "Paraguay"),
        ("PE", "Peru"),
        ("PH", "Philippines"),
        ("PL", "Poland, Polska"),
        ("PT", "Portugal"),
        ("PR", "Puerto Rico"),
        ("QA", "Qatar, قطر"),
        ("RO", "Romania, România"),
        ("RU", "Russia, Россия"),
        ("SA", "Saudi Arabia, العربية السعودية"),
        ("SN", "Senegal, Sénégal"),
        ("RS", "Serbia, Србија"),
        ("SG", "Singapore"),
        ("SK", "Slovakia, Slovensko"),
        ("SI", "Slovenia, Slovenija"),
        ("ZA", "South Africa"),
        ("KR", "South Korea, 한국"),
        ("ES", "Spain, España"),
        ("LK", "Sri Lanka"),
        ("SE", "Sweden, Sverige"),
        ("CH", "Switzerland"),
        ("TW", "Taiwan, 台灣"),
        ("TZ", "Tanzania"),
        ("TH", "Thailand, ประเทศไทย"),
        ("TN", "Tunisia, تونس"),
        ("TR", "Turkey, Türkiye"),
        ("UG", "Uganda"),
        ("UA", "Ukraine, Україна"),
        ("AE", "United Arab Emirates, دولة الإمارات العربية المتحدة"),
        ("GB", "United Kingdom"),
        ("US", "United States"),
        ("UY", "Uruguay"),
        ("VE", "Venezuela"),
        ("VN", "Vietnam, Việt Nam"),
        ("YE", "Yemen, اليَمَن"),
        ("ZW", "Zimbabwe")
    )
)

def selectRegion():
    region = getSetting("regional.region", str)
    keys = list(regions.keys())
    values = list(regions.values())
    preselect = keys.index(region) if region in regions else -1
    if (
        (
            index := selectDialog(
                [f"({k})\t{v}" for k, v in regions.items()],
                heading=40123,
                preselect=preselect
            )
        ) >= 0
    ):
        setSetting("regional.region", keys[index], str)
        setSetting("regional.region.text", values[index], str)
