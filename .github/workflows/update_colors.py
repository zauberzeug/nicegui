import re

import requests
import webcolors


def get_tailwind_colors():
    """
    Retrieves the Tailwind CSS color variables from the official Tailwind CSS GitHub repository.

    This function makes an HTTP GET request to the Tailwind CSS GitHub repository to fetch the color variables
    defined in the colors.js file. It then processes the response to extract the color names and their corresponding
    hexadecimal values. The extracted color variables are returned as a string in the format expected by Tailwind CSS.

    Returns:
        str: A string containing the Tailwind CSS color variables.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the HTTP request.

    Example:
        >>> colors = get_tailwind_colors()
        >>> print(colors)
        INHERIT = "inherit"
        CURRENT = "currentColor"
        TRANSPARENT = "transparent"
        BLACK = "#000"
        WHITE = "#fff"
        ...
    """
    r = requests.get('https://raw.githubusercontent.com/tailwindlabs/tailwindcss/master/src/public/colors.js', timeout=5)

    color = ""
    tailwind_color = 'INHERIT = "inherit"\nCURRENT = "currentColor"\nTRANSPARENT = "transparent"\nBLACK = "#000"\nWHITE = "#fff"\n'
    color_name = ''

    for line in r.text.split('\n'):
        try:
            if ": {" in line:
                color_name = line.split(": {")[0].strip(',').upper()
                color_name = re.sub(r'\W+', '', color_name)  # Remove non-alphanumeric characters

            if color_name:
                if ":" in line and "{" not in line:
                    name, value = line.split(':')
                    name = re.sub(r'\W+', '', name)  # Remove non-alphanumeric characters from name
                    value = re.sub(r'\W+', '', value)  # Remove non-alphanumeric characters from value

                    color += f'{color_name}{name.upper()} = "#{value}"\n'

                if "}" in line and "{" not in line:
                    tailwind_color += color
                    color = ''

        except ValueError:
            pass

    return tailwind_color


def get_quasar_colors():
    """
    Retrieves Quasar colors from a remote source and returns them as a string.

    This function fetches the Quasar colors from a specific URL and extracts the color values
    using regular expressions. It then formats the color values into a string representation
    with the color names as variables. The resulting string contains all the Quasar colors
    in the format 'COLOR_NAME = "COLOR_VALUE"'. Duplicate colors are removed.

    Returns:
        str: A string representation of the Quasar colors.

    Raises:
        requests.exceptions.RequestException: If there is an error while making the HTTP request.
    """

    r = requests.get('https://raw.githubusercontent.com/quasarframework/quasar/dev/ui/src/css/core/colors.sass', timeout=30)
    r.raise_for_status()

    quasar_color = 'PRIMARY = "#1976d2"\nSECONDARY = "#26A69A"\nACCENT = "#9C27B0"\nPOSITIVE = "#21BA45"\nNEGATIVE = "#C10015"\nINFO = "#31CCEC"\nWARNING = "#F2C037 "\nICE_DUST = "#00B4FF"\nCOLD_BLACK = "#050A14"\nMARS_SAND = "#EA5E13"\nVOID_SUIT = "#D8E1E5"\nSHIP_SHELL = "#8FA8B2"\nFLOATING_ROCK = "#475D66"\nBRAND_PRIMARY = "#00B4FF"\nBRAND_SECONDARY = "#475D66"\nBRAND_ACCENT = "#EA5E13"\nHEADER_BTN_COLOR_LIGHT = "#757575"\nHEADER_BTN_HOVER_COLOR_LIGHT = "#212121"\nHEADER_BTN_COLOR_DARK = "#929397"\nHEADER_BTN_HOVER_COLOR_DARK = "#fff"\nLIGHT_PILL = "#f5f5f5"\nLIGHT_TEXT = "#474747"\nLIGHT_BG = "#fafafa"\nDARK_TEXT = "#cbcbcb"\nDARK_BG = "#050A14"\nWHITE = "#fff"\nBLACK = "#000"\n'

    color_name = ''
    r = r.text.split('// @stylint off')[1]

    for line in r.split('\n'):
        if line.startswith('.'):
            color_name = line.split('-')
            color_name = '_'.join(color_name).upper()

            color_name = re.sub(r'\W+', '', color_name)
            color_name = color_name.replace("TEXT", "")
            color_name = color_name.replace("BG", "BACKGROUND")

        if color_name and ('color' in line or 'background' in line):
            color = re.findall(r'\$(.*?) !', line)[0]
            quasar_color += f'{color_name} = "{color}"\n'

    quasar_color = '\n'.join(list(set(quasar_color.split('\n')))) + '\n'

    return quasar_color


def get_css_colors():
    """
    Retrieves a dictionary of CSS color names and their corresponding hexadecimal values.

    This function combines CSS2, CSS2.1, CSS3, and HTML4 color names and their hexadecimal values
    into a dictionary. The dictionary is then converted into a string representation where each
    color name is uppercase and assigned its corresponding hexadecimal value.

    Returns:
        str: A string representation of the CSS color names and their hexadecimal values.

    Example:
        >>> colors = get_css_colors()
        >>> print(colors)
        ALICEBLUE = "#F0F8FF"
        ANTIQUEWHITE = "#FAEBD7"
        AQUA = "#00FFFF"
        ...
    """
    # Get all CSS color names
    css2_colors = webcolors.CSS2_NAMES_TO_HEX  # CSS2 used the same list as HTML 4.
    css21_colors = webcolors.CSS21_NAMES_TO_HEX  # CSS2.1 added orange.
    css3_colors = webcolors.CSS3_NAMES_TO_HEX
    html4_colors = webcolors.HTML4_NAMES_TO_HEX
    css_colors = {**css2_colors, **css21_colors, **css3_colors, **html4_colors}

    # Convert the dictionary to a string
    colors = '\n'.join([f'{name.upper()} = "{color}"' for name, color in css_colors.items()])

    return colors


tailwind_colors = get_tailwind_colors()
quasar_colors = get_quasar_colors()
css_colors = get_css_colors()

colors = tailwind_colors + quasar_colors + css_colors
# Remove underscore from color names starting with '_'
modified_lines = [color[1:] if color.startswith('_') else color for color in colors.split('\n')]
# Remove duplicate colors and sort the colors alphabetically
colors = '\n'.join(sorted(list(set(modified_lines))))

with open('nicegui/color.py', 'w') as f:
    f.write(colors)
