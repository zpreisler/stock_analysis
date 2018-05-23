#!/usr/bin/env python
class data:
    """
    Converting dictionary
    """
    def __init__(self,d):
        from numpy import array
        self.json=d.json()
        self.data=self.json['Time Series (Daily)']
        self.time=sorted([x for x in self.data])

        self.open,self.high,self.low,self.close,self.volume=self.get()

    def get(self):
        from numpy import array
        key=sorted(list(list(self.data.values())[0].keys()))
        v=[[] for _ in range(len(key))]
        for t in self.time:
            for i,k in enumerate(key):
                v[i]+=[float(self.data[t][k])]
        return array(v)

class vantage:
    """
    Get data from alpha vantage
    """
    def __init__(self):
        """
        API key must be set
        """
        from os import getenv
        api_key=getenv('ALPHAVANTAGE_API_KEY')
        self.url="https://www.alphavantage.co/query"
        self.params={
            'apikey':api_key,
            'datatype':'json',
            'function':'TIME_SERIES_DAILY'
            }

    def request(self,params):
        """
        Request stock quotes from alpha vantage
        """
        import requests
        import json
        self.params={**self.params,**params}
        print(self.params)
        setattr(self,
                self.params['symbol'],
                data(requests.get(self.url,params=self.params)))

def main():

    a=vantage()

    a.request({'symbol':'GOOG'})
    a.request({'symbol':'AMZN'})
    print(a.GOOG.open)
    from matplotlib.pyplot import show,figure,plot

    figure()
    plot(a.GOOG.low,'k-',alpha=0.1,linewidth=0.5)
    plot(a.GOOG.high,'k-',alpha=0.1,linewidth=0.5)

    plot(a.AMZN.low,'k-',alpha=0.1,linewidth=0.5)
    plot(a.AMZN.high,'k-',alpha=0.1,linewidth=0.5)

    figure()
    plot(a.GOOG.volume,'k-',alpha=0.1,linewidth=0.5)

    show()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl-C")



