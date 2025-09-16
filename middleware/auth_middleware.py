from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def authenticate_request(request:Request, call_next):
    auth_header=request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401,detail="Authorization header is missing")

        token = auth_header.split(" ")[1]
        if " " in auth_header else None 

        if not token:
            raidede HTTPException(status_code=401,detail=" Invalid token")
        
        response = await call_next(request)
        return response

# protected route 
@app.get("/protected")
async def protected_route():
    return {"message": "you have access to protected route"}


# public route
@app.get("/public")
async def public_route():
    return {"message": "you have access to public route"}   