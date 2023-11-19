from flask import Flask, request, render_template, redirect, url_for,send_from_directory
from readont import cottage_offer,update_ont

app = Flask(__name__)
offer = {}
reservation = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global offer
    book_info = {}
    offer = {}

    if request.method == 'POST':
        book_info['name'] = str(request.form['name'])
        book_info['num_people'] = str(request.form['num_people'])
        book_info['num_bedrooms'] = str(request.form['num_bedrooms'])
        book_info['max_lake_distance'] = str(request.form['max_lake_distance'])
        book_info['city'] = str(request.form['city'])
        book_info['max_city_distance'] = str(request.form['max_city_distance'])
        book_info['num_days'] = int(request.form['num_days'])
        book_info['start_date'] = str(request.form['start_date'])
        book_info['max_date_shift'] = int(request.form['max_date_shift'])

        offer = cottage_offer(book_info)

        return redirect(url_for('offers'))

    return render_template('index.html')


@app.route('/offers')
def offers():
    # offer = request.args.get('offer')
    # offer = ast.literal_eval(offer)
    return render_template('offers.html', data=offer)

@app.route('/choose_reservation', methods=['POST'])
def choose_reservation():
    global offer
    chosen_index = int(request.form['choose_button'])
    choosen_offer = {k:offer[k][chosen_index] for k in offer.keys()}
    update_ont(choosen_offer)
    return render_template('result.html', data=offer, i = chosen_index)

@app.route('/exampleService/onto/exampleOntology.owl')
def serve_ontology():
    ontology_path = 'ontology.owl'
    return send_from_directory('', ontology_path)


if __name__ == '__main__':
    app.run(debug=True)
