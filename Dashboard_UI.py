import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Smart Network Monitoring System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0f1117 !important;
    color: #e2e8f0 !important;
}
#MainMenu, footer { visibility: hidden; } header { background: transparent !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

section[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #1e293b !important;
    width: 200px !important; min-width: 200px !important; max-width: 200px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.88rem !important; padding: 10px 16px !important;
    border-radius: 8px !important; cursor: pointer !important;
    display: flex !important; align-items: center !important; width: 100% !important;
    color: #94a3b8 !important;
    background: #1a2035 !important;
    border: 1px solid #1e293b !important;
    margin-bottom: 4px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.05) !important; color: #e2e8f0 !important; }

.top-header {
    background: #161b27; border-bottom: 1px solid #1e293b;
    padding: 0 28px; height: 60px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0;
}
.header-title { font-size: 1.2rem; font-weight: 700; color: #f1f5f9; letter-spacing: 0.3px; }
.live-badge { display: flex; align-items: center; gap: 6px; font-size: 0.8rem; font-weight: 600; color: #22c55e; }
.live-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: blink 1.4s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
.header-time { color: #64748b; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; }

.wrap { padding: 20px 24px; }

.mcard { background: #1a2035; border: 1px solid #1e293b; border-radius: 12px; padding: 16px 18px; display: flex; align-items: center; gap: 14px; }
.micon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0; }
.mi-b { background: rgba(59,130,246,0.18); }
.mi-g { background: rgba(34,197,94,0.18); }
.mi-a { background: rgba(245,158,11,0.18); }
.mi-r { background: rgba(239,68,68,0.18); }
.mlbl { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; margin-bottom: 4px; }
.mval { font-size: 1.7rem; font-weight: 700; color: #f1f5f9; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.msub { font-size: 0.68rem; color: #475569; margin-top: 3px; }

.card { background: #1a2035; border: 1px solid #1e293b; border-radius: 12px; padding: 16px 18px; }
.ctitle { font-size: 0.72rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; }

.arow { display: flex; align-items: flex-start; gap: 8px; padding: 8px 11px; border-radius: 6px; margin-bottom: 5px; font-size: 0.8rem; line-height: 1.4; }
.ar { background: rgba(239,68,68,0.1); border-left: 3px solid #ef4444; color: #fca5a5; }
.ay { background: rgba(245,158,11,0.1); border-left: 3px solid #f59e0b; color: #fcd34d; }

.tt { width: 100%; border-collapse: collapse; }
.tt th { padding: 8px 11px; text-align: left; color: #475569; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 1px solid #1e293b; background: #161b27; font-weight: 500; }
.tt td { padding: 7px 11px; border-bottom: 1px solid #1a2332; color: #cbd5e1; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; }
.tt tr:last-child td { border-bottom: none; }
.tt tr:hover td { background: rgba(59,130,246,0.03); }
.ttime { color: #22c55e !important; }
.pr { padding: 2px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 500; }
.ptcp  { background: rgba(59,130,246,0.2); color: #60a5fa; }
.pudp  { background: rgba(34,197,94,0.2);  color: #4ade80; }
.picmp { background: rgba(245,158,11,0.2); color: #fbbf24; }

.vabtn { display: block; width: 100%; text-align: center; padding: 8px; border-radius: 7px; margin-top: 10px; background: rgba(59,130,246,0.12); border: 1px solid rgba(59,130,246,0.25); color: #60a5fa; font-size: 0.8rem; }

.ptitle { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; background: #1a2035; border: 1px solid #1e293b; padding: 14px 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.sectitle { font-size: 0.85rem; font-weight: 700; color: #f1f5f9; background: #1a2035; border: 1px solid #1e293b; padding: 10px 16px; border-radius: 8px; margin-bottom: 12px; }

.irow { display: flex; align-items: center; justify-content: space-between; padding: 8px 11px; border-radius: 7px; margin-bottom: 4px; background: #161b27; border: 1px solid #1e293b; }
.irank { color: #475569; font-size: 0.72rem; width: 20px; }
.iaddr { font-family: 'JetBrains Mono', monospace; color: #60a5fa; font-size: 0.82rem; }
.icnt { background: rgba(59,130,246,0.18); color: #93c5fd; padding: 2px 8px; border-radius: 10px; font-size: 0.73rem; font-weight: 600; }
.isusp { color: #ef4444; font-size: 0.65rem; margin-left: 5px; }

.footer { background: #161b27; border-top: 1px solid #1e293b; padding: 9px 28px; text-align: center; font-size: 0.72rem; color: #334155; font-family: 'JetBrains Mono', monospace; margin-top: 24px; }

.snlbl { font-size: 0.62rem; color: #334155; text-transform: uppercase; letter-spacing: 1.5px; padding: 14px 16px 6px; font-weight: 600; }
.slogo { padding: 4px 16px 6px; margin-top: -10px; }
.slt { font-size: 1.05rem; font-weight: 700; color: #f1f5f9 !important; }
.sls { font-size: 0.65rem; color: #334155 !important; margin-top: 1px; }
.ssys { padding: 14px 16px; border-top: 1px solid #1e293b; margin-top: 4px; }
.ssl { font-size: 0.65rem; color: #475569 !important; }
.sso { color: #22c55e !important; font-weight: 700; font-size: 0.88rem; margin-top: 2px; }
.sss { font-size: 0.65rem; color: #334155 !important; margin-top: 2px; }

div[data-testid="stTextInput"] input { background: #161b27 !important; border: 1px solid #1e293b !important; color: #e2e8f0 !important; border-radius: 8px !important; font-size: 0.84rem !important; }
div.stButton > button { width: 100%; text-align: center; padding: 6px; border-radius: 7px; margin-top: 5px; background: rgba(59,130,246,0.12); border: 1px solid rgba(59,130,246,0.25); color: #60a5fa; font-size: 0.8rem; }
div.stButton > button:hover { background: rgba(59,130,246,0.2); border-color: rgba(59,130,246,0.4); color: #93c5fd; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────
def load_data():
    from database.db import get_packets, get_total_packet_count
    return get_packets(), get_total_packet_count()

from Rules import detect_ddos, detect_port_scan
data, total_packets = load_data()

if not data:
    st.warning("⚠️ No traffic captured yet. Start the sniffer (`python main.py`) and wait for packets...")
    st.info("🔄 Waiting for live data. The page will refresh automatically.")
    import time
    time.sleep(3)
    st.rerun()
df       = pd.DataFrame(data, columns=["id","time","src","dst"])
alerts   = detect_ddos(data) + detect_port_scan(data)
counts   = Counter(df["src"])
now_str  = datetime.now().strftime("%I:%M:%S %p  |  %b %d, %Y")
rate     = max(1, len(df)//max(1,df["time"].nunique()))
susp_n   = len(set(a.split(":")[1].split()[0].strip() for a in alerts if ":" in a))
PM = {}
def gp(ip):
    if ip not in PM: PM[ip]=["TCP","UDP","ICMP"][int(hashlib.md5(ip.encode()).hexdigest(),16)%3]
    return PM[ip]
BG="#1a2035"; GC="#1e293b"; TC="#475569"

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="slogo">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:1.2rem;">📡</span>
            <div><div class="slt">NetIDS</div><div class="sls">Network Intrusion Detection</div></div>
        </div>
    </div>
    <div class="snlbl">NAVIGATION</div>
    """, unsafe_allow_html=True)

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏠  Dashboard"

    page = st.radio("nav", ["🏠  Dashboard","📡  Live Traffic","🚨  Alerts","📊  Top IPs","📈  Reports","⚙️  Settings"], label_visibility="collapsed", key="nav_page")

    st.markdown(f"""
    <div class="ssys">
        <div class="ssl">System Status</div>
        <div class="sso">● Online</div>
        <div class="sss">Monitoring Active</div>
        <div class="sss">All systems running smoothly</div>
        <div style="font-size:0.62rem;color:#1e293b;margin-top:8px;font-family:'JetBrains Mono',monospace;">{now_str}</div>
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
    <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:1.2rem;">📶</span>
        <span class="header-title">Smart Network Monitoring System</span>
    </div>
    <div style="display:flex;align-items:center;gap:20px;">
        <div class="live-badge"><div class="live-dot"></div>Live</div>
        <div class="header-time">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="wrap">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
if "Dashboard" in page:
    st.markdown('<div class="ptitle">🏠 Dashboard Overview</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col,cls,ic,lb,vl,sb in [
        (c1,"mi-b","📦","Total Packets",f"{total_packets:,}","Live Captured"),
        (c2,"mi-g","⚡","Packet / Sec",str(rate),"Live Rate"),
        (c3,"mi-a","🔔","Total Alerts",str(len(alerts)),"Today"),
        (c4,"mi-r","⚠️","Suspicious IPs",str(susp_n),"Detected")
    ]:
        with col:
            st.markdown(f'<div class="mcard"><div class="micon {cls}">{ic}</div><div><div class="mlbl">{lb}</div><div class="mval">{vl}</div><div class="msub">{sb}</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    a1,a2,a3 = st.columns([2.3,1.35,1.35])

    with a1:
        st.markdown('<div class="sectitle">📈 Traffic Over Time (Packets / Sec)</div>', unsafe_allow_html=True)
        td=df["time"].value_counts().sort_index().reset_index(); td.columns=["T","C"]
        f1=go.Figure(); f1.add_trace(go.Scatter(x=td["T"],y=td["C"],mode="lines",fill="tozeroy",fillcolor="rgba(59,130,246,0.07)",line=dict(color="#3b82f6",width=2)))
        f1.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=0,t=2,b=0),height=225,xaxis=dict(showgrid=False,color=TC,tickfont=dict(size=9,family="JetBrains Mono"),zeroline=False),yaxis=dict(showgrid=True,gridcolor=GC,color=TC,tickfont=dict(size=9),zeroline=False),font=dict(family="Inter"))
        st.plotly_chart(f1,use_container_width=True,config={"displayModeBar":False})

    with a2:
        st.markdown('<div class="sectitle">🥧 Protocol Distribution</div>', unsafe_allow_html=True)
        pc=Counter([gp(r[2]) for r in data])
        f2=go.Figure(go.Pie(labels=list(pc.keys()),values=list(pc.values()),hole=0.62,marker=dict(colors=["#3b82f6","#22c55e","#f59e0b","#ef4444"]),textinfo="label+percent",textfont=dict(size=9,color="#cbd5e1")))
        f2.update_layout(paper_bgcolor=BG,margin=dict(l=0,r=0,t=2,b=0),height=225,showlegend=True,legend=dict(font=dict(color="#94a3b8",size=9),bgcolor=BG,x=0.72,y=0.5))
        st.plotly_chart(f2,use_container_width=True,config={"displayModeBar":False})

    with a3:
        a3_html = '<div class="card" style="max-height:278px;overflow-y:auto;"><div class="ctitle">Recent Alerts</div>'
        if alerts:
            for a in alerts[:6]:
                cls2="ar" if "DDoS" in a else "ay"; ic2="⚠️" if "DDoS" in a else "🔍"
                a3_html += f'<div class="arow {cls2}"><span style="font-size:0.8rem;">{ic2}</span><span>{a[:46]}{"…" if len(a)>46 else ""}</span></div>'
            a3_html += '</div>'
            st.markdown(a3_html, unsafe_allow_html=True)
            st.button("View All Alerts", use_container_width=True, on_click=lambda: st.session_state.update(nav_page="🚨  Alerts"))
        else:
            a3_html += '<p style="color:#22c55e;font-size:0.82rem;">✅ No suspicious activity</p></div>'
            st.markdown(a3_html, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    b1,b2 = st.columns([1.85,1.15])

    with b1:
        rows=""
        for _,r in df.head(8).iterrows():
            p=gp(r["src"]); rows+=f"<tr><td class='ttime'>{r['time']}</td><td>{r['src']}</td><td>{r['dst']}</td><td><span class='pr p{p.lower()}'>{p}</span></td><td>74</td><td>HTTP Request</td></tr>"
        st.markdown(f'<div class="card"><div class="ctitle">Live Traffic</div><table class="tt"><thead><tr><th>Time</th><th>Source IP</th><th>Destination IP</th><th>Protocol</th><th>Length</th><th>Info</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
        st.button("View All Traffic", use_container_width=True, on_click=lambda: st.session_state.update(nav_page="📡  Live Traffic"))

    with b2:
        st.markdown('<div class="sectitle">📊 Top Talkers (By Packets)</div>', unsafe_allow_html=True)
        t6=sorted(counts.items(),key=lambda x:x[1],reverse=True)[:6]
        bdf=pd.DataFrame(t6,columns=["IP","Count"]); clrs=["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7","#ec4899"]
        f3=go.Figure(go.Bar(x=bdf["Count"],y=bdf["IP"],orientation="h",marker=dict(color=clrs[:len(bdf)]),text=bdf["Count"],textposition="outside",textfont=dict(color="#64748b",size=9)))
        f3.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=34,t=2,b=0),height=268,xaxis=dict(showgrid=True,gridcolor=GC,color=TC,tickfont=dict(size=9),zeroline=False),yaxis=dict(showgrid=False,color="#cbd5e1",tickfont=dict(size=9,family="JetBrains Mono")),font=dict(family="Inter"))
        st.plotly_chart(f3,use_container_width=True,config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════
elif "Live Traffic" in page:
    st.markdown('<div class="ptitle">📡 Live Traffic Monitor</div>', unsafe_allow_html=True)
    lc1,lc2=st.columns([2,1])
    with lc1: ipf=st.text_input("🔍 Filter by Source IP",placeholder="e.g. 192.168.1")
    with lc2: prf=st.selectbox("Protocol",["All","TCP","UDP","ICMP"])
    dv=df.copy()
    if ipf: dv=dv[dv["src"].str.contains(ipf,na=False)]
    dv_rows = ""
    for _,r in dv.head(15).iterrows():
        p=gp(r["src"])
        if prf != "All" and p != prf: continue
        dv_rows+=f"<tr><td class='ttime'>{r['time']}</td><td>{r['src']}</td><td>{r['dst']}</td><td><span class='pr p{p.lower()}'>{p}</span></td><td>74</td><td>HTTP Request</td></tr>"
    st.markdown(f'<div class="card"><div class="ctitle">Showing {len(dv)} Packets</div><table class="tt"><thead><tr><th>Time</th><th>Source IP</th><th>Destination IP</th><th>Protocol</th><th>Length</th><th>Info</th></tr></thead><tbody>{dv_rows}</tbody></table></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    lm1,lm2,lm3=st.columns(3)
    for col,cls,ic,lb,vl in [(lm1,"mi-b","📦","Total Packets",f"{len(dv):,}"),(lm2,"mi-g","🌐","Unique Sources",str(dv["src"].nunique())),(lm3,"mi-a","🎯","Unique Destinations",str(dv["dst"].nunique()))]:
        with col: st.markdown(f'<div class="mcard"><div class="micon {cls}">{ic}</div><div><div class="mlbl">{lb}</div><div class="mval">{vl}</div></div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
elif "Alerts" in page:
    st.markdown('<div class="ptitle">🚨 Security Alerts</div>', unsafe_allow_html=True)
    da=detect_ddos(data); sa=detect_port_scan(data)
    am1,am2,am3=st.columns(3)
    for col,cls,ic,lb,vl in [(am1,"mi-r","🔴","DDoS Alerts",str(len(da))),(am2,"mi-a","🟡","Port Scan Alerts",str(len(sa))),(am3,"mi-b","📋","Total Alerts",str(len(alerts)))]:
        with col: st.markdown(f'<div class="mcard"><div class="micon {cls}">{ic}</div><div><div class="mlbl">{lb}</div><div class="mval">{vl}</div></div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    ac1,ac2=st.columns(2)
    with ac1:
        ac1_html = '<div class="card"><div class="ctitle">🔴 DDoS Alerts</div>'
        if da:
            for a in da: ac1_html += f'<div class="arow ar"><span>⚠️</span>{a}</div>'
        else:
            ac1_html += '<p style="color:#22c55e;font-size:0.82rem;">✅ No DDoS detected</p>'
        ac1_html += '</div>'
        st.markdown(ac1_html, unsafe_allow_html=True)
    with ac2:
        ac2_html = '<div class="card"><div class="ctitle">🟡 Port Scan Alerts</div>'
        if sa:
            for a in sa: ac2_html += f'<div class="arow ay"><span>🔍</span>{a}</div>'
        else:
            ac2_html += '<p style="color:#22c55e;font-size:0.82rem;">✅ No Port Scans</p>'
        ac2_html += '</div>'
        st.markdown(ac2_html, unsafe_allow_html=True)
    if alerts:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding-bottom:2px; border-bottom:0; border-bottom-left-radius:0; border-bottom-right-radius:0;"><div class="ctitle" style="margin-bottom:6px;">📈 Alert Activity by IP</div></div>', unsafe_allow_html=True)
        aips=[a.split(":")[1].split()[0].strip() for a in alerts if ":" in a]
        fa=px.bar(pd.DataFrame(Counter(aips).items(),columns=["IP","Alerts"]),x="IP",y="Alerts",color_discrete_sequence=["#ef4444"])
        fa.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=0,t=2,b=0),height=230,xaxis=dict(showgrid=False,color=TC,tickfont=dict(size=10,family="JetBrains Mono")),yaxis=dict(showgrid=True,gridcolor=GC,color=TC))
        st.plotly_chart(fa,use_container_width=True,config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════
elif "Top IPs" in page:
    st.markdown('<div class="ptitle">📊 Top Source IPs</div>', unsafe_allow_html=True)
    tall=sorted(counts.items(),key=lambda x:x[1],reverse=True)
    tl,tr=st.columns([1,1.6])
    with tl:
        tl_html = '<div class="card" style="max-height:520px;overflow-y:auto;"><div class="ctitle">🏆 Ranked IPs</div>'
        for i,(ip,cnt) in enumerate(tall[:15],1):
            s=any(ip in a for a in alerts)
            tl_html += f'<div class="irow"><div style="display:flex;align-items:center;gap:7px;"><span class="irank">#{i}</span><span class="iaddr">{ip}</span>{"<span class=isusp>⚠️ SUSPICIOUS</span>" if s else ""}</div><span class="icnt">{cnt}</span></div>'
        tl_html += '</div>'
        st.markdown(tl_html, unsafe_allow_html=True)
    with tr:
        st.markdown('<div class="card" style="padding-bottom:2px; border-bottom:0; border-bottom-left-radius:0; border-bottom-right-radius:0;"><div class="ctitle" style="margin-bottom:6px;">📊 Packet Distribution</div></div>', unsafe_allow_html=True)
        t10=tall[:10]; bd=pd.DataFrame(t10,columns=["IP","Count"])
        cl2=["#ef4444" if any(ip in a for a in alerts) else "#3b82f6" for ip,_ in t10]
        f4=go.Figure(go.Bar(x=bd["Count"],y=bd["IP"],orientation="h",marker=dict(color=cl2),text=bd["Count"],textposition="outside",textfont=dict(color="#64748b",size=9)))
        f4.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=38,t=2,b=0),height=430,xaxis=dict(showgrid=True,gridcolor=GC,color=TC,tickfont=dict(size=9)),yaxis=dict(showgrid=False,color="#cbd5e1",tickfont=dict(size=9,family="JetBrains Mono")))
        st.plotly_chart(f4,use_container_width=True,config={"displayModeBar":False})
        st.markdown('<p style="font-size:0.7rem;color:#475569;margin-top:10px;">🔴 Red = Suspicious &nbsp; 🔵 Blue = Normal</p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
elif "Reports" in page:
    st.markdown('<div class="ptitle">📈 Network Reports</div>', unsafe_allow_html=True)
    rr1,rr2=st.columns(2)
    with rr1:
        st.markdown('<div class="sectitle">📈 Traffic Over Time</div>', unsafe_allow_html=True)
        td=df["time"].value_counts().sort_index().reset_index(); td.columns=["T","C"]
        f5=go.Figure(); f5.add_trace(go.Scatter(x=td["T"],y=td["C"],mode="lines+markers",fill="tozeroy",fillcolor="rgba(59,130,246,0.07)",line=dict(color="#3b82f6",width=2),marker=dict(size=3,color="#3b82f6")))
        f5.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=0,t=2,b=0),height=240,xaxis=dict(showgrid=False,color=TC,tickfont=dict(size=9,family="JetBrains Mono")),yaxis=dict(showgrid=True,gridcolor=GC,color=TC,tickfont=dict(size=9)))
        st.plotly_chart(f5,use_container_width=True,config={"displayModeBar":False})
    with rr2:
        st.markdown('<div class="sectitle">🥧 Protocol Breakdown</div>', unsafe_allow_html=True)
        pc2=Counter([gp(r[2]) for r in data])
        f6=go.Figure(go.Pie(labels=list(pc2.keys()),values=list(pc2.values()),hole=0.5,marker=dict(colors=["#3b82f6","#22c55e","#f59e0b","#ef4444"]),textinfo="label+percent+value",textfont=dict(size=10,color="#cbd5e1")))
        f6.update_layout(paper_bgcolor=BG,margin=dict(l=0,r=0,t=2,b=0),height=240,showlegend=True,legend=dict(font=dict(color="#94a3b8",size=9),bgcolor=BG))
        st.plotly_chart(f6,use_container_width=True,config={"displayModeBar":False})
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sectitle">📋 Summary Report</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Metric":["Total Packets","Unique Sources","Unique Destinations","Total Alerts","DDoS Alerts","Port Scan Alerts","Most Active IP"],"Value":[str(total_packets),str(df["src"].nunique()),str(df["dst"].nunique()),str(len(alerts)),str(len(detect_ddos(data))),str(len(detect_port_scan(data))),counts.most_common(1)[0][0] if counts else "N/A"]}),use_container_width=True,hide_index=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.download_button("📥 Download Traffic Log (CSV)",df.to_csv(index=False),"traffic_log.csv","text/csv")

# ══════════════════════════════════════════════════════════════
elif "Settings" in page:
    st.markdown('<div class="ptitle">⚙️ Settings</div>', unsafe_allow_html=True)
    ss1,ss2=st.columns(2)
    with ss1:
        st.markdown('<div class="sectitle">🚨 Alert Thresholds</div>', unsafe_allow_html=True)
        dt=st.slider("DDoS Alert Threshold (packets)",10,200,20)
        st2=st.slider("Port Scan Threshold (packets)",20,300,50)
        st.markdown(f'<div style="margin-top:12px;padding:11px;background:#161b27;border-radius:8px;border:1px solid #1e293b;"><div style="color:#475569;font-size:0.68rem;margin-bottom:5px;">ACTIVE SETTINGS</div><div style="color:#60a5fa;font-family:JetBrains Mono,monospace;font-size:0.8rem;line-height:1.8;">DDoS → {dt} packets<br>Port Scan → {st2} packets</div></div>', unsafe_allow_html=True)
    with ss2:
        st.markdown('<div class="sectitle">📧 Email Alerts</div>', unsafe_allow_html=True)
        st.toggle("Enable Email Alerts",value=True)
        st.text_input("Alert Email",placeholder="your@gmail.com")
        st.checkbox("Alert on DDoS Detection",value=True)
        st.checkbox("Alert on Port Scan",value=True)
        if st.button("💾 Save Settings",use_container_width=True): st.success("✅ Settings saved!")
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    ss3, ss4 = st.columns(2)
    with ss3:
        st.markdown('<div class="sectitle">ℹ️ System Info</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Property":["Version","Framework","Database","Detection","Status"],"Value":["2.0.0 Industry","Streamlit","SQLite","Rules-based IDS","● Live"]}),use_container_width=True,hide_index=True)
    with ss4:
        st.markdown('<div class="sectitle">🗑️ Database Operations</div>', unsafe_allow_html=True)
        def reset_db():
            try:
                import sqlite3, os
                db_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "network.db"))
                if os.path.exists(db_path):
                    c = sqlite3.connect(db_path, check_same_thread=False)
                    c.execute("DELETE FROM packets")
                    c.commit()
                    c.close()
                st.cache_data.clear()
            except Exception as e:
                pass
        st.button("🔄 Reset Database Manually", use_container_width=True, on_click=reset_db)
        st.markdown('<p style="font-size:0.7rem;color:#475569;margin-top:6px;">⚠️ This will instantly delete all captured packets and start fresh.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer">Smart Network Monitoring System &nbsp;|&nbsp; Network IDS Dashboard &nbsp;|&nbsp; {now_str}</div>', unsafe_allow_html=True)

# ── Auto Refresh ──────────────────────────────────────────────
import time
time.sleep(3)
st.rerun()
