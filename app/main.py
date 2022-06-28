from fastapi import FastAPI

from pydantic import BaseModel
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
import uuid


from mangum import Mangum


app = FastAPI()

class UnicornIn(BaseModel):
    name: str
    power: str

class UnicornOut(BaseModel):
    name: str
    power: str

def generate_uuid():
    return str(uuid.uuid4())

class UnicornModel(Model):
    """ Unicorn model """
    class Meta:
        table_name = "magicTable"

    pk = UnicodeAttribute(hash_key=True, default="UNICORN")
    id =  UnicodeAttribute(range_key=True, default=generate_uuid())
    name = UnicodeAttribute(null=False)
    power = UnicodeAttribute(default="rainbows")

'''
if not UnicornModel.exists():
        UnicornModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
'''

@app.get("/")
def unicornApp():
    description = {
        "overview": "This app allows a user to create and look up unicorns",
        "create": "User can create a unicorn",
        "list": "User can query all unicorns",
        "get_by_id": "User can look up a unicorn by it's uuid",
        "notes": "For interactive documentation add '/docs' to the url in the address bar"
    }

    return description

@app.get("/unicorns")
def list_unicorns():
    try:
        # query all unicrons
        all_unicorns = UnicornModel.query(hash_key="UNICORN")
        unicorn_list = []
        # format data
        for u in all_unicorns:
            unicorn = {
                "name": u.name,
                "power": u.power,
                "id": u.id
            }
            unicorn_list.append(unicorn)

        # if no unicorns exist
        if len(unicorn_list) == 0:
            unicorn_list = "Unicorn list is empty"

        # create response
        res = {
            "status_code": 200,
            "message": "List all Unicorns",
            "list": unicorn_list
        }

        # return response
        return res

    except:

        # if something goes wrong raise error
        error = {
            "status_code": 404,
            "message": "Could not list all unicorns"
        }

        # return error
        return error

@app.get("/unicorn/{id}")
def get_unicorn(id: str, unicorn: UnicornOut):
    try:
        # query a unicorn by id
        unicorn = UnicornModel.get("UNICORN", id)

        # format res
        res = {
            "status_code": 200,
            "message": f"{unicorn.name} found!",
            "details": unicorn
        }

        # return the response
        return res

    except:

        error = {
            "status_code": 404,
            "message": "Error finding unicorn"
        }

        # return error
        return error



@app.post("/unicorn")
def post_unicorn(unicorn: UnicornIn):

    new_unicorn = UnicornModel(
        name=unicorn.name,
        power=unicorn.power
    )

    new_unicorn.save()
    res = {
        "status_code": 201,
        "message": "unicorn created!"
    }
    return res

handler = Mangum(app)
