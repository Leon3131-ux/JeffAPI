import uvicorn
from fastapi import FastAPI
from controller import auth_controller, user_controller, question_controller
from data.data_init import init_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(question_controller.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_data()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
