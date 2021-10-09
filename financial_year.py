from nepali_datetime import date
import os

financial_year_start = '04-01'
databases = ['stock&vat.db','transactions.db']

def check_year():
    if 'old_databases' not in os.listdir():
        os.makedirs('old_databases')
    today_date = str(date.today())[5:]
    year = str(date.today())[:4]

    if (today_date==financial_year_start):
        new_dir = str(int(year)-1)+'-'+ year +'_databases'
        os.makedirs('old_databases/'+new_dir)

        
        for db in databases:
            os.rename(db,'old_databases/'+new_dir+'/'+db)