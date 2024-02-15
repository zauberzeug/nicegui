from tortoise import fields, models


class User(models.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        age (int): The age of the user.

    Usage:
        user = User(id=1, name="John Doe", age=25)
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
