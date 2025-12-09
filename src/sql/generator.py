def generate_insert_scripts(data, table_name="parts"):
    """
    JSON benzeri listeden SQL INSERT ifadeleri üretir.
    """
    scripts = []
    for row in data:
        cols = ", ".join(row.keys())
        vals = ", ".join([f"'{v}'" for v in row.values()])
        scripts.append(f"INSERT INTO {table_name} ({cols}) VALUES ({vals});")
    return scripts
