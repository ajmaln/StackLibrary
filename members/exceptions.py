

class MaximumIssuedBooks(Exception):
    message = ''

    def __init__(self, *args, message="MaximumIssuedBooks: Maximum issued books reached"):
        super().__init__(*args)
        self.message = message


class MaximumRenewalCount(Exception):
    message = ''

    def __init__(self, *args, message="MaximumRenewalCount: Maximum renewal count reached"):
        super().__init__(*args)
        self.message = message

