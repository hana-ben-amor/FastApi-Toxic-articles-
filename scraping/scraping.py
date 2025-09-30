import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["articles_db"]
collection = db["articles"]
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


#OK
def scrape_humanite():
    base = "https://www.humanite.fr"
    articles = []

    # parcourir les pages 1 à 15
    for page in range(1, 16):
        url = f"{base}/sections/monde?page={page}"
        resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code != 200:
            print(f"⚠️ Erreur {resp.status_code} sur {url}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # trouver tous les articles
        for art in soup.find_all("article", class_="article-card"):
            # titre
            h2 = art.find("h2", class_="article-card__title")
            # lien
            a = art.find("a")

            if h2 and a:
                title = h2.get_text(strip=True)
                href = urljoin(base, a.get("href"))
                articles.append({
                    "source": "humanite",
                    "url": href,
                    "title": title
                })

        print(f"Page {page} : {len(articles)} articles cumulés")

    return articles
#OK
def scrape_gamespot():
    base = "https://www.gamespot.com"
    resp = requests.get(base, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []
    # Exemple : les articles sur Gamespot ont souvent href de la forme "/news/..." ou "/reviews/..."
    for a in soup.select("a[href^='/news'], a[href^='/reviews'], a[href^='/articles']"):
        href = a.get("href")
        title = a.get_text(strip=True)
        if href and title:
            href = urljoin(base, href)
            articles.append({"source": "gamespot", "url": href, "title": title})
    return articles
#OK 
def scrape_marianne(max_pages=200):
    base = "https://www.marianne.net"
    section = "/monde"
    articles = []

    for page in range(1, max_pages + 1):
        url = f"{base}{section}"
        if page > 1:
            url += f"?p={page}"

        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"Erreur {resp.status_code} sur {url}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Chaque article est dans <h3 class="thumbnail__title"><a class="thumbnail__link">
        for art in soup.find_all("h3", class_="thumbnail__title"):
            a = art.find("a", class_="thumbnail__link")
            if a:
                href = urljoin(base, a.get("href"))
                title = a.get_text(strip=True)
                articles.append({
                    "source": "marianne",
                    "url": href,
                    "title": title
                })

    return articles

#OK
def scrape_lemonde(pages=2):
    base = "https://www.lemonde.fr"
    section = "international"
    articles = []

    for page in range(1, pages + 1):
        if page == 1:
            url = f"{base}/{section}/"
        else:
            url = f"{base}/{section}/{page}"

        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"Erreur {resp.status_code} sur {url}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Chaque article est dans <a class="teaser__link">
        for a in soup.find_all("a", class_="teaser__link"):
            title_tag = a.find("h3", class_="teaser__title")
            if title_tag:
                href = urljoin(base, a.get("href"))
                title = title_tag.get_text(strip=True)
                articles.append({
                    "source": "lemonde",
                    "url": href,
                    "title": title
                })

    return articles

#OK
def scrape_france24():
    base = "https://www.france24.com"
    resp = requests.get(base + "/fr/", headers=headers, timeout=15)
    print("Status:", resp.status_code)

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []

    # 1) Avec find_all
    for div in soup.find_all("div", class_="article__title"):
        a = div.find("a")  # premier <a>
        h2 = div.find("h2")  # le titre
        if a and h2:
            href = urljoin(base, a.get("href"))
            title = h2.get_text(strip=True)
            articles.append({"source": "france24", "url": href, "title": title})

    return articles

#OK
def scrape_france3_regions(pages=10):
    base = "https://www.franceinfo.fr"
    articles = []

    for page in range(1, pages + 1):
        if page == 1:
            url = f"{base}/monde/"
        else:
            url = f"{base}/monde/{page}.html"

        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"Erreur {resp.status_code} sur {url}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Chaque article est dans <article class="card-article-list-l">
        for art in soup.find_all("article", class_="card-article-list-l"):
            a = art.find("a", class_="card-article-list-l__link")
            title_tag = art.find("p", class_="card-article-list-l__title")
            if a and title_tag:
                href = urljoin(base, a.get("href"))
                title = title_tag.get_text(strip=True)
                articles.append({
                    "source": "franceinfo",
                    "url": href,
                    "title": title
                })

    return articles

#OK
def scrape_mediacites(max_pages=134):
    base = "https://www.mediacites.fr/category/breve/"
    articles = []

    for page in range(1, max_pages + 1):
        if page == 1:
            url = base
        else:
            url = f"{base}page/{page}/"

        print(f"[Scraping] Page {page} -> {url}")
        resp = requests.get(url, headers=headers, timeout=15, proxies=None)

        if resp.status_code != 200:
            print(f"Erreur {resp.status_code} sur {url}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        container = soup.find("div", class_="mediacites-article-list")
        if not container:
            print(f"Pas trouvé de bloc article sur {url}")
            break

        for art in container.find_all("article"):
            h2 = art.find("h2", class_="title")
            if h2:
                a = h2.find("a")
                if a:
                    href = a.get("href")
                    title = a.get_text(strip=True)
                    articles.append({
                        "source": "mediacites",
                        "url": href,
                        "title": title
                    })

    return articles
#OK
def scrape_lepoint():
    base = "https://www.lepoint.fr/24h-infos/"
    resp = requests.get(base, headers=headers, timeout=15)
    print("Status:", resp.status_code)

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []

    # Trouver tous les blocs <article class="full-click">
    for art in soup.find_all("article", class_="full-click"):
        a = art.find("a")
        h2 = art.find("h2")
        if a and h2:
            href = urljoin(base, a.get("href"))
            title = h2.get_text(strip=True)
            articles.append({
                "source": "lepoint",
                "url": href,
                "title": title
            })

    return articles

# -------- SCRAPER CONTENU D'UN ARTICLE --------
def get_article_content(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Récupérer tous les <p> (paragraphe)
        content = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])
        return content
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return ""
scrapers = [
    # scrape_humanite,
    # scrape_gamespot,
    # scrape_marianne,
    # scrape_lemonde,
    # scrape_france24,
    scrape_france3_regions,
    scrape_mediacites,
    scrape_lepoint
]

all_articles = []

for scraper in scrapers:
    try:
        print(f"Scraping {scraper.__name__} ...")
        site_articles = scraper()
        print(f" {len(site_articles)} articles trouvés via {scraper.__name__}")

        for art in site_articles:
            # Ajouter le contenu de l'article
            art["content"] = get_article_content(art["url"])

            # Vérifier doublons avant insertion
            if not collection.find_one({"url": art["url"]}):
                collection.insert_one(art)
                all_articles.append(art)

    except Exception as e:
        print(f"Erreur avec {scraper.__name__}: {e}")

print(f"\n Total {len(all_articles)} nouveaux articles insérés dans MongoDB.")