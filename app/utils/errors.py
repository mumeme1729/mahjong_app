class ApiError(Exception):
    status_code:int = 400
    detail:str = "error"

    def __init__(self,status_code:int = 400,detail:str = "error"):
        self.status_code = status_code
        self.detail = detail