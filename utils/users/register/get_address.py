import requests


async def get_address(latitude, longitude) -> str:
    """
    Получает адрес и оборачивает в сообщения по градусам широты и долготы
    :param latitude: градус широты
    :param longitude: градус долготы
    :param user_id: user_id пользователя
    :return: Inline-keyboard, string
    """
    token = 'pk.11293f385d4a71bd2d7afa847cd031ed'
    headers = {"Accept-Language": "ru"}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={latitude}&lon={longitude}&format=json',
        headers=headers).json()
    return f"{address['address'].get('country')}, {address['address'].get('city')}, {address['address'].get('road')} {address['address'].get('house_number')}"
