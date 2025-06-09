from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_aws import ChatBedrockConverse
from langchain.tools import tool
from pydantic import BaseModel
from typing import Optional
import uvicorn
import yfinance as yf
from datetime import datetime
import os
import uuid
#--------------------------------Tools Initialization---------------------------------------------------

Rstatus=""
Astatus=""

@tool(description="Fetchs the Current and Closest Stock price for a given ticker symbol (eg. AAPL, MSFT), REALTIME Price of the Stock")
def retrieve_realtime_stock_price(ticker:str)->str:
    """
    Fetchs the Current and Closest Stock price for a given ticker symbol (eg. AAPL, MSFT)
    """
    global Rstatus
    try:
        stock=yf.Ticker(ticker.upper())
        price=stock.history(period="1d")["Close"][-1]
        Rstatus=f"The Current Price of {ticker.upper()} is ${price:.2f}"
        return price
    except Exception as e:
        Rstatus=f"Error fetching stock price for {ticker}: {str(e)}"
        return Rstatus
    
@tool(description="Fetches the Stock Price of a company/ticker the user requests for a period of time FROM and TO. If the user does not give an interval, use '1d' as default.")
def Retrieve_historical_stock_price(ticker: str, start: str, end: str, interval: str = "1d") -> str:
    """
    Fetch historical stock prices for a given ticker symbol between a date range. If the user is asking for a period of time, give all the values don't stop if they ask for 1 year also give the entire values fully in a well structured manner, like tables.
    
    Parameters:
    - ticker (str): Ticker symbol (e.g., 'AAPL')
    - start (str): Start date in 'YYYY-MM-DD' format
    - end (str): End date in 'YYYY-MM-DD' format
    - interval (str): Data interval (default is '1d'). Valid intervals: 1m, 2m, 5m, 15m, 1d, 1wk, 1mo
    
    Returns:
    - str: Summary of historical prices
    """
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(start=start, end=end, interval=interval)

        if hist.empty:
            return f"No historical data found for {ticker.upper()} from {start} to {end} with interval '{interval}'."

        # Format the first few rows as a string
        hist_reset = hist.reset_index()
        hist_str = hist_reset[["Date", "Open", "High", "Low", "Close"]].head(5).to_string(index=False)
        #return f"Historical prices for {ticker.upper()} from {start} to {end} (interval: {interval}):\n{hist_str}"
        return hist_str
    except Exception as e:
        return f"Error fetching historical stock data for {ticker.upper()}: {str(e)}"

    
@tool(description="Tool which will return real tie datetime")
def get_current_datetime()->str:
    """
    Get the current date and time in a human-readable format.
    """

    now=datetime.now()
    return now

#--------------------------------Tools Declared---------------------------------------------------

app=FastAPI()
# memory=MemorySaver()
# guardrail_id=os.getenv("GUARDRAIL_ID")

async def StreamResponses(question:str,thinking:bool,name:str):
    llm=ChatBedrockConverse(
    #model="us.meta.llama4-scout-17b-instruct-v1:0",
    model="us.amazon.nova-premier-v1:0",
    region_name="us-east-1",
    temperature=0.7
    )
    agent=create_react_agent(
    model=llm,
    tools=[retrieve_realtime_stock_price,Retrieve_historical_stock_price,get_current_datetime],
    prompt="You are a AI Assistant that will give user the Real-Time and Historical Stock Prices of Companies/Tickers as per user needs, You will only response in plain English and Human Understandable Format and in Times New Roman Font if possible, keep the font human understandable."
    )

    try:
        async for token, metadata in agent.astream(
            {"messages":[
                {
                    "role":"user",
                    "content":question
                }
            ],
            },
            stream_mode="messages"
        ):
            try:
                print("-"*60)
                # print(f"Name inside the Token: {name}")
                print(f"Full Chunk: {token}")
                print(f"Full MetaData: {metadata}")
                if isinstance(token.content, list):
                    print(f"Chunks: {token}")
                    for chunk in token.content:
                        if chunk['type']=='text':
                            if chunk['text']=="<thinking":
                                thinking=True
                                print(f"Warning : Chunk is Thinking: {thinking}")
                                continue
                            elif (chunk['text']==".</") or (chunk['text']=="</"):
                                thinking=False
                                print(f"Chunk Finished Thinking: {thinking} and content is: {chunk['text']}")
                                continue
                            elif thinking==False and (chunk['text']=="thinking" or chunk['text']=="thinking>"):
                                print(f"Clearing the Finishing the Thinking and content is: {chunk['text']}")
                                continue
                            elif thinking==False:
                                yield chunk['text']
                else:
                    print("Warning: Chunk is not a list")
            except Exception as e:
                print(f"Error When Fetching Token: {e}")

    except Exception as e:
        yield f"Error: {e}"

class StockQuestion(BaseModel):
    Stockquestion:Optional[str]=None
    name:Optional[str]=None

@app.post("/question")
def get_question(question:StockQuestion):
    print(f"Question: {question.Stockquestion}")
    # print(f"Name: {question.name}")
    # print(f"Guardrail Id: {guardrail_id}")
    return StreamingResponse(StreamResponses(question.Stockquestion,False,(question.name).capitalize()),media_type="text/event_stream")

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8080)