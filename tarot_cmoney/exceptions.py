class NoCardsRemainingError(Exception):
    def __init__(self):
        self.message = 'Attempted to draw a card from an empty deck.'
        super().__init__(self.message)

class UnexpectedDirectionError(Exception):
    def __init__(self, direction: str):
        self.message = (f'The inputted direction ("{direction}") is not a recognized value. '
                        f'Please input either "upright" or "reversed".')
        super().__init__(self.message)