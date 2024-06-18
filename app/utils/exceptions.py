class ObjectNotFound(Exception):
    def __init__(
            self,
            name_object: str,
            attribute_name: str,
            attribute_value: str
    ) -> None:
        super().__init__(f"{name_object} with {attribute_name} - "
                         f"{attribute_value} not found.")


class ObjectAlreadyExists(Exception):
    def __init__(
            self,
            name_object: str,
            attribute_name: str,
            attribute_value: str
    ) -> None:
        super().__init__(f"{name_object} with {attribute_name} - "
                         f"{attribute_value} already exists.")


class UserNotFoundException(ObjectNotFound):
    def __init__(
            self,
            attribute_name: str,
            attribute_value: str,
            name_object: str = "User"
    ) -> None:
        super().__init__(name_object, attribute_name, attribute_value)


class UserAlreadyExistsException(ObjectAlreadyExists):
    def __init__(
            self,
            attribute_name: str,
            attribute_value: str,
            name_object: str = "User"
    ) -> None:
        super().__init__(name_object, attribute_name, attribute_value)


class UserUnauthorizedException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Detail: {message}")


class RequestNotFoundException(ObjectNotFound):
    def __init__(
            self,
            attribute_name: str,
            attribute_value: str,
            name_object: str = "Request"
    ) -> None:
        super().__init__(name_object, attribute_name, attribute_value)


class AccessRequestException(Exception):
    def __init__(self, attribute_name: str, attribute_value: str) -> None:
        super().__init__(f"No access to request from {attribute_name}: {attribute_value}")
