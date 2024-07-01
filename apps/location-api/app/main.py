from typing import Annotated, Union

from fastapi import FastAPI,Header

app = FastAPI()


@app.get("/user_location")
def user_location(user_id: Annotated[str | None, Header()] = None):
    return {
        "User": user_id,
        "Location":{
            "x":"12",
            "y":"13"
        }
    }
