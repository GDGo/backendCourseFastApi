from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Дубай", "name": "Dubai"}
]


#Параметры запроса
@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


#Параметр пути
@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def add_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True)

):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1,
         "title": title,
         "name": name}
    )
    return {"Status": "OK"}


@app.put("/hotel/{hotel_id}")
def put_hotel(
        hotel_id : int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"Status": "OK"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id : int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if name:
            hotel["title"] = title
        if title:
            hotel["name"] = name
    return {"Status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)