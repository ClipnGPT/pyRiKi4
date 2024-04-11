#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime

import unicodedata

import pyodbc
import urllib
from sqlalchemy import create_engine
import pandas as pd

import queue
import threading
import subprocess



class qDB_class:

    def __init__(self, ):
        pass

    def init(self, server='', database='', username='', password='', ):
        self.server   = server
        self.database = database
        self.username = username
        self.password = password
        self.odbcver  = '17'
        return True

    def open(self, ):
        self.conn   = None
        self.cursor = None
        self.pdconn = None

        err_msg = ''
        for i in range(0,8):
            try:
                self.odbcver = str(20-i)
                self.conn = pyodbc.connect('DRIVER={ODBC Driver ' + self.odbcver + ' for SQL Server};' \
                    + 'SERVER=' +self.server+ ';DATABASE=' +self.database+ ';' \
                    + 'UID=' +self.username+ ';PWD=' +self.password+ ';' )
                    #+ 'Trusted_Connection=yes;' )
                self.cursor = self.conn.cursor()

                odbc_connect = urllib.parse.quote_plus(
                      'DRIVER={ODBC Driver ' + str(20-i) + ' for SQL Server};'
                    + 'SERVER=' +self.server+ ';DATABASE=' +self.database+ ';' \
                    + 'UID=' +self.username+ ';PWD=' +self.password+ ';' )
                engine = create_engine('mssql+pyodbc:///?odbc_connect=' + odbc_connect)
                self.pdconn = engine.connect()
                return True
            except Exception as e:
                #print(e)
                err_msg += str(e) + '\n'
        if (err_msg != ''):
            print(err_msg)
        return False

    def get_cursor(self, ):
        return self.cursor

    def get_conn(self, ):
        return self.conn

    def get_pdconn(self, ):
        return self.pdconn

    def sql2pandas(self, sql='', ):
        try:
            df = pd.read_sql(sql, self.pdconn )
            return True, df
        except Exception as e:
            print(e)
        return False, None

    def execute(self, sql='', ):
        try:
            self.cursor.execute(sql)
            return True, self.fetchone()[1]
        except Exception as e:
            print(e)
        return False, None

    def fetchone(self, ):
        try:
            row = self.cursor.fetchone()
            if (row != False):
                return True, row
        #except Exception as e:
        #    print(e)
        except:
            pass
        return False, None

    def pd2fields(self, pandas_df=None, sampling=None, ):

        # pandas_df → fields_df
        columns   = ['フィールド', 'タイプ', '最小値', '最大値', '合計値', '最大桁数', '小数桁数', '日付8桁数値', '日本語有', 'NULL有', 'NULL全件', 'サンプル', ]
        fields_df = pd.DataFrame(columns=columns, )

        # フィールド
        for c in range(len(pandas_df.columns)):
            col = pandas_df.columns[c]
            one_df    = pd.DataFrame({'フィールド':[col]},index=[c])
            fields_df = pd.concat([fields_df, one_df], axis=0)
        fields_df['最大桁数'] = 0
        fields_df['小数桁数'] = 0

        # タイプ
        df_dtypes = pandas_df.dtypes
        for i in range(len(df_dtypes)):
            フィールド = df_dtypes.index[i]
            タイプ     = df_dtypes.iloc[i]
            row = fields_df[fields_df['フィールド'] == フィールド]
            if (len(row) != 1):
                pass # あり得ない内部エラー
            else:
                # タイプ
                index = row.index[0]
                fields_df.loc[index, 'タイプ'] = str(タイプ)

        # Nullスキャン
        for f in fields_df.index:
            フィールド = fields_df.loc[f, 'フィールド']
            fields_df.loc[f, 'NULL有']   = False  # Nullが1件でもあればTrueに
            fields_df.loc[f, 'NULL全件'] = True   # 有効か1件でもあればFalseに
            n = 0
            for i in pandas_df.index:
                n += 1
                if (sampling is not None):
                    if (n > sampling):
                        break
                値 = pandas_df.loc[i, フィールド]
                if (pd.isnull(値)):
                    if(fields_df.loc[f, 'NULL有']  == False):
                        fields_df.loc[f, 'NULL有'] = True
                else:
                    if(fields_df.loc[f, 'NULL全件']  == True):
                        fields_df.loc[f, 'NULL全件'] = False
                if  (fields_df.loc[f, 'NULL有']   == True) \
                and (fields_df.loc[f, 'NULL全件'] == False):
                    break

        # Null列を文字化
        for f in fields_df.index:
            if (fields_df.loc[f, 'NULL全件'] == True):
                フィールド = fields_df.loc[f, 'フィールド']
                pandas_df[フィールド].astype('object')
                fields_df.loc[f, 'タイプ'] = 'object'

        # 作業用 df
        work_df = pandas_df.copy()

        # 数値項目　最小、最大、合計、最大桁数、小数桁数
        for f in fields_df.index:
            フィールド = fields_df.loc[f, 'フィールド']
            タイプ     = fields_df.loc[f, 'タイプ']
            if (タイプ[:3] == 'int') \
            or (タイプ[:5] == 'float'):
                work_df = work_df.fillna({フィールド:0})
                最小値 = work_df[フィールド].min()
                最大値 = work_df[フィールド].max()
                合計値 = work_df[フィールド].sum()
                fields_df.loc[f, '最小値'] = 最小値
                fields_df.loc[f, '最大値'] = 最大値
                fields_df.loc[f, '合計値'] = 合計値

                桁数1 = len(str(int(abs(float(最小値)))))
                fields_df.loc[f, '最大桁数'] = 桁数1
                桁数2 = len(str(int(abs(float(最大値)))))
                if (桁数2 > 桁数1):
                    fields_df.loc[f, '最大桁数'] = 桁数2

                サンプル    = "''"
                小数桁数    = 0
                日付8桁数値 = '？'
                n = 0
                for i in work_df.index:
                    n += 1
                    if (sampling is not None):
                        if (n > sampling):
                            break
                    値 = work_df.loc[i, フィールド]
                    if (サンプル == "''") or (サンプル == "'nan'") or (サンプル == "'NaT'"):
                        サンプル = "'" + str(値) + "'"
                    if (not pd.isnull(値)):
                        内容値 = abs(float(値))
                        整数値 = int(内容値)
                        if (内容値 != 整数値):
                            日付8桁数値 = 'NO'
                            小数値 = 内容値 - 整数値
                            桁数 = len(str(小数値)) - 2  # 0.の2文字
                            if (桁数 >= 10):
                                print('★小数桁数異常？ 値,内容値,整数値,小数値 = ',str(値),内容値,整数値,小数値)
                            else:
                                if (桁数 > 小数桁数):
                                    小数桁数 = 桁数
                        if (日付8桁数値 != 'NO') and (整数値 != 0):
                            if (len(str(整数値)) != 8):
                                日付8桁数値 = 'NO'
                            else:
                                try:
                                    年 = int(str(整数値)[0:4])
                                    月 = int(str(整数値)[4:6])
                                    日 = int(str(整数値)[6:8])
                                    check = datetime.datetime(年, 月, 日, 0, 0, 0)
                                    if (日付8桁数値 == '？'):
                                        日付8桁数値 = 'YES'
                                except:
                                    日付8桁数値 = 'NO'

                fields_df.loc[f, 'サンプル'] = サンプル
                fields_df.loc[f, '小数桁数'] = 小数桁数
                if (日付8桁数値 == 'YES'):
                    fields_df.loc[f, '日付8桁数値'] = True
                else:
                    fields_df.loc[f, '日付8桁数値'] = False

        # 文字項目　最大桁数、日本語
        for f in fields_df.index:
            フィールド = fields_df.loc[f, 'フィールド']
            タイプ     = fields_df.loc[f, 'タイプ']
            if  (タイプ[:3] != 'int') \
            and (タイプ[:5] != 'float'):
                work_df = work_df.fillna({フィールド:''})

                サンプル = "''"
                最大桁数 = 0
                日本語有 = False
                n = 0
                for i in work_df.index:
                    n += 1
                    if (sampling is not None):
                        if (n > sampling):
                            break
                    値 = work_df.loc[i, フィールド]
                    if (サンプル == "''") or (サンプル == "'nan'") or (サンプル == "'NaT'"):
                        サンプル = "'" + str(値) + "'"
                    if (not pd.isnull(値)):
                        文字列 = str(値)
                        try:
                            桁数 = len(文字列.encode('shift_jis'))
                        except:
                            桁数 = len(文字列)
                        if (桁数 > 最大桁数):
                            最大桁数 = 桁数
                        if (日本語有 == False):
                            日本語有 = self.in_japanese(txt=文字列)

                fields_df.loc[f, 'サンプル'] = サンプル
                fields_df.loc[f, '最大桁数'] = 最大桁数
                fields_df.loc[f, '日本語有'] = 日本語有

        #print('')
        #print(fields_df)
        #print('')

        return fields_df

    def in_japanese(self, txt=''):
        t = txt.replace('\r', '')
        t = t.replace('\n', '')
        try:
            for s in t:
                name = unicodedata.name(s) 
                if ('CJK UNIFIED' in name) \
                or ('HIRAGANA' in name) \
                or ('KATAKANA' in name):
                    return True
        except Exception as e:
            pass
        return False

    def pd2create(self, pandas_df=None, fields_df=None, table_id='CNV_TEST', commit=True, ):
        if (fields_df is None):
            fields_df = self.pd2fields(pandas_df=pandas_df)

        sql  = " CREATE TABLE " + table_id + " ("

        for f in fields_df.index:
            フィールド = fields_df.loc[f, 'フィールド']
            タイプ     = fields_df.loc[f, 'タイプ']
            最大桁数   = fields_df.loc[f, '最大桁数']
            小数桁数   = fields_df.loc[f, '小数桁数']

            if (f > 0):
                sql += ", "
            if   (タイプ[:3] == 'int'):
                sql += フィールド + ' int null'
            elif (タイプ[:5] == 'float'):
                sql += フィールド + ' float null'
            elif (タイプ[:8] == 'datetime'):
                sql += フィールド + ' datetime null'
            else: # (タイプ[:6] == 'object'):
                sql += フィールド + ' varchar(max) null'

        sql += " )"

        #self.cursor.execute(sql)
        #if (commit == True):
        #    self.conn.commit()
        #return True

        try:
            self.cursor.execute(sql)
            if (commit == True):
                self.conn.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def pd2db(self, pandas_df=None, fields_df=None, table_id='CNV_TEST', thread=False, chunk=500, ):
        if (fields_df is None):
            fields_df = self.pd2fields(pandas_df=pandas_df)

        sql  = ""
        batch_thread = []

        # データループ
        for i in range(len(pandas_df)):
            if ((i % chunk) == 0):
                if (sql != ''):
                    sys.stdout.write(str(i) + ', ')
                    sys.stdout.flush()
                    if (thread != True):
                        try:
                            self.cursor.execute(sql)
                        except Exception as e:
                            print(e)
                            return False
                    else:
                        alive = 99
                        while (alive >= 10):
                            alive = 0
                            for batch in batch_thread:
                                if (batch.is_alive()):
                                    alive += 1
                            time.sleep(0.50)

                        batch = threading.Thread(target=self.batch_execute, args=(
                                                 str(i),
                                                 self.server, self.database, self.username, self.password, 
                                                 sql, ), daemon=True, )
                        batch.start()
                        batch_thread.append(batch)

                    sql = ""

            if (sql == ""):
                sql += " INSERT INTO " + table_id + " VALUES "
            else:
                sql += ", "

            # 項目ループ
            sql += "  ( "
            for f in fields_df.index:
                フィールド = fields_df.loc[f, 'フィールド']
                タイプ     = fields_df.loc[f, 'タイプ']
                値         = pandas_df.loc[i, フィールド]
                if (f > 0):
                    sql += ", "
                # null
                if (pd.isnull(値)):
                    sql += " null "
                else:
                    # 数値
                    if   (タイプ[:3] == 'int') \
                    or   (タイプ[:5] == 'float'):
                        sql += " " + str(値) + " "
                    # 数値
                    elif (タイプ[:8] == 'datetime'):
                        日時 = 値.strftime('%Y/%m/%d %H:%M:%S')
                        sql += " '" + str(日時) + "' "
                    # 文字
                    else:
                        文字 = str(値)
                        文字 = 文字.replace("'", "''")
                        sql += " '" + 文字 + "' "
            sql += " ) "

        if (sql != ""):
                    if (i > chunk):
                        sys.stdout.write(str(i+1))
                        sys.stdout.flush()
                        print('')
                    if (thread != True):
                        try:
                            self.cursor.execute(sql)
                        except Exception as e:
                            print(e)
                            return False
                    else:
                        alive = 99
                        while (alive >= 5):
                            alive = 0
                            for batch in batch_thread:
                                if (batch.is_alive()):
                                    alive += 1
                            time.sleep(0.50)

                        batch = threading.Thread(target=self.batch_execute, args=(
                                                 str(i),
                                                 self.server, self.database, self.username, self.password, 
                                                 sql, ), daemon=True, )
                        batch.start()
                        batch_thread.append(batch)

        # 終了待機
        time.sleep(1.00)

        alive = 99
        while (alive != 0):
            alive = 0
            for batch in batch_thread:
                if (batch.is_alive()):
                    alive += 1
            time.sleep(0.50)

        time.sleep(10.00)

        return True

    def batch_execute(self, id=0, server=None, database=None, username=None, password=None, sql='', ):
        try:
            batch_conn = pyodbc.connect('DRIVER={ODBC Driver ' + self.odbcver + ' for SQL Server};' \
                + 'SERVER=' +server+ ';DATABASE=' +database+ ';' \
                + 'UID=' +username+ ';PWD=' +password+ ';' )
                #+ 'Trusted_Connection=yes;' )
            batch_cursor = batch_conn.cursor()
            batch_cursor.execute(sql)
            batch_conn.commit()
            batch_cursor.close()
            batch_conn.close()
            return True
        except Exception as e:
            print('batch_execute ' + str(id) + ' error !')
            print(e)
        return False

    def pd2table(self, pandas_df=None, fields_df=None, table_id='CNV_TEST', debug=True, ):
        if (fields_df is None):
            fields_df = self.pd2fields(pandas_df=pandas_df)

        replace_flag = False

        # 削除
        try:
            self.cursor.execute('DROP TABLE ' + table_id)
        except Exception as e:
            #print(e)
            pass
        self.conn.commit()

        # 作成
        res = self.pd2create(pandas_df=pandas_df, fields_df=fields_df, table_id=table_id, commit=True, )
        if (res == False):
            return False

        # バースト転送
        if (replace_flag == False):
            try:
                # 転送
                self.pd2db(pandas_df=pandas_df, fields_df=fields_df, table_id=table_id, thread=True, )
                replace_flag = True
            except:
                pass

        #replace_flag = False

        # レコード転送
        if (replace_flag == False):
            try:

                # 削除
                self.execute('DELETE ' + table_id)

                # 転送
                for i in range(len(pandas_df)):
                    if ((i % 1000) == 0):
                        print(i)
                    try:
                        work_df = pandas_df.iloc[i:i+1]
                        work_df.reset_index(inplace=True, drop=True,)

                        self.pd2db(pandas_df=work_df, fields_df=fields_df, table_id=table_id, thread=False, )
                        if (debug == True):
                            c0 = pandas_df.iat[i, 0]
                            c1 = pandas_df.iat[i, 1]
                            print(str(i) + ', ' + str(c0) + ', ' + str(c1))
                    except:
                        print('')
                        print('★エラー')
                        print(pandas_df.iloc[i:i+1])
                        print('')
                        #break
                replace_flag = True
            except Exception as e:
                print(e)

        return replace_flag

    def close(self, commit=True, ):
        try:
            if (commit == True):
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
            self.pdconn.close()
            return True
        except Exception as e:
            print(e)
        return False

    def pd2csvExcel(self, pandas_df=None, filename='temp.xlsx', csv=True, excel=True, ):
        csv_file   = filename
        excel_file = filename
        if (filename[-5:] == '.xlsx'):
            csv_file   = filename[:-5] + '.csv'
        if (filename[-4:] == '.csv'):
            excel_file = filename[:-5] + '.xlsx'

        res_csv   = False
        res_excel = False

        if (csv == True):
            try:
                pandas_df.to_csv(csv_file, index=False)
                res_csv = True
            except:
                try:
                    os.remove(csv_file)
                except:
                    pass

        if (excel == True):
            try:
                pandas_df.to_excel(excel_file, sheet_name='Sheet1', index=False)
                res_excel = True
            except:
                try:
                    os.remove(excel_file)
                except:
                    pass

        return res_csv, res_excel

    def excelCsv2pd(self, filename='temp.xlsx', excel=True, csv=True, ):
        excel_file = filename
        csv_file   = filename
        if (filename[-4:] == '.csv'):
            excel_file = filename[:-5] + '.xlsx'
        if (filename[-5:] == '.xlsx'):
            csv_file   = filename[:-5] + '.csv'

        res_excel  = False
        res_csv    = False
        res_df     = None
        res_df_csv = None

        if (excel == True):
            if (os.path.isfile(excel_file)):
                try:
                    res_df = pd.read_excel(excel_file, sheet_name=0)
                    res_excel = True
                except:
                    pass

        if (csv == True):
            if (os.path.isfile(csv_file)):
                try:
                    res_df_csv = pd.read_csv(csv_file)
                    res_csv = True
                    # Excel 優先
                    if (res_excel == False):
                        res_df = res_df_csv.copy()
                except:
                    pass

        return res_excel, res_csv, res_df



