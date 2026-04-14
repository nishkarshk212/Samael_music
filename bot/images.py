import os
import aiohttp
import random

# Base directory for assets
ASSETS_DIR = "downloads/assets"

class Images:
    # All 10 image URLs provided by the user
    ALL_IMAGE_URLS = [
        "https://i.ibb.co/CsvZ6LLN/anime-girl-kimono-misty-lake.jpg",
        "https://i.ibb.co/QF9skDj5/anime-girl-plays-guitar-by-water-night.jpg",
        "https://i.ibb.co/chFbdsnN/anime-style-couple-characters-with-fire.jpg",
        "https://i.ibb.co/rKMFy85W/boy-his-dog-beach-sunset.jpg",
        "https://i.ibb.co/PZ6w8vqF/illustration-anime-city.jpg",
        "https://i.ibb.co/rBzGsW4/anime-moon-landscape.jpg",
        "https://i.ibb.co/0pY5QDQ9/anime-character-traveling-2.jpg",
        "https://i.ibb.co/Jw7J8ByP/anime-girl-kimono-bamboo-forest.jpg",
        "https://i.ibb.co/gZRKshjV/anime-girl-rock-by-river-autumn-sunset-scenery.jpg",
        "https://i.ibb.co/DfzvHXx1/anime-landscape-person-traveling.jpg"
    ]
    
    PLAY_IMAGE_URL = "https://picsur.org/i/6c125539-06a3-48cb-9d9c-6728ce99eb02.jpg"
    QUEUE_IMAGE_URL = "https://picsur.org/i/1e8f8dd5-b815-4002-8ca0-916f1d2cd710.jpg"
    PING_IMAGE_URL = "https://picsur.org/i/caf5c9cc-f2eb-43e1-be03-f51991d788c3.jpg"

    # Local Paths
    ALL_IMAGES_LOCAL = [f"{ASSETS_DIR}/asset_{i}.jpg" for i in range(len(ALL_IMAGE_URLS))]
    PLAY_IMAGE = f"{ASSETS_DIR}/play.jpg"
    QUEUE_IMAGE = f"{ASSETS_DIR}/queue.jpg"
    PING_IMAGE = f"{ASSETS_DIR}/ping.jpg"

    @classmethod
    async def download_all(cls):
        """
        Downloads all asset images to local storage to avoid WEBPAGE_CURL_FAILED.
        """
        os.makedirs(ASSETS_DIR, exist_ok=True)
        
        mapping = {
            cls.PLAY_IMAGE_URL: cls.PLAY_IMAGE,
            cls.QUEUE_IMAGE_URL: cls.QUEUE_IMAGE,
            cls.PING_IMAGE_URL: cls.PING_IMAGE
        }
        
        # Add all start/general images to the download mapping
        for url, path in zip(cls.ALL_IMAGE_URLS, cls.ALL_IMAGES_LOCAL):
            mapping[url] = path
        
        async with aiohttp.ClientSession() as session:
            for url, path in mapping.items():
                if not os.path.exists(path):
                    try:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                with open(path, "wb") as f:
                                    f.write(await resp.read())
                                print(f"Downloaded asset: {path}")
                    except Exception as e:
                        print(f"Failed to download asset {url}: {e}")
        
        return True

    @classmethod
    def get_random_image(cls):
        """Returns a random image from the local ones that exist."""
        existing_images = [p for p in cls.ALL_IMAGES_LOCAL if os.path.exists(p)]
        if existing_images:
            return random.choice(existing_images)
        # Fallback to a random URL if none downloaded yet
        return random.choice(cls.ALL_IMAGE_URLS)

    @classmethod
    def get_start_image(cls):
        return cls.get_random_image()

    @classmethod
    def get_play_image(cls):
        return cls.get_random_image()

    @classmethod
    def get_queue_image(cls):
        return cls.get_random_image()

    @classmethod
    def get_ping_image(cls):
        return cls.get_random_image()
        
    @classmethod
    def get_help_image(cls):
        return cls.get_random_image()
