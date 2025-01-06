class Return(Exception):
    def __init__(self, value):
        super().__init__(None, None, None)
        self.value = value
