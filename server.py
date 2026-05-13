from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import uvicorn
from Bestbuy_pdp import fetch_bestbuy_response

app = FastAPI(title="Bestbuy Response API")

@app.post("/bestbuy_response", response_class=HTMLResponse)
def bestbuy_response(url:str = Query(..., description="URL to fetch")):
    try:
        html = fetch_bestbuy_response(url)
        return HTMLResponse(content=html, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ =="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
