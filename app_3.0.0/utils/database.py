# app/utils/database.py
import pymysql
import pandas as pd
import streamlit as st
from config import DB_CONFIG, DB_BASE_CONFIG, DB_ROLE_USERS, USE_DB_ROLES, ROLES
from utils.sql_queries import *

class DatabaseManager:
    def __init__(self, role: str = None):
        self.role = role
        self.connection = None
        # 连接逻辑
        if USE_DB_ROLES and role and role in DB_ROLE_USERS:
            self.config = {**DB_BASE_CONFIG, **DB_ROLE_USERS[role]}
        else:
            self.config = DB_CONFIG

    def connect(self) -> bool:
        try:
            if self.connection and self.connection.open: return True
            self.connection = pymysql.connect(**self.config)
            return True
        except Exception as e:
            st.error(f"连接失败: {e}")
            return False

    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        if not self.connect(): return pd.DataFrame()
        try:
            return pd.read_sql(query, self.connection, params=params)
        except Exception as e:
            print(f"查询错误: {e}")
            return pd.DataFrame()

    def execute_update(self, query: str, params: tuple = None) -> bool:
        if not self.connect(): return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            st.error(f"更新失败: {e}")
            return False

    def get_time_series_data(self):
        """首页仪表盘数据源"""
        return self.execute_query(Q_GET_TIME_SERIES)

    def get_all_models(self):
        """获取所有产品型号"""
        df = self.execute_query("SELECT DISTINCT Model FROM Model ORDER BY Model")
        return df['Model'].tolist() if not df.empty else []

    def get_all_countries(self):
        """获取所有国家"""
        df = self.execute_query("SELECT DISTINCT Country FROM Country ORDER BY Country")
        return df['Country'].tolist() if not df.empty else []

    def get_all_time_periods(self):
        """获取所有时间周期"""
        df = self.execute_query("SELECT DISTINCT h_Time FROM History ORDER BY h_Time DESC")
        return df['h_Time'].tolist() if not df.empty else []

    def log_event(self, username, action, details):
        """
        改进的系统日志记录
        自动从session_state获取角色信息
        """
        # 从session_state获取角色
        role = st.session_state.get('role', 'Unknown')
        
        # 获取角色的中文标签
        role_label = ROLES.get(role, {}).get('label', role)
        
        self.execute_update(Q_LOG_ACTION, (username, role_label, action, details))

    # ================= 新增：删除功能 =================
    def delete_history_data(self, h_time, country, model):
        """删除历史数据（History表）"""
        try:
            query = "DELETE FROM History WHERE h_Time = %s AND Country = %s AND Model = %s"
            return self.execute_update(query, (h_time, country, model))
        except Exception as e:
            st.error(f"删除历史数据失败: {e}")
            return False

    def delete_budget_data(self, h_time, country, model):
        """删除预算数据（Budget表）"""
        try:
            query = "DELETE FROM Budget WHERE h_Time = %s AND Country = %s AND Model = %s"
            return self.execute_update(query, (h_time, country, model))
        except Exception as e:
            st.error(f"删除预算数据失败: {e}")
            return False

    def delete_sales_price(self, record_id):
        """删除销售价格记录（Sales_Price表）"""
        try:
            query = "DELETE FROM Sales_Price WHERE id = %s"
            return self.execute_update(query, (record_id,))
        except Exception as e:
            st.error(f"删除销售价格失败: {e}")
            return False

    def delete_costs_data(self, costs_id):
        """删除成本数据（Costs表）"""
        try:
            query = "DELETE FROM Costs WHERE Costs_id = %s"
            return self.execute_update(query, (costs_id,))
        except Exception as e:
            st.error(f"删除成本数据失败: {e}")
            return False

    def delete_regional_expenses(self, country, expenses_time):
        """删除区域费用（Regional_Expenses表）"""
        try:
            query = "DELETE FROM Regional_Expenses WHERE Country = %s AND Expenses_time = %s"
            return self.execute_update(query, (country, expenses_time))
        except Exception as e:
            st.error(f"删除区域费用失败: {e}")
            return False

    # ================= 页面数据查询方法 =================
    def get_history_data(self, filters=None):
        """获取历史数据"""
        query = "SELECT * FROM History WHERE 1=1"
        params = []
        
        if filters:
            if 'time' in filters:
                query += " AND h_Time = %s"
                params.append(filters['time'])
            if 'country' in filters:
                query += " AND Country = %s"
                params.append(filters['country'])
            if 'model' in filters:
                query += " AND Model = %s"
                params.append(filters['model'])
        
        query += " ORDER BY h_Time DESC, Country, Model"
        return self.execute_query(query, tuple(params) if params else None)

    def get_budget_data(self, filters=None):
        """获取预算数据"""
        query = "SELECT * FROM Budget WHERE 1=1"
        params = []
        
        if filters:
            if 'time' in filters:
                query += " AND h_Time = %s"
                params.append(filters['time'])
            if 'country' in filters:
                query += " AND Country = %s"
                params.append(filters['country'])
            if 'model' in filters:
                query += " AND Model = %s"
                params.append(filters['model'])
        
        query += " ORDER BY h_Time DESC, Country, Model"
        return self.execute_query(query, tuple(params) if params else None)

    def get_costs_data(self, country=None):
        """获取成本数据（支持按国家筛选）"""
        if country:
            return self.execute_query(
                "SELECT * FROM Costs WHERE Country = %s ORDER BY Costs_time DESC, Model",
                (country,)
            )
        return self.execute_query("SELECT * FROM Costs ORDER BY Costs_time DESC, Country, Model")

    def get_sales_price_data(self, country=None):
        """获取销售价格数据（支持按国家筛选）"""
        if country:
            return self.execute_query(
                "SELECT * FROM Sales_Price WHERE Country = %s ORDER BY h_Time DESC, Model",
                (country,)
            )
        return self.execute_query("SELECT * FROM Sales_Price ORDER BY h_Time DESC, Country, Model")

    def get_comparison_data(self, time_period=None):
        """
        改进：获取预算vs预测对比数据（而不是预算vs历史）
        使用Display表作为预测数据，Budget表作为预算数据
        """
        if time_period:
            return self.execute_query("""
                SELECT d.h_Time, d.Country, d.Model, 
                       d.Sales as 预测销量, b.Sales as 预算销量,
                       d.Revenues as 预测收入, b.Revenues as 预算收入,
                       d.Gross_profits as 预测毛利, b.Gross_profits as 预算毛利,
                       d.Net_income as 预测净利, b.Net_income as 预算净利
                FROM Display d
                LEFT JOIN Budget b ON d.h_Time = b.h_Time AND d.Country = b.Country AND d.Model = b.Model
                WHERE d.h_Time = %s
            """, (time_period,))
        else:
            return self.execute_query("""
                SELECT d.h_Time, d.Country, d.Model, 
                       d.Sales as 预测销量, b.Sales as 预算销量,
                       d.Revenues as 预测收入, b.Revenues as 预算收入,
                       d.Gross_profits as 预测毛利, b.Gross_profits as 预算毛利,
                       d.Net_income as 预测净利, b.Net_income as 预算净利
                FROM Display d
                LEFT JOIN Budget b ON d.h_Time = b.h_Time AND d.Country = b.Country AND d.Model = b.Model
            """)

    def get_country_summary(self, time_period=None):
        """获取国家汇总数据（改用Display作为预测数据）"""
        if time_period:
            return self.execute_query("""
                SELECT Country, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                WHERE h_Time = %s
                GROUP BY Country
                ORDER BY 总收入 DESC
            """, (time_period,))
        else:
            return self.execute_query("""
                SELECT Country, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                GROUP BY Country
                ORDER BY 总收入 DESC
            """)

    def get_model_summary(self, time_period=None):
        """获取产品汇总数据（改用Display）"""
        if time_period:
            return self.execute_query("""
                SELECT Model, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                WHERE h_Time = %s
                GROUP BY Model
                ORDER BY 总收入 DESC
            """, (time_period,))
        else:
            return self.execute_query("""
                SELECT Model, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                GROUP BY Model
                ORDER BY 总收入 DESC
            """)

    # ================= 核心：财务公式自动计算 =================
    def calculate_financials(self, df_input: pd.DataFrame) -> pd.DataFrame:
        """根据《计算公式.docx》实现全链路自动计算"""
        # 1. 预加载所有参数表 (提高效率)
        df_ex = self.execute_query(Q_GET_ALL_EXCHANGE)
        df_cost = self.execute_query(Q_GET_ALL_COSTS)
        df_price = self.execute_query(Q_GET_ALL_PRICES)
        df_r1 = self.execute_query(Q_GET_ALL_RATIO1)
        df_r2 = self.execute_query(Q_GET_ALL_RATIO2)
        df_r3 = self.execute_query(Q_GET_ALL_RATIO3)
        df_reg = self.execute_query(Q_GET_ALL_REGIONAL)
        df_model = self.execute_query(Q_GET_MODELS_INFO)

        results = []
        for _, row in df_input.iterrows():
            try:
                time, country, model, sales = row['h_Time'], row['Country'], row['Model'], float(row['Sales'])
                
                # 获取基础元数据 (Series, Label)
                m_info = df_model[df_model['Model'] == model]
                series = m_info.iloc[0]['Series'] if not m_info.empty else ''
                label = m_info.iloc[0]['Model_label'] if not m_info.empty else ''
                
                # 获取市场
                country_info = self.execute_query("SELECT Market FROM Country WHERE Country = %s", (country,))
                market = country_info.iloc[0]['Market'] if not country_info.empty else ''

                # 1. 获取汇率 (Exchange)
                ex_rate = 1.0
                curr_ex = df_ex[df_ex['Exchange_time'] == time]
                if not curr_ex.empty: 
                    ex_rate = float(curr_ex.iloc[0]['Exchange_rate'])

                # 2. 获取价格并计算 true_Price
                price_row = df_price[(df_price['Model']==model) & (df_price['Country']==country) & (df_price['h_Time']==time)]
                true_price = 0.0
                if not price_row.empty:
                    p = float(price_row.iloc[0]['Price'])
                    curr = price_row.iloc[0]['Currency']
                    true_price = p * ex_rate if curr == 'USD' else p
                
                # 3. 获取单位成本 (Costs表)
                cost_row = df_cost[(df_cost['Model']==model) & (df_cost['Country']==country) & (df_cost['Costs_time']==time)]
                unit_cost = float(cost_row.iloc[0]['Costs']) if not cost_row.empty else 0.0

                # 4. 获取比率参数
                # Ratio 1 (按 Series)
                r1 = df_r1[df_r1['Series'] == series]
                soft_rate = float(r1.iloc[0]['Software_product_amortization_rate_acc_cost']) if not r1.empty else 0.0
                rand_rate = float(r1.iloc[0]['RandD_rate_acc_cost']) if not r1.empty else 0.0

                # Ratio 2 (按 Country)
                r2 = df_r2[df_r2['Country'] == country]
                func_rate = float(r2.iloc[0]['Functional_cost_allocation_rate_acc_cost']) if not r2.empty else 0.0
                hq_rate = float(r2.iloc[0]['Business_group_headquarters_allocation_rate_acc_cost']) if not r2.empty else 0.0
                mkt_prov_rate = float(r2.iloc[0]['Marketing_activities_provision_rate_acc_revenue']) if not r2.empty else 0.0

                # Ratio 3 (按 Label, Country)
                r3 = df_r3[(df_r3['Model_label']==label) & (df_r3['Country']==country)]
                after_sales_rate = float(r3.iloc[0]['After_sales_provision_rate_acc_cost']) if not r3.empty else 0.0

                # 5. 获取区域费用 (Regional)
                reg = df_reg[(df_reg['Country']==country) & (df_reg['Expenses_time']==time)]
                reg_mkt = float(reg.iloc[0]['Marketing_expenses']) if not reg.empty else 0.0
                reg_labor = float(reg.iloc[0]['Labor_cost']) if not reg.empty else 0.0
                reg_var = float(reg.iloc[0]['Other_variable_expenses']) if not reg.empty else 0.0
                reg_fixed = float(reg.iloc[0]['Other_fixed_expenses']) if not reg.empty else 0.0

                # === 执行计算 ===
                revenues = sales * true_price
                total_costs = unit_cost * sales 
                gross_profits = revenues - total_costs
                
                # 中间变量计算
                rand_d_exp = total_costs * (soft_rate + rand_rate)
                after_sales_prov = total_costs * after_sales_rate
                mkt_prov = revenues * mkt_prov_rate
                
                margin_profits = gross_profits - rand_d_exp - after_sales_prov - mkt_prov - reg_mkt - reg_labor - reg_var
                
                # 其他费用
                func_exp = total_costs * func_rate
                hq_exp = total_costs * hq_rate
                
                net_income = margin_profits - reg_fixed - func_exp - hq_exp

                # 填充结果
                row['Market'] = market
                row['Revenues'] = round(revenues, 2)
                row['Gross_profits'] = round(gross_profits, 2)
                row['Margin_profits'] = round(margin_profits, 2)
                row['Net_income'] = round(net_income, 2)
                row['Model_label'] = label
                row['Series'] = series
                
            except Exception as e:
                print(f"Calculation Error for {row}: {e}")
                
            results.append(row)
        return pd.DataFrame(results)

    def save_data(self, df: pd.DataFrame, table_name="History") -> bool:
        """保存并覆盖 (UPSERT)"""
        if df.empty: return True
        try:
            # 1. 先计算
            df_calc = self.calculate_financials(df)
            
            # 2. 再入库
            sql = Q_UPSERT_HISTORY if table_name == "History" else Q_UPSERT_BUDGET
            
            cursor = self.connection.cursor()
            data = []
            for _, r in df_calc.iterrows():
                # 确保顺序与SQL一致
                data.append((
                    r['h_Time'], r['Country'], r.get('Market', ''), r['Model'], 
                    r.get('Model_label', ''), r.get('Series', ''), r['Sales'], 
                    r.get('Revenues', 0), r.get('Gross_profits', 0), 
                    r.get('Margin_profits', 0), r.get('Net_income', 0)
                ))
            
            cursor.executemany(sql, data)
            self.connection.commit()
            return True
        except Exception as e:
            st.error(f"保存失败: {e}")
            return False

    def save_sales_price(self, df: pd.DataFrame) -> bool:
        """保存价格表 (业务员用)"""
        if df.empty: return True
        try:
            cursor = self.connection.cursor()
            data = []
            for _, r in df.iterrows():
                data.append((
                    r['id'], r['Model'], r['Country'], r['h_Time'], 
                    r['Currency'], r['Sales'], r['Price'], r['Exchange_time']
                ))
            cursor.executemany(Q_UPSERT_SALES_PRICE, data)
            self.connection.commit()
            return True
        except Exception as e:
            st.error(f"保存价格失败: {e}")
            return False

    def get_system_logs(self):
        """获取系统操作日志"""
        try:
            # 先检查表是否存在
            check_table = "SHOW TABLES LIKE 'System_Log'"
            result = self.execute_query(check_table)
            
            if result.empty:
                print("System_Log表不存在，尝试创建...")
                # 尝试创建表
                create_table = """
                    CREATE TABLE IF NOT EXISTS System_Log (
                        Log_ID INT AUTO_INCREMENT PRIMARY KEY,
                        Log_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        Username VARCHAR(100) NOT NULL,
                        Role VARCHAR(100),
                        Action_Type VARCHAR(100),
                        Details TEXT,
                        INDEX idx_username (Username),
                        INDEX idx_time (Log_Time),
                        INDEX idx_action (Action_Type)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
                self.execute_update(create_table)
            
            # 查询日志
            return self.execute_query(Q_GET_SYSTEM_LOGS)
        except Exception as e:
            print(f"获取系统日志失败: {e}")
            return pd.DataFrame()

@st.cache_resource
def get_db_manager(_role=None):
    return DatabaseManager(_role)