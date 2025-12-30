import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 检查权限 - 扩展权限检查
entry_perms = ['data_entry', 'data_entry_sales', 'data_entry_costs', 
               'data_entry_exchange', 'data_entry_expenses', 
               'data_entry_model', 'data_entry_country', 'data_entry_currency']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in entry_perms)

if not has_permission:
    st.error("您没有权限访问此页面")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="数据填报",
    layout="wide"
)

def main():
    """改进的数据填报页面 - 分角色录入"""
    st.title(" 数据录入管理")
    
    # 获取当前用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    permissions = st.session_state.permissions
    db = get_db_manager()
    
    # 根据角色显示不同的录入选项
    st.markdown("### 选择录入类型")
    
    entry_options = []
    
    # 财务人员（FBP）的录入选项
    if 'data_entry_costs' in permissions:
        entry_options.append(" 成本数据 (Costs)")
    if 'data_entry_exchange' in permissions:
        entry_options.append(" 汇率数据 (Exchange)")
    if 'data_entry_expenses' in permissions:
        entry_options.append(" 费用数据 (Expenses)")
    if 'data_entry_model' in permissions:
        entry_options.append(" 机型数据 (Model)")
    if 'data_entry_country' in permissions:
        entry_options.append(" 国家数据 (Country)")
    
    # 销售人员的录入选项
    if 'data_entry_sales' in permissions:
        entry_options.append(" 销售数据 (Sales & Price)")
    # if 'data_entry_currency' in permissions:
    #     entry_options.append(" 币种设置 (Currency)")
    
    # 通用数据录入（兼容旧版）
    if 'data_entry' in permissions and not entry_options:
        entry_options.append(" 历史数据 (History)")
        entry_options.append(" 预算数据 (Budget)")
    
    if not entry_options:
        st.error("您没有可用的录入选项")
        return
    
    selected_entry = st.radio("", entry_options, horizontal=True)
    
    st.markdown("---")
    
    # 根据选择显示对应的录入表单
    if "成本数据" in selected_entry:
        show_costs_entry(db, u)
    elif "汇率数据" in selected_entry:
        show_exchange_entry(db, u)
    elif "费用数据" in selected_entry:
        show_expenses_entry(db, u)
    elif "机型数据" in selected_entry:
        show_model_entry(db, u)
    elif "国家数据" in selected_entry:
        show_country_entry(db, u)
    elif "销售数据" in selected_entry:
        show_sales_entry(db, u)
    # elif "币种设置" in selected_entry:
    #     show_currency_entry(db, u)
    elif "历史数据" in selected_entry:
        show_history_entry(db, u)
    elif "预算数据" in selected_entry:
        show_budget_entry(db, u)

