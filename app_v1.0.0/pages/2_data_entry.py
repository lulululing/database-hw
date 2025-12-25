# pages/2_📝_数据填报.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 检查权限
if 'data_entry' not in st.session_state.get('permissions', []):
    st.error("您没有权限访问此页面")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="数据填报",
    layout="wide"
)
st.title("数据录入")
# 语言管理函数
def get_text(text_dict):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    return text_dict.get(lang, text_dict.get('zh', ''))

def main():
    """数据填报页面"""
    # 多语言标题
    title_text = {
        'zh': '📝 数据填报',
        'en': '📝 Data Entry'
    }
    st.markdown(f'<div class="main-header">{get_text(title_text)}</div>', unsafe_allow_html=True)
    
    # 获取当前用户信息
    u = st.session_state.user_info
    db = get_db_manager()
    
    # 多语言文本
    text = {
        'zh': {
            'region_note': '**当前区域**: {country} (您只能填报指定国家的数据)',
            'time_label': '时间周期 (YYYY-MM)',
            'time_help': '格式: YYYY-MM',
            'country_label': '国家',
            'model_label': '产品型号',
            'model_help': '从数据库选择产品型号',
            'sales_label': '本期销量',
            'sales_help': '输入本期的销售数量',
            'current_selection': '**当前选择**: {market} - {country}',
            'note': '💡 **说明**: 仅需输入销量。系统将根据汇率、价格表、成本表及各类比率参数，**自动计算** 收入、毛利、净利等所有财务指标。',
            'save_button': '保存并自动计算',
            'save_success': '✅ 数据保存成功！财务指标已自动生成。',
            'save_failed': '❌ 保存失败，请检查基础参数表（汇率、价格、成本等）是否完整。',
            'generated_metrics': '📊 生成的财务指标'
        },
        'en': {
            'region_note': '**Current Region**: {country} (You can only enter data for your assigned country)',
            'time_label': 'Time Period (YYYY-MM)',
            'time_help': 'Format: YYYY-MM',
            'country_label': 'Country',
            'model_label': 'Product Model',
            'model_help': 'Select product model from database',
            'sales_label': 'Sales Quantity',
            'sales_help': 'Enter sales quantity for this period',
            'current_selection': '**Current Selection**: {market} - {country}',
            'note': '💡 **Note**: You only need to input sales quantity. The system will **automatically calculate** all financial metrics based on exchange rates, price tables, cost tables, and various ratio parameters.',
            'save_button': 'Save & Auto-Calculate',
            'save_success': '✅ Data saved successfully! Financial metrics have been automatically generated.',
            'save_failed': '❌ Save failed. Please check if basic parameter tables are complete.',
            'generated_metrics': '📊 Generated Financial Metrics'
        }
    }
    current_text = get_text(text)
    
    # 如果是业务员，只能填报自己国家的数据
    if u.get('country'):
        st.info(current_text['region_note'].format(country=u['country']))
        default_country = u['country']
        country_select_disabled = True
    else:
        default_country = "India"
        country_select_disabled = False
    
    # 输入表单
    with st.form("data_entry_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time = st.text_input(current_text['time_label'], "2026-01", help=current_text['time_help'])
        
        with col2:
            if country_select_disabled:
                country = st.text_input(current_text['country_label'], default_country, disabled=True)
            else:
                country = st.selectbox(current_text['country_label'], ["India", "Pakistan", "Kenya", "South Africa", "Mexico", "Peru"])
        
        with col3:
            # 从数据库获取型号列表
            models = db.get_all_models()
            model = st.selectbox(current_text['model_label'], models, help=current_text['model_help'])
        
        # 市场映射
        market_map = {
            "India": "Asia", "Pakistan": "Asia", 
            "Kenya": "Africa", "South Africa": "Africa", 
            "Mexico": "South America", "Peru": "South America"
        }
        market = market_map.get(country, "Asia")
        
        st.markdown("---")
        
        col_input, col_info = st.columns([1, 2])
        
        with col_input:
            sales = st.number_input(current_text['sales_label'], min_value=0, value=0, step=1, 
                                   help=current_text['sales_help'])
        
        with col_info:
            st.info(f"{current_text['current_selection'].format(market=market, country=country)}\n\n{current_text['note']}")
        
        submitted = st.form_submit_button(current_text['save_button'], type="primary", use_container_width=True)
        
        if submitted:
            # 构建数据行
            row = {
                'h_Time': time,
                'Country': country,
                'Market': market,
                'Model': model,
                'Sales': sales
            }
            df = pd.DataFrame([row])
            
            # 自动计算 + 保存
            if db.save_data(df, "History"):
                db.log_event(u['id'], "DATA_ENTRY", f"Entered {model} sales {sales} for {country}")
                st.success(current_text['save_success'])
                
                # 显示计算后的数据预览
                with st.expander(current_text['generated_metrics']):
                    calculated_df = db.calculate_financials(df)
                    if not calculated_df.empty:
                        st.dataframe(calculated_df, use_container_width=True)
            else:
                st.error(current_text['save_failed'])

if __name__ == "__main__":
    main()