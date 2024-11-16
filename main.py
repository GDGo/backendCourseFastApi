from fastapi import FastAPI
import uvicorn

from hotels import router as router_hotel

app = FastAPI()
app.include_router(router_hotel)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)