import os
import requests

def download_images(topic, num_images, api_key):
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    params = {
        "q": topic,
        "count": num_images,
        "imageType": "photo",
        "safeSearch": "Moderate"
    }

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    if not os.path.exists("test_images"):
        os.makedirs("test_images")

    image_urls = [img["contentUrl"] for img in search_results["value"]]
    for idx, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join("downloads", f"{topic}_{idx+1}.jpg"), "wb") as img_file:
                img_file.write(img_data)
            print(f"Downloaded {topic}_{idx+1}.jpg")
        except Exception as e:
            print(f"Could not download {img_url}: {e}")

    return image_urls

# Example usage
topic = "houses in the woods"
num_images = 5
api_key = "672e8e31cba34268872c1008c1ebae4b"  # Replace with your Bing API key
downloaded_images = download_images(topic, num_images, api_key)
print(f"Downloaded {len(downloaded_images)} images for the topic '{topic}'")
for image in downloaded_images:
    print(image)
