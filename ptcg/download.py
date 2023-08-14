import requests


count = 8734

while count <= 8804:
    print(count)
    
    url = ("https://asia.pokemon-card.com/hk/card-img/hk0000{}.png").format(count)  # Replace with the URL of the image you want to download
    filename = ("hk0000{}.png").format(count)  # Replace with the desired filename for the downloaded image
    # https://asia.pokemon-card.com/hk/card-img/hk00008867.png
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)
    count += 1

print("Image downloaded successfully!")