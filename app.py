from itertools import combinations
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Hipodrom Sistem Bahis Simülatörü",
    page_icon="🏇",
    layout="wide",
)

# Custom CSS - Dark Mode Override & Tooltip / Popover Fixes
st.markdown(
    """
    <style>
    /* 1. UYGULAMA VE GENEL METİNLER */
    .stApp {
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #1f2937 !important;
    }

    /* 2. TOOLTIP / BİLGİ BALONCUKLARI VE HELP SİMGELERİ KESİN FIX */
    div[data-baseweb="tooltip"],
    div[role="tooltip"],
    div[data-testid="stTooltipContent"],
    .stTooltipHoverTarget {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="tooltip"] *,
    div[role="tooltip"] *,
    div[data-testid="stTooltipContent"] * {
        background-color: transparent !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Help simgesi ikonu (?) */
    div[data-testid="stMarkdownContainer"] svg,
    div[data-testid="stTooltipHoverTarget"] svg {
        fill: #64748b !important;
    }

    /* 3. INPUT, SELECTBOX & NUMBER INPUT KUTULARI */
    div[data-baseweb="input"], 
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    input, select, textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    /* Eksi/Artı Butonları */
    div[data-testid="stNumberInput"] button,
    div[data-testid="stNumberInputContainer"] button,
    button[aria-label="Decrease value"],
    button[aria-label="Increase value"] {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    div[data-testid="stNumberInput"] button *,
    button[aria-label="Decrease value"] *,
    button[aria-label="Increase value"] * {
        color: #0f172a !important;
        fill: #0f172a !important;
        stroke: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    /* 4. DROPDOWN (AÇILIR MENÜ) FIX */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[data-baseweb="popover"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    li[role="option"], div[role="option"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    li[role="option"]:hover, 
    li[role="option"][aria-selected="true"],
    div[role="option"]:hover {
        background-color: #f1f5f9 !important;
        color: #e11d48 !important;
        -webkit-text-fill-color: #e11d48 !important;
    }

    /* 5. EXPANDER FIX */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
    }

    div[data-testid="stExpander"] details summary {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] details summary * {
        color: #0f172a !important;
    }

    /* 6. BUTON HİZALAMALARI VE SIFIRLA BUTONU */
    div.stButton > button,
    div.stButton > button *,
    div.stButton > button div,
    div.stButton > button p {
        background-color: #e11d48 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
    }

    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
    }

    div.stButton > button:hover,
    div.stButton > button:hover * {
        background-color: #be123c !important;
        color: #ffffff !important;
    }

    /* BİLGİ KARTLARI */
    .horse-card {
        background-color: #ffffff !important;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #e11d48;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .summary-banner {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #e11d48;
        border-radius: 8px;
        padding: 14px 24px;
        margin-top: 15px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .summary-item {
        font-size: 16px;
        font-weight: 600;
        color: #1f2937 !important;
    }
    .summary-value {
        color: #e11d48 !important;
        font-weight: 700;
    }
    .total-payout-box {
        background-color: #0f172a !important;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
    }
    .total-payout-box h3, .total-payout-box h1, .total-payout-box p, .total-payout-box span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE BAŞLANGIÇ DEĞERLERİ & SIFIRLAMA MANTIĞI
# ---------------------------------------------------------
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False


def sifirla():
    st.session_state["radio_col_count"] = 4
    st.session_state["sys1"] = True
    st.session_state["sys2"] = True
    st.session_state["sys3"] = True
    st.session_state["sys4"] = False
    st.session_state["num_misli"] = 1

    for i in range(4):
        st.session_state[f"name_{i}"] = ""
        st.session_state[f"type_{i}"] = "Ganyan"
        st.session_state[f"oran_{i}"] = 1.00
        st.session_state[f"status_{i}"] = "Bekliyor / Geldi"


st.title("🏇 Hipodrom Sistem Bahis Hesaplayıcı")
st.caption(
    "Kombine kuponlarınızda sistem seçeneklerine göre tüm olası kombinasyonları ve kazançları inceleyin."
)

# ---------------------------------------------------------
# ADIM 1: KUPON YAPISI VE SİSTEM SEÇİMİ
# ---------------------------------------------------------
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    st.markdown("### 1. Kupon ve Sistem Yapısı")
with head_col2:
    st.button("🔄 Kuponu Sıfırla", on_click=sifirla, use_container_width=True)

col_setup1, col_setup2, col_setup3 = st.columns([1, 2, 1.5])

with col_setup1:
    col_count = st.radio(
        "Kuponda Kaç At Var?",
        options=[2, 3, 4],
        index=2,
        horizontal=True,
        key="radio_col_count",
        help="Sistem bahsi için en az 2, en fazla 4 at seçilmelidir.",
    )

with col_setup2:
    st.write("Sistem Seçimi")
    sys_cols = st.columns(4)

    sistem_1 = sys_cols[0].checkbox("Sistem 1", value=True, key="sys1")
    sistem_2 = sys_cols[1].checkbox("Sistem 2", value=True, key="sys2")
    sistem_3 = sys_cols[2].checkbox(
        "Sistem 3", value=(col_count >= 3), disabled=(col_count < 3), key="sys3"
    )
    sistem_4 = sys_cols[3].checkbox(
        "Sistem 4", value=(col_count == 4), disabled=(col_count < 4), key="sys4"
    )

with col_setup3:
    misli = st.number_input(
        "Misli Seçimi (Katsayı)",
        min_value=1,
        value=1,
        step=1,
        key="num_misli",
        help="Bilet tutarınız ve kazancınız seçtiğiniz misli ile çarpılır.",
    )
    kolon_birim_fiyati = 1.0


def hesapla_bahis_sayisi(at_sayisi):
    sistem_haritasi = {
        1: sistem_1,
        2: sistem_2,
        3: sistem_3 and at_sayisi >= 3,
        4: sistem_4 and at_sayisi == 4,
    }
    toplam_kolon = 0
    at_dummy = list(range(at_sayisi))
    for r, aktif in sistem_haritasi.items():
        if aktif and r <= at_sayisi:
            toplam_kolon += len(list(combinations(at_dummy, r)))
    return toplam_kolon


bahis_sayisi = hesapla_bahis_sayisi(col_count)
kupon_bedeli = bahis_sayisi * kolon_birim_fiyati * misli

st.markdown(
    f"""
    <div class="summary-banner">
        <div class="summary-item">📌 Bahis Sayısı: <span class="summary-value">{bahis_sayisi} Kolon</span></div>
        <div class="summary-item">✖️ Misli: <span class="summary-value">{misli} Misli</span></div>
        <div class="summary-item">💳 Kupon Bedeli: <span class="summary-value">{kupon_bedeli:,.2f} TL</span></div>
    </div>
""",
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------
# ADIM 2: AT DETAYLARI VE ORAN GİRDİLERİ
# ---------------------------------------------------------
st.markdown("### 2. At ve Koşu Detayları")

bahis_turleri = [
    "Ganyan",
    "İlk 2",
    "İlk 3",
    "İlk 4",
    "İkili Bahis",
    "Sıralı İkili Bahis",
]
at_data = []

grid_cols = st.columns(col_count)

for i in range(col_count):
    if f"name_{i}" not in st.session_state:
        st.session_state[f"name_{i}"] = ""
    if f"type_{i}" not in st.session_state:
        st.session_state[f"type_{i}"] = "Ganyan"
    if f"oran_{i}" not in st.session_state:
        st.session_state[f"oran_{i}"] = [5.50, 1.70, 25.00, 12.00][
            i if i < 4 else 0
        ]
    if f"status_{i}" not in st.session_state:
        st.session_state[f"status_{i}"] = "Bekliyor / Geldi"

    with grid_cols[i]:
        st.markdown(
            f"""
        <div class="horse-card">
            <h4 style="margin:0; color:#1f2937;">{i + 1}. At Seçimi</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )

        at_adi = st.text_input(
            "At Adı (İsteğe Bağlı)",
            placeholder=f"{i + 1}. At",
            key=f"name_{i}",
        )
        bahis_turu = st.selectbox(
            "Bahis Türü (İsteğe Bağlı)",
            options=bahis_turleri,
            key=f"type_{i}",
        )
        oran = st.number_input(
            "Oran (Zorunlu) *",
            min_value=1.00,
            step=0.10,
            key=f"oran_{i}",
        )
        durum = st.selectbox(
            "Sonuç Durumu",
            ["Bekliyor / Geldi", "Yattı (Kaybetti)", "Koşmaz (İade)"],
            key=f"status_{i}",
        )

        label_name = at_adi.strip() if at_adi.strip() != "" else f"{i + 1}. At"

        at_data.append(
            {
                "id": i + 1,
                "ad": label_name,
                "bahis_turu": bahis_turu,
                "oran": oran,
                "durum": durum,
            }
        )

