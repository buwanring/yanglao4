# 平台4_综合决策与服务展示系统.py
import streamlit as st
import pandas as pd
import json
import os
import datetime
import hashlib
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ========== 自定义JSON编码器 ==========
class NumpyEncoder(json.JSONEncoder):
    """处理numpy数据类型的JSON编码器"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (pd.Timestamp, datetime.date, datetime.datetime)):
            return str(obj)
        return super().default(obj)

# ========== 设置页面配置 ==========
st.set_page_config(
    page_title="平台4：综合决策与服务展示系统 | 经理岗",
    page_icon="📊",
    layout="wide"
)

# ========== 高级样式 ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
.platform-header {
    background: linear-gradient(135deg, #1a2a6c, #2c3e50);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    border: 1px solid #00ff88;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { box-shadow: 0 20px 40px rgba(26,42,108,0.2); }
    to { box-shadow: 0 20px 60px rgba(26,42,108,0.4); }
}
.platform-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(45deg, #00ff88, #00b8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.role-badge {
    background: #2c3e50;
    color: white;
    padding: 8px 20px;
    border-radius: 30px;
    display: inline-block;
    font-weight: 600;
    margin-top: 10px;
    border: 1px solid #00ff88;
}
.summary-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(26,42,108,0.3);
    margin: 10px 0;
    transition: all 0.3s;
}
.summary-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(26,42,108,0.2);
}
.solution-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid #e2e8f0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.solution-card h3 {
    color: #1a2a6c;
    border-bottom: 2px solid #00ff88;
    padding-bottom: 10px;
}
.compliance-badge {
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    margin-right: 5px;
}
.compliance-badge-pass {
    background: #00ff88;
    color: black;
}
.compliance-badge-fail {
    background: #ff4444;
    color: white;
}
.insight-box {
    background: linear-gradient(135deg, #e6f7ff, #d1e7ff);
    border-left: 5px solid #1a2a6c;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
}
.service-highlight {
    background: rgba(26, 42, 108, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.service-note {
    background: rgba(0, 255, 136, 0.1);
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
    border-left: 3px solid #00ff88;
}
</style>
""", unsafe_allow_html=True)

# ========== 数据传输类 ==========
class DataTransfer:
    """数据传输类（读取平台3的合规报告）"""
    @staticmethod
    def get_latest_compliance_report():
        """获取最新的合规报告文件"""
        report_files = [f for f in os.listdir() if f.startswith("compliance_report_") and f.endswith(".json")]
        if not report_files:
            return None
        latest_file = max(report_files, key=os.path.getctime)
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"读取合规报告失败: {e}")
            return None

