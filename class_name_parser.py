import re


def extract_class_data(class_info):
    # Split the input to separate class_name, class_type, and class_place
    class_info_parts = class_info.split(' ', 2)

    # Extract class_name (all text before the first space)
    class_name = class_info_parts[0]

    # check
    # print(class_name)

    # Extract class_type (apply different rules based on "W", "Ć", "K", "L")
    class_type = class_info_parts[1]

    # check
    # print(class_type)

    if class_type.startswith(('W', 'Ć')):
        class_type = class_type[0]  # Just take the first letter
    elif class_type.startswith(('K', 'L')):
        class_type = class_type[:3]  # Take the letter and next two characters
    # check
    # print(class_type)

    # Extract class_place (last 6 characters from the string)
    class_place = class_info_parts[1][-6:]

    # Remove '-n' or '-p' from class_place if present
    class_place = class_place.replace('-n', '').replace('-p', '')

    # If first letter is not in the allowed set, remove the first letter
    allowed_letters = "ABCDEFGJHK"
    if class_place[0] not in allowed_letters:
        class_place = class_place[1:]

    # Special cases
    if class_info == "WF (M) Ć w2 Hala1":
        class_name = "WF"
        class_type = "Ć"
        class_place = "Hala1"

    return [class_name, class_type, class_place]


# Example input
# class_info = "Algeliga W-(P)#ALGA124-p"
# result = extract_class_data(class_info)

# Output the result
# print(result)