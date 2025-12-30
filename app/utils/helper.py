import pandas as pd
import numpy as np
from utils.i18n import get_text
import streamlit as st

def detect_currency_columns(df):
    """
    智能检测金额列（增强版）
    """
    if df is None or df.empty:
        return []
    
    currency_columns = []
    
    # 金额列关键词（中文+英文）
    currency_keywords = [
        # 英文
        'revenue', 'profit', 'income', 'cost', 'price', 'expense', 'margin',
        'Revenues', 'Gross_profits', 'Margin_profits', 'Net_income', 
        'Costs', 'Price', 'Expenses',
        # 中文
        '毛利', '净利', '成本', '价格', '费用', '收入', '利润',
        # 列名
        'Revenue', 'GrossProfit', 'NetProfit', 'TotalCost'
    ]
    
    # 排除的非金额列
    exclude_keywords = [
        'id', 'sales', 'quantity', 'volume', '时间', '型号', '国家', 'country', 
        'model', 'time', 'currency', 'series', 'market', 'label'
    ]
    
    for col in df.columns:
        col_str = str(col).lower()
        
        # 检查是否应该排除
        should_exclude = any(exclude in col_str for exclude in exclude_keywords)
        if should_exclude:
            continue
        
        # 检查是否是金额相关列
        is_currency = False
        for keyword in currency_keywords:
            if keyword.lower() in col_str:
                is_currency = True
                break
        
        if is_currency:
            # 检查是否是数值类型
            if pd.api.types.is_numeric_dtype(df[col]):
                currency_columns.append(col)
            else:
                # 尝试转换
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    if not df[col].isna().all():  # 至少有一些数值
                        currency_columns.append(col)
                except:
                    continue
    
    return currency_columns

def apply_currency_conversion(df, db, target_currency='CNY', time_column=None):
    """
    完整的货币转换工具
    假设数据库中的数据以CNY为单位存储
    支持：CNY ↔ USD 转换
    
    :param df: 输入数据框
    :param db: 数据库管理器
    :param target_currency: 目标货币 ('CNY' 或 'USD')
    :param time_column: 时间列名，用于匹配汇率
    :return: (转换后的数据框, 货币符号)
    """
    if df is None or df.empty:
        return df, get_text('unit_yuan')
    
    # 如果目标货币是 CNY，无需转换（假设源数据就是CNY）
    if target_currency == 'CNY':
        return df, get_text('unit_yuan')
    
    # 如果目标货币是 USD，需要将CNY转换为USD
    if target_currency == 'USD':
        # 检测时间列
        if time_column is None:
            time_candidates = ['h_Time', 'Costs_time', 'Exchange_time', 'Expenses_time', '时间']
            for candidate in time_candidates:
                if candidate in df.columns:
                    time_column = candidate
                    break
        
        if time_column is None:
            st.warning("未找到时间列，使用默认汇率进行转换")
            # 使用默认汇率 7.0
            exchange_rate = 7.0
        else:
            # 获取汇率数据
            try:
                df_ex = db.get_exchange_rates_df()
                if df_ex is None or df_ex.empty:
                    st.warning("无法获取汇率数据，使用默认汇率")
                    exchange_rate = 7.0
                else:
                    # 创建临时合并列
                    df_temp = df.copy()
                    df_temp['_time_key'] = df_temp[time_column].astype(str)
                    df_ex['_time_key'] = df_ex['h_Time'].astype(str)
                    
                    # 合并汇率
                    df_merged = pd.merge(
                        df_temp, 
                        df_ex[['_time_key', 'Exchange_rate']], 
                        on='_time_key', 
                        how='left'
                    )
                    
                    # 处理缺失的汇率
                    if df_merged['Exchange_rate'].isna().any():
                        avg_rate = df_merged['Exchange_rate'].mean()
                        if pd.isna(avg_rate) or avg_rate <= 0:
                            avg_rate = 7.0
                        df_merged['Exchange_rate'] = df_merged['Exchange_rate'].fillna(avg_rate)
                    
                    # 应用转换：CNY → USD 除以汇率
                    exchange_rate = df_merged['Exchange_rate']
                    
                    # 检测金额列
                    currency_columns = detect_currency_columns(df_merged)
                    
                    # 执行转换
                    for col in currency_columns:
                        if col in df_merged.columns:
                            try:
                                df_merged[col] = df_merged[col] / df_merged['Exchange_rate']
                                df_merged[col] = df_merged[col].round(2)
                            except Exception as e:
                                st.warning(f"转换列 {col} 时出错: {e}")
                    
                    # 清理临时列
                    df_result = df_merged.drop(columns=['_time_key', 'Exchange_rate'], errors='ignore')
                    return df_result, get_text('unit_dollar')
                    
            except Exception as e:
                st.warning(f"获取汇率失败，使用默认汇率: {e}")
                exchange_rate = 7.0
        
        # 如果没有时间列，对整个数据框使用固定汇率
        currency_columns = detect_currency_columns(df)
        df_result = df.copy()
        
        for col in currency_columns:
            if col in df_result.columns:
                try:
                    df_result[col] = df_result[col] / exchange_rate
                    df_result[col] = df_result[col].round(2)
                except Exception as e:
                    st.warning(f"转换列 {col} 时出错: {e}")
        
        return df_result, get_text('unit_dollar')
    
    # 其他货币暂不支持
    st.warning(f"不支持的目标货币: {target_currency}")
    return df, get_text('unit_yuan')

