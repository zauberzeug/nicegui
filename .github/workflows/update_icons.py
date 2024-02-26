import json

import requests
from num2words import num2words


def clean_names_and_values(name, value=False, google_icons=True):
    if not value:
        name = name.upper()

        if name[:1].isdigit():
            name = num2words(name[:1]) + "_" + name[1:]
        if name[:2].isdigit():
            name = num2words(name[:2]) + "_" + name[2:]
        if name[:3].isdigit():
            name = num2words(name[:3]) + "_" + name[3:]

        name = name.replace("SYM_", "_SYM_")

        if name.endswith("SYM_ROUND"):
            name = name.replace("SYM_ROUND", "")

        if google_icons:
            if "TWO_TONE" in name:
                name = name.replace("TWO_TONE", "")  # two tone icons are not supported so we remove them
        else:
            print("Not supported yet")
    else:
        name = name.lower()

        if google_icons:
            if "outlined" in name:
                name = name.replace("outlined", "o_")

            if "rounded" in name:
                name = name.replace("sym_rounded", "sym_r_")

            if "round" in name:
                name = name.replace("round", "r_")

            if "sharp" in name:
                name = name.replace("sharp", "s_")

            # these are not supported yet
            elif "two_tone" in name:
                name = name.replace("two_tone", "")

    if name.startswith('_'):
        name = name[1:]
    if name.endswith('_'):
        name = name[:-1]

    return name


def get_google_icons():
    """
    Fetches Google icons metadata and returns a string containing the icon names and their corresponding values.

    Returns:
        str: A string containing the icon names and their corresponding values.

    Raises:
        requests.exceptions.RequestException: If there is an error while making the HTTP request.

    Example:
        >>> icons = get_google_icons()
        >>> print(icons)
        ICON_NAME_1 = "icon_value_1"
        ICON_NAME_2 = "icon_value_2"
        ...
    """
    url = "https://fonts.google.com/metadata/icons?incomplete=1&key=material_symbols"

    r = requests.get(url, timeout=30)

    response = json.loads(r.text[4:])

    icons = ''
    icon_name = ''

    families = ["Material Icons", "Material Icons Outlined", "Material Icons Round", "Material Icons Sharp", "Material Icons Two Tone",
                "Material Symbols Outlined", "Material Symbols Rounded", "Material Symbols Round", "Material Symbols Sharp"]

    for icon in response['icons']:
        for family in families:
            # for unsupported_family in icon['unsupported_families']:
            if family in icon['unsupported_families']:
                # print(f'Family {family} is not supported for {icon["name"]}')
                pass
            else:
                icon_name = str(icon['name'])
                icon_value = str(icon['name'])
                family_name = family.replace('Material Icons', '').replace(
                    'Material Symbols', 'Sym').upper().replace(' ', '_')

                icon_name = clean_names_and_values(icon_name + family_name)
                icons += f'{icon_name} = "{clean_names_and_values(family_name + icon_value, value=True)}"\n'

    return icons


def get_boostrap_icons():
    """
    Fetches Bootstrap icons metadata and returns a string containing the icon names and their corresponding values.

    Returns:
        str: A string containing the icon names and their corresponding values.

    Raises:
        requests.exceptions.RequestException: If there is an error while making the HTTP request.

    Example:
        >>> icons = get_boostrap_icons()
        >>> print(icons)
        ICON_NAME_1 = "icon_value_1"
        ICON_NAME_2 = "icon_value_2"
        ...
    """
    url = "https://github.com/twbs/icons/tree/main/icons"

    r = requests.get(url, timeout=30)

    response = json.loads(r.text)

    icons = ''
    icon_name = ''

    for icon in response['payload']['tree']['items']:
        icon_name = icon['name'].replace('.svg', '').replace('-', '_').upper()
        icon_value = icon['name'].replace('.svg', '')

        icons += f'{clean_names_and_values(icon_name, google_icons=False)} = "{icon_value}"\n'

    return icons


google_icons = get_google_icons()
# bootstrap_icons = get_boostrap_icons()

icons = google_icons  # + bootstrap_icons


# Remove underscore from color names starting with '_'
modified_lines = [icon[1:] if icon.startswith('_') else icon for icon in icons.split('\n')]
# Remove duplicate colors and sort the colors alphabetically
icons = '\n'.join(sorted(list(set(modified_lines))))

with open('nicegui/icon.py', 'w') as f:
    f.write(icons)