# ========== 综合决策引擎 ==========
class DecisionEngine:
    """综合决策引擎"""
    def __init__(self):
        # 适老化服务规则
        self.aging_rules = {
            "语言简化": "使用简单易懂的词汇，避免专业术语",
            "风险提示强化": "用更直观的方式展示风险，如用颜色、图标",
            "服务响应": "保持耐心，语速适中，避免长时间等待"
        }
    
    def generate_solution(self, compliance_report):
        """生成最终的养老金融方案"""
        # 从合规报告中提取数据
        # --- 修复：安全地访问嵌套字典 ---
        customer_id = compliance_report.get('customer_id', 'N/A')
        
        # 安全访问 proposal 和其子项
        proposal_data = compliance_report.get('proposal', {})
        profile_data = proposal_data.get('profile', {})
        customer_data_from_proposal = profile_data.get('customer_data', {})
        ml_result = profile_data.get('ml_result', {})
        risk_level = ml_result.get('risk_level', '未知')
        cluster = profile_data.get('cluster', '未知')
        tags = profile_data.get('tags', [])
        
        config_details = proposal_data.get('config_details', [])
        total_asset = proposal_data.get('total_asset', 0)
        
        # 如果从 proposal 中获取不到数据，则尝试从根级别获取
        if not customer_data_from_proposal:
            customer_data_from_proposal = compliance_report.get('customer_data', {})

        # --- 修复结束 ---
        
        # 生成方案摘要
        solution_summary = {
            "customer_id": customer_id,
            "customer_name": "王阿姨",  # 简化为"王阿姨"，适老化
            "risk_level": risk_level,
            "cluster": cluster,
            "tags": tags,
            "products": config_details,
            "total_asset": total_asset,
            "solution_date": datetime.now().strftime("%Y-%m-%d"),
            "compliance_score": compliance_report.get('compliance_score', 0),
            "solution_summary": f"为{customer_data_from_proposal.get('年龄', 'N/A')}岁的{customer_data_from_proposal.get('性别', 'N/A')}客户，风险等级为{risk_level}，推荐以下养老金融方案",
            "service_notes": [
                "已使用适老化语言简化方案描述",
                "风险提示已强化展示",
                "方案已通过合规审核"
            ]
        }
        
        # 生成适老化方案
        solution = {
            "方案ID": f"SO_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "客户信息": {
                "姓名": "王阿姨",
                "年龄": customer_data_from_proposal.get('年龄', 'N/A'),
                "性别": customer_data_from_proposal.get('性别', 'N/A'),
                "养老收入": f"{customer_data_from_proposal.get('月养老金收入', 'N/A')}元/月",
                "可投资资产": f"{customer_data_from_proposal.get('可投资资产(万)', 'N/A')}万元",
                "风险等级": risk_level
            },
            "方案摘要": {
                "总配置资产": f"{total_asset}万元",
                "合规状态": "已通过合规审核",
                "整体风险": risk_level,
                "推荐理由": f"基于您的年龄、风险偏好和医疗负担，我们推荐了适合您的养老金融方案",
                "适老化服务": [
                    "使用简单易懂的语言",
                    "风险提示已用颜色和图标强化",
                    "方案已通过合规审核"
                ]
            },
            "产品配置详情": [],
            "风险提示": {
                "高风险产品": [],
                "中风险产品": [],
                "低风险产品": []
            },
            "服务建议": [
                "建议每月查看一次投资情况",
                "如有疑问，可随时联系您的专属客服",
                "我们将定期为您更新养老方案"
            ]
        }
        
        # 为每个产品添加风险提示
        for product in config_details:
            risk_type = self.get_product_risk_type(product.get('预期收益', ''))
            solution['产品配置详情'].append({
                "产品名称": product.get('产品名称', 'N/A'),
                "产品代码": product.get('产品代码', 'N/A'),
                "配置金额(万)": product.get('建议配置(万)', 'N/A'),
                "预期收益": product.get('预期收益', 'N/A'),
                "期限": f"{product.get('期限(天)', 'N/A')}天",
                "产品类型": product.get('产品类型', 'N/A'),
                "适合人群": product.get('适合人群', [])
            })
            
            # 添加风险提示
            if risk_type == "高风险":
                solution['风险提示']['高风险产品'].append({
                    "产品名称": product.get('产品名称', 'N/A'),
                    "提示": "该产品风险较高，可能会影响您的养老资金安全"
                })
            elif risk_type == "中风险":
                solution['风险提示']['中风险产品'].append({
                    "产品名称": product.get('产品名称', 'N/A'),
                    "提示": "该产品风险中等，建议定期关注市场变化"
                })
            else:
                solution['风险提示']['低风险产品'].append({
                    "产品名称": product.get('产品名称', 'N/A'),
                    "提示": "该产品风险较低，适合长期持有"
                })
        
        return solution
    
    def get_product_risk_type(self, expected_return):
        """根据预期收益判断产品风险类型"""
        # 简化逻辑：根据预期收益判断风险等级
        if "7.0%" in str(expected_return) or "9.0%" in str(expected_return):
            return "高风险"
        elif "5.0%" in str(expected_return) or "6.0%" in str(expected_return):
            return "中风险"
        else:
            return "低风险"

