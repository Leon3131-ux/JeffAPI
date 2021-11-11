import uvicorn
from fastapi import FastAPI
from controller import auth_controller, user_controller

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(user_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
