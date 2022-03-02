# %%
import pandas as pd
df = pd.read_csv("/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/ds-toolkit/Dashboards/Global_Mobility_Report.csv")

# %%
df.head(20)
# %%
#drop columns we don't need
df = df.drop(columns=['sub_region_1','sub_region_2','metro_area','place_id','iso_3166_2_code','census_fips_code'])
# %%
print(df.columns)
# %%
import pycountry

def convert_to_country(x):
    try:
        return pycountry.countries.get(alpha_2=x).name
    except:
        return "Na"
# %%
df['country'] = df['country_region_code'].apply(lambda x: convert_to_country(x))

# %%
ALL = list(df.country_region_code.unique())
EU = ['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK']
ASIA = ['CN','HK','JP','KR','TW']
FMRUSSR = ['AF','AM','AZ','BH','BD','BT','BN','KH','CX','CC','CY','GE','IN','ID','IR','IQ','IL','JO','KZ','KZ','KP','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TJ','TH','TR','TM','AE','UZ','VN','YE']
AFRICA = ['DZ','AO','BJ','BW','IO','BF','BI','CM','CV','CF','TD','KM','CG','CD','DJ','EG','GQ','ER','ET','GA','GM','GH','GN','GW','CI','KE','LS','LR','LY','MG','MW','ML','MR','MU','YT','MA','MZ','NA','NE','NG','RE','RW','ST','SN','SC','SL','SO','ZA','SS','SD','SZ','TZ','TG','TN','UG','EH','ZM','ZW']
OCEANIA = ['AS','AU','CK','FJ','PF','GU','KI','MH','FM','NR','NC','NZ','NU','NF','MP','PW','PG','PN','WS','SB','TK','TO','TV','UM','VU','WF']
SOUTHAMERICA = ['AR','BO','BR','CL','CO','EC','FK','GF','GY','PY','PE','SR','UY','VE']
NORTHAMERICA = ['AG','BS','BB','BZ','CA','CR','CU','DM','DO','SV','GD','GT','HT','HN','JM','MX','NI','PA','PR','BL','KN','LC','MF','PM','VC','TT','US','VG','VI']
# %%
# subset of dataframe only EU countries
df = df[df.country_region_code.isin(EU)]
# %%
df.head(20)
# %%
import datetime as dt
#change date column to datetime object
df.date = pd.to_datetime(df.date)


# %%
temp = df.columns
select_ = []
for column in temp:
    if df[column].dtype == 'float64':
        select_.append(column)
        
print(select_)
# %%
import hvplot.pandas
import panel as pn

select_origin = pn.widgets.Select(name='Origin', options=ASIA)
select_cyl = pn.widgets.Select(name='cyl',options=select_)
@pn.depends(select_origin, select_cyl)

def exp_plot(select_origin, select_):
    return df[[df.country_region_code.isin(ASIA)]].hvplot(x='date', y=select_, title=select_origin+' '+select_)

pn.Column(select_origin, select_cyl, exp_plot).embed()
# %%
from bokeh.sampledata.autompg import autompg_clean as df

select_origin = pn.widgets.Select(options=['North America','Asia','Europe'], name='origin')
select_cyl = pn.widgets.Select(name='cyl',options=['cyl', 'displ'])
@pn.depends(select_origin, select_cyl)
def exp_plot(select_origin, select_cyl):
    return df[(df.origin==select_origin) & (df.cyl==select_cyl)].sort_values(by='mpg').hvplot(x='mpg', y=select_cyl, title=select_origin+' '+select_cyl)
    
    
pn.Column(select_origin, select_cyl, exp_plot).embed()
                                                          
# %%
