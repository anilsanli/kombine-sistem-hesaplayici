"""Streamlit render yardımcıları (bilet kartları, tablo, mini özet)."""
import html

import streamlit as st

from logic import at_chip_bilgisi


def _chips_html(at_obj_listesi):
    chips_html = ""
    for at in at_obj_listesi:
        chip_class, chip_icon = at_chip_bilgisi(at["durum"])
        at_adi = html.escape(str(at["ad"]))
        bahis_turu = html.escape(str(at["bahis_turu"]))
        chips_html += (
            f'<span class="{chip_class}">{chip_icon} {at_adi} '
            f"({bahis_turu})</span>"
        )
    return chips_html


def render_mini_summary(df, kupon_bedeli=None):
    """Bir sistem/grup için kompakt kesinleşen/bekleyen/iade özeti basar."""
    if df.empty:
        return

    kesinlesen = df.loc[df["Durum"] == "Kazandı", "Tahmini Kazanç"].sum()
    bekleyen = df.loc[df["Durum"] == "Bekliyor", "Tahmini Kazanç"].sum()
    iade = df.loc[df["Durum"] == "İade", "Tahmini Kazanç"].sum()

    html_out = f"""
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin: 6px 0 14px 0;">
        <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#047857; text-transform:uppercase;">Kesinleşen</span><br>
            <span style="font-size:14px; font-weight:800; color:#065f46;">{kesinlesen:,.2f} TL</span>
        </div>
        <div style="background:#fefce8; border:1px solid #fde68a; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#a16207; text-transform:uppercase;">Bekleyen Potansiyel</span><br>
            <span style="font-size:14px; font-weight:800; color:#854d0e;">{bekleyen:,.2f} TL</span>
        </div>
        <div style="background:#f1f5f9; border:1px solid #e2e8f0; border-radius:8px; padding:6px 12px;">
            <span style="font-size:10.5px; font-weight:700; color:#475569; text-transform:uppercase;">İade</span><br>
            <span style="font-size:14px; font-weight:800; color:#334155;">{iade:,.2f} TL</span>
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
    """Kombinasyonları dijital bilet kartları olarak basar."""
    if df_table.empty:
        st.info("Filtreye uygun kombinasyon bulunamadı.")
        return

    border_colors = {"won": "#10b981", "pending": "#f59e0b", "lost": "#f43f5e", "refund": "#94a3b8"}
    payout_colors = {"won": "#10b981", "pending": "#0f172a", "lost": "#64748b", "refund": "#475569"}

    cols_per_slip_row = 3
    rows = [
        df_table.iloc[i: i + cols_per_slip_row]
        for i in range(0, len(df_table), cols_per_slip_row)
    ]

    for row_chunk in rows:
        slip_cols = st.columns(len(row_chunk))
        for col_idx, (_, row) in enumerate(row_chunk.iterrows()):
            border_color = border_colors.get(row["DurumClass"], "#94a3b8")
            payout_color = payout_colors.get(row["DurumClass"], "#0f172a")

            with slip_cols[col_idx]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="border-left: 4px solid {border_color}; padding-left: 8px; margin-bottom: 8px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:12px; font-weight:800; color:#334155; text-transform:uppercase; letter-spacing:0.04em;">{row['Sistem']}</span>
                            {row['BadgeHTML']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    chips = _chips_html(row["AtObjeleri"])
                    st.markdown(
                        f'<div style="margin: 10px 0 12px 0; min-height: 48px; display:flex; flex-wrap:wrap; align-items:center;">{chips}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div style="display:flex; justify-content:space-between; align-items:flex-end; border-top:1.5px dashed #e2e8f0; padding-top:8px; margin-top:4px;">
                            <div>
                                <div style="font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase;">KOLON ORANI</div>
                                <div style="font-size:14px; font-weight:800; color:#0f172a;">{row['Kolon Oranı']:.2f}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase;">KAZANÇ / POTANSİYEL</div>
                                <div style="font-size:16px; font-weight:800; color:{payout_color};">{row['Tahmini Kazanç']:,.2f} TL</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def render_modern_table(df_table, show_system_col=False):
    """Kombinasyonları modern bir HTML tablo olarak döndürür."""
    if df_table.empty:
        return (
            '<div style="padding:24px; text-align:center; color:#64748b;'
            ' font-size:13px;">Filtreye uygun kolon bulunamadı.</div>'
        )

    badge_icons = {"won": "✅", "pending": "⏳", "lost": "❌", "refund": "↩️"}

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

        chips = _chips_html(row["AtObjeleri"])
        html_out += f'<td><div style="display:flex; flex-wrap:wrap; align-items:center;">{chips}</div></td>'

        html_out += f'<td style="text-align:right; font-weight:700;">{row["Kolon Oranı"]:.2f}</td>'

        badge_icon = badge_icons.get(row["DurumClass"], "⏳")
        html_out += f'<td style="text-align:center;"><span class="status-badge {row["DurumClass"]}">{badge_icon} {html.escape(row["Durum"])}</span></td>'

        won_class = "won" if row["DurumClass"] == "won" else ""
        html_out += f'<td style="text-align:right;" class="payout-val {won_class}">{row["Tahmini Kazanç"]:,.2f} TL</td>'
        html_out += "</tr>"

    html_out += "</tbody></table></div></div>"
    return html_out
