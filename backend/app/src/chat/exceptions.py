from exceptions import NotFound


class ChatNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="Chat not found.")
