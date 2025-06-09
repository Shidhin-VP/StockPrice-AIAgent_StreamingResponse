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
    print("Called Real-Time stock price")
    try:
        stock=yf.Ticker(ticker.upper())
        price=stock.history(period="1d")["Close"][-1]
        Rstatus=f"The Current Price of {ticker.upper()} is ${price:.2f}"
        return price
    except Exception as e:
        Rstatus=f"Error fetching stock price for {ticker}: {str(e)}"
        return Rstatus
    
@tool(description="Fetches the Stock Price of a company/ticker the user requests for a period of time FROM and TO. If the user does not give an interval, use '1d' as default.")
def retrieve_historical_stock_price(ticker: str, start: str, end: str, interval: str = "1d") -> str:
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

    print("Called Historical Price")
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(start=start, end=end, interval=interval)

        if hist.empty:
            return f"No historical data found for {ticker.upper()} from {start} to {end} with interval '{interval}'."

        # Format the first few rows as a string
        hist_reset = hist.reset_index()
        hist_str = hist_reset[["Date", "Open", "High", "Low", "Close"]].to_string(index=False)
        #return f"Historical prices for {ticker.upper()} from {start} to {end} (interval: {interval}):\n{hist_str}"
        return hist_str
    except Exception as e:
        return f"Error fetching historical stock data for {ticker.upper()}: {str(e)}"

    
@tool(name_or_callable="date_and_time_fetcher",description="Tool which will return real tie datetime")
def get_current_datetime()->str:
    """
    Get the current date and time in a human-readable format.
    """

    print("Called Time Tool")

    now=datetime.now()
    return now

#--------------------------------Tools Declared---------------------------------------------------

app=FastAPI()
# memory=MemorySaver()
# guardrail_id=os.getenv("GUARDRAIL_ID")

async def StreamResponses(question:str,thinking:bool,name:str):
    llm=ChatBedrockConverse(
    model="us.amazon.nova-micro-v1:0",
    region_name="us-east-1",
    temperature=0.7
    )
    agent=create_react_agent(
    model=llm,
    tools=[get_current_datetime,retrieve_realtime_stock_price,retrieve_historical_stock_price],
    #prompt=f"You are a AI Assistant that will give user the Real-Time and Historical Stock Prices of Companies/Tickers as per user needs and todays date and time for your reference is: {datetime.now()}, You will only response in plain English and Human Understandable Format and in Times New Roman Font if possible, keep the font human understandable."
    prompt = """
        You are an AI assistant that helps users retrieve real-time and historical stock prices for companies and ticker symbols.

        You have access to the following tools:
        - `get_realtime_datetime` (use this tool to find the current date)
        - `get_historical_prices` (use this tool to get the historical Price of a ticker, and use the 'get_realtime_datetime` tool if you need to fetch current date and time and proceed furter for fetching the historical data)
        - `get_realtime_price` (use this tool to get the real time price of the tinker or company)

        IMPORTANT:
        - When the user uses date-relative phrases such as "today", "yesterday", "this week", etc., you **must first call** `get_realtime_datetime` to get the current date.
        - Do not guess or assume the current date. Always call the datetime tool before computing historical time windows.
        - Only use real values returned from tools, never hallucinate dates.
        - Remind the user (once per session) that you are not a financial advisor and they should do their own research before making investment decisions.
"""

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
                #print("-"*60)
                # print(f"Name inside the Token: {name}")
                #print(f"Full Chunk: {token}")
                #print(f"Full MetaData: {metadata}")
                if isinstance(token.content, list):
                    for chunk in token.content:
                        if chunk['type']=='text':
                            if chunk['text']=="<thinking":
                                thinking=True
                                print(f"Warning : Chunk is Thinking: {thinking} \n TestingChunk: {chunk['text']}")
                                continue
                            elif (chunk['text']==".</") or (chunk['text']=="</"):
                                thinking=False
                                print(f"Chunk Finished Thinking: {thinking} and \n FinishedTestingChunk: {chunk['text']}")
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
        print(f"Error: {e}")
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