import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from Market import *                            
pd.options.plotting.backend = "plotly"


def main():                                               
    # Gets data from the chosen Stock by its name                      
    symbol = "WEGE3.SA"
    period = "1y"
    S = Stock(symbol,period)

    try:
        company = yf.Ticker(symbol).info["longName"]
    except:
        company = symbol
        
    # Subplots layout creation
    fig = make_subplots(rows=4, 
                        cols=1,
                        row_heights=[0.5,0.2,0.2,0.1],
                        vertical_spacing=0.0,
                        shared_xaxes=True)

    # Printing indicators values 
    yDict = dict()
    indicators = ["Hammer","InvertedHammer","ShootingStar","HangingMan"]
    for i in indicators:                 
        print(i+": "+str(len(S.GetValuesDict(i)["Date"])))
        
    ## Plotting main indicators
    #for k,y in yDict.items():
    #    fig.add_trace(
    #        go.Scatter(
    #            name=k,
    #            x=y["Date"], 
    #            y=y["Close"], 
    #            mode="markers",
    #            marker=dict(      
    #                #color="Orange"
    #                #symbol="square",
    #                opacity=0.4,
    #                size=20,
    #                line=dict(
    #                        #color="Purple",
    #                        width=2
    #                )
    #            )
    #        ),
    #    row=1, 
    #    col=1
    #    )                       

    # Plotting CandleStick series   
    fig.add_trace(
        go.Candlestick(
            name=symbol,
            x=S.History["Date"],
            open=S.History["Open"],
            high=S.History["High"],
            low=S.History["Low"],
            close=S.History["Close"],
            ),
        row=1, 
        col=1
        )  
               
    # Plotting Simple Moving Averages
    numbers = [20]
    for n in numbers:
        fig.add_trace(
            go.Scatter(
                x=list(S.SMA(n).keys()), 
                y=list(S.SMA(n).values()), 
                name="SMA({})".format(n),        
                line_shape='spline'
                ),
            row=1, 
            col=1
            )      
             
    # Plotting Exponential Moving Averages
    numbers = [20]
    for n in numbers:
        fig.add_trace(
            go.Scatter(
                x=list(S.EMA(n).keys()), 
                y=list(S.EMA(n).values()), 
                name="EMA({})".format(n),        
                line_shape='spline'
                ),
            row=1, 
            col=1
            )   
        
    # Plotting the MACD line
    fig.add_trace(
        go.Scatter(
            x=list(S.MACD().keys()), 
            y=list(S.MACD().values()), 
            name="MACD",        
            line_shape="spline",
            line_color="Green",
            ),
        row=2, 
        col=1
        )
    
     # Plotting the MACD-Signal line
    fig.add_trace(
        go.Scatter(
            x=list(S.MACD9().keys()), 
            y=list(S.MACD9().values()), 
            name="MACD-Signal(9)",        
            line_shape="spline",
            line_color="Red",
            ),
        row=2, 
        col=1
        ) 
    
    # Plotting the MACD difference histogram
    fig.add_trace(
        go.Bar(
            x=list(S.MACD_diff("+").keys()), 
            y=list(S.MACD_diff("+").values()), 
            name="MACD Histogram (+)", 
            yaxis="y2",
            marker_color="ForestGreen",
            ),
        row=2, 
        col=1
        )
    fig.add_trace(
        go.Bar(
            x=list(S.MACD_diff("-").keys()), 
            y=list(S.MACD_diff("-").values()), 
            name="MACD Histogram (-)",
            yaxis="y2",
            marker_color="IndianRed", 
            ),
        row=2, 
        col=1
        )
              
    # Plotting RSI
    fig.add_trace(
        go.Scatter(
            x=list(S.RSI().keys()), 
            y=list(S.RSI().values()), 
            name="RSI(14)",        
            line_shape="spline",
            line_color="black"),
        row=3, 
        col=1
        ) 
    fig.add_trace(
        go.Scatter(
            x=[list(S.History["Date"])[0], list(S.History["Date"])[-1]], 
            y=[30,30],
            mode="lines",
            showlegend=False,
            line=dict(width=1, dash="dot", color="red")),
        row=3, 
        col=1
        )
    fig.add_trace(
        go.Scatter(                                                   
            x=[list(S.History["Date"])[0], list(S.History["Date"])[-1]],  
            y=[70,70],
            mode="lines",
            showlegend=False,       
            line=dict(width=1, dash="dot", color="red")),
        row=3, 
        col=1
        ) 

    # Plotting volume
    fig.add_trace(
        go.Bar(
            name="Volume",
            x=S.History["Date"],
            y=S.History["Volume"],  
            marker_color="Gray"),
        row=4,
        col=1
        ) 

    # Updates layout and displays graph
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title=company,
        height=900,
        yaxis=dict(
            spikemode="across"),
        xaxis=dict(
            spikemode="across",
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="todate"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="todate"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="todate"),  
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                    ])
                ),
            rangeslider=dict(
                visible=False
                ),
            type="date"
            )
        )      
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])],
                     spikemode="across")
    fig.update_yaxes(title_text="Stock Price", row=1, col=1,
                     spikemode="across")
    fig.update_yaxes(title_text="MACD", row=2, col=1,
                     spikemode="across")
    fig.update_yaxes(title_text="RSI", row=3, col=1, 
                     spikemode="across",
                     tickvals=[0, 30, 50, 70, 100], range=[0,100])
    fig.update_yaxes(title_text="Volume", row=4, col=1, 
                     spikemode="across")
    fig.show()
            

    # Dash application
    # app = dash.Dash()
    # app.layout = html.Div([dcc.Graph(figure=fig), html.Button("Texto")])
    # app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter


def main2():                               
                                 
    #ibov = yf.download("^BVSP", period="1y")["Adj Close"] 
    #ibov.dropna(inplace=True)   
    
    tickers = ["ABEV3.SA", "ITSA4.SA", "WEGE3.SA", "USIM5.SA", "VALE3.SA"]    
    P = Portfolio(tickers)
                                     
    fig = P.Stocks.plot()
    fig.show()                   

                               
if __name__ == "__main__":
    main()  
                       