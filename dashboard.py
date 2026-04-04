import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import numpy as np

# --- DASHBOARD CONFIG ---
st.set_page_config(layout='wide', page_title='K-Beauty Persona Dashboard')

# 1. Data Setup
csv_data = """User_ID,Timestamp,Cosmetic_Name,Price_Range,Attraction,Location_Dong
a1b2_chn,2026-04-01 10:20,리쥬란 턴오버 앰플,50000-70000,세종문화회관 공연,명동
c3d4_jpn,2026-04-01 11:15,아누아 어성초 77 토너,20000-30000,국립중앙박물관,이촌동
e5f6_twn,2026-04-01 13:40,마녀공장 클렌징 오일,15000-25000,망원시장,망원동
g7h8_usa,2026-04-01 15:10,바이오던스 콜라겐 마스크,5000-10000,롯데월드 어드벤처,잠실동
i9j0_hkg,2026-04-01 17:50,에스트라 아토베리어 크림,30000-40000,DDP 전시회,을지로
k1l2_chn,2026-04-02 09:30,메디큐브 에이지알 디바이스,200000-300000,신세계백화점 본점,명동
m3n4_jpn,2026-04-02 10:45,토리든 다이브인 세럼,15000-25000,경복궁,사직동
o5p6_twn,2026-04-02 14:20,비플레인 녹두 클렌징폼,10000-20000,서울숲 공원,성수동
q7r8_usa,2026-04-02 16:00,넘버즈인 글루타치온 세럼,20000-30000,성수동 팝업스토어,성수동
s9t0_hkg,2026-04-02 19:15,라로슈포제 유비데아 선크림,30000-40000,블루스퀘어 뮤지컬,한남동
u1v2_chn,2026-04-03 11:00,넘버즈인 5번 세럼,25000-35000,롯데콘서트홀,잠실동
w3x4_jpn,2026-04-03 12:30,라운드랩 자작나무 크림,20000-30000,덕수궁 미술관,정동
y5z6_twn,2026-04-03 15:50,브링그린 티트리 시카 패드,15000-20000,광장시장,종로5가
a7b8_usa,2026-04-03 18:20,메디큐브 브라이트닝 앰플,30000-45000,더현대 서울,여의도동
c9d0_hkg,2026-04-03 21:00,바이오더마 센시비오 H2O,20000-30000,예술의전당,서초동
e1f2_chn,2026-04-04 10:05,리쥬란 힐러 마스크,30000-45000,현대백화점 압구정,압구정동
g3h4_jpn,2026-04-04 13:10,아누아 앰플,25000-35000,리움미술관,한남동
i5j6_twn,2026-04-04 14:40,마녀공장 퓨어 클렌징 폼,10000-15000,남산공원,예장동
k7l8_usa,2026-04-04 16:55,바이오던스 앰플,35000-50000,코엑스 별마당도서관,삼성동
m9n0_hkg,2026-04-04 20:30,에스트라 선크림,25000-35000,샤롯데씨어터,잠실동"""

df = pd.read_csv(io.StringIO(csv_data))
df['Nation'] = df['User_ID'].apply(lambda x: x.split('_')[1].upper())
df['Click_Count'] = [12, 8, 15, 22, 10, 5, 18, 20, 30, 14, 11, 13, 25, 28, 9, 7, 16, 19, 35, 12]
df['Stay_Time'] = [120, 85, 200, 150, 90, 300, 110, 140, 180, 210, 95, 105, 220, 250, 130, 160, 145, 125, 280, 115]

# --- NATION METRIC DATA ---
nations = ['CHN', 'JPN', 'TWN', 'USA', 'HKG']
metrics = ['Growth', 'Retention', 'Conversion', 'Loyalty']
nation_metrics = []
for n in nations:
    for m in metrics:
        val = np.random.randint(40, 95)
        nation_metrics.append({'Nation': n, 'Metric': m, 'Value': val})
ndf = pd.DataFrame(nation_metrics)

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

