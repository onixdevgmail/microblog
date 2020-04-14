from country_list import countries_for_language

countries = dict(countries_for_language('en'))


def add_countries():
    new_country = {}
    for country in countries:
        new_country[country] = countries[str(country)]
    return new_country
