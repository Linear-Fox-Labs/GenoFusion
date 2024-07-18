import os
import requests

class DatabaseIntegration:
    @staticmethod
    def fetch_sequence_from_genbank(accession):
        url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={accession}&db=nuccore&report=fasta"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch sequence from GenBank: {response.status_code}")

    @staticmethod
    def fetch_sequence_from_ensembl(id):
        url = f"https://rest.ensembl.org/sequence/id/{id}?content-type=text/x-fasta"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch sequence from Ensembl: {response.status_code}")