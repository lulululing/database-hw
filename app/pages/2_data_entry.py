# app/pages/2_data_entry.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager
from utils.i18n import get_text, show_sidebar_with_nav
from utils.helper import handle_save_success

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_warning'))
    st.switch_page("app.py")

show_sidebar_with_nav()

# 检查权限 - 扩展权限检查
entry_perms = ['data_entry', 'data_entry_sales', 'data_entry_costs', 
               'data_entry_exchange', 'data_entry_expenses', 
               'data_entry_model', 'data_entry_country', 'data_entry_currency']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in entry_perms)

if not has_permission:
    st.error(get_text('no_permission'))
    st.stop()

# 设置页面
st.set_page_config(
    page_title=get_text('entry_page_title'),
    layout="wide"
)

def main():
    """改进的数据填报页面 - 分角色录入"""
    try:
        db = get_db_manager()
        username = st.session_state.get('username', '')
        role = st.session_state.get('role', '')
        db.insert_system_log(
            action_type="VIEW",
            details=f"访问数据填报页面",
            username=username,
            role=role
        )
    except Exception as e:
        print(f"记录页面访问日志失败: {e}")
    st.title(f"{get_text('entry_page_title')}")
    
    # 获取当前用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    permissions = st.session_state.permissions
    db = get_db_manager()
    
    # 根据角色显示不同的录入选项 - 使用权限映射
    st.markdown(f"### {get_text('entry_select_type')}")
    
    # 构建权限映射字典
    options_map = {}
    
    # 财务人员（FBP）的录入选项
    if 'data_entry_costs' in permissions:
        options_map[get_text('entry_opt_costs')] = 'costs'
    if 'data_entry_exchange' in permissions:
        options_map[get_text('entry_opt_exchange')] = 'exchange'
    if 'data_entry_expenses' in permissions:
        options_map[get_text('entry_opt_expenses')] = 'expenses'
    if 'data_entry_model' in permissions:
        options_map[get_text('entry_opt_model')] = 'model'
    if 'data_entry_country' in permissions:
        options_map[get_text('entry_opt_country')] = 'country'
    
    # 销售人员的录入选项
    if 'data_entry_sales' in permissions:
        options_map[get_text('entry_opt_sales')] = 'sales'
    # if 'data_entry_currency' in permissions:
    #     options_map[get_text('entry_opt_currency')] = 'currency'
    
    # 通用数据录入（兼容旧版）
    if 'data_entry' in permissions and not options_map:
        options_map[get_text('entry_opt_history')] = 'history'
        options_map[get_text('entry_opt_budget')] = 'budget'
    
    if not options_map:
        st.error(get_text('msg_no_entry_opt'))
        return
    
    # 显示选项（使用翻译后的文本）
    selected_label = st.radio(
        "", 
        list(options_map.keys()), 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # 获取对应的内部标识
    selected_key = options_map[selected_label]
    
    st.markdown("---")
    
    # 根据选择显示对应的录入表单
    if selected_key == 'costs':
        show_costs_entry(db, u)
    elif selected_key == 'exchange':
        show_exchange_entry(db, u)
    elif selected_key == 'expenses':
        show_expenses_entry(db, u)
    elif selected_key == 'model':
        show_model_entry(db, u)
    elif selected_key == 'country':
        show_country_entry(db, u)
    elif selected_key == 'sales':
        show_sales_entry(db, u)
    elif selected_key == 'history':
        show_history_entry(db, u)
    elif selected_key == 'budget':
        show_budget_entry(db, u)

def show_costs_entry(db, u):
    """财务：成本数据录入"""
    st.markdown(f"### {get_text('costs_entry_title')}")
    
    tab1, tab2 = st.tabs([get_text('tab_add_update'), get_text('tab_delete')])
    
    with tab1:
        with st.form("costs_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                model = st.selectbox(get_text('ph_model'), db.get_all_models())
            
            with col2:
                country = st.selectbox(get_text('ph_country'), db.get_all_countries())
            
            with col3:
                costs_time = st.text_input(get_text('ph_time'), "2026-01")
            
            costs = st.number_input(get_text('ph_cost'), min_value=0.0, value=0.0, step=0.01)
            
            submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
            
            if submitted:
                try:
                    query = """
                        INSERT INTO Costs (Model, Country, Costs_time, Costs)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Costs = VALUES(Costs)
                    """
                    if db.execute_update(query, (model, country, costs_time, costs)):
                        handle_save_success(db, u['id'], "COSTS_ENTRY", get_text('costs_entry_title'), f"{model} in {country}")
                    else:
                        st.error(get_text('error'))
                except Exception as e:
                    st.error(f"{get_text('error')}: {e}")
    
    with tab2:
        st.markdown(f"#### {get_text('delete_title')}")
        
        # 显示现有数据
        df_costs = db.get_costs_data()
        if not df_costs.empty:
            st.dataframe(df_costs, use_container_width=True, height=300)
            
            # 删除表单
            with st.form("delete_costs_form"):
                costs_id = st.number_input(get_text('ph_cost_id'), min_value=1, step=1)
                
                delete_btn = st.form_submit_button(get_text('btn_delete'), type="secondary")
                
                if delete_btn:
                    if db.delete_costs_data(costs_id):
                        handle_save_success(db, u['id'], "COSTS_DELETE", get_text('delete_title'), f"ID: {costs_id}")
                        st.success(get_text('msg_del_success'))
                        st.rerun()
                    else:
                        st.error(get_text('error'))
        else:
            st.info(get_text('msg_no_data'))

def show_exchange_entry(db, u):
    """财务：汇率数据录入"""
    st.markdown(f"### {get_text('exchange_entry_title')}")
    
    with st.form("exchange_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            exchange_time = st.text_input(get_text('ph_time'), "2026-01")
        
        with col2:
            exchange_rate = st.number_input(get_text('ph_exchange_rate'), min_value=0.0, value=7.2, step=0.01)
        
        st.info(get_text('exchange_hint'))
        
        submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Exchange (Exchange_time, Exchange_rate)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE Exchange_rate = VALUES(Exchange_rate)
                """
                if db.execute_update(query, (exchange_time, exchange_rate)):
                    handle_save_success(db, u['id'], "EXCHANGE_ENTRY", get_text('exchange_entry_title'), f"{exchange_time}: {exchange_rate}")
                else:
                    st.error(get_text('error'))
            except Exception as e:
                st.error(f"{get_text('error')}: {e}")

def show_expenses_entry(db, u):
    """财务：区域费用数据录入（4类费用）"""
    st.markdown(f"### {get_text('expenses_entry_title')}")
    st.caption(get_text('expenses_hint'))
    
    tab1, tab2 = st.tabs([get_text('tab_add_update'), get_text('tab_delete')])
    
    with tab1:
        with st.form("expenses_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                country = st.selectbox(get_text('ph_country'), db.get_all_countries())
            
            with col2:
                expenses_time = st.text_input(get_text('ph_time'), "2026-01")
            
            st.markdown(f"#### {get_text('expenses_detail_title')}")
            col1, col2 = st.columns(2)
            
            with col1:
                marketing_expenses = st.number_input(get_text('ph_marketing_expenses'), min_value=0.0, value=0.0, step=100.0)
                labor_cost = st.number_input(get_text('ph_labor_cost'), min_value=0.0, value=0.0, step=100.0)
            
            with col2:
                other_variable = st.number_input(get_text('ph_other_variable'), min_value=0.0, value=0.0, step=100.0)
                other_fixed = st.number_input(get_text('ph_other_fixed'), min_value=0.0, value=0.0, step=100.0)
            
            submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
            
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
                        handle_save_success(db, u['id'], "EXPENSES_ENTRY", get_text('expenses_entry_title'), f"{country} at {expenses_time}")
                    else:
                        st.error(get_text('error'))
                except Exception as e:
                    st.error(f"{get_text('error')}: {e}")
    
    with tab2:
        st.markdown(f"#### {get_text('delete_title')}")
        
        df_expenses = db.execute_query("SELECT * FROM Regional_Expenses ORDER BY Expenses_time DESC")
        if not df_expenses.empty:
            st.dataframe(df_expenses, use_container_width=True, height=300)
            
            with st.form("delete_expenses_form"):
                col1, col2 = st.columns(2)
                with col1:
                    del_country = st.selectbox(get_text('ph_country'), db.get_all_countries(), key="del_exp_country")
                with col2:
                    del_time = st.text_input(get_text('ph_time'), "2026-01", key="del_exp_time")
                
                delete_btn = st.form_submit_button(get_text('btn_delete'), type="secondary")
                
                if delete_btn:
                    if db.delete_regional_expenses(del_country, del_time):
                        handle_save_success(db, u['id'], "EXPENSES_DELETE", get_text('delete_title'), f"{del_country} at {del_time}")
                        st.success(get_text('msg_del_success'))
                        st.rerun()
                    else:
                        st.error(get_text('error'))
        else:
            st.info(get_text('msg_no_data'))

def show_model_entry(db, u):
    """财务：机型数据录入"""
    st.markdown(f"### {get_text('model_entry_title')}")
    
    with st.form("model_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model = st.text_input(get_text('ph_model'), "ModelX")
        
        with col2:
            series = st.selectbox(get_text('ph_series'), ["Dog", "Cat", "Tiger"])
        
        with col3:
            model_label = st.selectbox(get_text('ph_model_label'), ["High-end", "Mid-range", "Entry-level"])
        
        submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Model (Model, Series, Model_label)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE Series = VALUES(Series), Model_label = VALUES(Model_label)
                """
                if db.execute_update(query, (model, series, model_label)):
                    handle_save_success(db, u['id'], "MODEL_ENTRY", get_text('model_entry_title'), f"{model}")
                else:
                    st.error(get_text('error'))
            except Exception as e:
                st.error(f"{get_text('error')}: {e}")

def show_country_entry(db, u):
    """财务：国家数据录入"""
    st.markdown(f"### {get_text('country_entry_title')}")
    
    with st.form("country_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            country = st.text_input(get_text('ph_country'), "Brazil")
        
        with col2:
            market = st.selectbox(get_text('ph_market'), ["Asia", "Africa", "South America"])
        
        submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
        
        if submitted:
            try:
                query = """
                    INSERT INTO Country (Country, Market)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE Market = VALUES(Market)
                """
                if db.execute_update(query, (country, market)):
                    handle_save_success(db, u['id'], "COUNTRY_ENTRY", get_text('country_entry_title'), f"{country}") 
                else:
                    st.error(get_text('error'))
            except Exception as e:
                st.error(f"{get_text('error')}: {e}")

def show_sales_entry(db, u):
    """销售：销售量和售价录入"""
    st.markdown(f"### {get_text('sales_entry_title')}")
    
    if u.get('country'):
        st.info(f"{get_text('current_region')}: **{u['country']}** ({get_text('region_hint')})")
        default_country = u['country']
        country_disabled = True
    else:
        default_country = "India"
        country_disabled = False
    
    tab1, tab2 = st.tabs([get_text('tab_add_update'), get_text('tab_delete')])
    
    with tab1:
        with st.form("sales_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                time = st.text_input(get_text('ph_time'), "2026-01")
            with col2:
                if country_disabled:
                    country = st.text_input(get_text('ph_country'), default_country, disabled=True)
                else:
                    country = st.selectbox(get_text('ph_country'), db.get_all_countries())
            with col3:
                model = st.selectbox(get_text('ph_model'), db.get_all_models())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                currency = st.selectbox(get_text('ph_currency'), ["CNY", "USD"])
            with col2:
                sales = st.number_input(get_text('ph_sales'), min_value=0, value=0, step=1)
            with col3:
                price = st.number_input(get_text('ph_price'), min_value=0.0, value=0.0, step=0.01)
            
            submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
            
            if submitted:
                try:
                    query = """
                        INSERT INTO Sales_Price (Model, Country, h_Time, Currency, Sales, Price, Exchange_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            Currency = VALUES(Currency),
                            Sales = VALUES(Sales),
                            Price = VALUES(Price)
                    """
                    params = (model, country, time, currency, sales, price, time)
                    
                    if db.execute_update(query, params):
                        handle_save_success(db, u['id'], "SALES_ENTRY", get_text('sales_entry_title'), f"{model} in {country}")
                except Exception as e:
                    st.error(f"{get_text('error')}: {e}")
    
    with tab2:
        st.markdown(f"#### {get_text('delete_title')}")
        df_sales = db.get_sales_price_data(u.get('country'))
        if not df_sales.empty:
            st.dataframe(df_sales, use_container_width=True, height=300)
            with st.form("delete_sales_form"):
                record_id_to_del = st.number_input(get_text('ph_record_id'), min_value=1, step=1)
                delete_btn = st.form_submit_button(get_text('btn_delete'), type="secondary")
                if delete_btn:
                    if db.delete_sales_price(record_id_to_del):
                        handle_save_success(db, u['id'], "SALES_DELETE", get_text('delete_title'), f"ID: {record_id_to_del}")
                        st.success(get_text('msg_del_success'))
                        st.rerun()
                    else:
                        st.error(get_text('error'))
        else:
            st.info(get_text('msg_no_data'))

def show_history_entry(db, u):
    """通用：历史数据录入（兼容旧版）"""
    st.markdown(f"### {get_text('history_entry_title')}")
    
    with st.form("history_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time = st.text_input(get_text('ph_time'), "2026-01")
        
        with col2:
            country = st.selectbox(get_text('ph_country'), db.get_all_countries())
        
        with col3:
            model = st.selectbox(get_text('ph_model'), db.get_all_models())
        
        sales = st.number_input(get_text('ph_sales'), min_value=0, value=0, step=1)
        
        submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
        
        if submitted:
            row = {'h_Time': time, 'Country': country, 'Model': model, 'Sales': sales}
            df = pd.DataFrame([row])
            
            if db.save_data(df, "History"):
                handle_save_success(db, u['id'], "HISTORY_ENTRY", get_text('history_entry_title'), f"{model} in {country}")
            else:
                st.error(get_text('error'))

def show_budget_entry(db, u):
    """通用：预算数据录入（兼容旧版）"""
    st.markdown(f"### {get_text('budget_entry_title')}")
    
    with st.form("budget_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time = st.text_input(get_text('ph_time'), "2026-01")
        
        with col2:
            country = st.selectbox(get_text('ph_country'), db.get_all_countries())
        
        with col3:
            model = st.selectbox(get_text('ph_model'), db.get_all_models())
        
        sales = st.number_input(get_text('ph_sales'), min_value=0, value=0, step=1)
        
        submitted = st.form_submit_button(get_text('btn_save'), type="primary", use_container_width=True)
        
        if submitted:
            row = {'h_Time': time, 'Country': country, 'Model': model, 'Sales': sales}
            df = pd.DataFrame([row])
            
            if db.save_data(df, "Budget"):
                handle_save_success(db, u['id'], "BUDGET_ENTRY", get_text('budget_entry_title'), f"{model} in {country}")
            else:
                st.error(get_text('error'))

if __name__ == "__main__":
    main()