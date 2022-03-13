# %%
import pandas as pd
df = pd.read_csv("/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/ds-toolkit/Dashboards/Global_Mobility_Report.csv")

#drop columns we don't need
df = df.drop(columns=['sub_region_1','sub_region_2','metro_area','place_id','iso_3166_2_code','census_fips_code'])
# %%
print(df.columns)
# %%
#Convert country codes to country names
# import pycountry

# def convert_to_country(x):
#     try:
#         return pycountry.countries.get(alpha_2=x).name
#     except:
#         return "Na"
# df['country'] = df['country_region_code'].apply(lambda x: convert_to_country(x))
df.rename(columns = {'country_region_code':'code', 'country_region':'country','retail_and_recreation_percent_change_from_baseline':'rec_retail','grocery_and_pharmacy_percent_change_from_baseline':'pharm_grocery','parks_percent_change_from_baseline':'parks', 'transit_stations_percent_change_from_baseline':'pub_transit', 'workplaces_percent_change_from_baseline':'workplace','residential_percent_change_from_baseline':'residentional'}, inplace=True)
# %%
ALL = list(df.code.unique())
EU = ['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK']
ASIA = ['CN','HK','JP','KR','TW']
FMRUSSR = ['AF','AM','AZ','BH','BD','BT','BN','KH','CX','CC','CY','GE','IN','ID','IR','IQ','IL','JO','KZ','KZ','KP','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TJ','TH','TR','TM','AE','UZ','VN','YE']
AFRICA = ['DZ','AO','BJ','BW','IO','BF','BI','CM','CV','CF','TD','KM','CG','CD','DJ','EG','GQ','ER','ET','GA','GM','GH','GN','GW','CI','KE','LS','LR','LY','MG','MW','ML','MR','MU','YT','MA','MZ','NA','NE','NG','RE','RW','ST','SN','SC','SL','SO','ZA','SS','SD','SZ','TZ','TG','TN','UG','EH','ZM','ZW']
OCEANIA = ['AS','AU','CK','FJ','PF','GU','KI','MH','FM','NR','NC','NZ','NU','NF','MP','PW','PG','PN','WS','SB','TK','TO','TV','UM','VU','WF']
SOUTHAMERICA = ['AR','BO','BR','CL','CO','EC','FK','GF','GY','PY','PE','SR','UY','VE']
NORTHAMERICA = ['AG','BS','BB','BZ','CA','CR','CU','DM','DO','SV','GD','GT','HT','HN','JM','MX','NI','PA','PR','BL','KN','LC','MF','PM','VC','TT','US','VG','VI']
# %%
# subset of dataframe only EU countries
# df = df[df.country_region_code.isin(ALL)]

#

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
pn.extension(comms='vscode')
# %%

# select_origin = pn.widgets.Select(name='Origin', options=ASIA)
# select_cyl = pn.widgets.Select(name='cyl',options=select_)
# @pn.depends(select_origin, select_cyl)

# def exp_plot(select_origin, select_):
#     return df[[df.country_region_code.isin(ASIA)]].hvplot(x='date', y=select_, title=select_origin+' '+select_)

# pn.Column(select_origin, select_cyl, exp_plot).embed()
# # %%
# from bokeh.sampledata.autompg import autompg_clean as df

# select_origin = pn.widgets.Select(options=['North America','Asia','Europe'], name='origin')
# select_cyl = pn.widgets.Select(name='cyl',options=['cyl', 'displ'])
# @pn.depends(select_origin, select_cyl)
# def exp_plot(select_origin, select_cyl):
#     return df[(df.origin==select_origin) & (df.cyl==select_cyl)].sort_values(by='mpg').hvplot(x='mpg', y=select_cyl, title=select_origin+' '+select_cyl)
    
    
# pn.Column(select_origin, select_cyl, exp_plot).embed()
                                                          
# %%
import datashader as ds, bokeh, holoviews as hv  # noqa
from distutils.version import LooseVersion

min_versions = dict(ds='0.13.0', bokeh='2.3.2', hv='1.14.4')

for lib, ver in min_versions.items():
    v = globals()[lib].__version__
    if LooseVersion(v) < LooseVersion(ver):
        print("Error: expected {}={}, got {}".format(lib,ver,v))
    else:
        print('Everything is Kosher!\U0001F60E')
# %%
hv.extension('bokeh', 'matplotlib')
# %%
df[df['country_region_code'] =='AE'].plot(x='date', y='transit_stations_percent_change_from_baseline',figsize=(20,10))

# %%

# %%
df.head()
# %%
#Personal Tool
# collect all methods in a list and use a for loop to get help on each method and create a markdown file

def methods_deepdive(x, deep=False):
    # from mdutils.mdutils import MdUtils
    # from mdutils import Html
    
    # mdFile = MdUtils(file_name=(x+'.markdown'), title=f('{x}')) 
    
    methods = dir(x)
    print(methods)
    if deep = True:
        for method in methods:
                print(method)
                temp = print(f'{x}.{method}()')
                help(temp)
         
# %%
methods_deepdive(df)
# %%
#RETURN year from date object
def get_year(x):
    return x.year


# %%
import pandas as pd
import panel as pn
import xarray as xr
import holoviews as hv

pn.extension('tabulator', template='material', sizing_mode='stretch_width')

import colorcet as cc
import hvplot.xarray
import hvplot.pandas
# %%
slider = pn.widgets.RangeSlider(name='Magnitude', start=0, end=10, value=(0,10))

slider
# %%
range_ = pn.widgets.DateRangeSlider(name='Date Range',
                                    start=dt.datetime(2017, 1, 1),
                                    end=dt.datetime(2019, 1, 1),
                                    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)))

range_
# %%
#filter df date based on filter range 
def filter_by_date(df, start, end):
    return df[(df.date >= start) & (df.date <= end)]


# %%
filtered_view = pn.Row(
    pn.Column(range_,df.pub_transit),
    pn.panel(pn.bind(filter_by_date(df,range_.value[0], range_.value[1]))))

# %%

country_select = pn.widgets.Select(name='Country', options=ALL)



dataF = pn.panel(df[df.code == country_select.value].sample(n=10))

def df_callback(event):
    dataF.object = df[df == (event.new)].compute()
    
country_select.param.watch(df_callback, 'value')

pn.Column(country_select, dataF, width=400)

# %%
# dataF = pn.panel(df[df.code == 'PY'])
# dataF
# %%
def filter_country(x):
    print(x)
    return df[df.code == x].sample(n=10)

bound_fn = pn.bind(filter_country(country_select.value))
pn.Column(country_select, pn.panel(bound_fn))
# %%


@pn.depends(country_select)
def filter_country(df, x):
    print(x)
    return df[df.code == x].sample(n=10)

data = filter_country(df, country_select.value)
xview = pn.panel(data)
pn.Row(country_select,xview)

# %%
def filter_country(df, x):
    print(x)
    return df[df.code == x].sample(n=10)



y = pn.widgets.Select(name='Country', options=ALL)
data = filter_country(df, y.value)
xview = pn.panel(data)
layout = pn.Row(pn.Column('Main',y,xview),pn.panel(xview))


def update(event):
    layout.object = pn.panel(filter_country(df, y.value))
y.param.watch(update, 'value')
layout


# %%
y = pn.widgets.Select(name='Country', options=ALL)


# %%

d = pn.widgets.DataFrame((df[df.code == 'AE'].sample(n=10)),name="TRee")
d
# %%