if __name__ == '__main__':

    db_server   = 'tcp:#server#,1433'
    db_database = '#database#'
    db_username = 'kondo'
    db_password = 'secret'

    qDB = qDB_class()
    qDB.init(db_server, db_database, db_username, db_password, )

    res = qDB.open()
    if (res == False):
       print('open error')
       sys.exit(0)

    table_id = 'HOGE'

    res, df = qDB.sql2pandas(sql='SELECT * FROM ' + table_id)
    if (res == False):
       print('sql2pandas error')
       sys.exit(0)

    else:
        print(df)

    res, row = qDB.execute(sql='SELECT COUNT(*) FROM ' + table_id)
    if (res == False):
       print('sql_execute error')
       sys.exit(0)

    while row not in (None, False):
       print( row[0] )
       _, row = qDB.fetchone()

    res = qDB.pd2table(pandas_df=df, table_id='CNV_TEST')
    if (res == False):
       print('pd2table error')
       sys.exit(0)

    res = qDB.close()
    if (res == False):
       print('close error')
       sys.exit(0)

    filename = 'temp.xlsx'
    res_csv, res_excel = qDB.pd2csvExcel(pandas_df=df, filename=filename, )
    if (res_csv == False) and (res_excel == False):
       print('pd2csvExcel error')
       sys.exit(0)

    filename = 'temp.xlsx'
    res_excel, res_csv, res_df = qDB.excelCsv2pd(filename=filename, )
    if (res_excel == False) and (res_csv == False):
       print('excelCsv2pd error')
       sys.exit(0)

    print(res_df)



