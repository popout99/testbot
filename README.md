
# MapBan Bot 🎮

Discord bot do eliminacji map przez dwóch graczy.

## Komendy
- `/startmapban` — rozpoczyna eliminację map

## Funkcje
- Losuje gracza zaczynającego
- Kolejno usuwa mapy z listy aż zostanie jedna
- 30 sekund na wybór, przypomnienie po 20 sek
- Jeśli brak odpowiedzi — usuwa pierwszą z listy

## Uruchomienie lokalne
1. `pip install -r requirements.txt`
2. Dodaj token bota do zmiennej środowiskowej `DISCORD_TOKEN`
3. `python main.py`

## Hosting 24/7 na Render.com
1. Wgraj ten kod na GitHuba
2. Utwórz Web Service na [render.com](https://render.com)
3. Start command: `python3 main.py`
4. Dodaj zmienną `DISCORD_TOKEN` w środowisku

Gotowe!
