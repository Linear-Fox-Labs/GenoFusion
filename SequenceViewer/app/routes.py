from flask import request, render_template, redirect, url_for, flash
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
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
        
    if file:
        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('view_file', filename=file.filename))
    
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return redirect(url_for('index'))
        
    file_type = filename.split('.')[-1].lower()
    if file_type not in ['fasta', 'fa', 'fastq', 'gb', 'genbank']:
        return redirect(url_for('index'))

    try:
        sequences = []
        with open(filepath, "r") as handle:
            for record in SeqIO.parse(handle, file_type):
                sequence_str = str(record.seq)
                highlighted_sequence, enzyme_sites = find_enzyme_sites(sequence_str, 'All Commercial')
                
                sequence_data = {
                    "id": record.id,
                    "sequence": sequence_str,
                    "highlighted_sequence": highlighted_sequence,
                    "amino_acid_sequence": translate_sequence(sequence_str),
                    "features": [],
                    "enzyme_objects": []
                }

                # Process enzyme sites
                for enzyme, start, end in enzyme_sites:
                    color = get_color_for_enzyme(enzyme.__name__)
                    sequence_data["features"].append((enzyme.__name__, start, end, color))
                    sequence_data["enzyme_objects"].append({
                        "name": enzyme.__name__,
                        "rseq": str(enzyme.site),
                        "fcut": 0,
                        "rcut": len(enzyme.site),
                        "color": color
                    })
                
                sequences.append(sequence_data)

        if not sequences:
            return render_template('view.html', 
                                sequences=[], 
                                filename=filename,
                                error="No sequences found in file")
                                
        return render_template('view.html', 
                             sequences=sequences,
                             filename=filename)
                             
    except Exception as e:
        return render_template('view.html', 
                             sequences=[],
                             filename=filename,
                             error=f"Error processing file: {str(e)}")