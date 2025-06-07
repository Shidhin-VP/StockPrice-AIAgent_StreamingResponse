from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langgraph.prebuilt import create_react_agent
from langchain_aws import ChatBedrockConverse
from langchain.tools import tool
from pydantic import BaseModel
from typing import Optional
import uvicorn
import yfinance as yf
from datetime import datetime

#--------------------------------Tools Initialization---------------------------------------------------

@tool(description="Fetches the Real Time Stock Price of a Company or a Ticker")
def retrieve_realtime_stock_price(ticker:str)->str:
    """
        Fetches the Real-Time Stock Price for a given Ticker Symbol (eg.AAPL, MSFT)
    """
    try:
        stock=yf.Ticker(ticker.upper())
        price=stock.history(period="1d")["Close"][-1]
        return price
    except Exception as e:
        return f"Error fetching real-time stock price for {ticker} and the Error is: {str(e)}"
    
@tool(description="Fetches the Current Date and Time (Datetime)")
def get_current_datetime()->str:
    """
        Fetches Current Date and Time to understand and give the correct price of the Stock
    """
    return datetime.now()

tools=[retrieve_realtime_stock_price,get_current_datetime]

#--------------------------------Tools Declared---------------------------------------------------

app=FastAPI()

async def StreamResponses(question:str,thinking:bool):
    llm=ChatBedrockConverse(
        model="us.amazon.nova-micro-v1:0",
        region_name="us-east-1",
        temperature=0.7
    )

    agent=create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a AI Assistant that will give user the Real-Time and Historical Stock Prices of Companies/Tickers as per user needs, You will only response in plain English and Human Understandable Format and in Times New Roman Font if possible, keep the font human understandable. Also, ONLY FOR YOUR REFERENCE: Warn Them as this is about price saying something like, but not exactly like this warn them in your own word (IMPORTANT) **You are just a help but the user needs to understand and research before any purchace or financial process**"
        # prompt="""
        #     You are an AI Assistant, where you help the user to get real-time and historical stock price of Companies/Tickers.
        #     Moreover, You will only response in plain english text and human understandable formats and the font in Times New Romans.
        #     Keep the Fonts in Human Readable and Understandable formats.
        #     ONLY FOR YOUR REFERENCE: **Important** Warn the Users just ones after RESPONDING to the users question something like, but not exactly this: I am here only a help to get real-time and historical stock price data, but the you(user) needs to do researches if investing (this AI is not a Financial Advisor, Just a help for Assisting to get the real time  and historical stock prices) 
        # """
    )

    try:
        for token, metadata in agent.stream(
            {"messages":[
                {
                    "role":"user",
                    "content":question
                }
            ]},
            stream_mode="messages"
        ):
            try:
                print("-"*85)
                print(f"Full Chunk: {token}")
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
                print("Error to Parse Data and Response was not was not a List")

    except Exception as e:
        yield f"Error: {e}"

class StockQuestion(BaseModel):
    Stockquestion:Optional[str]=None

@app.post("/question")
def get_question(question:StockQuestion):
    print(f"Question: {question.Stockquestion}")
    return StreamingResponse(StreamResponses(question.Stockquestion,False),media_type="text/event_stream")

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8080)