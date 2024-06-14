from concurrent.futures import ThreadPoolExecutor
import json
import random
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

places_data = {"places": []}

names = [
    "Café do Bairro",
    "Bella Café",
    "Café Aconchego",
    "Café Charmoso",
    "Café da Esquina",
    "Café das Artes",
    "Café com Carinho",
    "Café com Prosa",
    "Café dos Amigos",
    "Café do Dia",
    "Café e Cia",
    "Café Especial",
    "Café Expresso",
    "Café Saboroso",
    "Café Saudade",
    "Café Simpatia",
    "Café Sonhador",
    "Café Tentador",
    "Café Viver",
    "Café do Brasil",
    "Museu do Índio",
    "Museu do Imigrante",
    "Observatório",
    "Museu do Trem",
    "Museu Naval",
    "Museu do Café",
    "Museu do Homem do Nordeste",
    "Museu de Antropologia",
    "Museu de Geologia",
    "Museu de História",
    "Museu de Paleontologia",
    "Museu da Vida",
    "Museu da República",
    "Museu do Mar",
    "Museu Ferroviário",
    "Museu Histórico e Artístico",
    "Museu de Ciências e Tecnologia",
    "Museu de Arte Sacra",
    "Museu da Memória",
    "Museu da Revolução",
    "Museu de Zoologia",
    "Museu do Folclore",
    "Museu do Boi",
    "Museu do Carro",
    "Museu da Aviação",
    "Museu do Futebol Brasileiro",
    "Museu do Patrimônio Histórico",
    "Museu do Patrimônio Cultural",
    "Museu da Herança",
    "Shopping Westfield",
    "Shopping of America",
    "Shopping The Dubai",
    "Shopping West Edmonton",
    "Shopping of the Emirates",
    "Shopping Paragon",
    "Shopping SM of Asia",
    "Berjaya Times Shopping Square",
    "Shopping CentralWorld",
    "The Shopping Galleria",
    "Chadstone Shopping Shopping Centre",
    "Tokyo Shopping Midtown",
    "Grand Shopping Indonesia",
    "ABC Shopping Achrafieh",
    "King of Shopping Prussia",
    "South Coast Shopping Plaza",
    "Shopping Malha",
    "Canal Walk Shopping Shopping Centre",
    "Shopping VivoCity",
    "Westfield Stratford Shopping City",
    "Festa das Cores",
    "Festa da Alegria",
    "Festa Tropical",
    "Festa no Céu",
    "Festa do Luau",
    "Festa dos Sonhos",
    "Festa da Fantasia",
    "Festa do Pijama",
    "Festa da Amizade",
    "Festa do Brilho",
    "Festa das Estrelas",
    "Festa das Flores",
    "Festa do Sorriso",
    "Festa da Música",
    "Festa da Dança",
    "Festa da Lua Cheia",
    "Festa da Primavera",
    "Festa do Verão",
    "Festa do Carnaval",
    "Festa do Ano Novo",
    "Rock Arena",
    "Rock Star Lounge",
    "Rock Metalhead Tavern",
    "Rock Heavy Metal Hangout",
    "Rock Rockabilly Joint",
    "Rock The Blues Basement Rock Band",
    "Rock The Rockers",
    "Rock Rebellion",
    "Rock Electric Avenue",
    "Rock Guitar Gods' Den",
    "Rock Punk Paradise",
    "Rock Alternative Alley",
    "Rock Rock Riot",
    "Rock Grungy Garage",
    "Rock Funkadelic Fort",
    "Rock Soulful Stage",
    "Rock Hard Rock Haven",
    "Rock Thrash Thrive",
    "Rock Psychedelic Pitstop",
    "Rock Indie Inn",
    "Rock Bluesy Boulevard",
    "Rock Riff Rendezvous",
    "Rock Jamming Junction",
    "Rock Rock Reservoir",
    "Rock Metal Mayhem",
    "Igreja da Graça Divina",
    "Igreja da Esperança Renovada",
    "Igreja do Sagrado Coração",
    "Igreja da Comunhão Fraternal",
    "Igreja da Nova Aliança",
    "Igreja da Renovação Espiritual",
    "Igreja do Evangelho Eterno",
    "Igreja do Amor Infinito",
    "Igreja do Caminho Verdadeiro",
    "Igreja do Divino Salvador",
    "Igreja do Amor Fraternal",
    "Igreja do Perdão Divino",
    "Igreja da Fé Inabalável",
    "Igreja da Salvação Eterna",
    "Igreja da Luz Celestial",
    "Galeria do Rock",
    "Galeria de Arte Moderna",
    "Galeria dos Artistas",
    "Galeria Vanguarda",
    "Galeria Contemporânea",
    "Galeria Expressão",
    "Galeria da Criatividade",
    "Galeria das Cores",
    "Galeria Urbana",
    "Galeria Arte Viva",
    "Galeria Cultural",
    "Galeria da Vanguarda",
    "Galeria da Inovação",
    "Galeria das Ideias",
    "Galeria dos Sonhos",
    "Galeria dos Mestres",
    "Galeria da Alma",
    "Galeria da Luz",
    "Galeria dos Ventos",
    "Galeria dos Sentidos",
    "Galeria do Olhar",
    "Galeria das Estrelas",
    "Galeria da Inspiração",
    "Galeria dos Momentos",
    "Galeria da Harmonia",
    "Academia BodyFit",
    "Academia PowerHouse",
    "Academia IronWorks",
    "Academia FitZone",
    "Academia Fitness Plus",
    "Academia ShapeUp",
    "Academia BodyStrong",
    "Academia MuscleMax",
    "Academia EliteFit",
    "Academia PowerFlex",
    "Academia IronGym",
    "Academia FitPro",
    "Academia BodyPump",
    "Academia MuscleMania",
    "Academia CoreZone",
    "Academia FitnessFusion",
    "Academia FlexFit",
    "Academia StrengthCamp",
    "Academia BodyTech",
    "Academia PowerLift",
    "Academia IronClad",
    "Academia FitForce",
    "Academia BodyBlast",
    "Academia MuscleFactory",
    "Academia FlexGym",
    "Zoológico WildLife",
    "Zoológico JungleLand",
    "Zoológico SafariWorld",
    "Zoológico NaturePark",
    "Zoológico Animalia",
    "Zoológico ZooHaven",
    "Zoológico FaunaPark",
    "Zoológico SafariZone",
    "Zoológico WildlifeReserve",
    "Zoológico ZooQuest",
    "Zoológico WildKingdom",
    "Zoológico SafariScape",
    "Zoológico NatureReserve",
    "Zoológico ZooVista",
    "Zoológico FaunaValley",
    "Metal Forge",
    "Metal Mania",
    "Metallica Haven",
    "Metal Masters",
    "Metal Mayhem",
    "Metal Kingdom",
    "Metal Militia",
    "Metal Works",
    "Metal Meltdown",
    "Metal Madness",
    "Metal Empire",
    "Metallica Frontier",
    "Metal Mountain",
    "Metal Mashup",
    "Metal Madness",
    "Parque da Floresta",
    "Parque das Águas",
    "Parque da Cidade",
    "Parque da Aventura",
    "Parque da Vida",
    "Parque das Rosas",
    "Parque da Paz",
    "Parque da Diversão",
    "Parque das Estrelas",
    "Parque dos Sonhos",
    "Parque da Serenidade",
    "Parque da Juventude",
    "Parque da Imaginação",
    "Parque das Cores",
    "Parque da Harmonia",
    "Parque da Liberdade",
    "Parque da Felicidade",
    "Parque das Maravilhas",
    "Parque da Amizade",
    "Parque das Crianças",
    "Parque da Beleza",
    "Parque da Sabedoria",
    "Parque da Fantasia",
    "Parque da Seriedade",
    "Parque da Diversidade",
]

