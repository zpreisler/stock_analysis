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
        """
        Convert json data into arrays
        """
        from numpy import array
        key=sorted(list(list(self.data.values())[0].keys()))
        v=[[] for _ in range(len(key))]
        for t in self.time:
            for i,k in enumerate(key):
                v[i]+=[float(self.data[t][k])]
        return array(v)

    def plot(self):
        """
        Plot data
        """
        from matplotlib.pyplot import show,figure,subplot
        import matplotlib.gridspec as gridspec
        from numpy import array,arange
        gs=gridspec.GridSpec(2,1,width_ratios=[1], height_ratios=[3,1])

        fig=figure(figsize=(10,6))
        ax1=subplot(gs[0])
        ax2=subplot(gs[1],sharex=ax1)

        h=array(self.close-self.open) #bar heigth
        x=arange(len(h))

        p=h[h>0]; m=h[h<0]
        xp=x[h>0]; xm=x[h<0]
        bp=self.open[h>0]; bm=self.open[h<0]

        ax1.set_title(self.json['Meta Data']['2. Symbol'])
        ax1.vlines(x,ymin=self.low,ymax=self.high,linewidth=0.66)
        ax1.bar(xp,p,bottom=bp,color='g',width=0.66)
        ax1.bar(xm,m,bottom=bm,color='r',width=0.66)
        ax1.set_ylabel(r"price [\,\$\,]")

        ax2.bar(x,self.volume,alpha=0.33)
        ax2.set_ylabel(r"volume")
        ax2.set_xlabel(r"date")

        fig.subplots_adjust(hspace=0,left=0.1)

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

    stock=vantage()

    stock.request({'symbol':'GOOG'})
    #stock.request({'symbol':'AMZN'})
    #stock.request({'symbol':'IBM'})
    from matplotlib.pyplot import show
    stock.GOOG.plot()
    #stock.AMZN.plot()
    #stock.IBM.plot()
    show()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl-C")
