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
    # GETS DATA FROM THE CHOSEN STOCK BY ITS NAME                      
    symbol = "CAP.PA"
    period = "6mo"
    S = Stock(symbol,period)

    try:
        company = yf.Ticker(symbol).info["longName"]
    except:
        company = symbol
        
    # SUBPLOTS LAYOUT CREATION
    fig = make_subplots(rows=4, 
                        cols=1,
                        row_heights=[0.6,0.15,0.15,0.1],
                        vertical_spacing=0.0,
                        shared_xaxes=True)


    # INDICATORS DICTIONARIES CREATION
    indicators = dict()
    names, colors = [], []     
    #names += ["Hammer","InvertedHammer","ShootingStar","HangingMan"]
    #names += ["MorningStar","EveningStar"]            
    #names += ["BearishEngulfing","BullishEngulfing"]
    names += ["Top","Bottom"]
    colors += ["Blue","Red"]                  
    colorDict = dict(zip(names,colors))   
    for i in names:
        indicators[i] = S._getDict(i, "Avg")
        print(i+": "+str(len(indicators[i])))     
        

    # PLOTTING MAIN INDICATORS
    for k, v in indicators.items():
        fig.add_trace(
            go.Scatter(
                name=k,
                x=list(v.keys()), 
                y=list(v.values()), 
                mode="markers",
                marker=dict( 
                    symbol="circle-open",     
                    opacity=1,
                    size=30,
                    line=dict(
                            color=colorDict[k],
                            width=1),
                    #color="Orange",
                    )
                ),
            row=1, 
            col=1
            )   
        
        
    # PLOTTING CANDLESTICK SERIES   
    fig.add_trace(
        go.Candlestick(
            name=symbol,
            x=S.History["Date"],
            open=S.History["Open"],
            high=S.History["High"],
            low=S.History["Low"],
            close=S.History["Close"],
            increasing = dict(
                fillcolor = "White",
                line = dict(
                    color = "Gray",
                    width = 1),
                ),
            decreasing = dict(
                fillcolor = "Black",
                line = dict(
                    color = "Black",
                    width = 1),
                ),
            ),
        row=1, 
        col=1
        )  
                                             

    # PLOTTING SIMPLE MOVING AVERAGES
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
             
    # PLOTTING EXPONENTIAL MOVING AVERAGES
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
        
    # PLOTTING THE MACD LINE
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
    
     # PLOTTING THE MACD-SIGNAL LINE
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
    
    # PLOTTING THE MACD DIFFERENCE HISTOGRAM
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
              
    # PLOTTING THE RSI
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

    # PLOTTING VOLUME
    fig.add_trace(
        go.Bar(
            name="Volume",
            x=S.History["Date"],
            y=S.History["Volume"],  
            marker_color="Gray"),
        row=4,
        col=1
        ) 

    # UPDATES LAYOUT AND DISPLAYS GRAPH
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title=company,
        height=800,
        yaxis=dict(
            spikemode="across"),
        xaxis=dict(
            spikemode="across",
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),  
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

    # ADDS OTHER BUTTONS
    button_layer_1_height = 1.08
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["colorscale", "Viridis"],
                        label="Viridis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Cividis"],
                        label="Cividis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Blues"],
                        label="Blues",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Greens"],
                        label="Greens",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 20, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="right",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=["reversescale", False],
                        label="False",
                        method="restyle"
                    ),
                    dict(
                        args=["reversescale", True],
                        label="True",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 20, "t": 10},
                showactive=True,
                x=0.37,
                xanchor="right",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=[{"contours.showlines": False, "type": "contour"}],
                        label="Hide lines",
                        method="restyle"
                    ),
                    dict(
                        args=[{"contours.showlines": True, "type": "contour"}],
                        label="Show lines",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 20, "t": 10},
                showactive=True,
                x=0.58,
                xanchor="right",
                y=button_layer_1_height,
                yanchor="top"
            ),
        ]
    )

    fig.update_layout(
        annotations=[
            dict(text="colorscale", x=0, xref="paper", y=1.06, yref="paper",
                                 align="left", showarrow=False),
            dict(text="Reverse<br>Colorscale", x=0.25, xref="paper", y=1.07,
                                 yref="paper", showarrow=False),
            dict(text="Lines", x=0.54, xref="paper", y=1.06, yref="paper",
                                 showarrow=False)
        ])
                                  
    fig.show()
            

     # DASH APPLICATION
     #app = dash.Dash()
     #app.layout = html.Div([dcc.Graph(figure=fig), html.Button("Texto")])
     #app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter


def main2():                               
                                 
    #ibov = yf.download("^BVSP", period="1y")["Adj Close"] 
    #ibov.dropna(inplace=True)   
    
    tickers = ["ABEV3.SA", "ITSA4.SA", "WEGE3.SA", "USIM5.SA", "VALE3.SA"]    
    P = Portfolio(tickers)
                                     
    fig = P.Stocks.plot()
    fig.show()                   

                               
if __name__ == "__main__":
    main()  
                       