from django.db import models


# Creating Pokemon models here.
class Pokemon(models.Model):
    """This Model Represents the Pokemon Objects with attributes describing it.
    Args:
        name: str
        description: str
        stats: str
        abilities: str
        Moves: str
        weight: str
    Returns:
        str: description of the object.
    """
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    stats = models.CharField(max_length=40)
    abilities = models.CharField(max_length = 40)
    # TODO: Need to change M of `Moves` to small case.
    Moves = models.CharField(max_length = 40)
    weight = models.CharField(max_length = 40)

    def __str__(self):
        return f"{self.description}"
