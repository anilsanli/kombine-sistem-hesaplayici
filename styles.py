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
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    border-radius: 16px;
    padding: 24px 28px;
    color: #ffffff;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.12);
}
.hero-title {
    font-size: 24px;
    font-weight: 800;
    margin: 0;
    color: #ffffff !important;
    display: flex;
    align-items: center;
    gap: 10px;
}
.hero-subtitle {
    font-size: 13.5px;
    color: #cbd5e1 !important;
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
    background: linear-gradient(135deg, #090d16 0%, #111827 100%) !important;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.2);
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
    font-size: 20px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}
.kpi-number.accent {
    color: #fb7185 !important;
}
.kpi-number.highlight {
    color: #34d399 !important;
    font-size: 23px !important;
}
.kpi-divider {
    width: 1px;
    height: 32px;
    background: rgba(255, 255, 255, 0.15);
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
    border-bottom: 1.5px dashed #f1f5f9;
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

/* At & Bilet Rozet Stilleri */
.chip-at-won {
    background: #dcfce7 !important;
    border: 1px solid #86efac !important;
    color: #14532d !important;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin: 2px;
}
.chip-at-lost {
    background: #fee2e2 !important;
    border: 1px solid #fca5a5 !important;
    color: #7f1d1d !important;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin: 2px;
    text-decoration: line-through;
    opacity: 0.85;
}
.chip-at-pending {
    background: #fef9c3 !important;
    border: 1px solid #fde047 !important;
    color: #713f12 !important;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin: 2px;
}
.chip-at-refund {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    color: #475569 !important;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin: 2px;
}

.slip-badge-won {
    background: #dcfce7;
    color: #15803d;
    font-weight: 800;
    font-size: 11.5px;
    padding: 3px 10px;
    border-radius: 9999px;
    border: 1px solid #86efac;
}
.slip-badge-pending {
    background: #fef9c3;
    color: #854d0e;
    font-weight: 800;
    font-size: 11.5px;
    padding: 3px 10px;
    border-radius: 9999px;
    border: 1px solid #fef08a;
}
.slip-badge-lost {
    background: #fee2e2;
    color: #b91c1c;
    font-weight: 800;
    font-size: 11.5px;
    padding: 3px 10px;
    border-radius: 9999px;
    border: 1px solid #fca5a5;
}
.slip-badge-refund {
    background: #f1f5f9;
    color: #475569;
    font-weight: 800;
    font-size: 11.5px;
    padding: 3px 10px;
    border-radius: 9999px;
    border: 1px solid #cbd5e1;
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
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}
.status-badge.pending {
    background: #fef9c3;
    color: #854d0e;
    border: 1px solid #fef08a;
}
.status-badge.lost {
    background: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
}
.status-badge.refund {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
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

/* İpucu Banner */
.helper-banner {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 16px;
    font-size: 13px;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

/* İkramiye Özet Hero Paneli */
.payout-hero {
    background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e293b 100%);
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 28px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.25);
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
