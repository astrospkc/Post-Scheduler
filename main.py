from fastapi import FastAPI
import uvicorn
from routes import (user, auth, post)

def main():
    print("Hello from postscheduler!")
    
    uvicorn.run(app, host="0.0.0.0", port=9000)

app = FastAPI()
app.include_router(user, prefix="/users", tags=["users"])
app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(post, prefix="/posts", tags=["posts"])

@app.get("/")
async def root():
    return {"message": "Hello scheduler"}
if __name__ == "__main__":
    main()
