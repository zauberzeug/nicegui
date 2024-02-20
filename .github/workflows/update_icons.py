import json

import requests

# Define a dictionary mapping numbers to their word representations.
number_words = {
    '10K': 'TEN_K',
    '10MP': 'TEN_MP',
    '11MP': 'ELEVEN_MP',
    '123': 'ONE_TWO_THREE',
    '12MP': 'TWELVE_MP',
    '13MP': 'THIRTEEN_MP',
    '14MP': 'FOURTEEN_MP',
    '15MP': 'FIFTEEN_MP',
    '16MP': 'SIXTEEN_MP',
    '17MP': 'SEVENTEEN_MP',
    '18_UP_RATING': 'EIGHTEEN_UP_RATING',
    '18MP': 'EIGHTEEN_MP',
    '19MP': 'NINETEEN_MP',
    '1K': 'ONE_K',
    '1K_PLUS': 'ONE_K_PLUS',
    '1X_MOBILEDATA': 'ONE_X_MOBILEDATA',
    '1X_MOBILEDATA_BADGE': 'ONE_X_MOBILEDATA_BADGE',
    '20MP': 'TWENTY_MP',
    '21MP': 'TWENTY_ONE_MP',
    '22MP': 'TWENTY_TWO_MP',
    '23MP': 'TWENTY_THREE_MP',
    '24MP': 'TWENTY_FOUR_MP',
    '2D': 'TWO_D',
    '2K': 'TWO_K',
    '2K_PLUS': 'TWO_K_PLUS',
    '2MP': 'TWO_MP',
    '30FPS': 'THIRTY_FPS',
    '30FPS_SELECT': 'THIRTY_FPS_SELECT',
    '360': 'THREE_SIXTY',
    '3D_ROTATION': 'THREE_D_ROTATION',
    '3G_MOBILEDATA': 'THREE_G_MOBILEDATA',
    '3G_MOBILEDATA_BADGE': 'THREE_G_MOBILEDATA_BADGE',
    '3K': 'THREE_K',
    '3K_PLUS': 'THREE_K_PLUS',
    '3MP': 'THREE_MP',
    '3P': 'THREE_P',
    '4G_MOBILEDATA': 'FOUR_G_MOBILEDATA',
    '4G_MOBILEDATA_BADGE': 'FOUR_G_MOBILEDATA_BADGE',
    '4G_PLUS_MOBILEDATA': 'FOUR_G_PLUS_MOBILEDATA',
    '4K': 'FOUR_K',
    '4K_PLUS': 'FOUR_K_PLUS',
    '4MP': 'FOUR_MP',
    '50MP': 'FIFTY_MP',
    '5G': 'FIVE_G',
    '5G_MOBILEDATA_BADGE': 'FIVE_G_MOBILEDATA_BADGE',
    '5K': 'FIVE_K',
    '5K_PLUS': 'FIVE_K_PLUS',
    '5MP': 'FIVE_MP',
    '60FPS': 'SIXTY_FPS',
    '60FPS_SELECT': 'SIXTY_FPS_SELECT',
    '6_FT_APART': 'SIX_FT_APART',
    '6K': 'SIX_K',
    '6K_PLUS': 'SIX_K_PLUS',
    '6MP': 'SIX_MP',
    '7K': 'SEVEN_K',
    '7K_PLUS': 'SEVEN_K_PLUS',
    '7MP': 'SEVEN_MP',
    '8K': 'EIGHT_K',
    '8K_PLUS': 'EIGHT_K_PLUS',
    '8MP': 'EIGHT_MP',
    '9K': 'NINE_K',
    '9K_PLUS': 'NINE_K_PLUS',
    '9MP': 'NINE_MP',
    '0_CIRCLE_FILL': 'CERO_CIRCLE_FILL',
    '0_CIRCLE': 'CERO_CIRCLE',
    '0_SQUARE_FILL': 'CERO_SQUARE_FILL',
    '0_SQUARE': 'CERO_SQUARE',
    '1_CIRCLE_FILL': 'ONE_CIRCLE_FILL',
    '1_CIRCLE': 'ONE_CIRCLE',
    '1_SQUARE_FILL': 'ONE_SQUARE_FILL',
    '1_SQUARE': 'ONE_SQUARE',
    '2_CIRCLE_FILL': 'TWO_CIRCLE_FILL',
    '2_CIRCLE': 'TWO_CIRCLE',
    '2_SQUARE_FILL': 'TWO_SQUARE_FILL',
    '2_SQUARE': 'TWO_SQUARE',
    '3_CIRCLE_FILL': 'THREE_CIRCLE_FILL',
    '3_CIRCLE': 'THREE_CIRCLE',
    '3_SQUARE_FILL': 'THREE_SQUARE_FILL',
    '3_SQUARE': 'THREE_SQUARE',
    '4_CIRCLE_FILL': 'FOUR_CIRCLE_FILL',
    '4_CIRCLE': 'FOUR_CIRCLE',
    '4_SQUARE_FILL': 'FOUR_SQUARE_FILL',
    '4_SQUARE': 'FOUR_SQUARE',
    '5_CIRCLE_FILL': 'FIVE_CIRCLE_FILL',
    '5_CIRCLE': 'FIVE_CIRCLE',
    '5_SQUARE_FILL': 'FIVE_SQUARE_FILL',
    '5_SQUARE': 'FIVE_SQUARE',
    '6_CIRCLE_FILL': 'SIX_CIRCLE_FILL',
    '6_CIRCLE': 'SIX_CIRCLE',
    '6_SQUARE_FILL': 'SIX_SQUARE_FILL',
    '6_SQUARE': 'SIX_SQUARE',
    '7_CIRCLE_FILL': 'SEVEN_CIRCLE_FILL',
    '7_CIRCLE': 'SEVEN_CIRCLE',
    '7_SQUARE_FILL': 'SEVEN_SQUARE_FILL',
    '7_SQUARE': 'SEVEN_SQUARE',
    '8_CIRCLE_FILL': 'EIGHT_CIRCLE_FILL',
    '8_CIRCLE': 'EIGHT_CIRCLE',
    '8_SQUARE_FILL': 'EIGHT_SQUARE_FILL',
    '8_SQUARE': 'EIGHT_SQUARE',
    '9_CIRCLE_FILL': 'NINE_CIRCLE_FILL',
    '9_CIRCLE': 'NINE_CIRCLE',
    '9_SQUARE_FILL': 'NINE_SQUARE_FILL',
    '9_SQUARE': 'NINE_SQUARE',
}


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

    for icon in response['icons']:
        icon_name = str(icon['name']).upper()
        icon_value = str(icon['name'])

        if icon_name in number_words:
            icons += f'{number_words[icon_name]} = "{icon_value}"\n'
        else:
            icons += f'{icon_name} = "{icon_value}"\n'

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

        if icon_name in number_words:
            icons += f'{number_words[icon_name]} = "{icon_value}"\n'
        else:
            icons += f'{icon_name} = "{icon_value}"\n'

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
