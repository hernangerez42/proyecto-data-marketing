import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\Pochito\Desktop\1° Protecto\dataset original\bank_marketing.csv')

#separammos el df en 3 dataframes llamados client, campaign, economics y seleccionaos las columnas.
client = df[['client_id',
            'age',
            'job',
            'marital',
            'education', 
            'credit_default', 
            'housing', 
            'loan']]

campaing = df[['client_id',
               'campaign',
               'duration',
               'pdays',
               'previous',
               'poutcome',
               'y']]     

economics = df[['client_id',
                'emp_var_rate',
                'cons_price_idx',
                'euribor3m',
                'nr_employed']]       
    
#Cambiamos el nombre de client_id a id en el dataframe client
client = client.rename(columns={'client_id':'id'})

#renombramos otras columnas
campaing = campaing.rename(columns={'duration':'contact_duration',
                                    'previous':'previous_campaign_contacts',
                                    'y':'campaign_outcome',
                                    'poutcome':'previous_outcome',
                                    'campaign':'number_contacts'})

economics = economics.rename(columns={'euribor3m':'euribor_tree_months',
                                        'nr_employed':'number_employed'})

#cambiamos . por _ en la columna education
client['education'] = client['education'].str.replace('.', '_')
#rellenmos los valores nulos con unknown de la columna education
client['education'] = client['education'].fillna('unknown')

#eliminamos los puntos de la columna job
client['job'] = client['job'].str.replace('.', '')

#Convierta "success"y "failure"en las columnas "previous_outcome"y "campaign_outcome"en binario ( 1o 0), junto con el cambio "nonexistent"a los valores nulos de NumPy en "previous_outcome".
campaing['previous_outcome'] = campaing['previous_outcome'].replace(['success', 'failure', 'nonexistent'], [1, 0, np.nan])
campaing['campaign_outcome'] = campaing['campaign_outcome'].replace(['yes', 'no'], [1, 0])

#Agregue una columna denominada campaign_id, campaigndonde todas las filas tengan un valor de 1
campaing['campaign_id'] = 1

# Verificar y reemplazar valores nulos en df['day'] y df['month']
df['day'] = df['day'].fillna('')
df['month'] = df['month'].fillna('')
# Convertir las columnas en cadenas
df['day'] = df['day'].astype(str)
df['month'] = df['month'].astype(str)
#Cree una datetimecolumna llamada last_contact_date, en el formato de "year-month-day", donde el año es 2022, y los valores de mes y día se toman de las columnas "month"y ."day"
campaing['last_contact_date'] = pd.to_datetime(df['day'] + '-' + df['month'] + '-' + '2022', format='%d-%b-%Y')

#ordenamos las columnas
campaing = campaing[['campaign_id',
                        'client_id',
                        'number_contacts',
                        'contact_duration',
                        'pdays',
                        'previous_campaign_contacts',
                        'previous_outcome',
                        'campaign_outcome',
                        'last_contact_date']]

client = client[['id',
                'age',
                'job',	
                'marital',
                'education',
                'credit_default',
                'housing',
                'loan']]

economics = economics[['client_id',
                        'emp_var_rate',
                        'cons_price_idx',
                        'euribor_tree_months',
                        'number_employed']]

#Guarde los tres DataFrames en archivos csv sin índice como client.csv, campaign.csvy economics.csvrespectivamente.
client.to_csv(r'C:\Users\Pochito\Desktop\1° Protecto\dataset limpios\client.csv', index=False)
campaing.to_csv(r'C:\Users\Pochito\Desktop\1° Protecto\dataset limpios\campaign.csv', index=False)
economics.to_csv(r'C:\Users\Pochito\Desktop\1° Protecto\dataset limpios\economics.csv', index=False)