st.divider()


# ---------------------------------------------------------
# KOMBİNASYON HESAPLAMA MOTORU
# ---------------------------------------------------------
def hesapla_sistem_gruplari(at_listesi):
    sistem_haritasi = {
        1: sistem_1,
        2: sistem_2,
        3: sistem_3 and col_count >= 3,
        4: sistem_4 and col_count == 4,
    }

    gruplanmis_kombinasyonlar = {}

    for r, aktif in sistem_haritasi.items():
        if aktif and r <= len(at_listesi):
            kombinasyon_listesi = []

            for comb in combinations(at_listesi, r):
                kolon_orani = 1.0
                kazandi_mi = True

                at_detaylari = []
                for at in comb:
                    at_detaylari.append(f"{at['ad']} ({at['bahis_turu']})")
                    if at["durum"] == "Yattı (Kaybetti)":
                        kazandi_mi = False
                        kolon_orani *= 0
                    elif at["durum"] == "Koşmaz (İade)":
                        kolon_orani *= 1.0
                    else:
                        kolon_orani *= at["oran"]

                kombinasyon_listesi.append(
                    {
                        "Kombinasyon Detayı": " ➔ ".join(at_detaylari),
                        "Kolon Oranı": (
                            round(kolon_orani, 2) if kazandi_mi else 0.00
                        ),
                        "Durum": (
                            "✅ Kazandı"
                            if (kazandi_mi and kolon_orani > 0)
                            else (
                                "❌ Kaybetti"
                                if not kazandi_mi
                                else "⏳ Bekliyor/İade"
                            )
                        ),
                        "Tahmini Kazanç": (
                            round(kolon_orani * misli, 2) if kazandi_mi else 0.00
                        ),
                    }
                )

            gruplanmis_kombinasyonlar[r] = pd.DataFrame(kombinasyon_listesi)

    return gruplanmis_kombinasyonlar


