class Command():
    def __init__(self) -> None:
        self.events = []
    
    def execute(self) -> None:
        raise NotImplementedError()