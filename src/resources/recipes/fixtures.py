
from src.resources.recipes.enums import TAGEnum

def tag_fixtures(target, connection, *args, **kwargs):

    values_to_insert = []
    for enum in TAGEnum:
        values_to_insert.append({"title": enum})

    connection.execute(target.insert().values(values_to_insert))

    return True
