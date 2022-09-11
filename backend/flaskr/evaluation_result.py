import json


class EvaluationResult():
    def __init__(self):
        self.original:str = ""
        self.modelName:str = ""
        self.success:bool = False
        self.failedReason:str = ""
        self.result:str = ""
        self.hasScore:bool = False
        self.score:float = 0

    def toDict(self):
        return self.__dict__