# --- HELPERS ---
def apply_apple_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family="'SF Pro Display', sans-serif", font_color=APPLE_PALETTE['primary_content'],
        margin=dict(t=40, b=40, l=40, r=40),
        colorway=[APPLE_PALETTE['system_indigo'], APPLE_PALETTE['system_teal'], APPLE_PALETTE['sky_blue'], APPLE_PALETTE['system_gray']]
    )
    fig.update_xaxes(showgrid=True, gridcolor=APPLE_PALETTE['background_tertiary'], zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=APPLE_PALETTE['background_tertiary'], zeroline=False)
    return fig

def render_progress_ring(value, color=APPLE_PALETTE['system_blue']):
    fig = go.Figure(go.Pie(
        values=[value, 100-value], hole=0.7,
        marker=dict(colors=[color, APPLE_PALETTE['background_tertiary']]),
        textinfo='none', hoverinfo='none', sort=False
    ))
    fig.update_layout(
        showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=220,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text=f'{value}%', x=0.5, y=0.5, font=dict(size=22, family="'SF Pro Display', sans-serif", color=APPLE_PALETTE['primary_content']), showarrow=False)]
    )
    return fig

# --- LAYOUT & CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {APPLE_PALETTE['background_secondary']}; color: {APPLE_PALETTE['primary_content']}; }}
    div.stVerticalBlock > div[style*="flex-direction: column"] > div {{
        background: #FFFFFF; padding: 48px; border-radius: 32px; border: 1px solid rgba(0, 0, 0, 0.02); margin-bottom: 48px;
    }}
    h1 {{ font-size: 64px !important; font-weight: 800 !important; letter-spacing: -0.06em !important; text-align: center; margin-bottom: 0.2rem !important; }}
    .subtitle {{ font-size: 24px !important; font-weight: 500; color: {APPLE_PALETTE['secondary_content']}; text-align: center; margin-bottom: 4rem !important; }}
    
    h2 {{ 
        font-size: 32px !important; font-weight: 700 !important; 
        border-bottom: 1.5px solid {APPLE_PALETTE['background_tertiary']}; 
        padding-bottom: 20px; margin-top: 120px !important; margin-bottom: 16px !important; 
    }}
    
    .section-desc {{
        font-size: 20px !important; /* Scaled back down to professional large */
        color: {APPLE_PALETTE['secondary_content']}; 
        margin-bottom: 24px; 
        line-height: 1.4;
        font-weight: 400;
    }}

    .section-label {{
        background-color: {APPLE_PALETTE['background_tertiary']}; color: {APPLE_PALETTE['secondary_content']};
        padding: 6px 14px; border-radius: 10px; font-size: 16px; font-weight: 700; display: inline-block; margin-bottom: 8px;
    }}

    .metric-label {{
        text-align: center; font-size: 12px; font-weight: 600; color: {APPLE_PALETTE['tertiary_content']};
        margin-top: 24px; letter-spacing: 0.05em;
    }}

    hr.apple-hr {{
        border: 0; height: 1.5px; background: {APPLE_PALETTE['background_tertiary']}; margin: 24px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>K-Beauty Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Comprehensive Market Analysis & Persona Insight</p>", unsafe_allow_html=True)

# 1. Executive Summary
st.markdown("<div class='section-label'>EXECUTIVE SUMMARY</div>", unsafe_allow_html=True)
st.markdown("<hr class='apple-hr'>", unsafe_allow_html=True) # Line under section title
st.markdown("<p class='section-desc'>글로벌 시장의 전반적인 성장성과 고객 유지율, 전환율, 충성도 지표의 통합 요약입니다. </p>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.plotly_chart(render_progress_ring(72, APPLE_PALETTE['system_blue']), use_container_width=True)
    st.markdown(f"<p class='metric-label'>AGGREGATED GROWTH</p>", unsafe_allow_html=True)
with m2:
    st.plotly_chart(render_progress_ring(85, APPLE_PALETTE['system_indigo']), use_container_width=True)
    st.markdown(f"<p class='metric-label'>AGGREGATED RETENTION</p>", unsafe_allow_html=True)
with m3:
    st.plotly_chart(render_progress_ring(64, APPLE_PALETTE['system_teal']), use_container_width=True)
    st.markdown(f"<p class='metric-label'>AGGREGATED CONVERSION</p>", unsafe_allow_html=True)
with m4:
    st.plotly_chart(render_progress_ring(92, APPLE_PALETTE['system_gray']), use_container_width=True)
    st.markdown(f"<p class='metric-label'>AGGREGATED LOYALTY</p>", unsafe_allow_html=True)

# Regional KPI
st.markdown("<h2 style='margin-top: 50px !important;'>Regional Key Performance Indicators</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>국가별 주요 KPI 성과를 심층 비교 분석합니다.</p>", unsafe_allow_html=True)
fig_metrics = px.bar(ndf, x='Metric', y='Value', color='Nation', barmode='group', text_auto='.1s')
st.plotly_chart(apply_apple_style(fig_metrics).update_layout(colorway=[APPLE_PALETTE['system_indigo'], APPLE_PALETTE['system_teal'], APPLE_PALETTE['sky_blue'], '#AEAEB2', '#E5E5EA']), use_container_width=True)

# 2. Market Velocity (Major boundary)
st.markdown("<hr class='apple-hr'><hr class='apple-hr'>", unsafe_allow_html=True)
st.markdown("<h2>Global Market Velocity</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>국가별 유동성 점유율과 사용자의 사이트 체류 집중도 간의 관계를 시각화합니다.</p>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 1.2])
with c1:
    st.markdown("### National Share")
    fig = px.pie(df, names='Nation', hole=0.6)
    st.plotly_chart(apply_apple_style(fig), use_container_width=True)
with c2:
    st.markdown("### Engagement Matrix")
    fig = px.scatter(df, x='Stay_Time', y='Click_Count', color='Nation', size='Click_Count', opacity=0.7)
    st.plotly_chart(apply_apple_style(fig), use_container_width=True)

# 3. Synergy & Preferences
st.markdown("<h2>Synergy & Attraction Preferences</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>화장품 브랜드와 연계 방문 관광지 간의 시너지 분석 결과입니다.</p>", unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.markdown("### Synergy Ranking")
    synergy_df = df.groupby(['Attraction', 'Cosmetic_Name']).size().reset_index(name='Freq').sort_values(by='Freq', ascending=False)
    st.dataframe(synergy_df.head(10), use_container_width=True)
with c4:
    st.markdown("### Attraction Preference by Nation")
    attr_df = df.groupby(['Nation', 'Attraction']).size().reset_index(name='Count')
    fig_pref = px.bar(attr_df, x='Attraction', y='Count', color='Nation', barmode='group')
    st.plotly_chart(apply_apple_style(fig_pref), use_container_width=True)

# 4. Laboratory
st.markdown("<h2>Laboratory Intelligence</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>AI 알고리즘이 감지한 신규 페르소나 패턴과 행동 진단 결과입니다.</p>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='background: {APPLE_PALETTE['background_secondary']}; padding: 48px; border-radius: 28px;'>
        <div style='font-size: 20px; font-weight: 700; color: {APPLE_PALETTE['primary_content']}; margin-bottom: 16px;'>NEW INTELLIGENCE INSIGHT</div>
        <div style='font-size: 20px; color: {APPLE_PALETTE['secondary_content']}; line-height: 1.4; margin-bottom: 32px;'>
            Based on current velocity, "<b>Art Enthusiasts</b>" exhibit a <b>92% compatibility</b> with premium cosmetic curated offerings.
        </div>
        <div style='background-color: {APPLE_PALETTE['system_blue']}; color: white; padding: 4px 10px; border-radius: 6px; font-size: 18px; font-weight: 700; display: inline-block; margin-bottom: 10px;'>RECOMMENDED ACTION PLAN</div>
        <div class='action-item'>1. 주요 미술관 및 갤러리 내 'Art-Beauty' 전용 팝업 큐레이션 존 구성</div>
        <div class='action-item'>2. 인사동, 성수동 등 '예술 테마' 지역 대상 초정밀 타겟팅 광고 집행</div>
    </div>
""", unsafe_allow_html=True)
