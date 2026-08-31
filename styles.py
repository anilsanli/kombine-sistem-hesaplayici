"""Uygulama genelinde kullanılan özel CSS."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f1f5f9 !important;
    color: #0f172a;
}

/* Hero Banner */
.hero-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 24px;
    color: #0f172a;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
}
.hero-title {
    font-size: 21px;
    font-weight: 800;
    margin: 0;
    color: #0f172a !important;
    display: flex;
    align-items: center;
    gap: 10px;
}
.hero-title .hero-icon-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 11px;
    background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
    font-size: 19px;
    flex-shrink: 0;
}
.hero-subtitle {
    font-size: 13.5px;
    color: #64748b !important;
    margin-top: 6px;
    margin-bottom: 0;
}

/* Segmented / Pill Radio Stili */
div[data-testid="stRadio"] > div {
    background-color: #f1f5f9;
    padding: 3px;
    border-radius: 10px;
    display: flex;
    gap: 3px;
    border: 1px solid #e2e8f0;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background: transparent;
    border-radius: 7px;
    padding: 5px 12px !important;
    margin: 0 !important;
    transition: all 0.2s ease;
    cursor: pointer;
    border: none !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: #0f172a !important;
}
div[data-testid="stRadio"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 700 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] input {
    display: none !important;
}

/* Sistem Seçimi Checkbox Rozetleri */
.system-pill div[data-testid="stCheckbox"] {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 6px 4px;
    transition: all 0.15s ease;
    text-align: center;
}
.system-pill div[data-testid="stCheckbox"]:has(input:checked) {
    background: #fff1f2 !important;
    border-color: #e11d48 !important;
}
.system-pill div[data-testid="stCheckbox"]:has(input:checked) span {
    color: #e11d48 !important;
    font-weight: 700 !important;
}

/* Finansal Kokpit Çubuğu */
.integrated-kpi-bar {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #f8fafc !important;
    border-radius: 12px;
    padding: 14px 20px;
    margin-top: 14px;
    border: 1px solid #e2e8f0;
    flex-wrap: wrap;
    gap: 12px;
}
.kpi-segment {
    display: flex;
    flex-direction: column;
    gap: 2px;
    text-align: center;
}
.kpi-title {
    font-size: 11.5px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8 !important;
}
.kpi-number {
    font-size: 19px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
}
.kpi-number.accent {
    color: #e11d48 !important;
}
.kpi-number.highlight {
    color: #e11d48 !important;
    font-size: 22px !important;
}
.kpi-divider {
    width: 1px;
    height: 32px;
    background: #e2e8f0;
}

/* Koşu & Bilet Kartı Konteyneri */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff;
    border-radius: 14px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.2s ease-in-out;
    padding: 4px;
    margin-bottom: 8px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #cbd5e1 !important;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08) !important;
}

/* Kart Başlığı */
.card-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    margin-bottom: 10px;
    border-bottom: 1px solid #f1f5f9;
}
.race-pill {
    background: #f1f5f9;
    color: #475569 !important;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
}
.selection-title {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a !important;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Sekmeler (Tabs) */
button[data-baseweb="tab"] {
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #e11d48 !important;
    border-bottom-color: #e11d48 !important;
}

/* Bilet Kartı (Sade) */
.slip-card {
    border-left: 3px solid transparent;
    padding: 2px 4px 2px 12px;
}
.slip-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.slip-card-sistem {
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.slip-card-status {
    font-size: 11.5px;
    font-weight: 700;
    white-space: nowrap;
}
.slip-card-horses {
    font-size: 13px;
    line-height: 1.8;
    color: #334155;
    margin-bottom: 14px;
    min-height: 24px;
}
.slip-card-bottom {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding-top: 10px;
    border-top: 1px solid #f1f5f9;
}
.slip-card-oran {
    font-size: 11.5px;
    color: #94a3b8;
}
.slip-card-oran strong {
    font-size: 13px;
    color: #475569;
    font-weight: 700;
}
.slip-card-payout {
    font-size: 19px;
    font-weight: 800;
}

/* Modern Tablo Formatı */
.table-responsive-wrapper {
    width: 100%;
    overflow-x: auto;
    display: flex;
    justify-content: flex-start;
    margin-top: 10px;
}
.modern-table-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow-y: auto;
    max-height: 440px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    display: inline-block;
    min-width: 650px;
    width: 100%;
}
.modern-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    text-align: left;
}
.modern-table th {
    background: #f8fafc;
    color: #64748b;
    font-weight: 700;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 12px 16px;
    border-bottom: 1.5px solid #e2e8f0;
    position: sticky;
    top: 0;
    z-index: 10;
}
.modern-table td {
    padding: 11px 16px;
    border-bottom: 1px solid #e2e8f0;
    color: #1e293b;
    vertical-align: middle;
}

.modern-table tbody tr.row-won {
    background-color: #ecfdf5 !important;
}
.modern-table tbody tr.row-won:hover {
    background-color: #d1fae5 !important;
}
.modern-table tbody tr.row-pending {
    background-color: #ffffff !important;
}
.modern-table tbody tr.row-pending:hover {
    background-color: #f8fafc !important;
}
.modern-table tbody tr.row-lost {
    background-color: #fff1f2 !important;
    opacity: 0.85;
}
.modern-table tbody tr.row-lost:hover {
    background-color: #ffe4e6 !important;
}
.modern-table tbody tr.row-refund {
    background-color: #f8fafc !important;
    opacity: 0.9;
}
.modern-table tbody tr.row-refund:hover {
    background-color: #f1f5f9 !important;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 700;
}
.status-badge.won {
    background: #ecfdf5;
    color: #059669;
}
.status-badge.pending {
    background: #fffbeb;
    color: #d97706;
}
.status-badge.lost {
    background: #fff1f2;
    color: #e11d48;
}
.status-badge.refund {
    background: #f1f5f9;
    color: #64748b;
}
.payout-val {
    font-weight: 800;
    color: #0f172a;
}
.payout-val.won {
    color: #16a34a;
}

/* Form Elemanları */
div[data-baseweb="input"] {
    background-color: #f8fafc !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #e11d48 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.12) !important;
}
div[data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    margin-top: 8px !important;
}
div[data-testid="stExpander"] summary {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #64748b !important;
}

/* Butonlar */
div.stButton > button {
    background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(225, 29, 72, 0.2) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(225, 29, 72, 0.3) !important;
}

/* İpucu / Bilgi Banner (tek tip, sakin görünüm; renk yalnızca sol kenarlıkta) */
.helper-banner {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #94a3b8;
    border-radius: 10px;
    padding: 9px 14px;
    margin-bottom: 14px;
    font-size: 12.5px;
    color: #475569;
    display: flex;
    align-items: center;
    gap: 8px;
}
.helper-banner strong {
    color: #1e293b;
}

/* İkramiye Özet Hero Paneli */
.payout-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 28px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 28px -8px rgba(15, 23, 42, 0.18);
}
.payout-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 16px;
    align-items: stretch;
}
.payout-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    transition: all 0.2s ease;
}
.payout-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.12);
}
.payout-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.payout-amount {
    font-size: 30px;
    font-weight: 800;
    margin: 0;
    line-height: 1.1;
}

/* Yasal Uyarı Kutusu */
.legal-box {
    background-color: #fffbeb;
    border: 1px solid #fef3c7;
    border-left: 5px solid #f59e0b;
    padding: 16px 20px;
    border-radius: 12px;
    margin-top: 28px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.05);
}
.legal-title {
    margin: 0;
    font-size: 13.5px;
    color: #b45309 !important;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}
.legal-text {
    margin-top: 6px;
    margin-bottom: 0;
    font-size: 12px;
    color: #78350f !important;
    line-height: 1.6;
}

/* Footer */
.footer-card {
    text-align: center;
    padding: 24px 0 10px 0;
    color: #64748b;
    font-size: 13px;
}
.footer-link {
    color: #e11d48;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.15s;
}
.footer-link:hover {
    color: #be123c;
    text-decoration: underline;
}

/* Mobil ekranlar için sıkışıklığı azaltan düzenlemeler */
@media (max-width: 640px) {
    .hero-title {
        font-size: 19px;
    }
    .hero-subtitle {
        font-size: 12.5px;
    }
    .integrated-kpi-bar {
        justify-content: flex-start;
        padding: 14px;
    }
    .kpi-segment {
        flex: 1 1 40%;
    }
    .payout-amount {
        font-size: 24px;
    }
    .modern-table-container {
        min-width: 0;
    }
    /* At Sayısı / Aktif Sistemler / Misli satırını mobilde 3 dar sütuna
       sıkıştırmak yerine tam genişlikte alt alta dizer. */
    div[data-testid="stElementContainer"]:has(.mobile-stack-anchor) + div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    div[data-testid="stElementContainer"]:has(.mobile-stack-anchor) + div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Aktif Sistemler satırındaki 7 checkbox'ı (tam genişlik kazandıktan
       sonra) yatay ve sarmalı (wrap) bir pill grubu olarak tutar. */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)):not(:has(> div[data-testid="stColumn"]:nth-child(8))) {
        flex-wrap: wrap !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)):not(:has(> div[data-testid="stColumn"]:nth-child(8))) > div[data-testid="stColumn"] {
        min-width: 46px !important;
        width: auto !important;
        flex: 1 1 46px !important;
    }
}
</style>
"""
