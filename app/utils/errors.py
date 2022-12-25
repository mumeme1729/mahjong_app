class ApiException(Exception):
    """
    HTTPエラーハンドリングクラス
    
    """
    def __init__(self, status_code: int, status:str, detail:str):
        self.status_code = status_code
        self.status = status
        self.detail = detail