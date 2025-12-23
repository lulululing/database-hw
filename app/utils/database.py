"""
数据库连接和操作模块
Database Connection and Operations Module
"""

import pymysql
import pandas as pd
from typing import Optional, List, Dict, Any
import streamlit as st
from config import DB_CONFIG, DB_BASE_CONFIG, DB_ROLE_USERS, USE_DB_ROLES


class DatabaseManager:
    """数据库管理器类"""
    
    def __init__(self, role: str = None):
        """
        初始化数据库连接
        Args:
            role: 用户角色，用于选择对应的数据库用户
        """
        self.role = role
        self.connection = None
        
        # 根据角色选择数据库配置
        if USE_DB_ROLES and role and role in DB_ROLE_USERS:
            # 使用数据库层权限控制
            self.config = {
                **DB_BASE_CONFIG,
                'user': DB_ROLE_USERS[role]['user'],
                'password': DB_ROLE_USERS[role]['password']
            }
        else:
            # 使用默认配置（root用户）
            self.config = DB_CONFIG
    
    def connect(self) -> bool:
        """
        建立数据库连接
        Returns:
            bool: 连接是否成功
        """
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset']
            )
            return True
        except Exception as e:
            st.error(f"数据库连接失败: {str(e)}")
            return False
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[pd.DataFrame]:
        """
        执行查询并返回DataFrame
        Args:
            query: SQL查询语句
            params: 查询参数
        Returns:
            pd.DataFrame: 查询结果
        """
        try:
            if not self.connection or not self.connection.open:
                if not self.connect():
                    return None
            
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except Exception as e:
            st.error(f"查询执行失败: {str(e)}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """
        执行更新操作（INSERT, UPDATE, DELETE）
        Args:
            query: SQL语句
            params: 参数
        Returns:
            bool: 是否成功
        """
        try:
            if not self.connection or not self.connection.open:
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            st.error(f"更新操作失败: {str(e)}")
            if self.connection:
                self.connection.rollback()
            return False
    
    # ==================== 数据查询方法 ====================
    
    def get_history_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """获取历史销售数据"""
        query = """
        SELECT h_Time as 时间, Country as 国家, Market as 市场, 
               Model as 型号, Model_label as 标签, Series as 系列,
               Sales as 销量, Revenues as 收入, 
               Gross_profits as 毛利, Margin_profits as 边际利润,
               Net_income as 净收入
        FROM History
        WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('time'):
                query += " AND h_Time = %s"
                params.append(filters['time'])
            if filters.get('country'):
                query += " AND Country = %s"
                params.append(filters['country'])
            if filters.get('model'):
                query += " AND Model = %s"
                params.append(filters['model'])
        
        query += " ORDER BY h_Time DESC, Country, Model"
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def get_budget_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """获取预算数据"""
        query = """
        SELECT h_Time as 时间, Country as 国家, Market as 市场,
               Model as 型号, Model_label as 标签, Series as 系列,
               Sales as 销量, Revenues as 收入,
               Gross_profits as 毛利, Margin_profits as 边际利润,
               Net_income as 净收入
        FROM Budget
        WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('time'):
                query += " AND h_Time = %s"
                params.append(filters['time'])
            if filters.get('country'):
                query += " AND Country = %s"
                params.append(filters['country'])
            if filters.get('model'):
                query += " AND Model = %s"
                params.append(filters['model'])
        
        query += " ORDER BY h_Time DESC, Country, Model"
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def get_sales_price_data(self) -> pd.DataFrame:
        """获取销售价格数据"""
        query = """
        SELECT id, Model as 型号, Country as 国家, 
               h_Time as 时间, Currency as 货币,
               Sales as 销量, Price as 价格
        FROM Sales_Price
        ORDER BY h_Time DESC, Country, Model
        """
        return self.execute_query(query)
    
    def get_costs_data(self) -> pd.DataFrame:
        """获取成本数据"""
        query = """
        SELECT Costs_id as ID, Model as 型号, Country as 国家,
               Costs_time as 时间, Costs as 成本
        FROM Costs
        ORDER BY Costs_time DESC, Country, Model
        """
        return self.execute_query(query)
    
    def get_comparison_data(self, time_period: str = None) -> pd.DataFrame:
        """获取预算与实际对比数据"""
        query = """
        SELECT 
            COALESCE(h.h_Time, b.h_Time) as 时间,
            COALESCE(h.Country, b.Country) as 国家,
            COALESCE(h.Model, b.Model) as 型号,
            h.Sales as 实际销量,
            b.Sales as 预算销量,
            h.Revenues as 实际收入,
            b.Revenues as 预算收入,
            h.Net_income as 实际净收入,
            b.Net_income as 预算净收入,
            ROUND((h.Sales - b.Sales) / b.Sales * 100, 2) as 销量达成率,
            ROUND((h.Revenues - b.Revenues) / b.Revenues * 100, 2) as 收入达成率,
            ROUND((h.Net_income - b.Net_income) / b.Net_income * 100, 2) as 净收入达成率
        FROM History h
        FULL OUTER JOIN Budget b 
            ON h.h_Time = b.h_Time 
            AND h.Country = b.Country 
            AND h.Model = b.Model
        WHERE 1=1
        """
        
        if time_period:
            query += " AND COALESCE(h.h_Time, b.h_Time) = %s"
            return self.execute_query(query, (time_period,))
        
        return self.execute_query(query)
    
    def get_country_summary(self, time_period: str = None) -> pd.DataFrame:
        """按国家汇总数据"""
        query = """
        SELECT 
            Country as 国家,
            Market as 市场,
            SUM(Sales) as 总销量,
            ROUND(SUM(Revenues), 2) as 总收入,
            ROUND(SUM(Gross_profits), 2) as 总毛利,
            ROUND(SUM(Net_income), 2) as 总净收入,
            ROUND(SUM(Gross_profits) / SUM(Revenues) * 100, 2) as 毛利率,
            ROUND(SUM(Net_income) / SUM(Revenues) * 100, 2) as 净利率
        FROM History
        """
        
        if time_period:
            query += " WHERE h_Time = %s"
            query += " GROUP BY Country, Market ORDER BY 总收入 DESC"
            return self.execute_query(query, (time_period,))
        
        query += " GROUP BY Country, Market ORDER BY 总收入 DESC"
        return self.execute_query(query)
    
    def get_model_summary(self, time_period: str = None) -> pd.DataFrame:
        """按产品型号汇总数据"""
        query = """
        SELECT 
            Model as 型号,
            Model_label as 标签,
            Series as 系列,
            SUM(Sales) as 总销量,
            ROUND(SUM(Revenues), 2) as 总收入,
            ROUND(SUM(Gross_profits), 2) as 总毛利,
            ROUND(SUM(Net_income), 2) as 总净收入,
            ROUND(AVG(Gross_profits / Revenues * 100), 2) as 平均毛利率
        FROM History
        """
        
        if time_period:
            query += " WHERE h_Time = %s"
            query += " GROUP BY Model, Model_label, Series ORDER BY 总收入 DESC"
            return self.execute_query(query, (time_period,))
        
        query += " GROUP BY Model, Model_label, Series ORDER BY 总收入 DESC"
        return self.execute_query(query)
    
    def get_time_series_data(self) -> pd.DataFrame:
        """获取时间序列数据"""
        query = """
        SELECT 
            h_Time as 时间,
            SUM(Sales) as 总销量,
            ROUND(SUM(Revenues), 2) as 总收入,
            ROUND(SUM(Gross_profits), 2) as 总毛利,
            ROUND(SUM(Net_income), 2) as 总净收入
        FROM History
        GROUP BY h_Time
        ORDER BY h_Time
        """
        return self.execute_query(query)
    
    def get_regional_expenses(self, country: str = None) -> pd.DataFrame:
        """获取区域费用数据"""
        query = """
        SELECT 
            Country as 国家,
            Expenses_time as 时间,
            Marketing_expenses as 市场费用,
            Labor_cost as 人工成本,
            Other_variable_expenses as 其他变动费用,
            Other_fixed_expenses as 其他固定费用
        FROM Regional_Expenses
        """
        
        if country:
            query += " WHERE Country = %s ORDER BY Expenses_time"
            return self.execute_query(query, (country,))
        
        query += " ORDER BY Country, Expenses_time"
        return self.execute_query(query)
    
    # ==================== 辅助方法 ====================
    
    def get_all_countries(self) -> List[str]:
        """获取所有国家列表"""
        query = "SELECT DISTINCT Country FROM Country ORDER BY Country"
        df = self.execute_query(query)
        return df['Country'].tolist() if df is not None else []
    
    def get_all_models(self) -> List[str]:
        """获取所有产品型号列表"""
        query = "SELECT DISTINCT Model FROM Model ORDER BY Model"
        df = self.execute_query(query)
        return df['Model'].tolist() if df is not None else []
    
    def get_all_time_periods(self) -> List[str]:
        """获取所有时间段列表"""
        query = "SELECT DISTINCT h_Time FROM History ORDER BY h_Time DESC"
        df = self.execute_query(query)
        return df['h_Time'].tolist() if df is not None else []
    
    def get_all_series(self) -> List[str]:
        """获取所有产品系列"""
        query = "SELECT DISTINCT Series FROM Ratio_Expenses1 ORDER BY Series"
        df = self.execute_query(query)
        return df['Series'].tolist() if df is not None else []


# 创建全局数据库管理器实例
@st.cache_resource
def get_db_manager(_role: str = None):
    """
    获取数据库管理器实例（使用缓存）
    Args:
        _role: 用户角色，用下划线前缀避免被缓存键使用
    """
    # 从session_state获取实际角色
    role = st.session_state.get('db_role', None) if hasattr(st, 'session_state') else None
    return DatabaseManager(role=role)
