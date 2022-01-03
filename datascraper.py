  def worldbank_get(indicator, *args, **kwargs):
    import requests
    
    """
    Get World Bank API data
    :param base: base url
    :param country: country code
    :param indicator: indicator code
    :param format: json or xml
    :param args: additional arguments
    :param kwargs: additional keyword arguments
    :return: dataframe
    """
    
    base = "http://api.worldbank.org/v2/"
    country = "all"
    indicator = indicator
    format = "json"
    url = base + 'country/' + country + '/indicator/' + indicator + '?format=' + format
    if args:
        url += '&' + '&'.join(args)
    if kwargs:
        url += '&' + '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        
    print("Getting Data from ", url)

    def print_dict(d):
        for k, v in d.items():
            print("%s : %s " %(k, v))
            
    r = requests.get(url)
    print_dict(r.json()[0])
    df = pd.json_normalize(r.json()[1])
    
    
    return df