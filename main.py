import os
import requests
from dotenv import load_dotenv
import openai
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import pandas as pd
import uuid

load_dotenv()

qdrant = QdrantClient(host="localhost", port=6333)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

openai.api_key = OPENAI_API_KEY

# Naziv kolekcije
collection_name = "proizvodi"

# Učitaj Excel
excel_path = "proizvodi.xlsx"  # <-- promijeni naziv datoteke po potrebi
df = pd.read_excel(excel_path)

# Provjera stupaca
required_columns = {"id", "description"}
if not required_columns.issubset(set(df.columns)):
    raise ValueError(f"Excel mora sadržavati stupce: {required_columns}")

# (Re)kreiraj kolekciju
if not qdrant.collection_exists("proizvodi"):
    qdrant.create_collection(
        collection_name="proizvodi",
        vectors_config={
            "size": 1536,
            "distance": "Cosine"
        }
    )
else:
    print("Kolekcija 'proizvodi' već postoji.")

# Funkcija za dobivanje embeddinga
def get_embedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Generiraj embeddinge i upiši u Qdrant
points = []
for _, row in df.iterrows():
    opis = f"{row['id']}. {row['description']}"
    embedding = get_embedding(opis)
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={
            "id": str(row["id"]),
            "description": row["description"]
        }
    )
    points.append(point)

# Upis u kolekciju
#qdrant.upsert(collection_name=collection_name, points=points)

#print("✅ Uspješno upisano u Qdrant.")

query_text = "Oprema za hladno i vjetrovito vrijeme"
query_vector = get_embedding(query_text)

results = qdrant.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=1
)

for r in results:
    print(r.payload["id"], "-", r.payload["description"])
    
