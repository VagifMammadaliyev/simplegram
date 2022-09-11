class DatabaseError(Exception):
    pass


class DuplicateKeyError(DatabaseError):
    def __init__(
        self, duplicate_key_name: str, duplicate_key_value: str, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.duplicate_key_name = duplicate_key_name
        self.duplicate_key_value = duplicate_key_value

    def __str__(self):
        return (
            f"Duplicate key error. "
            f"Key name: {self.duplicate_key_name}, "
            f"key value: {self.duplicate_key_value}"
        )
