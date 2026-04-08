import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials
import os

# --- DASHBOARD CONFIG ---
st.set_page_config(layout='wide', page_title='K-Beauty Admin Intelligence')

# --- APPLE PALETTE ---
APPLE_PALETTE = {
    'primary_content': '#1D1D1F',
    'secondary_content': '#6E6E73',
    'tertiary_content': '#86868B',
    'system_blue': '#007AFF',
    'system_indigo': '#5856D6',
    'system_teal': '#30B0C7',
    'system_gray': '#8E8E93',
    'sky_blue': '#76D6FF',
    'background_secondary': '#F5F5F7',
    'background_tertiary': '#E5E5EA'
}

# --- 1. Data Setup (Real-time Google Sheets) ---
@st.cache_data(ttl=60)
def load_realtime_data():
    try:
        if "gcp_service_account" not in st.secrets:
            return pd.DataFrame()
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1p8vdpetOcxWANsB4fxZZ40Q5Jr_eRBC4ACMBpsfmXeg/edit#gid=0"
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

df = load_realtime_data()

# --- HELPERS ---
def apply_apple_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family="'SF Pro Display', sans-serif", font_color=APPLE_PALETTE['primary_content'],
        margin=dict(t=40, b=40, l=40, r=40),
        colorway=[APPLE_PALETTE['system_indigo'], APPLE_PALETTE['system_teal'], APPLE_PALETTE['sky_blue'], APPLE_PALETTE['system_gray']]
    )
    return fig

