import asyncio
import json
import re

from playwright.async_api import async_playwright


class BertusApiKeyFetcher:

    def __init__(self):
        asyncio.run(self.fetch_bertus_token())

    async def fetch_bertus_token(self):
        config_path = 'Resources/config.json'
        try:

            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        except FileNotFoundError as e:
            print('Configuration file not found! (Resources/config.py)')
            return None

        email = config.get('bertus_email')
        password = config.get('bertus_password')

        if not email or not password:
            print("Hiba: A bejelentkezési adatok hiányoznak a config.json-ból.")
            return None

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            print('Bertus felkeresése...')
            try:
                # Bejelentkezési oldal megnyitása
                await page.goto("https://myapi-portal.bertus.com/signin")
                print('Bejelentkezés...')
                # Bejelentkezési adatok kitöltése
                await page.fill('input[id="email"]', email)
                await page.fill('input[id="password"]', password)
                await page.click('button[id="signin"]')

                # Várakozás a bejelentkezésre
                await page.wait_for_url("https://myapi-portal.bertus.com/")
                print('Példa Api keresése...')
                # Navigálás az API tesztelő oldalra
                await page.goto(
                    "https://myapi-portal.bertus.com/api-details#api=mybertus-api-production&operation=Articles_Get")

                # "Try it" gomb megnyomása
                try:
                    try_it_button = await page.wait_for_selector('button:has-text("Try it")', timeout=10000)
                    await try_it_button.click()
                except:
                    # Ha már nyitva van a konzol
                    pass
                print('Auth Flow beállítása...')
                # Authorization flow beállítása implicit-re a token generálásához
                auth_flow_select = await page.wait_for_selector('select[id="authFlow"]')
                await auth_flow_select.select_option(index=1)  # implicit

                # Várakozás a token megjelenésére a DOM-ban
                # A token egy "Bearer ey..." kezdetű karakterlánc
                print('Token kinyerése...')
                token = None
                for _ in range(10):  # Többszöri próbálkozás
                    content = await page.content()
                    match = re.search(r'Bearer\s+(ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_=]*)', content)
                    if match:
                        token = match.group(0)
                        break
                    await asyncio.sleep(1)

                if token:
                    print(f"Sikeresen kinyert token: {token[:50]}...")

                    # Config frissítése
                    config['Authorization'] = token
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=4)

                    return token
                else:
                    print("Hiba: Nem sikerült megtalálni az Authorization tokent az oldalon.")
                    return None

            except Exception as e:
                print(f"Hiba történt az automatizálás során: {e}")
                return None
            finally:
                await browser.close()