def highlight_rows(row):
    if row["Durum"] == "✅ Kazandı":
        return [
            "background-color: #ecfdf5; color: #065f46; font-weight: 500;"
        ] * len(row)
    elif row["Durum"] == "❌ Kaybetti":
        return [
            "background-color: #fef2f2; color: #991b1b; opacity: 0.8;"
        ] * len(row)
    return [""] * len(row)


# ---------------------------------------------------------
# ADIM 3: SONUÇLAR VE KOMBİNASYON LİSTESİ
# ---------------------------------------------------------
st.markdown("### 3. Kombinasyon ve İkramiye Detayları")

gruplar = hesapla_sistem_gruplari(at_data)

if gruplar:
    toplam_kazanc = 0.0

    for sistem_no, df in gruplar.items():
        grup_kazanc = df["Tahmini Kazanç"].sum()
        toplam_kazanc += grup_kazanc
        kazanan_sayisi = len(df[df["Durum"] == "✅ Kazandı"])

        expander_title = f"🎯 Sistem {sistem_no} ({sistem_no}'li Kombinasyonlar)  |  {len(df)} Kolon  |  Kazanan: {kazanan_sayisi}  |  Grup Kazancı: {grup_kazanc:,.2f} TL"

        with st.expander(expander_title, expanded=True):
            styled_df = df.style.apply(highlight_rows, axis=1).format(
                {"Kolon Oranı": "{:.2f}", "Tahmini Kazanç": "{:,.2f} TL"}
            )

            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Kombinasyon Detayı": st.column_config.TextColumn(
                        "Kombinasyondaki Atlar", width="large"
                    ),
                    "Kolon Oranı": st.column_config.NumberColumn(
                        "Kolon Oranı", format="%.2f"
                    ),
                    "Durum": st.column_config.TextColumn(
                        "Sonuç", width="small"
                    ),
                    "Tahmini Kazanç": st.column_config.TextColumn(
                        "Tahmini Kazanç (TL)", width="medium"
                    ),
                },
            )

    net_kar_zarar = toplam_kazanc - kupon_bedeli
    if net_kar_zarar > 0:
        kar_durum_metni = (
            f"<span style='color:#34d399;'>Net Kâr: +{net_kar_zarar:,.2f} TL</span>"
        )
    elif net_kar_zarar < 0:
        kar_durum_metni = f"<span style='color:#f87171;'>Net Zarar: {net_kar_zarar:,.2f} TL</span>"
    else:
        kar_durum_metni = (
            "<span style='color:#9ca3af;'>Başabaş (0.00 TL)</span>"
        )

    st.markdown(
        f"""
        <div class="total-payout-box">
            <h3 style="margin:0; font-size: 20px; color: #a5f3fc; font-weight:500;">🏆 TOPLAM KAZANÇ DURUMU</h3>
            <h1 style="margin:12px 0; font-size: 42px; color: #34d399;">{toplam_kazanc:,.2f} TL</h1>
            <p style="margin:0; font-size: 16px; color: #cbd5e1;">Kupon Bedeli: {kupon_bedeli:,.2f} TL &nbsp;|&nbsp; {kar_durum_metni}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

else:
    st.info(
        "Lütfen yukarıdan en az bir sistem seçeneğini (Sistem 1, 2 vb.) işaretleyin."
    )