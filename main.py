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
def megacidade(cidade, cities):
    return any(filter(lambda c: c["city"] == cidade and int(c["population"]) > 10000000, cities))

# Verificar se uma cidade é uma metropole
def metropole(cidade, cities):
    return any(filter(lambda c: c["city"] == cidade and 1000000 < int(c["population"]) < 10000000, cities))

# Encontrar todas as cidades que contêm uma determinada substring
def cidades_busca(busca, cities):
    return list(filter(lambda c: substring(c["city"], busca), cities))

# Encontrar todas as cidades que começam com uma determinada letra
def cidades_letra(letra, cities):
    return list(map(lambda c: c["city"], filter(lambda c: c["city"].startswith(letra), cities)))

# Encontrar a população total de um país
def populacao_total(country, cities):
    return reduce(lambda acc, c: acc + int(c["population"]), filter(lambda c: c["country"] == country, cities), 0)

# Encontrar todas as cidades de um país
def list_cidades_pais(country, cities):
    return list(map(lambda c: c["city"], filter(lambda c: c["country"] == country, cities)))

# Contar quantas metropoles existem em um país
def contar_metropoles(country, cities):
    return len(list(filter(lambda c: metropole(c["city"], cities), filter(lambda c: c["country"] == country, cities))))

# Verificar se uma cidade é uma capital
def capital(cidade, cities):
    return any(filter(lambda c: c["city"] == cidade and c["city"] == c["capital"], cities))

# Listar todas as capitais
def listar_capitais(cities):
    return list(map(lambda c: c["capital"], cities))

# Listar todas as capitais que são megacidades
def capitais_megacidades(cities):
    return list(filter(lambda c: megacidade(c, cities), listar_capitais(cities)))

# Listar todas as capitais que não são metropoles nem megacidades
def capitais_nao_metropole_megacidades(cities):
    return list(filter(lambda c: not megacidade(c, cities) and not metropole(c, cities), listar_capitais(cities)))

res = getRes(results)

# Exemplos:

# # Lista todas as megacidades
# megacidades = list(filter(lambda c: megacidade(c["city"], res), res))
# for cidade in megacidades:
#     print(cidade)

# # Retorna se a cidade é uma megacidade
# print(megacidade("Cairo", res))
# print(megacidade("Paris", res))

# # Lista todas as metropoles
# metropoles = list(filter(lambda c: metropole(c["city"], res), res))
# for cidade in metropoles:
#     print(cidade)

# # Retorna se a cidade é uma metropole
# print(metropole("Cairo", res))
# print(metropole("Berlin", res))

# # Encontrar todas as cidades que contêm uma determinada substring
# substring_search = "Bra"
# cities_with_substring = cidades_busca(substring_search, res)
# print(f"Cidades contendo '{substring_search}':")
# for city in cities_with_substring:
#     print(city)

# # Encontrar todas as cidades que começam com uma determinada letra
# starting_letter = "B"
# cities_with_letter = cidades_letra(starting_letter, res)
# print(f"Cities que começam com a letra '{starting_letter}':")
# for city in cities_with_letter:
#     print(city)

# # Encontrar a população total de um país
# country = "Brazil"
# total_population = populacao_total(country, res)
# print(f"População toltal do(a) {country}: {total_population}")

# country = "China"
# total_population = populacao_total(country, res)
# print(f"População toltal do(a) {country}: {total_population}")

# # Encontrar todas as cidades de um país
# country = "Brazil"
# cities_in_country = list_cidades_pais(country, res)
# print(f"Cidades no(a) {country}:")
# for city in cities_in_country:
#     print(city)

# country = "Japan"
# cities_in_country = list_cidades_pais(country, res)
# print(f"Cidades no(a) {country}:")
# for city in cities_in_country:
#     print(city)

# # Contar quantas metropoles existem em um país
# country = "Brazil"
# metropolises_count = contar_metropoles(country, res)
# print(f"Número de metropoles no(a) {country}: {metropolises_count}")

# country = "China"
# metropolises_count = contar_metropoles(country, res)
# print(f"Número de metropoles no(a) {country}: {metropolises_count}")

# # Verificar se uma cidade é uma capital
# print("Ouro Preto é uma capital?", capital("Ouro Preto", res))
# print("Moscow é uma capital?", capital("Moscow", res))

# Filter to get only capitals
capitais = list(filter(lambda c: c["city"] == c["capital"], res))

# Lista todas as capitais
print("Todas as capitais:")
for capital in capitais:
    print(capital)

# List all capitals that are megacities
capitais_megacidades_list = capitais_megacidades(capitais)
print("Capitais que são megacidades:")
print(capitais_megacidades_list)

# List all capitals that are neither metropolises nor megacities
capitais_nao_metropole_megacidades_list = capitais_nao_metropole_megacidades(capitais)
print("Capitais que não são metrópoles nem megacidades:")
print(capitais_nao_metropole_megacidades_list)