products = [
  {"id": "1", "name": "Vjetrovka", "description": "Lagana jakna otporna na vjetar, idealna za vjetrovito vrijeme."},
  {"id": "2", "name": "Kišobran", "description": "Sklopivi kišobran za kišne dane."},
  {"id": "3", "name": "Sunčane naočale", "description": "Zaštita očiju tijekom sunčanog vremena."},
  {"id": "4", "name": "Termos boca", "description": "Za držanje toplih napitaka po hladnom vremenu."},
  {"id": "5", "name": "Kapa", "description": "Topla kapa za hladne zimske dane."},
  {"id": "6", "name": "Ljetna haljina", "description": "Lagani materijal, savršeno za tople dane."},
  {"id": "7", "name": "Rukavice", "description": "Tople vunene rukavice za zimske dane."},
  {"id": "8", "name": "Boca za vodu", "description": "Prijenosna boca za hidrataciju tijekom vježbanja."},
  {"id": "9", "name": "Planinarske čarape", "description": "Deblje čarape za duge šetnje u prirodi."},
  {"id": "10", "name": "Šal", "description": "Mekani šal za hladnije dane."},
  {"id": "11", "name": "Sportske tenisice", "description": "Idealne za svakodnevne aktivnosti i šetnje."},
  {"id": "12", "name": "Punjač za mobitel", "description": "Brzi punjač kompatibilan s većinom uređaja."},
  {"id": "13", "name": "Ruksak", "description": "Prostrani ruksak za školu ili izlete."},
  {"id": "14", "name": "LED svjetiljka", "description": "Džepna svjetiljka visoke svjetlosti."},
  {"id": "15", "name": "Sendvič sa šunkom", "description": "Svježe pripremljen sendvič sa šunkom i sirom."},
  {"id": "16", "name": "Jogurt s jagodom", "description": "Voćni jogurt s komadićima jagode."},
  {"id": "17", "name": "Kišna kabanica", "description": "Vodootporna kabanica za jake kiše."},
  {"id": "18", "name": "Bluetooth slušalice", "description": "Bežične slušalice s dugim trajanjem baterije."},
  {"id": "19", "name": "Topli čaj", "description": "Zeleni čaj s đumbirom za grijanje zimi."},
  {"id": "20", "name": "Krema za sunčanje", "description": "Zaštita kože od UV zračenja."},
  {"id": "21", "name": "Sandale", "description": "Otvorena obuća za vruće dane."},
  {"id": "22", "name": "Jakna s kapuljačom", "description": "Vodootporna jakna za promjenjivo vrijeme."},
  {"id": "23", "name": "Zimske čizme", "description": "Izolirane čizme za snijeg i led."},
  {"id": "24", "name": "Baterije AA", "description": "Pakiranje od 4 alkalne baterije."},
  {"id": "25", "name": "Dječji sokić", "description": "Voćni sok bez dodatnih šećera."},
  {"id": "26", "name": "Polo majica", "description": "Pamučna polo majica kratkih rukava."},
  {"id": "27", "name": "Sladoled od vanilije", "description": "Klasični okus u praktičnom pakiranju."},
  {"id": "28", "name": "Bežični miš", "description": "Ergonomski dizajn za ugodniji rad."},
  {"id": "29", "name": "Lopta za plažu", "description": "Šarena lopta za ljetne igre na plaži."},
  {"id": "30", "name": "Zobene pahuljice", "description": "Zdrav doručak bogat vlaknima."},
  {"id": "31", "name": "Pametni sat", "description": "Fitness funkcije i praćenje koraka."},
  {"id": "32", "name": "Kiseli krastavci", "description": "Tradicionalno ukiseljeni krastavci."},
  {"id": "33", "name": "Sunčani šešir", "description": "Široki obod za zaštitu od sunca."},
  {"id": "34", "name": "Zaštitna maska", "description": "Višekratna maska za lice."},
  {"id": "35", "name": "Vlažne maramice", "description": "Pakiranje od 20 komada."},
  {"id": "36", "name": "Planinarske hlače", "description": "Otporne na habanje i vremenske uvjete."},
  {"id": "37", "name": "Majica bez rukava", "description": "Idealna za ljetne temperature."},
  {"id": "38", "name": "Čokoladica", "description": "Mliječna čokolada s lješnjacima."},
  {"id": "39", "name": "Dekica", "description": "Mekana i topla dekica za kauč."},
  {"id": "40", "name": "Prijenosni ventilator", "description": "USB ventilator za vruće dane."},
  {"id": "41", "name": "Krema za ruke", "description": "Njega i zaštita kože zimi."},
  {"id": "42", "name": "Ribarska kapica", "description": "Za sunčane izlete i ribolov."},
  {"id": "43", "name": "Papuče", "description": "Udobne kućne papuče."},
  {"id": "44", "name": "Banana", "description": "Zrela banana – prirodni izvor energije."},
  {"id": "45", "name": "Mini hladnjak", "description": "Idealno za kampiranje ili ured."},
  {"id": "46", "name": "Punjiva baterija", "description": "Ekološki prihvatljivo punjenje uređaja."},
  {"id": "47", "name": "Topli napitak u limenci", "description": "Instant kakao za hladna jutra."},
  {"id": "48", "name": "Antibakterijski gel", "description": "Za dezinfekciju ruku u pokretu."},
  {"id": "49", "name": "Zimski kaput", "description": "Elegantni kaput s postavom."},
  {"id": "50", "name": "Voda u boci", "description": "0.5L prirodne izvorske vode."},
  {"id": "51", "name": "Proteinska pločica", "description": "Snack bogat proteinima."},
  {"id": "52", "name": "Kupaće gaće", "description": "Za plivanje i sunčanje."},
  {"id": "53", "name": "Šilterica", "description": "Zaštita od sunca i stila."},
  {"id": "54", "name": "Keks s čokoladom", "description": "Hrskavi keks s punjenjem."},
  {"id": "55", "name": "Topli šal", "description": "Vuneni šal za zimu."},
  {"id": "56", "name": "Kuhana jaja", "description": "Pakiranje od 2 tvrdo kuhana jaja."},
  {"id": "57", "name": "Čajnik", "description": "Za pripremu toplih napitaka kod kuće."},
  {"id": "58", "name": "Termalna deka", "description": "Zadržava toplinu zimi."},
  {"id": "59", "name": "Gumene čizme", "description": "Idealne za blatnjave dane."},
  {"id": "60", "name": "Četkica za zube", "description": "Mekana vlakna za osjetljive desni."},
  {"id": "61", "name": "Sunđer za suđe", "description": "Dvostrana upotreba za čišćenje."},
  {"id": "62", "name": "Pametni telefon", "description": "Srednji rang s dugom baterijom."},
  {"id": "63", "name": "Sapun", "description": "Prirodni sapun s mirisom lavande."},
  {"id": "64", "name": "Mliječni puding", "description": "S desertnim preljevom od karamele."},
  {"id": "65", "name": "Komplet čarapa", "description": "5 pari pamučnih čarapa."},
  {"id": "66", "name": "USB kabel", "description": "Kabel za punjenje i prijenos podataka."},
  {"id": "67", "name": "Voćna salata", "description": "Mješavina svježeg sezonskog voća."},
  {"id": "68", "name": "Sportska boca", "description": "Plastična boca s pipcem za trčanje."},
  {"id": "69", "name": "Zimski set odjeće", "description": "Kapa, rukavice i šal u kompletu."},
  {"id": "70", "name": "Sok od naranče", "description": "100% prirodni sok bez šećera."},
  {"id": "71", "name": "Maslac od kikirikija", "description": "Kremasti namaz s komadićima kikirikija."},
  {"id": "72", "name": "Granola mix", "description": "Mješavina zobi, orašastih plodova i suhog voća."},
  {"id": "73", "name": "Sunčani losion", "description": "Zaštita kože pri izlaganju suncu."},
  {"id": "74", "name": "Vodootporne slušalice", "description": "Idealne za aktivnosti na otvorenom."},
  {"id": "75", "name": "Mini kišobran", "description": "Stane u torbicu, idealan za iznenadne pljuskove."},
  {"id": "76", "name": "LED lampa", "description": "Noćna lampa s podešavanjem jačine."},
  {"id": "77", "name": "Biciklističke rukavice", "description": "Zaštita i udobnost tijekom vožnje."},
  {"id": "78", "name": "Tjestenina", "description": "Brza priprema i pun okus."},
  {"id": "79", "name": "Kišna jakna", "description": "Lagano i vodonepropusno rješenje."},
  {"id": "80", "name": "Med", "description": "Prirodni med iz lokalnog pčelinjaka."},
  {"id": "81", "name": "Zobeni keksi", "description": "Zdrava alternativa slasticama."},
  {"id": "82", "name": "Dezodorans", "description": "Svježina tijekom cijelog dana."},
  {"id": "83", "name": "Lubenica", "description": "Sočno i osvježavajuće ljetno voće."},
  {"id": "84", "name": "Sušene marelice", "description": "Prirodni snack bez dodanog šećera."},
  {"id": "85", "name": "Prijenosni punjač", "description": "Power bank za punjenje u pokretu."},
  {"id": "86", "name": "Zimska majica", "description": "Topla pamučna majica dugih rukava."},
  {"id": "87", "name": "Sjemenke suncokreta", "description": "Lagani i zdravi međuobrok."},
  {"id": "88", "name": "Električni grijač", "description": "Za brzo zagrijavanje prostorije."},
  {"id": "89", "name": "Voćni smoothie", "description": "Hranjivi napitak s prirodnim sastojcima."},
  {"id": "90", "name": "Termalna boca", "description": "Održava temperaturu napitka do 12h."},
  {"id": "91", "name": "Prozračne tenisice", "description": "Za sportske aktivnosti po toplom vremenu."},
  {"id": "92", "name": "Kapa s šiltom", "description": "Zaštita i stil tijekom ljeta."},
  {"id": "93", "name": "Čokoladni napitak", "description": "Instant napitak za sve uzraste."},
  {"id": "94", "name": "Čarape za planinarenje", "description": "Dodatno ojačane za duge rute."},
  {"id": "95", "name": "Keks s maslacem", "description": "Klasik za uz čaj ili kavu."},
  {"id": "96", "name": "Kava u kapsulama", "description": "Intenzivan okus za brz početak dana."},
  {"id": "97", "name": "Čaj od mente", "description": "Umirujući topli napitak."},
  {"id": "98", "name": "Multivitaminski sok", "description": "Obogaćen vitaminima i mineralima."},
  {"id": "99", "name": "Začini mix", "description": "Mješavina začina za kuhanje."},
  {"id": "100", "name": "Keks s voćem", "description": "Lagani desert za svaki dan."}
]

