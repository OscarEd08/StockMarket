from fastapi import FastAPI
from app.routes import market_data, trading, gpt_analysis

app = FastAPI()

app.include_router(market_data.router, prefix="/market")
app.include_router(trading.router, prefix="/trading")
app.include_router(gpt_analysis.router, prefix="/gpt")

@app.get("/")
def root():
    return {"message": "Sistema de Trading Automatizado"}