def handle_save_success(db, user_info, action_type, message_prefix, details, operation_type="保存"):
    """
    通用保存成功处理函数（增强版）
    :param db: 数据库管理器实例
    :param user_info: 用户信息字典，至少包含 'id' 和 'username'
    :param action_type: 日志动作类型 (如 'COSTS_ENTRY', 'SALES_ENTRY')
    :param message_prefix: 提示前缀 (如 '成本数据') -> 最终显示 '成本数据保存成功！'
    :param details: 日志详情
    :param operation_type: 操作类型 ('保存', '删除', '更新')
    """
    try:
        # 1. 记录日志 - 使用新的insert_system_log函数
        if isinstance(user_info, dict):
            user_id = user_info.get('id', '')
            username = user_info.get('username', user_id)
            role = user_info.get('role', st.session_state.get('role', 'User'))
        else:
            # 向后兼容
            user_id = str(user_info)
            username = user_id
            role = st.session_state.get('role', 'User')
        
        # 使用新的insert_system_log函数
        log_success = db.insert_system_log(
            action_type=action_type,
            details=f"{operation_type}操作: {details}",
            username=username,
            role=role
        )
        
        if not log_success:
            print(f"记录操作日志失败: {username}, {action_type}, {details}")
        
        # 2. 清除缓存
        try:
            st.cache_data.clear()
        except:
            pass
        
        # 3. 显示成功消息
        success_messages = {
            '保存': f"{message_prefix}保存成功！",
            '删除': f"{message_prefix}删除成功！",
            '更新': f"{message_prefix}更新成功！"
        }
        
        message = success_messages.get(operation_type, f"{message_prefix}操作成功！")
        
        # 使用更可靠的提示方式
        st.success(message)
        
        # 可选：显示短暂的成功提示
        try:
            st.toast(message)
        except:
            pass
        
        return True
        
    except Exception as e:
        st.error(f"记录操作日志失败: {e}")
        return False
    
def format_large_number(num):
    """
    格式化大数字显示
    """
    try:
        if pd.isna(num):
            return "-"
        
        num = float(num)
        
        if abs(num) >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f}B"
        elif abs(num) >= 1_000_000:
            return f"{num/1_000_000:.2f}M"
        elif abs(num) >= 1_000:
            return f"{num/1_000:.2f}K"
        else:
            return f"{num:,.2f}"
    except:
        return str(num)

def calculate_summary_stats(df, currency_symbol='¥'):
    """
    计算数据摘要统计
    """
    if df is None or df.empty:
        return {}
    
    stats = {}
    
    # 检测金额列
    currency_cols = detect_currency_columns(df)
    
    for col in currency_cols:
        if col in df.columns:
            stats[f'{col}_total'] = f"{currency_symbol}{df[col].sum():,.2f}"
            stats[f'{col}_avg'] = f"{currency_symbol}{df[col].mean():,.2f}"
            stats[f'{col}_min'] = f"{currency_symbol}{df[col].min():,.2f}"
            stats[f'{col}_max'] = f"{currency_symbol}{df[col].max():,.2f}"
    
    # 销售数据统计
    if 'Sales' in df.columns:
        stats['sales_total'] = f"{df['Sales'].sum():,.0f}"
        stats['sales_avg'] = f"{df['Sales'].mean():,.0f}"
    
    # 记录数
    stats['record_count'] = len(df)
    
    return stats