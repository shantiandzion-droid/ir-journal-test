"""
国关顶刊动态助手 正式版
自动每周更新11本顶级SSCI期刊最新内容
"""
import streamlit as st
import pandas as pd
from datetime import date, datetime
import json
import os

# 页面配置
st.set_page_config(
    page_title="国关顶刊动态助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 加载数据
@st.cache_data(ttl=86400) # 缓存1天
def load_articles():
    # 优先加载已处理的正式数据
    if os.path.exists("articles.json"):
        with open("articles.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # 兜底测试数据
    return [
        {
            "id": 1,
            "title": "中美科技竞争的地缘政治经济学分析",
            "authors": [{"name": "张三", "affiliation": "北京大学国际关系学院"}],
            "journal": "International Organization",
            "journal_zh": "国际组织",
            "publish_date": "2024-01-15",
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
        }
    ]

ARTICLES = load_articles()
RESEARCH_AREAS = ["中美关系", "亚太安全", "美国联盟体系", "科技与大国竞争", "中美科技竞争", "美国出口管制", "美国科技政策"]

# 侧边栏
st.sidebar.title("📚 国关顶刊动态助手")
st.sidebar.markdown("### 功能导航")
page = st.sidebar.radio("", ["最新文献", "高级搜索", "导出中心"])

# 筛选条件
st.sidebar.markdown("### 筛选条件")
selected_journal = st.sidebar.multiselect(
    "期刊",
    options=list(set([art["journal_zh"] for art in ARTICLES]))
)
selected_area = st.sidebar.multiselect(
    "研究方向",
    options=RESEARCH_AREAS
)
date_range = st.sidebar.date_input(
    "发表日期",
    value=(date(2024, 1, 1), date.today())
)

# 主页面
if page == "最新文献":
    st.title("📰 最新文献")
    st.info(f"📊 共收录 {len(ARTICLES)} 篇符合研究方向的顶刊文章，每周一自动更新")

    # 筛选数据
    filtered_articles = ARTICLES
    if selected_journal:
        filtered_articles = [art for art in filtered_articles if art["journal_zh"] in selected_journal]
    if selected_area:
        filtered_articles = [art for art in filtered_articles if any(area in selected_area for area in art["research_areas"])]
    if date_range:
        start_date, end_date = date_range
        filtered_articles = [art for art in filtered_articles if start_date <= datetime.strptime(art["publish_date"], "%Y-%m-%d").date() <= end_date]

    # 展示文章列表
    for art in filtered_articles:
        with st.expander(f"**{art['title']}**", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**作者**：{'; '.join([a['name'] for a in art['authors']])}")
                st.markdown(f"**期刊**：{art['journal_zh']} ({art['journal']})")
                st.markdown(f"**发表日期**：{art['publish_date']}")
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
        search_journal = st.selectbox("期刊", options=["全部"] + list(set([art["journal_zh"] for art in ARTICLES])))
    with col2:
        search_area = st.selectbox("研究方向", options=["全部"] + RESEARCH_AREAS)

    if st.button("搜索"):
        results = ARTICLES
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
                st.markdown(f"**发表日期**：{art['publish_date']}")
                st.markdown(f"**摘要**：{art['abstract']}")

elif page == "导出中心":
    st.title("📥 文献导出")
    selected_ids = st.multiselect(
        "选择要导出的文章",
        options=[art['id'] for art in ARTICLES],
        format_func=lambda x: next(art['title'] for art in ARTICLES if art['id'] == x)
    )
    export_format = st.selectbox("导出格式", options=["Markdown", "Word", "CSV"])

    if st.button("生成导出文件") and selected_ids:
        selected_articles = [art for art in ARTICLES if art['id'] in selected_ids]
        if export_format == "Markdown":
            # 生成Markdown内容
            md_content = "# 国关顶刊文献汇总\n\n"
            for art in selected_articles:
                authors = "; ".join([a["name"] for a in art["authors"]])
                summary = art["structured_summary"]
                md_content += f"## {art['title']}\n\n"
                md_content += f"- **作者**: {authors}\n"
                md_content += f"- **期刊**: {art['journal_zh']} ({art['journal']})\n"
                md_content += f"- **发表日期**: {art['publish_date']}\n"
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
st.sidebar.info("📌 正式版每周一自动更新11本顶级SSCI期刊最新内容")
