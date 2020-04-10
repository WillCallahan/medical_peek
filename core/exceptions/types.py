class UnexpectedTypeError(TypeError):
    """
    Inappropriate argument type.
    """

    def __init__(self, expected, actual, message = ""):
        if isinstance(expected, (tuple, list)):
            super(UnexpectedTypeError, self).__init__(
                "Invalid argument type; expected any of " + ', '.join(
                    expected) + " but got a " + actual.__class__.__name__ + (
                    message if "\r\n\t" + message else ""))
        else:
            super(UnexpectedTypeError, self).__init__(
                "Invalid argument type; expected a " + expected.__class__.__name__ + " but got a " +
                actual.__class__.__name__ + (message if "\r\n\t" + message else ""))