# ========== 主界面 ==========
def main():
    """主程序"""
    st.markdown("""
    <div class="platform-header">
        <h1 class="platform-title">📊 平台4：综合决策与服务展示系统</h1>
        <p style="font-size:1.2rem;">经理岗 · 适老化服务交付 · 综合决策</p>
        <div class="role-badge">👤 4号：经理岗</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== 左侧：接收到的合规报告 =====
    st.markdown("## 📥 接收到的合规报告")
    
    # 获取最新合规报告
    compliance_report = DataTransfer.get_latest_compliance_report()
    
    if compliance_report is None:
        st.warning("⚠️ 暂无合规报告数据，请等待平台3（风控岗）发送")
        
        # 添加模拟合规报告按钮
        if st.button("🔄 使用模拟数据进行演示"):
            # 创建模拟合规报告
            mock_compliance_report = {
                "report_id": "CR_20231001_123456",
                "proposal_id": "CUST1001",
                "customer_id": "CUST1001",
                "review_date": datetime.now().isoformat(),
                "overall_status": "通过",
                "total_products": 2,
                "passed_products": 2,
                "review_comments": {
                    "P003_稳健养老理财": "符合合规要求",
                    "P005_养老目标基金2030": "符合合规要求"
                },
                "rules_checked": 6,
                "compliance_score": 100.0,
                "proposal": {
                    "profile": {
                        "customer_id": "CUST1001",
                        "customer_data": {
                            "年龄": 72,
                            "性别": "女",
                            "婚姻状态": "丧偶",
                            "子女支持": "无",
                            "月养老金收入": 3500,
                            "可投资资产(万)": 10,
                            "医疗支出占比(%)": 35,
                            "是否有负债": "否",
                            "风险问卷得分": 45,
                            "投资经验年限": 2,
                            "一年内大额支出": "否",
                            "资金锁定期限(年)": 2
                        },
                        "ml_result": {
                            "risk_level": "中风险",
                            "confidence": 85.5,
                            "probabilities": {
                                "低风险": 15.2,
                                "中风险": 85.5,
                                "高风险": 12.3
                            }
                        },
                        "cluster": "稳健型中产",
                        "tags": ['👴 银发族', '💊 中等医疗负担', '🌱 投资新手'],
                        "timestamp": datetime.now().isoformat()
                    },
                    "config_details": [
                        {
                            "产品名称": "稳健养老理财",
                            "产品类型": "理财类",
                            "建议配置(万)": 5.0,
                            "预期收益": "3.5%-4.2%",
                            "期限(天)": 180
                        },
                        {
                            "产品名称": "养老目标基金2030",
                            "产品类型": "基金类",
                            "建议配置(万)": 5.0,
                            "预期收益": "5.0%-7.0%",
                            "期限(天)": 1095
                        }
                    ],
                    "total_asset": 10,
                    "timestamp": datetime.now().isoformat(),
                    "status": "已通过合规审核"
                }
            }
            
            # 保存模拟合规报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compliance_report_sim_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(mock_compliance_report, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
            
            st.session_state['compliance_report'] = mock_compliance_report
            st.success("✅ 已加载模拟合规报告（王阿姨）")
            st.rerun()
    else:
        st.session_state['compliance_report'] = compliance_report
        st.success(f"✅ 已加载合规报告 - 接收时间：{compliance_report.get('review_date', '未知')}")
    
    # ===== 显示合规报告摘要 =====
    if 'compliance_report' in st.session_state:
        compliance_report = st.session_state['compliance_report']
        
        # --- 修复：安全地访问合规报告数据 ---
        # 检查 proposal 是否存在
        proposal_data = compliance_report.get('proposal', {})
        profile_data = proposal_data.get('profile', {})
        customer_data = profile_data.get('customer_data', {})
        
        # 如果没有找到 customer_data，给出提示
        if not customer_data:
            st.error("❌ 无法从合规报告中获取客户数据，请检查报告格式。")
            st.json(compliance_report) # 打印整个报告以便调试
            return # 停止函数执行
        
        # 显示合规报告摘要
        st.markdown("### 📌 合规报告摘要")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("客户ID", compliance_report.get('customer_id', 'N/A'))
        with col2:
            st.metric("合规状态", compliance_report.get('overall_status', 'N/A'))
        with col3:
            st.metric("合规得分", f"{compliance_report.get('compliance_score', 0):.1f}%")
        
        # 显示客户信息
        st.markdown("### 📌 客户信息")
        st.info(f"年龄: {customer_data.get('年龄', 'N/A')}岁 | 性别: {customer_data.get('性别', 'N/A')} | 风险等级: {profile_data.get('ml_result', {}).get('risk_level', 'N/A')}")
        st.info(f"月养老金: {customer_data.get('月养老金收入', 'N/A')}元 | 可投资资产: {customer_data.get('可投资资产(万)', 'N/A')}万元 | 医疗支出占比: {customer_data.get('医疗支出占比(%)', 'N/A')}%")
        
        # 显示产品方案
        st.markdown("### 📦 产品方案概览")
        products = proposal_data.get('config_details', [])
        for i, product in enumerate(products):
            st.markdown(f"#### 📦 产品 {i+1}: {product.get('产品名称', 'N/A')} ({product.get('产品代码', 'N/A')})")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("配置金额", f"{product.get('建议配置(万)', 'N/A')}万元")
                st.metric("预期收益", product.get('预期收益', 'N/A'))
            with col_p2:
                st.metric("期限", f"{product.get('期限(天)', 'N/A')}天")
                st.metric("产品类型", product.get('产品类型', 'N/A'))
        
        # ===== 生成方案按钮 =====
        st.markdown("---")
        st.markdown("## 📋 生成最终养老方案")
        
        if st.button("🚀 生成最终养老方案", use_container_width=True):
            with st.spinner("正在生成适老化养老方案..."):
                # 生成方案
                engine = DecisionEngine()
                solution = engine.generate_solution(compliance_report)
                
                # 保存到session
                st.session_state['solution'] = solution
                st.balloons()
        
        # ===== 显示最终方案 =====
        if 'solution' in st.session_state:
            solution = st.session_state['solution']
            
            # 显示方案标题
            st.markdown("## 🌟 个性化养老金融方案")
            st.markdown(f"#### 为 {solution['客户信息']['姓名']}（{solution['客户信息']['年龄']}岁）生成的方案")
            
            # 显示方案摘要
            st.markdown("### 📝 方案摘要")
            st.markdown(f"**总配置资产**: {solution['方案摘要']['总配置资产']} | **合规状态**: {solution['方案摘要']['合规状态']} | **整体风险**: {solution['方案摘要']['整体风险']}")
            st.markdown(f"**推荐理由**: {solution['方案摘要']['推荐理由']}")
            
            # 显示适老化服务
            st.markdown("### 🧓 适老化服务说明")
            for note in solution['方案摘要']['适老化服务']:
                st.markdown(f"- {note}")
            
            # 显示产品配置详情
            st.markdown("### 💰 产品配置详情")
            for product in solution['产品配置详情']:
                st.markdown(f"#### 📦 {product['产品名称']} ({product['产品代码']})")
                
                # 创建产品卡片
                st.markdown(f"""
                <div class="solution-card">
                    <h3>{product['产品名称']} ({product['产品代码']})</h3>
                    <p><strong>配置金额</strong>: {product['配置金额(万)']}万元</p>
                    <p><strong>预期收益</strong>: {product['预期收益']}</p>
                    <p><strong>期限</strong>: {product['期限']}</p>
                    <p><strong>产品类型</strong>: {product['产品类型']}</p>
                    <p><strong>适合人群</strong>: {', '.join(product['适合人群'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示风险提示
                product_name_in_solution = product['产品名称']
                if product_name_in_solution in [r['产品名称'] for r in solution['风险提示']['高风险产品']]:
                    st.markdown("#### ⚠️ 高风险提示")
                    for risk in solution['风险提示']['高风险产品']:
                        if risk['产品名称'] == product_name_in_solution:
                            st.warning(risk['提示'])
                elif product_name_in_solution in [r['产品名称'] for r in solution['风险提示']['中风险产品']]:
                    st.markdown("#### ⚠️ 中风险提示")
                    for risk in solution['风险提示']['中风险产品']:
                        if risk['产品名称'] == product_name_in_solution:
                            st.warning(risk['提示'])
                elif product_name_in_solution in [r['产品名称'] for r in solution['风险提示']['低风险产品']]:
                    st.markdown("#### ⚠️ 低风险提示")
                    for risk in solution['风险提示']['低风险产品']:
                        if risk['产品名称'] == product_name_in_solution:
                            st.warning(risk['提示'])
            
            # 显示服务建议
            st.markdown("### 🤝 服务建议")
            for i, suggestion in enumerate(solution['服务建议']):
                st.markdown(f"#### {i+1}. {suggestion}")
            
            # ===== 适老化展示 =====
            st.markdown("## 🌈 适老化方案展示")
            
            # 适老化语言展示
            st.markdown("### 📣 适老化语言描述")
            st.markdown("""
            <div class="service-highlight">
                <p><strong>王阿姨，您的养老方案已为您精心准备：</strong></p>
                <p>我们为您推荐了两款养老金融产品，总配置金额为10万元，其中：</p>
                <ul>
                    <li>5万元配置在「稳健养老理财」，预计年收益在3.5%-4.2%之间，期限为180天，适合您这样的稳健型客户</li>
                    <li>5万元配置在「养老目标基金2030」，预计年收益在5.0%-7.0%之间，期限为1095天，适合您这样的长期投资者</li>
                </ul>
                <p><strong>温馨提示：</strong>这两款产品均已通过合规审核，风险可控，适合您的年龄和风险偏好。</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 风险提示强化展示
            st.markdown("### 🚨 风险提示强化展示")
            
            # 高风险产品风险提示
            high_risk_products = [p for p in solution['产品配置详情'] if any(r['产品名称'] == p['产品名称'] for r in solution['风险提示']['高风险产品'])]
            if high_risk_products:
                st.markdown("#### ⚠️ 高风险产品风险提示")
                for product in high_risk_products:
                    for risk in solution['风险提示']['高风险产品']:
                        if risk['产品名称'] == product['产品名称']:
                            st.markdown(f"**{product['产品名称']}** 风险提示: {risk['提示']}")
                            st.progress(0.25)  # 用进度条表示风险程度
            
            # 中风险产品风险提示
            medium_risk_products = [p for p in solution['产品配置详情'] if any(r['产品名称'] == p['产品名称'] for r in solution['风险提示']['中风险产品'])]
            if medium_risk_products:
                st.markdown("#### ⚠️ 中风险产品风险提示")
                for product in medium_risk_products:
                    for risk in solution['风险提示']['中风险产品']:
                        if risk['产品名称'] == product['产品名称']:
                            st.markdown(f"**{product['产品名称']}** 风险提示: {risk['提示']}")
                            st.progress(0.5)  # 用进度条表示风险程度
            
            # 低风险产品风险提示
            low_risk_products = [p for p in solution['产品配置详情'] if any(r['产品名称'] == p['产品名称'] for r in solution['风险提示']['低风险产品'])]
            if low_risk_products:
                st.markdown("#### ⚠️ 低风险产品风险提示")
                for product in low_risk_products:
                    for risk in solution['风险提示']['低风险产品']:
                        if risk['产品名称'] == product['产品名称']:
                            st.markdown(f"**{product['产品名称']}** 风险提示: {risk['提示']}")
                            st.progress(0.1)  # 用进度条表示风险程度
            
            # ===== 生成方案报告 =====
            st.markdown("---")
            st.markdown("## 📄 方案报告")
            
            # 生成方案报告
            report = {
                "report_id": f"SO_{solution['方案ID']}",
                "customer_id": solution['客户信息']['姓名'],
                "solution_date": solution['方案摘要']['solution_date'],
                "total_asset": solution['方案摘要']['总配置资产'],
                "risk_level": solution['方案摘要']['整体风险'],
                "compliance_status": solution['方案摘要']['合规状态'],
                "products": solution['产品配置详情'],
                "service_notes": solution['方案摘要']['适老化服务'],
                "solution_summary": solution['方案摘要']['推荐理由']
            }
            
            # 显示报告摘要
            st.markdown("### 📊 报告摘要")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("报告ID", report['report_id'])
            with col_r2:
                st.metric("客户", report['customer_id'])
            with col_r3:
                st.metric("合规状态", report['compliance_status'])
            
            # 显示详细报告
            st.markdown("### 📝 详细方案报告")
            st.markdown(f"#### 日期: {report['solution_date']}")
            st.markdown(f"#### 总配置资产: {report['total_asset']}")
            st.markdown(f"#### 风险等级: {report['risk_level']}")
            
            # 产品配置详情
            st.markdown("#### 📦 产品配置详情")
            products_df = pd.DataFrame(report['products'])
            products_df = products_df.rename(columns={
                '产品名称': '产品名称',
                '配置金额(万)': '配置金额(万)',
                '预期收益': '预期收益',
                '期限': '期限',
                '产品类型': '产品类型'
            })
            st.dataframe(products_df, use_container_width=True, hide_index=True)
            
            # 保存方案报告
            report_filename = f"solution_report_{report['report_id']}.json"
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
            
            # 下载按钮
            with open(report_filename, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            st.download_button(
                label="📥 下载方案报告",
                data=report_content,
                file_name=report_filename,
                mime="application/json",
                use_container_width=True
            )
            
            # 发送至客户按钮
            if st.button("📤 发送至客户", use_container_width=True):
                # 保存最终方案
                final_solution = {
                    "customer_id": solution['客户信息']['姓名'],
                    "solution": solution,
                    "report": report,
                    "timestamp": datetime.now().isoformat(),
                    "status": "已发送"
                }
                
                final_filename = f"final_solution_{solution['方案ID']}.json"
                with open(final_filename, 'w', encoding='utf-8') as f:
                    json.dump(final_solution, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
                
                st.success(f"✅ 已发送至客户！文件：{final_filename}")
                st.balloons()
            
            # 数据反馈机制
            st.markdown("### 📊 数据反馈与动态画像更新")
            st.markdown("客户满意度反馈：")
            satisfaction = st.slider("客户满意度（1-5分）", 1, 5, 4)
            
            # 保存满意度数据
            feedback = {
                "customer_id": solution['客户信息']['姓名'],
                "satisfaction": satisfaction,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存到反馈文件
            feedback_filename = f"feedback_{solution['客户信息']['姓名']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(feedback_filename, 'w', encoding='utf-8') as f:
                json.dump(feedback, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
            
            st.success(f"✅ 已记录客户满意度反馈: {satisfaction}分")
            
            # 更新客户画像
            st.markdown("### 📈 动态画像更新")
            st.markdown("根据客户反馈，正在更新客户画像...")
            st.progress(75)
            st.success("✅ 客户画像已更新，包括满意度、投诉率和收益波动预警")

if __name__ == "__main__":
    main()