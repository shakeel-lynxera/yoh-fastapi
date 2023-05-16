import json
import redis
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis import client
from BaseModels import *
from response import api_response
from utils import calculate_distance

try:
    client_ = redis.Redis(
        host="",
        port=6379,
        socket_timeout=5,
    )
    try:
        ping = client_.ping()
    except Exception as e:
        print("Failed to ping Redis")
        print(e)
        exit()
except redis.AuthenticationError:
    print("AuthenticationError")
    exit()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/set-user-gps")
async def set_user_gps(usergps: UserGPS):
    """Saving user gps
    Example:
        API call: https://apisearch.yoyoyoh.com/set-user-gps
        Method: POST
        Request body:
            {
                "resource_type": "driver",
                "id": "12345",
                "session_id": "456",
                "latitude": "34.043369",
                "longitude": "71.629313",
                "timestamp": "1970-01-01 00:00:01"
            }
        Response:
            {
                "message": "Success",
                "data": {},
                "status_code": 200
            }
    """

    value = {"id": usergps.id,
             "resource_type": usergps.resource_type,
             "session_id": usergps.session_id,
             "longitude": usergps.longitude,
             "latitude": usergps.latitude,
             "timestamp": usergps.timestamp
             }
    key = f"{usergps.resource_type}:{usergps.id}"
    client_.hset(key, usergps.resource_type, json.dumps(value))
    return JSONResponse(content=api_response(message="Success",
                                             status_code=200), status_code=200)


@app.put("/update-user-gps")
async def update_user_gps(usergps: UserGPS):
    """Updating user gps
    Example:
        API call: https://apisearch.yoyoyoh.com/update-user-gps
        Method: POST
        Request body:
            {
                "resource_type": "driver",
                "id": "12345",
                "session_id": "456",
                "latitude": "34.043369",
                "longitude": "71.629313",
                "timestamp": "1970-01-01 00:00:01"
            }
        Response:
            {
                "message": "Success",
                "data": {},
                "status_code": 200
            }
    """
    value = {"id": usergps.id,
             "resource_type": usergps.resource_type,
             "session_id": usergps.session_id,
             "longitude": usergps.longitude,
             "latitude": usergps.latitude,
             "timestamp": usergps.timestamp
             }
    key = f"{usergps.resource_type}:{usergps.id}"
    data = client_.hget(key, usergps.resource_type)
    if data is None:
        return JSONResponse(content=api_response(message="No data found",
                                                 status_code=404), status_code=404)
    client_.hset(key, usergps.resource_type, json.dumps(value))
    return JSONResponse(content=api_response(message="Success",
                                             status_code=200), status_code=200)


@app.post("/get-user-gps")
async def get_user_gps(id: str, resource_type: str):
    """Getting user gps
    Example:
        API call: https://apisearch.yoyoyoh.com/get-user-gps?id=123&resource_type=driver
        Method: POST
        Response:
            {
                "message": "Success",
                "data": {
                    "id": "123",
                    "resource_type": "driver",
                    "session_id": "456",
                    "longitude": "71.629313",
                    "latitude": "34.043369",
                    "timestamp": "1970-01-01 00:00:01"
                },
                "status_code": 200
            }
    """
    key = f"{resource_type}:{id}"
    data = client_.hget(key, resource_type)
    if data is None:
        return JSONResponse(content=api_response(message="No data found",
                                                 status_code=404), status_code=404)
    data = json.loads(data)
    return JSONResponse(content=api_response(message="Success",
                                             data=data, status_code=200), status_code=200)


@app.post("/get-nearby-users")
async def get_nearby_users(req_attr: UsersSearchGPS):
    """Getting nearby users
    Example:
        API call: https://apisearch.yoyoyoh.com/get-nearby-users
        Method: POST
        Request body:
            {
                "resource_type": "driver",
                "distance": "10",
                "longitude": "71.739624",
                "latitude": "34.043389",
                "distance_unit": "km" (meters, km, miles)
            }
        Response:
            {
                "message": "Success",
                "data": [
                    {
                        "id": "123",
                        "resource_type": "driver",
                        "session_id": "456",
                        "longitude": "71.629313",
                        "latitude": "34.043369",
                        "timestamp": "1970-01-01 00:00:01",
                        "distance": 6.33,
                        "distance_unit": "miles"
                    },
                    {
                        "id": "1234",
                        "resource_type": "driver",
                        "session_id": "456",
                        "longitude": "71.629313",
                        "latitude": "34.043369",
                        "timestamp": "1970-01-01 00:00:01",
                        "distance": 6.33,
                        "distance_unit": "miles"
                    }
                ],
                "status_code": 200
            }
    """
    list_ = []
    resource_type = req_attr.resource_type
    latitude = req_attr.latitude
    longitude = req_attr.longitude
    distance = float(req_attr.distance)
    distance_unit = req_attr.distance_unit
    try:
        for key in client_.scan_iter(f"{resource_type}:*"):
            object = json.loads(client_.hget(key, resource_type))
            distance_instance = calculate_distance(latitude, longitude,
                                                   object["latitude"], object["longitude"], distance_unit)
            if distance_instance <= distance:
                object["distance"] = distance_instance
                object["distance_unit"] = req_attr.distance_unit
                list_.append(object)
        return JSONResponse(content=api_response(message="Success",
                                                 data=list_, status_code=200), status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content=api_response(message="No data found",
                                                 status_code=404), status_code=404)


"""User Searching"""


