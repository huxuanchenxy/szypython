import requests


count = 155

while count <= 166:
    print(count)
    
    # url = ("https://tcg.pokemon.com/assets/img/expansions/lost-origin/cards/en-us/SWSH11_EN_TG_{}-2x.jpg").format(count)  # Replace with the URL of the image you want to download
    # url = ("https://asia.pokemon-card.com/hk/card-img/hk0000{}.png").format(count) 
    url = ("https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SSP/SSP_{}_R_EN.png").format(count) 
    
    filename = ("SSP_{}_R_EN.png").format(count)  # Replace with the desired filename for the downloaded image
    # https://asia.pokemon-card.com/hk/card-img/hk00008867.png
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)
    count += 1

print("Image downloaded successfully!")