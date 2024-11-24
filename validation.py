# Validation for fields size: as same as size of fields which needs to validate
User_Validation = {
    'username': 6
}
Group_Validation = {
    'group_name': 60,
    'description':250
}
Event_Validation = {
    'title': 250,
    'context':250,
    'location': 200
}

# Sample: only have user.username validation done by python. 
# Other fields controls (in Group module and Event module) are validated by CSS only.
def validate_input(validation_rule, fieldname, fieldvalue):
    max_length = validation_rule.get(fieldname, "")  # Get the field value, default to an empty string
    if len(fieldvalue) <= max_length:
        return True
    return False

# Below section is for validation for dates controls
def is_date_from_earlier_date_to(date_from, date_to):
    return date_from <= date_to



