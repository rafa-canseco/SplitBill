from datetime import datetime

class User:
    def __init__(self, name: str,address:str,  email:str):
        self.id = None
        self.name = name
        self.address = address
        self.email = email