"""
国关顶刊动态助手 测试版
一键部署到Streamlit Cloud即可获得访问地址
"""
import streamlit as st
import pandas as pd
from datetime import date
import json

# 页面配置
st.set_page_config(
    page_title="国关顶刊动态助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 预置测试数据
MOCK_ARTICLES = [
    {
        "id": 1,
        "title": "中美科技竞争的地缘政治经济学分析",
        "authors": [{"name": "张三", "affiliation": "北京大学国际关系学院"}],
        "journal": "International Organization",
        "journal_zh": "国际组织",
        "publish_date": date(2024, 1, 15),
        "volume": "78",
        "issue": "1",
        "pages": "45-78",
        "doi": "10.1017/S002081832300045X",
        "url": "https://www.cambridge.org/core/journals/international-organization/article/abs/10.1017/S002081832300045X",
        "abstract": "本文分析了中美科技竞争的演变逻辑与影响，重点探讨了半导体出口管制、技术脱钩等政策对全球科技格局的重塑作用。研究发现，中美科技竞争不仅是技术层面的较量，更是制度和治理模式的竞争，将对未来全球经济秩序产生深远影响。",
        "research_areas": ["中美关系", "中美科技竞争", "科技与大国竞争"],
        "structured_summary": {
            "core_problem": "本文聚焦中美科技竞争的内在逻辑与全球影响，探讨了美国出口管制政策的实施背景、作用机制及其对中国科技发展和全球科技治理的挑战。",
            "main_points": "1. 中美科技竞争的本质是技术主导权的争夺，美国通过出口管制、实体清单等手段试图遏制中国高科技产业发展；2. 科技脱钩将导致全球科技产业链的碎片化，形成中美两大技术体系并存的格局；3. 中小国家在科技竞争中面临选边站的压力，技术主权意识不断增强。",
            "framework": "本文采用地缘政治经济学分析框架，结合技术民族主义理论，通过对美国出口管制政策文本和半导体产业数据的实证分析，构建了科技竞争的动态博弈模型。",
            "conclusions": "中美科技竞争将是长期化的常态化趋势，中国需要在自主创新和国际合作之间寻求平衡，积极参与全球科技治理规则制定，应对脱钩带来的挑战。",
            "innovation": "本文首次提出了\"技术治权\"的分析概念，揭示了科技竞争背后的制度性博弈逻辑，弥补了现有研究对治理维度的忽视。"
        },
        "summary_quality": 95,
        "created_at": "2024-03-14"
    },
    {
        "id": 2,
        "title": "美国亚太联盟体系的转型与未来走向",
        "authors": [{"name": "李四", "affiliation": "复旦大学美国研究中心"}, {"name": "王五", "affiliation": "斯坦福大学亚太研究中心"}],
        "journal": "International Security",
        "journal_zh": "国际安全",
        "publish_date": date(2024, 2, 20),
        "volume": "48",
        "issue": "3",
        "pages": "89-123",
        "doi": "10.1162/isec_a_00456",
        "url": "https://www.mitpressjournals.org/doi/10.1162/isec_a_00456",
        "abstract": "本文探讨了拜登政府时期美国亚太联盟体系的调整与转型，分析了印太战略框架下美日、美澳、美韩同盟的新变化，以及QUAD、AUKUS等新型多边安全机制的发展趋势。研究认为，美国正在构建多层次的安全网络，应对中国崛起带来的地区秩序挑战。",
        "research_areas": ["亚太安全", "美国联盟体系"],
        "structured_summary": {
            "core_problem": "本文研究了后冷战时代美国亚太联盟体系的适应性变革，以及其在印太战略背景下的功能扩展与制度创新对地区安全秩序的影响。",
            "main_points": "1. 美国亚太联盟正在从传统的双边轴辐模式向\"网络化安全架构\"转型，QUAD、AUKUS等多边机制成为重要补充；2. 联盟的功能从传统的军事防御向经济安全、科技安全、供应链安全等新领域扩展；3. 东盟的中心地位受到挑战，地区安全格局呈现\"双轨竞争\"态势。",
            "framework": "本文基于联盟理论和制度变迁理论，采用案例研究方法，对美日澳韩四个核心盟友的战略调整进行了比较分析。",
            "conclusions": "美国亚太联盟体系的转型将长期影响亚太安全格局，中国需要构建包容性的地区安全架构，对冲联盟体系扩张带来的安全压力。",
            "innovation": "本文提出了\"联盟网络化\"的分析框架，揭示了美国安全战略从\"地缘政治\"向\"地缘技术\"的转向。"
        },
        "summary_quality": 92,
        "created_at": "2024-03-14"
    },
    {
        "id": 3,
        "title": "美国半导体出口管制的政策逻辑与实施效果评估",
        "authors": [{"name": "赵六", "affiliation": "清华大学公共管理学院"}],
        "journal": "Review of International Political Economy",
        "journal_zh": "国际政治经济学评论",
        "publish_date": date(2024, 3, 10),
        "volume": "31",
        "issue": "2",
        "pages": "234-267",
        "doi": "10.1080/09692290.2023.2298765",
        "url": "https://www.tandfonline.com/doi/full/10.1080/09692290.2023.2298765",
        "abstract": "本文系统评估了美国对华半导体出口管制政策的实施效果，通过分析2018-2023年的产业数据，发现出口管制虽然在短期内对中国半导体产业造成了一定冲击，但也刺激了中国的自主研发投入，推动了国内供应链的国产化替代进程。",
        "research_areas": ["美国出口管制", "中美科技竞争", "科技与大国竞争"],
        "structured_summary": {
            "core_problem": "本文评估了特朗普和拜登政府时期实施的一系列半导体出口管制政策的实际效果，探讨了技术管制在大国竞争中的有效性边界。",
            "main_points": "1. 美国出口管制政策的核心目标是维持至少10-15年的技术代差，遏制中国在先进计算、人工智能等领域的发展；2. 管制政策产生了\"双刃剑\"效应，在制约中国的同时也损害了美国半导体企业的利益；3. 中国半导体产业的自主创新速度超出预期，国产化率不断提升。",
            "framework": "本文采用全球价值链分析框架，结合企业层面的专利数据和贸易数据，构建了技术管制效果的评估模型。",
            "conclusions": "出口管制无法阻止中国半导体产业的发展，反而会加速技术自主进程，美国需要重新审视其技术竞争战略。",
            "innovation": "本文首次量化评估了出口管制对中美半导体产业的双向影响，提出了\"技术管制的悖论\"这一核心命题。"
        },
        "summary_quality": 98,
        "created_at": "2024-03-14"
    }
]

# 侧边栏
st.sidebar.title("📚 国关顶刊动态助手")
st.sidebar.markdown("### 功能导航")
page = st.sidebar.radio("", ["最新文献", "高级搜索", "导出中心"])

# 筛选条件
st.sidebar.markdown("### 筛选条件")
selected_journal = st.sidebar.multiselect(
    "期刊",
    options=list(set([art["journal_zh"] for art in MOCK_ARTICLES]))
)
selected_area = st.sidebar.multiselect(
    "研究方向",
    options=["中美关系", "亚太安全", "美国联盟体系", "科技与大国竞争", "中美科技竞争", "美国出口管制", "美国科技政策"]
)
date_range = st.sidebar.date_input(
    "发表日期",
    value=(date(2024, 1, 1), date(2024, 12, 31))
)

# 主页面
if page == "最新文献":
    st.title("📰 最新文献")

    # 筛选数据
    filtered_articles = MOCK_ARTICLES
    if selected_journal:
        filtered_articles = [art for art in filtered_articles if art["journal_zh"] in selected_journal]
    if selected_area:
        filtered_articles = [art for art in filtered_articles if any(area in selected_area for area in art["research_areas"])]
    if date_range:
        start_date, end_date = date_range
        filtered_articles = [art for art in filtered_articles if start_date <= art["publish_date"] <= end_date]

    # 展示文章列表
    for art in filtered_articles:
        with st.expander(f"**{art['title']}**", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**作者**：{'; '.join([a['name'] for a in art['authors']])}")
                st.markdown(f"**期刊**：{art['journal_zh']} ({art['journal']})")
                st.markdown(f"**发表日期**：{art['publish_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**研究方向**：{' '.join([f'`{area}`' for area in art['research_areas']])}")
                st.markdown(f"**DOI**：[{art['doi']}]({art['url']})")
                st.markdown(f"**摘要**：{art['abstract']}")

                # 结构化摘要
                st.markdown("---")
                st.markdown("### 📋 结构化摘要")
                with st.container():
                    st.markdown("#### 🔍 核心问题")
                    st.write(art['structured_summary']['core_problem'])

                    st.markdown("#### 💡 主要观点")
                    st.write(art['structured_summary']['main_points'])

                    st.markdown("#### 📊 分析框架")
                    st.write(art['structured_summary']['framework'])

                    st.markdown("#### ✅ 研究结论")
                    st.write(art['structured_summary']['conclusions'])

                    st.markdown("#### ✨ 创新之处")
                    st.write(art['structured_summary']['innovation'])

            with col2:
                st.button("📥 导出本文", key=f"export_{art['id']}")
                st.button("🔗 访问原文", key=f"visit_{art['id']}", on_click=lambda u=art['url']: st.markdown(f'<meta http-equiv="refresh" content="0; url={u}">', unsafe_allow_html=True))

elif page == "高级搜索":
    st.title("🔍 高级搜索")
    keyword = st.text_input("关键词（标题、作者、摘要）")
    col1, col2 = st.columns(2)
    with col1:
        search_journal = st.selectbox("期刊", options=["全部"] + list(set([art["journal_zh"] for art in MOCK_ARTICLES])))
    with col2:
        search_area = st.selectbox("研究方向", options=["全部"] + ["中美关系", "亚太安全", "美国联盟体系", "科技与大国竞争", "中美科技竞争", "美国出口管制", "美国科技政策"])

    if st.button("搜索"):
        results = MOCK_ARTICLES
        if keyword:
            results = [art for art in results if keyword.lower() in art['title'].lower() or keyword.lower() in art['abstract'].lower() or any(keyword.lower() in a['name'].lower() for a in art['authors'])]
        if search_journal != "全部":
            results = [art for art in results if art['journal_zh'] == search_journal]
        if search_area != "全部":
            results = [art for art in results if search_area in art['research_areas']]

        st.success(f"找到 {len(results)} 条结果")
        for art in results:
            with st.expander(f"**{art['title']}**", expanded=False):
                st.markdown(f"**作者**：{'; '.join([a['name'] for a in art['authors']])}")
                st.markdown(f"**期刊**：{art['journal_zh']}")
                st.markdown(f"**发表日期**：{art['publish_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**摘要**：{art['abstract']}")

elif page == "导出中心":
    st.title("📥 文献导出")
    selected_ids = st.multiselect(
        "选择要导出的文章",
        options=[art['id'] for art in MOCK_ARTICLES],
        format_func=lambda x: next(art['title'] for art in MOCK_ARTICLES if art['id'] == x)
    )
    export_format = st.selectbox("导出格式", options=["Markdown", "Word", "CSV"])

    if st.button("生成导出文件") and selected_ids:
        selected_articles = [art for art in MOCK_ARTICLES if art['id'] in selected_ids]
        if export_format == "Markdown":
            # 生成Markdown内容
            md_content = "# 国关顶刊文献汇总\n\n"
            for art in selected_articles:
                authors = "; ".join([a["name"] for a in art["authors"]])
                summary = art["structured_summary"]
                md_content += f"## {art['title']}\n\n"
                md_content += f"- **作者**: {authors}\n"
                md_content += f"- **期刊**: {art['journal_zh']} ({art['journal']})\n"
                md_content += f"- **发表日期**: {art['publish_date'].strftime('%Y-%m-%d')}\n"
                md_content += f"- **DOI**: [{art['doi']}]({art['url']})\n\n"
                md_content += f"### 核心问题\n{summary['core_problem']}\n\n"
                md_content += f"### 主要观点\n{summary['main_points']}\n\n"
                md_content += f"### 分析框架\n{summary['framework']}\n\n"
                md_content += f"### 研究结论\n{summary['conclusions']}\n\n"
                md_content += f"### 创新之处\n{summary['innovation']}\n\n"
                md_content += "---\n\n"

            st.download_button(
                label="📥 下载Markdown文件",
                data=md_content,
                file_name="articles_export.md",
                mime="text/markdown"
            )
            st.success("导出文件已生成，点击下载即可！")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("📌 测试版仅包含样例数据，正式版将自动更新11本顶级SSCI期刊最新内容")