cities = [
    "Zagreb", "Split", "Rijeka", "Osijek", "Dubrovnik",
    "Vienna", "Berlin", "Paris", "Madrid", "Rome",
    "London", "Amsterdam", "Brussels", "Lisbon", "Prague",
    "Warsaw", "Budapest", "Copenhagen", "Oslo", "Stockholm",
    "Athens", "Dublin", "Helsinki", "Belgrade", "Sarajevo",
    "Skopje", "Podgorica", "Ljubljana", "Sofia", "Bucharest",
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa",
    "Mexico City", "Guadalajara", "Monterrey", "Lima", "Bogotá",
    "Buenos Aires", "Santiago", "São Paulo", "Rio de Janeiro", "Brasília",
    "Tokyo", "Osaka", "Kyoto", "Seoul", "Busan",
    "Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Hong Kong",
    "Bangkok", "Hanoi", "Ho Chi Minh City", "Jakarta", "Manila",
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
    "Istanbul", "Tehran", "Baghdad", "Riyadh", "Dubai",
    "Cairo", "Alexandria", "Johannesburg", "Cape Town", "Nairobi",
    "Sydney", "Melbourne", "Brisbane", "Perth", "Auckland",
    "Wellington", "Suva", "Reykjavik", "Tallinn", "Vilnius",
    "Riga", "Luxembourg", "Monaco", "San Marino", "Andorra la Vella",
    "Doha", "Kuwait City", "Manama", "Muscat", "Amman"
]

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=hr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def generate_weather_response(weather_data, city):
     
    if weather_data:
            prognoza = weather_data["weather"][0]["description"]
            temperatura = weather_data["main"]["temp"]
            vlaznost = weather_data["main"]["humidity"]
            vjetar_brzina = weather_data["wind"]["speed"]
            osjecaj = weather_data["main"]["feels_like"]
            tlak = weather_data["main"]["pressure"]
            vidljivost = weather_data.get("visibility", "N/A")
            oblaci = weather_data["clouds"]["all"]
            smjer_vjetra = weather_data["wind"].get("deg", "N/A")

    else:
            print(f"Nema podataka za {city}")
            results.append({"Grad": city, "Preporučeni proizvodi": "No weather data"})

    print(city, prognoza, temperatura, vlaznost, vjetar_brzina, osjecaj, tlak, vidljivost, oblaci, smjer_vjetra)

    #description = "sunny and 30 degrees celsius"

    baze={json.dumps(products, indent=2, ensure_ascii=False)}
    

    prompt = f"""Give me a product reccomendation using weather report for today {city}{prognoza}{temperatura}{vlaznost}{vjetar_brzina}{osjecaj}{tlak}{vidljivost}{oblaci}{smjer_vjetra}, degrees are in celsius, but do not mention the weather just recommend retail products that user could be interested in (food, electronics, clothes, cosmetics, beverages) based on the weather. Products must be diverse.Provide only product decription like this:
    - A soothing and hydrating gel with aloe vera extracts 
    - A compact and rechargeable fan
    - lightweight t-shirt Made from breathable fabric
   return JSON object with 5 relevant products.
    
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    results = []
    for city in cities:
        weather = get_weather(city)
        preporuka = generate_weather_response(weather, city)
        print(preporuka)
        print("-----")
        results.append({"Grad": city, "Preporučeni proizvodi": preporuka})