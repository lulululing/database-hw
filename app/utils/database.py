# app/utils/database.py
from datetime import datetime
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
        """获取所有时间周期（改为从Display表获取）"""
        # 将 History 改为 Display
        df = self.execute_query("SELECT DISTINCT h_Time FROM Display ORDER BY h_Time DESC")
        return df['h_Time'].tolist() if not df.empty else []

    def insert_system_log(self, action_type, details, username=None, role=None):
        """
        向System_Log表插入日志记录（统一函数）
        
        参数:
        - action_type: 操作类型，如'LOGIN', 'LOGOUT', 'DATA_ENTRY'等
        - details: 操作详情描述
        - username: 用户名（可选，默认从session获取）
        - role: 角色（可选，默认从session获取）
        
        返回:
        - bool: 插入是否成功
        """
        try:
            # 从session_state获取用户信息（如果未提供）
            username = username or st.session_state.get('username', 'unknown')
            role = role or st.session_state.get('role', 'unknown')
            
            # 构建插入语句 - Log_Time使用数据库的CURRENT_TIMESTAMP
            query = """
            INSERT INTO System_Log (Username, Role, Action_Type, Details)
            VALUES (%s, %s, %s, %s)
            """
            
            params = (username, role, action_type, details)
            success = self.execute_update(query, params)
            
            if not success:
                print(f"日志插入失败: {username}, {role}, {action_type}, {details}")
            
            return success
            
        except Exception as e:
            print(f"插入系统日志失败: {e}")
            return False
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

    def delete_costs_data(self, costs_id=None, model=None, country=None, costs_time=None):
        """增强的删除成本数据方法，支持多种删除方式"""
        try:
            if costs_id:
                query = "DELETE FROM Costs WHERE Costs_id = %s"
                params = (costs_id,)
            elif model and country and costs_time:
                query = "DELETE FROM Costs WHERE Model = %s AND Country = %s AND Costs_time = %s"
                params = (model, country, costs_time)
            else:
                st.error("删除成本数据需要提供ID或(型号+国家+时间)")
                return False
            
            return self.execute_update(query, params)
            
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

    # ================= 新增：汇率获取方法 =================
    def get_exchange_rates_df(self):
        """获取汇率表用于货币转换"""
        return self.execute_query(Q_GET_EXCHANGE_RATES)

    # ================= 核心：财务公式自动计算（保留V1结构，但集成V2的去重和缺失值处理） =================
    def calculate_financials(self, df_input: pd.DataFrame) -> pd.DataFrame:
        """根据《计算公式.docx》实现全链路自动计算，集成数据去重和缺失值处理"""
        if df_input.empty:
            return df_input
            
        # 1. 预加载所有参数表（按需加载，保持V1方式）
        df_ex = self.execute_query(Q_GET_ALL_EXCHANGE)
        df_cost = self.execute_query(Q_GET_ALL_COSTS)
        df_price = self.execute_query(Q_GET_ALL_PRICES)
        df_r1 = self.execute_query(Q_GET_ALL_RATIO1)
        df_r2 = self.execute_query(Q_GET_ALL_RATIO2)
        df_r3 = self.execute_query(Q_GET_ALL_RATIO3)
        df_reg = self.execute_query(Q_GET_ALL_REGIONAL)
        df_model = self.execute_query(Q_GET_MODELS_INFO)
        df_country = self.execute_query("SELECT Country, Market FROM Country")

        # 2. 数据去重处理（从V2迁移的关键修复）
        # Ratio_Expenses3表去重：按ID倒序，保留最新配置
        if not df_r3.empty and 'Ratio_expenses3_id' in df_r3.columns:
            df_r3 = df_r3.sort_values('Ratio_expenses3_id', ascending=False) \
                         .drop_duplicates(subset=['Model_label', 'Country'], keep='first')
        
        # 其他表防御性去重
        if not df_cost.empty:
            df_cost = df_cost.drop_duplicates(subset=['Model', 'Country', 'Costs_time'], keep='first')
        if not df_price.empty:
            df_price = df_price.drop_duplicates(subset=['Model', 'Country', 'h_Time'], keep='first')
        if not df_reg.empty:
            df_reg = df_reg.drop_duplicates(subset=['Country', 'Expenses_time'], keep='first')

        results = []
        for _, row in df_input.iterrows():
            try:
                time, country, model, sales = row['h_Time'], row['Country'], row['Model'], float(row['Sales'])
                
                # 获取基础元数据 (Series, Label)
                m_info = df_model[df_model['Model'] == model]
                series = m_info.iloc[0]['Series'] if not m_info.empty else ''
                label = m_info.iloc[0]['Model_label'] if not m_info.empty else ''
                
                # 获取市场
                market_row = df_country[df_country['Country'] == country]
                market = market_row.iloc[0]['Market'] if not market_row.empty else ''

                # 1. 获取汇率 (Exchange)
                ex_rate = 1.0
                curr_ex = df_ex[df_ex['Exchange_time'] == time]
                if not curr_ex.empty: 
                    ex_rate = float(curr_ex.iloc[0]['Exchange_rate'])

                # 2. 获取价格并计算 true_Price（改进的货币转换逻辑）
                true_price = 0.0
                price_row = df_price[(df_price['Model']==model) & (df_price['Country']==country) & (df_price['h_Time']==time)]
                if not price_row.empty:
                    p = float(price_row.iloc[0]['Price'])
                    curr = price_row.iloc[0]['Currency']
                    # 改进的货币转换：USD需要乘汇率，其他货币直接使用
                    true_price = p * ex_rate if curr == 'USD' else p
                else:
                    # 缺失值处理：如果找不到价格，设为0
                    true_price = 0.0
                
                # 3. 获取单位成本 (Costs表) - 增加缺失值处理
                unit_cost = 0.0
                cost_row = df_cost[(df_cost['Model']==model) & (df_cost['Country']==country) & (df_cost['Costs_time']==time)]
                if not cost_row.empty:
                    unit_cost = float(cost_row.iloc[0]['Costs'])

                # 4. 获取比率参数 - 增加缺失值处理
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

                # 5. 获取区域费用 (Regional) - 增加缺失值处理
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
                # 出错时使用默认值填充关键字段
                row['Market'] = row.get('Market', '')
                row['Revenues'] = 0.0
                row['Gross_profits'] = 0.0
                row['Margin_profits'] = 0.0
                row['Net_income'] = 0.0
                row['Model_label'] = row.get('Model_label', '')
                row['Series'] = row.get('Series', '')
                
            results.append(row)
        return pd.DataFrame(results)

    def save_data(self, df: pd.DataFrame, table_name="History") -> bool:
        """保存并覆盖 (UPSERT)，自动更新Display表"""
        if df.empty:
            return True
            
        try:
            # 1. 先计算
            df_calc = self.calculate_financials(df)
            
            # 2. 再入库
            sql = Q_UPSERT_HISTORY if table_name == "History" else Q_UPSERT_BUDGET
            
            cursor = self.connection.cursor()
            data = []
            affected_records = []  # 记录影响的记录
            
            for _, r in df_calc.iterrows():
                data.append(( 
                    r['h_Time'], r['Country'], r.get('Market', ''), r['Model'], 
                    r.get('Model_label', ''), r.get('Series', ''), r['Sales'], 
                    r.get('Revenues', 0), r.get('Gross_profits', 0), 
                    r.get('Margin_profits', 0), r.get('Net_income', 0)
                ))
                affected_records.append({
                    'time': r['h_Time'],
                    'country': r['Country'],
                    'model': r['Model']
                })
            
            cursor.executemany(sql, data)
            self.connection.commit()
            
            # 3. 自动更新Display表
            for record in affected_records:
                self.update_display_table(
                    time_period=record['time'],
                    country=record['country'],
                    model=record['model']
                )
            
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

    # ================= 新增：成本数据保存方法 =================
    def save_costs_data(self, df: pd.DataFrame) -> bool:
        """保存成本数据（修复版）"""
        if df.empty:
            return True
        
        try:
            # 确保有必要的列
            required_cols = ['Model', 'Country', 'Costs_time', 'Costs']
            for col in required_cols:
                if col not in df.columns:
                    raise ValueError(f"缺少必要列: {col}")
            
            # 执行保存
            success = True
            for _, row in df.iterrows():
                query = """
                    INSERT INTO Costs (Model, Country, Costs_time, Costs)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE Costs = VALUES(Costs)
                """
                params = (
                    row['Model'], 
                    row['Country'], 
                    row['Costs_time'], 
                    float(row['Costs'])
                )
                
                if not self.execute_update(query, params):
                    success = False
            
            return success
            
        except Exception as e:
            st.error(f"保存成本数据失败: {e}")
            return False
        
    def get_system_logs(self, user_filter=None, start_date=None, end_date=None):
        """获取系统日志，支持用户筛选和时间筛选"""
        query = "SELECT Log_ID, Log_Time, Username, Role, Action_Type, Details FROM System_Log"
        
        conditions = []
        params = []
        
        if user_filter:
            conditions.append("Username = %s")
            params.append(user_filter)
        
        if start_date:
            conditions.append("Log_Time >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("Log_Time <= %s")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY Log_Time DESC"
        
        return pd.read_sql_query(query, self.connection, params=params if params else None)

    def update_display_table(self, time_period=None, country=None, model=None):
        """
        自动更新Display表数据
        基于最新的History/Budget数据和参数表重新计算
        """
        try:
            # 获取需要计算的数据
            if time_period and country and model:
                # 特定记录
                query = """
                    SELECT h_Time, Country, Model, Sales
                    FROM History 
                    WHERE h_Time = %s AND Country = %s AND Model = %s
                    UNION
                    SELECT h_Time, Country, Model, Sales
                    FROM Budget 
                    WHERE h_Time = %s AND Country = %s AND Model = %s
                """
                params = (time_period, country, model, time_period, country, model)
            elif time_period:
                # 特定时间段的所有记录
                query = """
                    SELECT DISTINCT h_Time, Country, Model, Sales
                    FROM History 
                    WHERE h_Time = %s
                    UNION
                    SELECT DISTINCT h_Time, Country, Model, Sales
                    FROM Budget 
                    WHERE h_Time = %s
                """
                params = (time_period, time_period)
            else:
                # 最近3个月的数据
                query = """
                    SELECT DISTINCT h_Time, Country, Model, Sales
                    FROM History 
                    WHERE h_Time >= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 3 MONTH), '%Y-%m')
                    UNION
                    SELECT DISTINCT h_Time, Country, Model, Sales
                    FROM Budget 
                    WHERE h_Time >= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 3 MONTH), '%Y-%m')
                """
                params = None
            
            df_to_calculate = self.execute_query(query, params)
            
            if df_to_calculate.empty:
                return True
            
            # 计算财务数据
            df_calculated = self.calculate_financials(df_to_calculate)
            
            if df_calculated.empty:
                return False
            
            # 更新Display表
            cursor = self.connection.cursor()
            
            for _, row in df_calculated.iterrows():
                upsert_query = """
                    INSERT INTO Display (h_Time, Country, Market, Model, Model_label, Series, 
                                        Sales, Revenues, Gross_profits, Margin_profits, Net_income)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        Market = VALUES(Market),
                        Model_label = VALUES(Model_label),
                        Series = VALUES(Series),
                        Sales = VALUES(Sales),
                        Revenues = VALUES(Revenues),
                        Gross_profits = VALUES(Gross_profits),
                        Margin_profits = VALUES(Margin_profits),
                        Net_income = VALUES(Net_income)
                """
                
                cursor.execute(upsert_query, (
                    row['h_Time'], row['Country'], row.get('Market', ''),
                    row['Model'], row.get('Model_label', ''), row.get('Series', ''),
                    float(row['Sales']), float(row.get('Revenues', 0)),
                    float(row.get('Gross_profits', 0)), float(row.get('Margin_profits', 0)),
                    float(row.get('Net_income', 0))
                ))
            
            self.connection.commit()
            cursor.close()
            
            # 记录日志
            st.session_state['last_display_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return True
            
        except Exception as e:
            st.error(f"更新Display表失败: {e}")
            return False

    def get_display_update_status(self):
        """获取Display表更新状态"""
        try:
            query = """
                SELECT MAX(h_Time) as latest_time, 
                    COUNT(*) as record_count,
                    MAX(updated_at) as last_update
                FROM Display
            """
            df = self.execute_query(query)
            return df.iloc[0] if not df.empty else None
        except:
            return None


def get_db_manager(_role=None):

    return DatabaseManager(_role)
