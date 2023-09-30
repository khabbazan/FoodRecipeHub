from src.resources.recipes.enums import TAGEnum


def tag_fixtures(target, connection, *args, **kwargs):
    """
    Load tag fixtures into the database.

    This function inserts tag values from the TAGEnum enumeration into the specified target table in the database.

    Args:
        target: The target table to insert values into.
        connection: The database connection.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        bool: True if the fixtures were successfully loaded into the database.
    """
    values_to_insert = []
    for enum in TAGEnum:
        values_to_insert.append({"title": enum})

    connection.execute(target.insert().values(values_to_insert))

    return True
