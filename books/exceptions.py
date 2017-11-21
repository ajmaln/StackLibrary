

class AlreadyIssuedException(Exception):
    message = ''

    def __init__(self, *args, message="Book already Issued to {}"):
        super().__init__(*args)
        self.message = message