def show_costs_entry(db, u):
    """财务：成本数据录入"""
    st.markdown("###  成本数据录入")
    
    tab1, tab2 = st.tabs([" 新增/修改", " 删除"])
    
    with tab1:
        with st.form("costs_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                model = st.selectbox("产品型号", db.get_all_models())
            
            with col2:
                country = st.selectbox("国家", db.get_all_countries())
            
            with col3:
                costs_time = st.text_input("成本时间 (YYYY-MM)", "2026-01")
            
            costs = st.number_input("单位成本 (¥)", min_value=0.0, value=0.0, step=0.01)
            
            submitted = st.form_submit_button(" 保存成本数据", type="primary", use_container_width=True)
            
            if submitted:
                try:
                    # 不指定Costs_id，让数据库自动生成
                    query = """
                        INSERT INTO Costs (Model, Country, Costs_time, Costs)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Costs = VALUES(Costs)
                    """
                    if db.execute_update(query, (model, country, costs_time, costs)):
                        db.log_event(u['id'], "COSTS_ENTRY", f"Added/Updated costs for {model} in {country}")
                        st.success(" 成本数据保存成功！")
                    else:
                        st.error(" 保存失败")
                except Exception as e:
                    st.error(f" 错误: {e}")
    
    with tab2:
        st.markdown("#### 删除成本数据")
        
        # 显示现有数据
        df_costs = db.get_costs_data()
        if not df_costs.empty:
            st.dataframe(df_costs, use_container_width=True, height=300)
            
            # 删除表单
            with st.form("delete_costs_form"):
                costs_id = st.number_input("输入要删除的 Costs_id", min_value=1, step=1)
                
                delete_btn = st.form_submit_button(" 删除", type="secondary")
                
                if delete_btn:
                    if db.delete_costs_data(costs_id):
                        db.log_event(u['id'], "COSTS_DELETE", f"Deleted costs_id {costs_id}")
                        st.success(" 删除成功！")
                        st.rerun()
                    else:
                        st.error(" 删除失败")
        else:
            st.info("暂无成本数据")

def show_exchange_entry(db, u):
    """财务：汇率数据录入"""
    st.markdown("###  汇率数据录入")
    
    with st.form("exchange_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            exchange_time = st.text_input("汇率时间 (YYYY-MM)", "2026-01")
        
        with col2:
            exchange_rate = st.number_input("USD汇率 (USD to CNY)", min_value=0.0, value=7.2, step=0.01)
        
        st.info(" 提示：输入1美元兑换人民币的汇率")
        
        submitted = st.form_submit_button(" 保存汇率", type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Exchange (Exchange_time, Exchange_rate)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE Exchange_rate = VALUES(Exchange_rate)
                """
                if db.execute_update(query, (exchange_time, exchange_rate)):
                    db.log_event(u['id'], "EXCHANGE_ENTRY", f"Set exchange rate {exchange_rate} for {exchange_time}")
                    st.success(" 汇率保存成功！")
                else:
                    st.error(" 保存失败")
            except Exception as e:
                st.error(f" 错误: {e}")

def show_expenses_entry(db, u):
    """财务：区域费用数据录入（4类费用）"""
    st.markdown("###  区域费用数据录入")
    st.caption("包括：营销费用、人工成本、其他变动费用、其他固定费用")
    
    tab1, tab2 = st.tabs([" 新增/修改", " 删除"])
    
    with tab1:
        with st.form("expenses_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                country = st.selectbox("国家", db.get_all_countries())
            
            with col2:
                expenses_time = st.text_input("费用时间 (YYYY-MM)", "2026-01")
            
            st.markdown("#### 费用明细")
            col1, col2 = st.columns(2)
            
            with col1:
                marketing_expenses = st.number_input("营销费用 (¥)", min_value=0.0, value=0.0, step=100.0)
                labor_cost = st.number_input("人工成本 (¥)", min_value=0.0, value=0.0, step=100.0)
            
            with col2:
                other_variable = st.number_input("其他变动费用 (¥)", min_value=0.0, value=0.0, step=100.0)
                other_fixed = st.number_input("其他固定费用 (¥)", min_value=0.0, value=0.0, step=100.0)
            
            submitted = st.form_submit_button(" 保存费用数据", type="primary", use_container_width=True)
            
            if submitted:
                try:
                    query = """
                        INSERT INTO Regional_Expenses (Country, Expenses_time, Marketing_expenses, 
                                                       Labor_cost, Other_variable_expenses, Other_fixed_expenses)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            Marketing_expenses = VALUES(Marketing_expenses),
                            Labor_cost = VALUES(Labor_cost),
                            Other_variable_expenses = VALUES(Other_variable_expenses),
                            Other_fixed_expenses = VALUES(Other_fixed_expenses)
                    """
                    if db.execute_update(query, (country, expenses_time, marketing_expenses, 
                                                 labor_cost, other_variable, other_fixed)):
                        db.log_event(u['id'], "EXPENSES_ENTRY", f"Added expenses for {country} at {expenses_time}")
                        st.success(" 费用数据保存成功！")
                    else:
                        st.error(" 保存失败")
                except Exception as e:
                    st.error(f" 错误: {e}")
    
    with tab2:
        st.markdown("#### 删除费用数据")
        
        df_expenses = db.execute_query("SELECT * FROM Regional_Expenses ORDER BY Expenses_time DESC")
        if not df_expenses.empty:
            st.dataframe(df_expenses, use_container_width=True, height=300)
            
            with st.form("delete_expenses_form"):
                col1, col2 = st.columns(2)
                with col1:
                    del_country = st.selectbox("国家", db.get_all_countries(), key="del_exp_country")
                with col2:
                    del_time = st.text_input("费用时间", "2026-01", key="del_exp_time")
                
                delete_btn = st.form_submit_button(" 删除", type="secondary")
                
                if delete_btn:
                    if db.delete_regional_expenses(del_country, del_time):
                        db.log_event(u['id'], "EXPENSES_DELETE", f"Deleted expenses for {del_country} at {del_time}")
                        st.success(" 删除成功！")
                        st.rerun()
                    else:
                        st.error(" 删除失败")
        else:
            st.info("暂无费用数据")

def show_model_entry(db, u):
    """财务：机型数据录入"""
    st.markdown("###  机型数据录入")
    
    with st.form("model_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model = st.text_input("产品型号", "ModelX")
        
        with col2:
            series = st.selectbox("系列", ["Dog", "Cat", "Tiger"])
        
        with col3:
            model_label = st.selectbox("型号标签", ["High-end", "Mid-range", "Entry-level"])
        
        submitted = st.form_submit_button(" 保存机型", type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Model (Model, Series, Model_label)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE Series = VALUES(Series), Model_label = VALUES(Model_label)
                """
                if db.execute_update(query, (model, series, model_label)):
                    db.log_event(u['id'], "MODEL_ENTRY", f"Added model {model}")
                    st.success(" 机型保存成功！")
                else:
                    st.error(" 保存失败")
            except Exception as e:
                st.error(f" 错误: {e}")

def show_country_entry(db, u):
    """财务：国家数据录入"""
    st.markdown("###  国家数据录入")
    
    with st.form("country_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            country = st.text_input("国家名称", "Brazil")
        
        with col2:
            market = st.selectbox("市场区域", ["Asia", "Africa", "South America"])
        
        submitted = st.form_submit_button(" 保存国家", type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Country (Country, Market)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE Market = VALUES(Market)
                """
                if db.execute_update(query, (country, market)):
                    db.log_event(u['id'], "COUNTRY_ENTRY", f"Added country {country}")
                    st.success(" 国家保存成功！")
                else:
                    st.error(" 保存失败")
            except Exception as e:
                st.error(f" 错误: {e}")

def show_sales_entry(db, u):
    """销售：销售量和售价录入"""
    st.markdown("###  销售数据录入")
    
    if u.get('country'):
        st.info(f" 当前区域: **{u['country']}** (您只能录入本国数据)")
        default_country = u['country']
        country_disabled = True
    else:
        default_country = "India"
        country_disabled = False
    
    tab1, tab2 = st.tabs([" 新增/修改", " 删除"])
    
    with tab1:
        with st.form("sales_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                time = st.text_input("时间周期 (YYYY-MM)", "2026-01")
            with col2:
                if country_disabled:
                    country = st.text_input("国家", default_country, disabled=True)
                else:
                    country = st.selectbox("国家", db.get_all_countries())
            with col3:
                model = st.selectbox("产品型号", db.get_all_models())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                currency = st.selectbox("币种", ["CHY", "USD"])
            with col2:
                sales = st.number_input("销售量", min_value=0, value=0, step=1)
            with col3:
                price = st.number_input("销售单价", min_value=0.0, value=0.0, step=0.01)
            
            submitted = st.form_submit_button(" 保存销售数据", type="primary", use_container_width=True)
            
            if submitted:
                try:
                    # 【修改点】：彻底删除 hashlib 相关代码
                    # 【修改点】：SQL 中删掉 id 字段，让数据库自增（仿照 Costs 逻辑）
                    query = """
                        INSERT INTO Sales_Price (Model, Country, h_Time, Currency, Sales, Price, Exchange_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            Currency = VALUES(Currency),
                            Sales = VALUES(Sales),
                            Price = VALUES(Price)
                    """
                    # 参数列表只保留 7 个，不再传入 record_id
                    params = (model, country, time, currency, sales, price, time)
                    
                    if db.execute_update(query, params):
                        db.log_event(u['id'], "SALES_ENTRY", f"Added sales for {model} in {country}")
                        st.success("  销售数据保存成功！")
                    else:
                        st.error("  保存失败")
                except Exception as e:
                    st.error(f"  错误: {e}")
    
    with tab2:
        st.markdown("#### 删除销售数据")
        df_sales = db.get_sales_price_data(u.get('country'))
        if not df_sales.empty:
            st.dataframe(df_sales, use_container_width=True, height=300)
            with st.form("delete_sales_form"):
                record_id_to_del = st.number_input("输入要删除的记录ID", min_value=1, step=1)
                delete_btn = st.form_submit_button(" 删除", type="secondary")
                if delete_btn:
                    if db.delete_sales_price(record_id_to_del):
                        db.log_event(u['id'], "SALES_DELETE", f"Deleted sales record {record_id_to_del}")
                        st.success(" 删除成功！")
                        st.rerun()
                    else:
                        st.error(" 删除失败")
        else:
            st.info("暂无销售数据")




def show_history_entry(db, u):
    """通用：历史数据录入（兼容旧版）"""
    st.markdown("###  历史数据录入")
    
    with st.form("history_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time = st.text_input("时间周期 (YYYY-MM)", "2026-01")
        
        with col2:
            country = st.selectbox("国家", db.get_all_countries())
        
        with col3:
            model = st.selectbox("产品型号", db.get_all_models())
        
        sales = st.number_input("销售量", min_value=0, value=0, step=1)
        
        submitted = st.form_submit_button(" 保存", type="primary", use_container_width=True)
        
        if submitted:
            row = {'h_Time': time, 'Country': country, 'Model': model, 'Sales': sales}
            df = pd.DataFrame([row])
            
            if db.save_data(df, "History"):
                db.log_event(u['id'], "HISTORY_ENTRY", f"Added history for {model} in {country}")
                st.success(" 数据保存成功！")
            else:
                st.error(" 保存失败")

def show_budget_entry(db, u):
    """通用：预算数据录入（兼容旧版）"""
    st.markdown("###  预算数据录入")
    
    with st.form("budget_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time = st.text_input("时间周期 (YYYY-MM)", "2026-01")
        
        with col2:
            country = st.selectbox("国家", db.get_all_countries())
        
        with col3:
            model = st.selectbox("产品型号", db.get_all_models())
        
        sales = st.number_input("预算销售量", min_value=0, value=0, step=1)
        
        submitted = st.form_submit_button(" 保存", type="primary", use_container_width=True)
        
        if submitted:
            row = {'h_Time': time, 'Country': country, 'Model': model, 'Sales': sales}
            df = pd.DataFrame([row])
            
            if db.save_data(df, "Budget"):
                db.log_event(u['id'], "BUDGET_ENTRY", f"Added budget for {model} in {country}")
                st.success(" 预算数据保存成功！")
            else:
                st.error(" 保存失败")

if __name__ == "__main__":
    main()