"""Streamlit render yardımcıları (bilet kartları, tablo, mini özet)."""
import html

import streamlit as st

from logic import DURUM_GELDI, DURUM_IADE, DURUM_YATTI

_DURUM_METIN_STIL = {
    DURUM_GELDI: ("#059669", "✓", False),
    DURUM_YATTI: ("#94a3b8", "✕", True),
    DURUM_IADE: ("#94a3b8", "↩", False),
}

_DURUM_CLASS_STIL = {
    "won": {"accent": "#10b981", "status": "#059669", "payout": "#059669", "icon": "✓"},
    "pending": {"accent": "#f59e0b", "status": "#d97706", "payout": "#0f172a", "icon": "⏳"},
    "lost": {"accent": "#f43f5e", "status": "#e11d48", "payout": "#94a3b8", "icon": "✕"},
    "refund": {"accent": "#94a3b8", "status": "#64748b", "payout": "#64748b", "icon": "↩"},
}


def _horse_list_inline(at_obj_listesi):
    """Atları ağır rozet kutuları yerine sade, renk kodlu bir satır olarak listeler."""
    parcalar = []
    for at in at_obj_listesi:
        renk, ikon, ustu_cizili = _DURUM_METIN_STIL.get(
            at["durum"], ("#334155", "⏳", False)
        )
        ad = html.escape(str(at["ad"]))
        stil = f"color:{renk};"
        if ustu_cizili:
            stil += " text-decoration:line-through;"
        parcalar.append(f'<span style="{stil}">{ikon} {ad}</span>')
    ayrac = '<span style="color:#cbd5e1;"> · </span>'
    return ayrac.join(parcalar)


def render_mini_summary(df, kupon_bedeli=None):
    """Bir sistem/grup için kompakt kesinleşen/bekleyen/iade özeti basar."""
    if df.empty:
        return

    kesinlesen = df.loc[df["Durum"] == "Kazandı", "Tahmini Kazanç"].sum()
    bekleyen = df.loc[df["Durum"] == "Bekliyor", "Tahmini Kazanç"].sum()
    iade = df.loc[df["Durum"] == "İade", "Tahmini Kazanç"].sum()

    html_out = f"""
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin: 6px 0 14px 0;">
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#059669; text-transform:uppercase;">Kesinleşen</span><br>
            <span style="font-size:14px; font-weight:800; color:#0f172a;">{kesinlesen:,.2f} TL</span>
        </div>
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#d97706; text-transform:uppercase;">Bekleyen Potansiyel</span><br>
            <span style="font-size:14px; font-weight:800; color:#0f172a;">{bekleyen:,.2f} TL</span>
        </div>
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#64748b; text-transform:uppercase;">İade</span><br>
            <span style="font-size:14px; font-weight:800; color:#0f172a;">{iade:,.2f} TL</span>
        </div>
    </div>
    """
    st.markdown(html_out, unsafe_allow_html=True)


def uygula_siralama(df, siralama_secimi):
    """Seçilen sıralama moduna göre DataFrame'i sıralar."""
    if df.empty:
        return df
    if siralama_secimi == "Kazanç (Yüksek → Düşük)":
        return df.sort_values("Tahmini Kazanç", ascending=False)
    if siralama_secimi == "Kazanç (Düşük → Yüksek)":
        return df.sort_values("Tahmini Kazanç", ascending=True)
    if siralama_secimi == "Oran (Yüksek → Düşük)":
        return df.sort_values("Kolon Oranı", ascending=False)
    if siralama_secimi == "Oran (Düşük → Yüksek)":
        return df.sort_values("Kolon Oranı", ascending=True)
    return df


def render_native_bet_slips(df_table):
    """Kombinasyonları sade, dengeli bilet kartları olarak basar."""
    if df_table.empty:
        st.info("Filtreye uygun kombinasyon bulunamadı.")
        return

    cols_per_slip_row = 3
    rows = [
        df_table.iloc[i: i + cols_per_slip_row]
        for i in range(0, len(df_table), cols_per_slip_row)
    ]

    for row_chunk in rows:
        slip_cols = st.columns(len(row_chunk))
        for col_idx, (_, row) in enumerate(row_chunk.iterrows()):
            stil = _DURUM_CLASS_STIL.get(row["DurumClass"], _DURUM_CLASS_STIL["pending"])
            horse_list = _horse_list_inline(row["AtObjeleri"])

            with slip_cols[col_idx]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="slip-card" style="border-left-color:{stil['accent']};">
                            <div class="slip-card-top">
                                <span class="slip-card-sistem">{row['Sistem']}</span>
                                <span class="slip-card-status" style="color:{stil['status']};">{stil['icon']} {row['Durum']}</span>
                            </div>
                            <div class="slip-card-horses">{horse_list}</div>
                            <div class="slip-card-bottom">
                                <span class="slip-card-oran">Oran <strong>{row['Kolon Oranı']:.2f}</strong></span>
                                <span class="slip-card-payout" style="color:{stil['payout']};">{row['Tahmini Kazanç']:,.2f} TL</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def render_modern_table(df_table, show_system_col=False):
    """Kombinasyonları sade bir HTML tablo olarak döndürür."""
    if df_table.empty:
        return (
            '<div style="padding:24px; text-align:center; color:#64748b;'
            ' font-size:13px;">Filtreye uygun kolon bulunamadı.</div>'
        )

    badge_icons = {"won": "✓", "pending": "⏳", "lost": "✕", "refund": "↩"}

    html_out = '<div class="table-responsive-wrapper"><div class="modern-table-container"><table class="modern-table"><thead><tr>'
    if show_system_col:
        html_out += '<th style="width: 100px;">SİSTEM</th>'
    html_out += "<th>KOMBİNASYONDAKİ ATLAR</th>"
    html_out += '<th style="width: 110px; text-align:right;">ORAN</th>'
    html_out += '<th style="width: 130px; text-align:center;">DURUM</th>'
    html_out += (
        '<th style="width: 160px; text-align:right;">KAZANÇ / POTANSİYEL'
        " (TL)</th>"
    )
    html_out += "</tr></thead><tbody>"

    for _, row in df_table.iterrows():
        row_class = f"row-{row['DurumClass']}"
        html_out += f'<tr class="{row_class}">'

        if show_system_col:
            html_out += f'<td style="font-weight:700; color:#475569;">{html.escape(row["Sistem"])}</td>'

        horse_list = _horse_list_inline(row["AtObjeleri"])
        html_out += f'<td><div style="line-height:1.7;">{horse_list}</div></td>'

        html_out += f'<td style="text-align:right; font-weight:700;">{row["Kolon Oranı"]:.2f}</td>'

        badge_icon = badge_icons.get(row["DurumClass"], "⏳")
        html_out += f'<td style="text-align:center;"><span class="status-badge {row["DurumClass"]}">{badge_icon} {html.escape(row["Durum"])}</span></td>'

        won_class = "won" if row["DurumClass"] == "won" else ""
        html_out += f'<td style="text-align:right;" class="payout-val {won_class}">{row["Tahmini Kazanç"]:,.2f} TL</td>'
        html_out += "</tr>"

    html_out += "</tbody></table></div></div>"
    return html_out
