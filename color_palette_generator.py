import turtle
import random
import requests
from colorthief import ColorThief
from io import BytesIO
from config import BING_API_KEY, BING_SEARCH_URL

def get_image_url(query):
    """Fetch the first image URL from Bing Image Search API."""
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "count": 1}
    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    image_url = response.json()['value'][0]['contentUrl']
    return image_url

def get_palette_from_image_url(image_url):
    """Fetch image and extract color palette."""
    response = requests.get(image_url)
    img_data = BytesIO(response.content)
    color_thief = ColorThief(img_data)
    palette = color_thief.get_palette(color_count=5) 
    return palette

def draw_palette(palette):
    """Use Turtle to draw color palette as random dots."""
    turtle.bgcolor('black')
    turtle.colormode(255)
    turtle.speed(0)

    for color in palette * 20:
        turtle.pencolor(color)
        turtle.penup()
        turtle.goto(random.randint(-200, 200), random.randint(-200, 200))
        turtle.pendown()
        turtle.dot(random.randint(10, 50))
    
    print("Would you like to draw another palette? (y/n)")
    response = input()
    if response.lower() == 'y':
        main()
    else:
        print("Goodbye!")

def main():
    character = input("Enter a character and where they're from (e.g., 'Elsa from Frozen'): ")
    try:
        print("Searching for image...")
        image_url = get_image_url(character)
        print(f"Image found: {image_url}")

        print("Extracting color palette...")
        palette = get_palette_from_image_url(image_url)
        print(f"Palette: {palette}")

        print("Drawing color palette with turtle...")
        draw_palette(palette)

        print("Would you like to draw another palette? (y/n)")
        response = input()
        if response.lower() == 'y':
            main()
        else:
            turtle.hideturtle()
            turtle.done()
            print("Goodbye!")
            return

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