@app.post("/save-terms")
async def save_terms(req_attr: SaveTerm):
    """Saving term
    Example:
        API call: https://apisearch.yoyoyoh.com/save-terms
        Method: POST
        Request body:
            {
                "phrase": "hello there world",
                "customer_id": 1,
                "source_id": 2,
                "timestamp": "2021-11-24 13:12:01.675420"
            }
        Response:
            {
                "message": "Success",
                "data": {},
                "status_code": 200
            }
    """
    value = {"phrase": req_attr.phrase,
             "customer_id": req_attr.customer_id,
             "source_id": req_attr.source_id,
             "timestamp": req_attr.timestamp}
    key = f"phrase:{req_attr.phrase}"
    client_.hset(key, "term", json.dumps(value))
    # get_data = json.loads(client_.hget(key, "term"))
    return JSONResponse(content=api_response(message="Success",
                                             status_code=200), status_code=200)


@app.post("/save-search-terms")
async def save_search_terms(req_attr: SaveSearchTerm):
    value = {
        "term": req_attr.term,
        "search_type": req_attr.search_type
    }
    get_data = client_.hget(req_attr.term, req_attr.search_type)
    if get_data is None:
        value["count"] = 1
        client_.hset(req_attr.term, req_attr.search_type, json.dumps(value))
    else:
        get_data = json.loads(get_data)
        value["count"] = get_data["count"] + 1
        client_.hset(req_attr.term, req_attr.search_type, json.dumps(value))

    # appending to general search terms
    key = f"{req_attr.term}:{req_attr.search_type}"
    get_general_data = client_.hget(key, "general")
    if get_general_data is None:
        value["count"] = 1
        client_.hset(key, "general", json.dumps(value))
    else:
        get_general_data = json.loads(get_general_data)
        value["count"] = get_general_data["count"] + 1
        client_.hset(key, "general", json.dumps(value))
    return JSONResponse(content=api_response(message="Success",
                                             status_code=200), status_code=200)


@app.post("/get-search-terms")
async def get_terms(req_attr: GetSearchTerm):
    list_of_terms = []
    with client_.pipeline() as pipe:
        try:
            pipe.watch(req_attr.term)
            keys = pipe.keys(f"*{req_attr.term}*")
            keys = list(
                x.decode("utf-8").split(":")[0] for x in keys if x.decode("utf-8").endswith(req_attr.search_type))
            print(keys)
            for key in keys:
                object = pipe.hget(key, req_attr.search_type)
                list_of_terms.append(json.loads(object))
            list_of_terms = sorted(list_of_terms, key=lambda d: d['count'], reverse=True)[:req_attr.search_length]
            return JSONResponse(content=api_response(message="Success",
                                                     status_code=200, data=list_of_terms), status_code=200)
        except redis.WatchError:
            return JSONResponse(content=api_response(message="No data found",
                                                     status_code=404), status_code=404)


@app.post("/get-general-search-terms")
async def get_general_search(req_attr: GetGeneralTerm):
    list_of_terms = []
    with client_.pipeline() as pipe:
        try:
            pipe.watch(req_attr.term)
            keys = pipe.keys(f"*{req_attr.term}*")
            for key in keys:
                object = pipe.hget(key, "general")
                if object is not None:
                    list_of_terms.append(json.loads(object))
            list_of_terms = sorted(list_of_terms, key=lambda d: d['count'], reverse=True)[:req_attr.search_length]
            return JSONResponse(content=api_response(message="Success",
                                                     status_code=200, data=list_of_terms), status_code=200)
        except redis.WatchError:
            return JSONResponse(content=api_response(message="No data found",
                                                     status_code=404), status_code=404)


@app.post("/set-auto-complete-term")
async def set_auto_complete_term(term: str, search_type: str):
    """Setting auto complete term
    Example:
        API call: https://apisearch.yoyoyoh.com/set-auto-complete-term?term=Dell&search_type=laptop
        Method: POST
        Response:
            {
                "message": "Success",
                "data": {},
                "status_code": 200
            }
    """
    term, search_type = term.strip().lower(), search_type.strip().lower()
    client_.zadd(search_type, {term: 1}, incr=True)
    client_.zadd("general", {term: 1}, incr=True)
    return JSONResponse(content=api_response(message="Success",
                                             status_code=200), status_code=200)


@app.post("/get-auto-complete-term")
async def get_auto_complete_term(term: str, search_type: str):
    """Getting auto complete term
    Example:
        API call: https://apisearch.yoyoyoh.com/get-auto-complete-term?term=dell&search_type=laptop
        Method: POST
        Response:
            {
                "message": "Success",
                "data": [
                    "dell",
                    "dell computer",
                ],
                "status_code": 200
            }
    """
    term, search_type = term.strip().lower(), search_type.strip().lower()
    try:
        data = client_.zscan(name=search_type, match=f"*{term}*", count=100)
        data = list(x[0].decode("utf-8") for x in data[1])
        data = list(dict.fromkeys(data))[:7]
        return JSONResponse(content=api_response(message="Success",
                                                 data=data,
                                                 status_code=200), status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content=api_response(message="No data found",
                                                 status_code=404), status_code=404)


@app.get("/upload-file")
async def upload_file():
    data = open('random_dataset.txt')
    lines = data.readlines()
    for line in lines:
        client_.zadd("general", {line.strip().lower(): 1}, incr=True)
        client_.zadd("random", {line.strip().lower(): 1}, incr=True)

    return JSONResponse(content=api_response(message="chats",
                                             status_code=200), status_code=200)
