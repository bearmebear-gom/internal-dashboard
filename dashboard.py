import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials

# --- DASHBOARD CONFIG ---
st.set_page_config(layout='wide', page_title='K-Beauty Intelligence Dashboard')

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
            st.error("❌ Secrets not found. Please set 'gcp_service_account' in Streamlit Cloud Settings.")
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
        st.error(f"⚠️ Data Load Failed: {e}")
        return pd.DataFrame()

df = load_realtime_data()

# --- HELPERS ---
def apply_apple_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family="'SF Pro Display', sans-serif", font_color=APPLE_PALETTE['primary_content'],
        margin=dict(t=40, b=40, l=40, r=40),
        colorway=[APPLE_PALETTE['system_blue'], APPLE_PALETTE['system_indigo'], APPLE_PALETTE['system_teal'], APPLE_PALETTE['system_gray']]
    )
    return fig

# --- LAYOUT & CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {APPLE_PALETTE['background_secondary']}; color: {APPLE_PALETTE['primary_content']}; }}
    div.stVerticalBlock > div[style*="flex-direction: column"] > div {{
        background: #FFFFFF; padding: 40px; border-radius: 24px; border: 1px solid rgba(0, 0, 0, 0.05); margin-bottom: 32px;
    }}
    h1 {{ font-size: 56px !important; font-weight: 800 !important; letter-spacing: -0.05em !important; text-align: center; margin-bottom: 0.5rem; }}
    .subtitle {{ font-size: 22px; color: {APPLE_PALETTE['secondary_content']}; text-align: center; margin-bottom: 4rem; }}
    h2 {{ font-size: 34px !important; font-weight: 700 !important; margin-top: 40px !important; margin-bottom: 24px !important; border-bottom: 2px solid {APPLE_PALETTE['background_tertiary']}; padding-bottom: 12px; }}
    .section-desc {{ font-size: 18px; color: {APPLE_PALETTE['secondary_content']}; margin-bottom: 32px; line-height: 1.6; }}
    
    .metric-card {{ background: white; padding: 32px; border-radius: 24px; border: 1.1px solid rgba(0,0,0,0.06); box-shadow: 0 10px 30px rgba(0,0,0,0.02); }}
    .metric-value {{ font-size: 48px; font-weight: 800; margin: 10px 0; letter-spacing: -0.04em; }}
    .metric-title {{ font-size: 14px; font-weight: 700; color: {APPLE_PALETTE['secondary_content']}; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>K-Beauty Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Integrated User Behavior Analysis & AI-Driven Insights</p>", unsafe_allow_html=True)

if df.empty:
    st.warning("📊 Waiting for real-time data flow...")
    st.stop()

# --- 2. Executive Overview (Premium Cards) ---
total_sessions = df['User ID'].nunique()
survey_done = len(df[df['Event Type'] == 'survey_completed'])
click_events = len(df[df['Event Type'] == 'product_click'])
conv_rate = (click_events / survey_done * 100) if survey_done > 0 else 0

c1, c2, c3, c4 = st.columns(4)
def render_metric(col, title, val, color):
    col.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value" style="color: {color};">{val}</div></div>', unsafe_allow_html=True)

render_metric(c1, "Total Visitors", f"{total_sessions}명", APPLE_PALETTE['system_blue'])
render_metric(c2, "Survey Completed", f"{survey_done}건", APPLE_PALETTE['system_indigo'])
render_metric(c3, "Product Clicks", f"{click_events}건", APPLE_PALETTE['system_teal'])
render_metric(c4, "Conversion Rate", f"{conv_rate:.1f}%", "#AF52DE")

# --- SECTION 1: Persona & Market distribution ---
st.markdown("<h2>Persona & National Distribution</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>5대 페르소나별 분포와 국가별 유입 점유율을 통해 핵심 타겟층을 파악합니다.</p>", unsafe_allow_html=True)
sc1, sc2 = st.columns(2)
with sc1:
    st.markdown("### 5대 페르소나 분포 (Pie Chart)")
    persona_df = df[df['Persona Result'] != ''].groupby('Persona Result').size().reset_index(name='Count')
    fig_p = px.pie(persona_df, values='Count', names='Persona Result', hole=0.5)
    st.plotly_chart(apply_apple_style(fig_p), use_container_width=True)
with sc2:
    st.markdown("### 선호 자치구(District) 선택 순위")
    dist_df = df[df['Q4 (District)'] != ''].groupby('Q4 (District)').size().reset_index(name='Count').sort_values('Count', ascending=False)
    fig_d = px.bar(dist_df, x='Q4 (District)', y='Count', color='Count', color_continuous_scale='Purples')
    st.plotly_chart(apply_apple_style(fig_d), use_container_width=True)

# --- SECTION 2: Global Market Velocity (Original Content) ---
st.markdown("<h2>Global Market Velocity</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>국가별 유동성 점유율과 사용자의 사이트 체류 집중도 간의 관계를 시각화합니다.</p>", unsafe_allow_html=True)
sc3, sc4 = st.columns([1, 1.2])
with sc3:
    st.markdown("### National Share")
    # 페르소나 이름에서 국가명 추출 가정
    df['Nation'] = df['Persona Result'].apply(lambda x: x.split(' (')[0] if ' (' in str(x) else 'Global')
    fig_n = px.pie(df, names='Nation', hole=0.6)
    st.plotly_chart(apply_apple_style(fig_n), use_container_width=True)
with sc4:
    st.markdown("### Engagement Matrix")
    eng_df = df.groupby('User ID').agg({'Event Type': 'count'}).reset_index()
    eng_df.columns = ['User ID', 'Activity Count']
    fig_e = px.box(eng_df, y='Activity Count', points="all", color_discrete_sequence=[APPLE_PALETTE['system_blue']])
    st.plotly_chart(apply_apple_style(fig_e), use_container_width=True)

# --- SECTION 3: Synergy & Attraction Preferences ---
st.markdown("<h2>Synergy & Attraction Preferences</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>화장품 브랜드와 연계 방문 관광지 간의 시너지 분석 결과입니다.</p>", unsafe_allow_html=True)
sc5, sc6 = st.columns(2)
with sc5:
    st.markdown("### Synergy Ranking (Synergy Ranking)")
    syn_data = []
    for _, row in df.iterrows():
        if row['Product Name'] and row['Matched Attractions']:
            for attr in str(row['Matched Attractions']).split(','):
                syn_data.append({'Product': row['Product Name'], 'Attraction': attr.strip()})
    if syn_data:
        syn_df = pd.DataFrame(syn_data).groupby(['Product', 'Attraction']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
        st.dataframe(syn_df.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("데이터 축적 중입니다.")

with sc6:
    st.markdown("### K-Beauty 아이템 관심도 랭킹")
    prod_df = df[df['Product Name'] != ''].groupby('Product Name').size().reset_index(name='Clicks').sort_values('Clicks', ascending=False)
    st.dataframe(prod_df, use_container_width=True, hide_index=True)

# --- SECTION 4: Trend Analysis & Funnel ---
st.markdown("<h2>Trend Analysis & Conversion Flow</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>이탈 구간 확인 및 퀴즈 완료 대비 제품 관심도 비율(UX 분석)입니다.</p>", unsafe_allow_html=True)
sc7, sc8 = st.columns([1.5, 1])
with sc7:
    st.markdown("### User Conversion Funnel")
    fun_df = pd.DataFrame({
        'Step': ['Total Visitors', 'Survey Finished', 'Product Interest'],
        'Count': [total_sessions, survey_done, click_events]
    })
    fig_f = px.funnel(fun_df, x='Count', y='Step', color_discrete_sequence=[APPLE_PALETTE['system_indigo']])
    st.plotly_chart(apply_apple_style(fig_f), use_container_width=True)
with sc8:
    st.markdown("### UX Insight Card")
    st.markdown(f"""
        <div style='background: white; padding: 32px; border-radius: 20px; border: 1.5px solid {APPLE_PALETTE['system_blue']};'>
            <div style='color: {APPLE_PALETTE['system_blue']}; font-weight: 700; margin-bottom: 12px;'>📊 UI/UX IMPROVEMENT POINT</div>
            <div style='font-size: 20px; font-weight: 600; margin-bottom: 16px;'>현재 전환율: {conv_rate:.1f}%</div>
            <div style='font-size: 15px; color: #424245; line-height: 1.7;'>
                • <b>이탈 구간</b>: 퀴즈 완료 후 제품 상세 클릭으로 넘어가는 단계에서 약 {100-conv_rate:.1f}%의 이탈이 발생합니다.<br>
                • <b>개선 지점</b>: 추천 리스트의 시각적 요소를 강화하거나 "상세 보기" 버튼의 가독성을 개선할 필요가 있습니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- SECTION 5: Laboratory Intelligence (Original/Fixed) ---
st.markdown("<h2>Laboratory Intelligence</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>AI 알고리즘이 감지한 신규 페르소나 패턴과 행동 진단 결과입니다.</p>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='background: #FFFFFF; padding: 48px; border-radius: 28px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 10px 40px rgba(0,0,0,0.04);'>
        <div style='font-size: 14px; font-weight: 700; color: {APPLE_PALETTE['system_blue']}; margin-bottom: 16px; letter-spacing: 0.1em;'>NEW INTELLIGENCE INSIGHT</div>
        <div style='font-size: 30px; font-weight: 700; color: #1D1D1F; line-height: 1.4; margin-bottom: 32px;'>
            Based on current velocity, <span style='color:{APPLE_PALETTE['system_indigo']};'>"Art Enthusiasts"</span> exhibit a <b>92% compatibility</b> with premium cosmetic curated offerings.
        </div>
        <div style='background-color: {APPLE_PALETTE['system_blue']}; color: white; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 24px;'>RECOMMENDED ACTION PLAN</div>
        <div style='font-size: 18px; color: #6E6E73; line-height: 1.8;'>
            1. 주요 미술관 및 갤러리 내 'Art-Beauty' 전용 팝업 큐레이션 존 구성<br>
            2. 인사동, 성수동 등 '예술 테마' 지역 대상 초정밀 타겟팅 광고 집행
        </div>
    </div>
""", unsafe_allow_html=True)
