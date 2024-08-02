from SPARQLWrapper import SPARQLWrapper, JSON
from functools import reduce

#set endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql") 

#set query
sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
SELECT DISTINCT ?city ?country ?population ?capital
   WHERE {
       ?city_uri a dbo:City;
                 rdfs:label ?city;
                 dbo:populationTotal ?population;
                 dbo:country ?country_uri.
       ?country_uri rdfs:label ?country;
                    dbo:capital ?capital_uri.
       ?capital_uri rdfs:label ?capital.
       FILTER ((lang(?city) = 'en') && (lang(?country) = 'en') && (lang(?capital) = 'en'))
  } 
  ORDER BY DESC(?population) ?city
""")

#set return format to JSON
sparql.setReturnFormat(JSON) 

# execute query and returns result in JSON format
results = sparql.query().convert() 

def getRes(resDcit):
  VALUES = resDcit['results']['bindings']
  return list( map ( lambda item: dict( 
                     map ( lambda key: (key, item[key]['value']) 
                           , item.keys() )
             ) , VALUES) )

# Verifica se a substring é parte da string
substring = lambda string, sub: sub in string

# Verificar se uma cidade é uma megacidade
def megacidade(cities, cidade=None):
    if cidade is None:
        # Retorna todas as megacidades
        return list(filter(lambda c: int(c["population"]) > 10000000, cities))
    # Retorna se a cidade específica é uma megacidade
    return any(filter(lambda c: c["city"] == cidade and int(c["population"]) > 10000000, cities))

# Verificar se uma cidade é uma metropole
def metropole(cities, cidade=None):
    if cidade is None:
        # Retorna todas as metrópoles
        return list(filter(lambda c: 1000000 < int(c["population"]) < 10000000, cities))
    # Retorna se a cidade específica é uma metrópole
    return any(filter(lambda c: c["city"] == cidade and 1000000 < int(c["population"]) < 10000000, cities))

# Encontrar todas as cidades que contêm uma determinada substring
def cidades_busca(cities, busca=None, country=None):
    if busca is None:
        # Retorna todas as cidades
        return cities
    # Retorna as cidades que contêm a substring
    elif country is not None:
        return list(filter(lambda c: substring(c["city"], busca) and c["country"] == country, cities))
    return list(filter(lambda c: substring(c["city"], busca), cities))

# Encontrar todas as cidades que começam com uma determinada letra
def cidades_letra(cities, letra=None):
    if letra is None:
        # Retorna todas as cidades
        return cities
    # Retorna as cidades que começam com a letra
    return list(map(lambda c: c["city"], filter(lambda c: c["city"].startswith(letra), cities)))

# Encontrar a população total de um país
def populacao_total(cities, country=None):
    if country is None:
        # Retorna a população total de todos os países/cidades
        return reduce(lambda acc, c: acc + int(c["population"]), cities, 0)
    # Retorna a população total de um país específico
    return reduce(lambda acc, c: acc + int(c["population"]), filter(lambda c: c["country"] == country, cities), 0)

# Encontrar todas as cidades de um país
def list_cidades_pais(cities, country=None):
    if country is None:
        # Retorna todas as cidades
        return cities
    # Retorna todas as cidades de um país específico
    return list(map(lambda c: c["city"], filter(lambda c: c["country"] == country, cities)))

# Contar quantas metropoles existem em um país
def contar_metropoles(cities, country=None):
    if country is None:
        # Retorna a contagem de metrópoles em todos os países
        return len(list(filter(lambda c: metropole(cities, c["city"]), cities)))
    # Retorna a contagem de metrópoles em um país específico
    return len(list(filter(lambda c: metropole(cities, c["city"]), filter(lambda c: c["country"] == country, cities))))

# Verificar se uma cidade é uma capital
def capital(cities, cidade=None):
    if cidade is None:
        # Retorna todas as capitais
        return list(filter(lambda c: c["city"] == c["capital"], cities))
    # Retorna se a cidade específica é uma capital
    return any(filter(lambda c: c["city"] == cidade and c["city"] == c["capital"], cities))

# Listar todas as capitais
def listar_capitais(cities):
    return capital(cidade=None, cities=cities)

# Listar todas as capitais que são megacidades
def capitais_megacidades(cities):
    return list(filter(lambda c: megacidade(cities, c["city"]), listar_capitais(cities)))

# Listar todas as capitais que não são metrópoles nem megacidades
def capitais_nao_metropole_megacidades(cities):
    return list(filter(lambda c: not megacidade(cities, c["city"]) and not metropole(cities, c["city"]), listar_capitais(cities)))

cidades = getRes(results)

# Exemplos:

# # Lista todas as cidades
# print("Todas as cidades:")
# for cidade in cidades:
#     print(cidade)

# # Lista todas as megacidades
# print("Todas as megacidades:")
# megacidades = megacidade(cidades)
# for cidade in megacidades:
#     print(cidade)

# # Retorna se uma cidade específica é uma megacidade
# print("É 'Cairo' uma megacidade?", megacidade(cidades, "Cairo"))
# print("É 'Paris' uma megacidade?", megacidade(cidades, "Paris"))

# # Lista todas as metrópoles
# print("Todas as metrópoles:")
# metropoles = metropole(cidades)
# for cidade in metropoles:
#     print(cidade)

# # Retorna se uma cidade específica é uma metrópole
# print("É 'Cairo' uma metrópole?", metropole(cidades, "Cairo"))
# print("É 'Berlin' uma metrópole?", metropole(cidades, "Berlin"))

# # Encontrar todas as cidades que contêm uma determinada substring
# substring_search = "Bra"
# print(f"Cidades contendo '{substring_search}':")
# cities_with_substring = cidades_busca(cidades, substring_search)
# for city in cities_with_substring:
#     print(city)

# substring_search = "Bra"
# country = "United Kingdom"
# print(f"Cidades contendo '{substring_search}' em United Kingdom:")
# cities_with_substring = cidades_busca(cidades, substring_search, country)
# for city in cities_with_substring:
#     print(city)

# # Lista todas as cidades
# print(cidades_busca(cidades))

# # Encontrar todas as cidades que começam com uma determinada letra
# starting_letter = "B"
# print(f"Cidades que começam com a letra '{starting_letter}':")
# cities_with_letter = cidades_letra(cidades, starting_letter)
# for city in cities_with_letter:
#     print(city)

# starting_letter = "S"
# print(f"Cidades que começam com a letra '{starting_letter}':")
# cities_with_letter = cidades_letra(cidades, starting_letter)
# for city in cities_with_letter:
#     print(city)

# # Lista todas as cidades
# print(cidades_letra(cidades))

# # Encontrar a população total de um país
# country = "Brazil"
# print(f"População total do(a) {country}: {populacao_total(cidades, country)}")

# country = "China"
# print(f"População total do(a) {country}: {populacao_total(cidades, country)}")

# # Encontrar a população total de todos os países/cidades
#print(populacao_total(cidades))

# # Encontrar todas as cidades de um país
# country = "Brazil"
# print(f"Cidades no(a) {country}:")
# cities_in_country = list_cidades_pais(cidades, country)
# for city in cities_in_country:
#     print(city)

# country = "Japan"
# print(f"Cidades no(a) {country}:")
# cities_in_country = list_cidades_pais(cidades, country)
# for city in cities_in_country:
#     print(city)

# # Lista todas as cidades
# print(list_cidades_pais(cidades))

# # Contar quantas metrópoles existem em um país
# country = "Brazil"
# print(f"Número de metrópoles no(a) {country}: {contar_metropoles(cidades, country)}")

# country = "China"
# print(f"Número de metrópoles no(a) {country}: {contar_metropoles(cidades, country)}")

# # Contar quantas metrópoles existem em todos os países
# print(contar_metropoles(cidades))

# # Verificar se uma cidade é uma capital
# print("É 'Ouro Preto' uma capital?", capital(cidades, "Ouro Preto"))
# print("É 'Moscow' uma capital?", capital(cidades, "Moscow"))

# # Retorna todas as capitais
# print(capital(cidades))

# # Lista todas as capitais
# print("Todas as capitais:")
# capitais = listar_capitais(cidades)
# for capital in capitais:
#     print(capital)

# # Lista todas as capitais que são megacidades
# print("Capitais que são megacidades:")
# capitais_megacidades_list = capitais_megacidades(cidades)
# for capital in capitais_megacidades_list:
#     print(capital)

# # Lista todas as capitais que não são metrópoles nem megacidades
# print("Capitais que não são metrópoles nem megacidades:")
# capitais_nao_metropole_megacidades_list = capitais_nao_metropole_megacidades(cidades)
# for capital in capitais_nao_metropole_megacidades_list:
#     print(capital)



