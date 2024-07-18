from flask import request, render_template, redirect, url_for
from Bio import SeqIO
from GenoFusion.Utils import get_sequence_properties
import os
from app import app
from .sequence_tools import translate_sequence, find_enzyme_sites, get_color_for_enzyme, enzyme_groups

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('view_file', filename=file.filename))
    return redirect(request.url)

@app.route('/view/<filename>')
def view_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_type = filename.split('.')[-1].lower()
    sequences = []

    with open(filepath, "r") as handle:
        for record in SeqIO.parse(handle, file_type):
            sequence_str = str(record.seq)
            highlighted_sequence, enzyme_sites = find_enzyme_sites(sequence_str, selected_group='All Commercial')
            sequence_properties = get_sequence_properties(sequence_str)
            amino_acid_sequence = translate_sequence(sequence_str)
            sequences.append({
                "id": record.id,
                "sequence": sequence_str,
                "highlighted_sequence": highlighted_sequence,
                "amino_acid_sequence": amino_acid_sequence,
                "features": enzyme_sites,
                "properties": sequence_properties
            })

    selected_enzyme_type = request.args.get('enzyme_type', '6+ Cutters')
    filtered_sequences = []

    for sequence in sequences:
        filtered_features = []
        enzyme_objects = []
        for enzyme_info in sequence['features']:
            enzyme = enzyme_info[0]
            start = enzyme_info[1]
            end = enzyme_info[2]
            color = get_color_for_enzyme(enzyme.__name__)
            if selected_enzyme_type == 'Fermentas' or selected_enzyme_type in enzyme_groups or selected_enzyme_type in enzyme.__class__.__name__:
                filtered_features.append((enzyme, start, end, color))
                enzyme_objects.append({
                    "name": enzyme.__name__,
                    "rseq": enzyme.site,
                    "fcut": 0,
                    "rcut": len(enzyme.site),
                    "color": color
                })
        sequence['features'] = filtered_features
        sequence['enzyme_objects'] = enzyme_objects
        filtered_sequences.append(sequence)

    sequences_data = [{
        'id': sequence['id'],
        'description': '',
        'sequence': sequence.get('sequence', ''),
        'amino_acid_sequence': sequence['amino_acid_sequence'],
        'features': sequence['features'],
        'enzyme_objects': sequence['enzyme_objects']
    } for sequence in filtered_sequences]

    return render_template('view.html', sequences=sequences_data, filename=filename)