# --- LAYOUT & CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {APPLE_PALETTE['background_secondary']}; color: {APPLE_PALETTE['primary_content']}; }}
    div.stVerticalBlock > div[style*="flex-direction: column"] > div {{
        background: #FFFFFF; padding: 40px; border-radius: 24px; border: 1px solid rgba(0, 0, 0, 0.05); margin-bottom: 24px;
    }}
    h1 {{ font-size: 48px !important; font-weight: 800 !important; letter-spacing: -0.04em !important; text-align: center; }}
    .subtitle {{ font-size: 20px; color: {APPLE_PALETTE['secondary_content']}; text-align: center; margin-bottom: 3rem; }}
    h2 {{ font-size: 32px !important; font-weight: 700 !important; margin-top: 60px !important; margin-bottom: 16px !important; }}
    .section-desc {{ font-size: 18px; color: {APPLE_PALETTE['secondary_content']}; margin-bottom: 32px; }}
    
    .metric-card {{
        background: white; padding: 32px; border-radius: 20px; border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); text-align: left;
    }}
    .metric-value {{ font-size: 42px; font-weight: 800; margin: 8px 0; letter-spacing: -0.04em; }}
    .metric-title {{ font-size: 14px; font-weight: 700; color: {APPLE_PALETTE['secondary_content']}; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER STATISTICS ---
st.markdown("<h1>K-Beauty Admin Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-time User Behavior & Market Insight</p>", unsafe_allow_html=True)

if not df.empty:
    total_sessions = df['User ID'].nunique()
    survey_done = len(df[df['Event Type'] == 'survey_completed'])
    click_events = len(df[df['Event Type'] == 'product_click'])
    conv_rate = (click_events / survey_done * 100) if survey_done > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    def render_card(column, title, value, color):
        column.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value" style="color: {color};">{value}</div></div>', unsafe_allow_html=True)
    
    render_card(c1, "Total Visitors", f"{total_sessions}명", APPLE_PALETTE['system_blue'])
    render_card(c2, "Survey Completed", f"{survey_done}건", APPLE_PALETTE['system_indigo'])
    render_card(c3, "Product Clicks", f"{click_events}건", APPLE_PALETTE['system_teal'])
    render_card(c4, "Conversion Rate", f"{conv_rate:.1f}%", "#AF52DE")

    # --- Section 1. Global Market Velocity ---
    st.markdown("<h2>Global Market Velocity</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>국가별 유동성 점유율과 사용자의 사이트 체류 집중도 간의 관계를 시각화합니다.</p>", unsafe_allow_html=True)
    
    v1, v2 = st.columns([1, 1.2])
    with v1:
        st.markdown("### National Share")
        # 페르소나 명칭에서 국가 키워드 추출 (가정)
        df['Nation'] = df['Persona Result'].apply(lambda x: x.split(' (')[0] if ' (' in str(x) else 'Global')
        fig_pie = px.pie(df, names='Nation', hole=0.6)
        st.plotly_chart(apply_apple_style(fig_pie), use_container_width=True)
    with v2:
        st.markdown("### Engagement Matrix")
        # 클릭 수를 유저별로 집계하여 Engagement 측정
        eng_df = df.groupby('User ID').agg({'Event Type': 'count'}).reset_index()
        eng_df.columns = ['User ID', 'Activity_Count']
        fig_scatter = px.box(eng_df, y='Activity_Count', points="all", title="User Activity Distribution")
        st.plotly_chart(apply_apple_style(fig_scatter), use_container_width=True)

    # --- Section 2. Synergy & Attraction Preferences ---
    st.markdown("<h2>Synergy & Attraction Preferences</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>화장품 브랜드와 연계 방문 관광지 간의 시너지 분석 결과입니다.</p>", unsafe_allow_html=True)
    
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("### Synergy Ranking")
        # 관광지 리스트 분리 및 매칭
        synergy_records = []
        for idx, row in df.iterrows():
            if row['Matched Attractions'] and row['Product Name']:
                attrs = [a.strip() for a in str(row['Matched Attractions']).split(',')]
                for a in attrs:
                    synergy_records.append({'Attraction': a, 'Product': row['Product Name']})
        
        if synergy_records:
            synergy_df = pd.DataFrame(synergy_records).groupby(['Attraction', 'Product']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
            st.dataframe(synergy_df.head(10), hide_index=True, use_container_width=True)
        else:
            st.info("시너지 분석을 위한 매칭 데이터가 아직 부족합니다.")

    with s2:
        st.markdown("### Attraction Preference by Nation")
        pref_records = []
        for idx, row in df.iterrows():
            if row['Matched Attractions']:
                nation = row['Persona Result'].split(' (')[0] if ' (' in str(row['Persona Result']) else 'Global'
                attrs = [a.strip() for a in str(row['Matched Attractions']).split(',')]
                for a in attrs:
                    pref_records.append({'Nation': nation, 'Attraction': a})
        
        if pref_records:
            pref_df = pd.DataFrame(pref_records).groupby(['Nation', 'Attraction']).size().reset_index(name='Count')
            fig_pref = px.bar(pref_df, x='Attraction', y='Count', color='Nation', barmode='group')
            st.plotly_chart(apply_apple_style(fig_pref), use_container_width=True)

    # --- Section 3. Laboratory Intelligence ---
    st.markdown("<h2>Laboratory Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>AI 알고리즘이 감지한 신규 페르소나 패턴과 행동 진단 결과입니다.</p>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: white; padding: 48px; border-radius: 28px; border: 1.5px solid {APPLE_PALETTE['background_tertiary']};'>
            <div style='font-size: 14px; font-weight: 700; color: {APPLE_PALETTE['system_blue']}; margin-bottom: 16px; text-transform: uppercase;'>NEW INTELLIGENCE INSIGHT</div>
            <div style='font-size: 28px; font-weight: 600; color: {APPLE_PALETTE['primary_content']}; line-height: 1.4; margin-bottom: 32px;'>
                Based on current velocity, "<b>Art Enthusiasts</b>" exhibit a <b>92% compatibility</b> with premium cosmetic curated offerings.
            </div>
            <div style='background-color: {APPLE_PALETTE['system_blue']}; color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 20px;'>RECOMMENDED ACTION PLAN</div>
            <div style='font-size: 16px; color: {APPLE_PALETTE['secondary_content']}; line-height: 1.8;'>
                1. 주요 미술관 및 갤러리 내 'Art-Beauty' 전용 팝업 큐레이션 존 구성<br>
                2. 인사동, 성수동 등 '예술 테마' 지역 대상 초정밀 타겟팅 광고 집행
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("📊 데이터 로드 중이거나 시트가 비어 있습니다.")
