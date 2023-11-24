from flask import Flask, request, jsonify,Response
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from sswap_utils import read_rig,fill_rrg
from readont import cottage_offer,update_ont

cottage_service = Flask(__name__)


@cottage_service.route('/cottageServices/getAvailableCottage', methods=['GET'])
def send_rdg():
    file_path = 'checkavailable.rdf'
    g = Graph()
    g.parse(file_path, format='n3')
    rdg = g.serialize(format='n3')
    response = Response(rdg)
    return response


@cottage_service.route('/cottageServices/getAvailableCottage', methods=['POST'])
def searchCottage():
    rig = request.get_data(as_text=True)

    user_input = read_rig(rig)
    offer = cottage_offer(user_input)

    rrg = fill_rrg(rig,offer)

    response = Response(rrg)
    return response












if __name__ == '__main__':
    cottage_service.run(port=5001)
    # my_rdg()