locations = [
    "São Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Brasília",
    "Salvador",
    "Fortaleza",
    "Curitiba",
    "Manaus",
    "Recife",
    "Belém",
    "Porto Alegre",
    "Goiânia",
    "Guarulhos",
    "Campinas",
    "São Luís",
    "São Gonçalo",
    "Maceió",
    "Duque de Caxias",
    "Natal",
    "Campo Grande",
    "Teresina",
    "São Bernardo do Campo",
    "Nova Iguaçu",
    "João Pessoa",
    "Santo André",
    "Osasco",
    "Jaboatão dos Guararapes",
    "Ribeirão Preto",
    "Uberlândia",
    "Contagem",
    "Sorocaba",
    "Aracaju",
    "Feira de Santana",
    "Cuiabá",
    "Joinville",
    "Aparecida de Goiânia",
    "Londrina",
    "Ananindeua",
    "Niterói",
    "Porto Velho",
    "Campos dos Goytacazes",
    "Mauá",
    "São José dos Campos",
    "Santos",
    "Diadema",
    "Mogi das Cruzes",
    "Betim",
    "Jundiaí",
    "Caxias do Sul",
    "Florianópolis",
    "Macapá",
    "Canoas",
    "Bauru",
    "Vitória",
    "São Vicente",
    "Pelotas",
    "Franca",
    "Blumenau",
    "Ponta Grossa",
    "Petrolina",
    "Campina Grande",
    "Boa Vista",
    "Piracicaba",
    "Montes Claros",
    "Rio Branco",
    "Santarém",
    "Cascavel",
    "Hortolândia",
    "Rondonópolis",
    "Palmas",
    "Várzea Grande",
    "Marabá",
    "Itaquaquecetuba",
    "Maringá",
    "Anápolis",
    "Barueri",
    "Vila Velha",
    "Volta Redonda",
    "Santa Maria",
    "Suzano",
    "Sete Lagoas",
    "Divinópolis",
    "Caruaru",
    "Ibirité",
    "Criciúma",
    "São José do Rio Preto",
    "Colombo",
    "Limeira",
    "Teófilo Otoni",
    "Sinop",
    "Itabuna",
    "Governador Valadares",
    "Marília",
    "Ipatinga",
    "Taboão da Serra",
    "Petrópolis",
    "Vitória da Conquista",
    "Sobral",
    "Indaiatuba",
    "Mossoró",
    "Cachoeiro de Itapemirim",
]


def get_image_url(place_name):
    search_url = "https://www.bing.com/images/search"
    params = {"q": place_name, "FORM": "HDRSC2"}
    response = requests.get(search_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    img_tag = soup.find("a", class_="iusc")
    if img_tag:
        img_url = img_tag.get("m")
        img_url = img_url.split('"murl":"')[1].split('"')[0]
        return img_url
    return None


def generate(i):
    name = names[i]
    return {
        "place_id": str(i),
        "name": name,
        "location": random.choice(locations),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "likes": random.randint(50, 1000),
        "image": get_image_url(name)
        or "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTw_HeSzHfBorKS4muw4IIeVvvRgnhyO8Gn8w&s",
    }


import concurrent.futures

with ThreadPoolExecutor(max_workers=16) as executor:
    f = {executor.submit(generate, i): i for i in tqdm(range(len(names)))}

    for future in concurrent.futures.as_completed(f):
        data = f[future]
        try:
            data = future.result()
            places_data["places"].append(data)
        except Exception as exc:
            print("%r generated an exception: %s" % (data, exc))

        with open("model/data/places.json", "w", encoding="utf-8") as file:
            json_data = json.dumps(places_data, indent=2, ensure_ascii=False)
            file.write(json_data)