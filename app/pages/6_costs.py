import streamlit as st
import pandas as pd
import io
from utils.database import get_db_manager
from utils.i18n import get_text
from utils.helper import apply_currency_conversion
from utils.i18n import show_sidebar_with_nav, get_text
# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_required'))
    st.switch_page("app.py")

# 检查权限 - 扩展：业务员也能查看
view_perms = ['view_costs', 'view_costs_country']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in view_perms)

if not has_permission:
    st.error(get_text('no_permission'))
    st.stop()

# 设置页面
st.set_page_config(
    page_title=get_text('nav_costs'),
    layout="wide"
)
show_sidebar_with_nav()

def log_view_action(db, page_name, filter_details=""):
    """记录查看操作的日志"""
    try:
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        details = f"查看{page_name}页面"
        if filter_details:
            details += f" | 筛选条件: {filter_details}"
        
        from utils.helper import handle_save_success
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="VIEW",
            message_prefix="数据查询",
            details=details,
            operation_type="查看"
        )
    except Exception as e:
        st.warning(f"记录日志失败: {e}")
        return False

def log_export_action(db, page_name, export_type, record_count):
    """记录导出操作的日志"""
    try:
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        details = f"导出{page_name}页面数据({export_type}), 记录数: {record_count}"
        
        from utils.helper import handle_save_success
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="EXPORT",
            message_prefix="数据导出",
            details=details,
            operation_type="导出"
        )
    except Exception as e:
        print(f"记录导出日志失败: {e}")
        return False

def main():
    st.title(get_text('nav_costs'))
    
    # 获取用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    permissions = st.session_state.permissions
    db = get_db_manager()
    
    # 根据角色显示提示
    if u.get('country'):
        st.info(get_text('msg_current_region', region=u['country']))
        country_filter = u['country']
        country_disabled = True
    else:
        st.info(get_text('msg_view_all_region'))
        country_filter = None
        country_disabled = False
    
    # 先查询基础数据（保持V1的先查询后筛选模式）
    if country_disabled:
        df = db.get_costs_data(country=country_filter)
    else:
        df = db.get_costs_data()
    
    # 初始化筛选变量
    selected_country = get_text('view_all_option')
    selected_model = get_text('view_all_option')
    currency_opt = "CNY"
    
    if not df.empty:
        # 筛选功能 - 三列布局，默认展开
        with st.expander(get_text('filter_title'), expanded=True):
            col1, col2, col3 = st.columns(3)
            
            # 国家筛选
            current_df = df.copy()
            with col1:
                if not country_disabled:
                    countries = [get_text('view_all_option')] + sorted(df['Country'].unique().tolist())
                    selected_country = st.selectbox(get_text('select_country'), countries)
                else:
                    st.text_input(get_text('select_country'), country_filter, disabled=True)
                    selected_country = country_filter
            
            # 型号筛选
            with col2:
                models = [get_text('view_all_option')] + sorted(current_df['Model'].unique().tolist())
                selected_model = st.selectbox(get_text('select_model'), models)
            
            # 货币选择（新增功能）
            with col3:
                default_idx = 0 if st.session_state.get('language') == 'zh' else 1
                currency_opt = st.selectbox(
                    get_text('currency'), 
                    ["CNY", "USD"], 
                    index=default_idx, 
                    key="curr_select"
                )
        
        # 应用筛选条件
        current_df = df.copy()
        
        # 国家筛选
        if not country_disabled and selected_country != get_text('view_all_option'):
            current_df = current_df[current_df['Country'] == selected_country]
        elif country_disabled:
            current_df = current_df[current_df['Country'] == country_filter]
        
        # 型号筛选
        if selected_model != get_text('view_all_option'):
            current_df = current_df[current_df['Model'] == selected_model]
        
        # 记录查看日志（每次页面加载或筛选变化时）
        filter_details = []
        if not country_disabled and selected_country != get_text('view_all_option'):
            filter_details.append(f"国家: {selected_country}")
        elif country_disabled:
            filter_details.append(f"国家: {country_filter}")
        if selected_model != get_text('view_all_option'):
            filter_details.append(f"型号: {selected_model}")
        filter_details.append(f"货币: {currency_opt}")
        
        # 记录查看日志
        log_view_action(
            db=db,
            page_name=get_text('nav_costs'),
            filter_details="; ".join(filter_details) if filter_details else "无筛选"
        )
        
        # 应用筛选后的数据
        if len(current_df) > 0:
            # 应用货币转换（已统一保留2位小数）
            df_converted, currency_symbol = apply_currency_conversion(current_df, db, currency_opt)
            
            st.success(get_text('msg_found_records', count=len(df_converted)))
            
            # 显示数据（转换后的数据已统一保留2位小数）
            st.markdown(f"### {get_text('header_preview')}")
            st.dataframe(df_converted, use_container_width=True, height=400)
            
            # 统计信息
            st.markdown(f"### {get_text('header_stats')}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(get_text('metric_records'), len(df_converted))
            
            with col2:
                if 'Costs' in df_converted.columns:
                    avg_cost = df_converted['Costs'].mean()
                    st.metric(get_text('metric_avg_cost'), f"{currency_symbol}{avg_cost:,.2f}")
            
            with col3:
                if 'Costs' in df_converted.columns:
                    min_cost = df_converted['Costs'].min()
                    max_cost = df_converted['Costs'].max()
                    st.metric(get_text('metric_cost_range'), f"{currency_symbol}{min_cost:,.2f} - {currency_symbol}{max_cost:,.2f}")
            
            # 双导出功能（CSV + Excel）
            if 'export' in permissions:
                st.markdown("---")
                st.markdown(f"### {get_text('header_export')}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # CSV导出（使用转换后的数据，已经统一保留2位小数）
                    csv_data = df_converted.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label=get_text('btn_export_csv'),
                        data=csv_data,
                        file_name=f"costs_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        on_click=lambda: log_export_action(
                            db=db, 
                            page_name=get_text('nav_costs'),
                            export_type="CSV", 
                            record_count=len(df_converted)
                        )
                    )
                
                with col2:
                    # Excel导出
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_converted.to_excel(writer, index=False, sheet_name='Costs_Data')
                    
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label=get_text('btn_export_excel'),
                        data=excel_data,
                        file_name=f"costs_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        on_click=lambda: log_export_action(
                            db=db, 
                            page_name=get_text('nav_costs'),
                            export_type="Excel", 
                            record_count=len(df_converted)
                        )
                    )
        else:
            st.warning(get_text('msg_no_data'))
    else:
        st.warning(get_text('msg_no_data'))

if __name__ == "__main__":
    main()