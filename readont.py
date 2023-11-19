import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF
from datetime import datetime, timedelta



# def get_availablePeriod(start_date,available_days, unavailablePeriod):
#     unavailablePeriods = unavailablePeriod.split(' ')
#     for p in unavailablePeriods:
#         P_start_date,P_end_date = p.split('To')
#         ##TODO





def check_date(user_input,start_date,available_days):

    user_start_date = user_input['start_date'].split('-')
    user_start_date = datetime(int(user_start_date[0]), int(user_start_date[1]), int(user_start_date[2]),)
    user_num_days = timedelta(days=int(user_input['num_days']))
    user_shift_days = timedelta(days=int(user_input['max_date_shift']))
    #
    user_min_start_date = user_start_date - user_shift_days
    user_max_start_date = user_start_date + user_shift_days
    user_max_end_date = user_max_start_date + user_num_days

    #
    co_start_date = str(start_date).split('-')
    co_start_date = datetime(int(co_start_date[0]), int(co_start_date[1]), int(co_start_date[2]),)
    co_num_days = timedelta(days=int(available_days))
    #
    co_avail_end_date = co_start_date + co_num_days

    end_date_diff = co_avail_end_date - user_max_end_date
    start_date_diff = user_min_start_date - co_start_date

    return end_date_diff.days >=0 and start_date_diff.days >=0



def cottage_offer(user_input):
    #
    g = rdflib.Graph()
    g.parse("ontology.rdf", format="turtle")

    query = f"""
    PREFIX ex: <http://example.org#>
    SELECT ?cottage ?address ?image ?num_places ?num_bedrooms ?lake_distance ?nearest_city ?start_date ?available_days ?unavailablePeriod
    WHERE {{
        ?cottage a ex:Cottage ;
                 ex:address ?address ;
                 ex:places ?num_places ;
                 ex:bedrooms ?num_bedrooms ;
                 ex:distanceToLake ?lake_distance ;
                 ex:nearestCity ?nearest_city ;
                 ex:availableDays ?available_days ;
                 ex:unavailablePeriod ?unavailablePeriod;
                 ex:startDate ?start_date ;
                 ex:imageURL ?image.
        
        FILTER (?num_places >= {user_input['num_people']} &&
                ?num_bedrooms >= {user_input['num_bedrooms']} &&
                ?lake_distance <= {user_input['max_lake_distance']} &&
                ?nearest_city = "{user_input['city']}" &&
                ?available_days >= {user_input['num_days']} ).
    }}
    """
    results = g.query(query, initNs={"": Namespace("http://example.org/cottage#")})

    offer = {'cottage':[],
             'booker_name':[],
             'booking_num': [],
             'address': [],
             'image': [],
             'num_places': [],
             'num_bedrooms': [],
             'lake_distance': [],
             'nearest_city': [],
             'start_date': [],
             'end_date': [],
             }

    for result in results:

        cottage, address, image, num_places, num_bedrooms, lake_distance, nearest_city, start_date, available_days, unavailablePeriod= result
        if str(unavailablePeriod) == '1':
            continue

        if check_date(user_input,start_date,available_days):
            tmp_start_date = str(user_input['start_date']).split('-')
            end_date = datetime(int(tmp_start_date[0]), int(tmp_start_date[1]), int(tmp_start_date[2]),) + timedelta(days=int(user_input['num_days']))
            end_date = f'{str(end_date.year)}-{str(end_date.month)}-{str(end_date.day)}'
            offer['cottage'].append(cottage.split("#")[-1])
            offer['booker_name'].append(user_input['name'])
            offer['address'].append(str(address))
            offer['image'].append(str(image))
            offer['num_places'].append(str(num_places))
            offer['num_bedrooms'].append(str(num_bedrooms))
            offer['lake_distance'].append(str(lake_distance))
            offer['nearest_city'].append(str(nearest_city))
            offer['start_date'].append(str(user_input['start_date']))
            offer['end_date'].append(str(end_date))
            booking_num = f'{str(cottage).split("#")[-1]}-{str(user_input["start_date"])}-{str(end_date)}'
            offer['booking_num'].append(str(booking_num))

    return offer

def update_ont(resevation):

    g = rdflib.Graph()
    ontology_file = 'ontology.rdf'
    g.parse(ontology_file, format="turtle")
    ex = Namespace('http://example.org#')

    cottage_uri = URIRef(f'http://example.org#{resevation["cottage"]}')


    g.set((cottage_uri, ex.unavailablePeriod, Literal('1')))
    g.serialize(ontology_file, format='turtle')

