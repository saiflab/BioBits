
import streamlit as st
from Bio import SeqIO
from io import StringIO

# Title and description
st.title("Bioinformatics Sequence Analyzer")
st.write("Upload a DNA/RNA FASTA file to get basic sequence statistics.")
st.write("Created by Ahmed Saif")

# Upload FASTA file
uploaded_file = st.file_uploader("Choose a FASTA file", type="fasta")

if uploaded_file is not None:
    # Read the file as a string
    fasta_text = uploaded_file.read().decode("utf-8")
    st.text(f"FASTA file content:\n{fasta_text[:500]}...")  # Show a snippet of the sequence

    # Parse FASTA file
    fasta_io = StringIO(fasta_text)
    record = SeqIO.read(fasta_io, "fasta")
    
    # Get sequence
    sequence = str(record.seq)
    
    # Calculate metrics
    seq_length = len(sequence)
    gc_content = 100 * (sequence.count('G') + sequence.count('C')) / seq_length
    nucleotide_distribution = {
        'A': sequence.count('A'),
        'T': sequence.count('T'),
        'G': sequence.count('G'),
        'C': sequence.count('C'),
        'Other': seq_length - (sequence.count('A') + sequence.count('T') + sequence.count('G') + sequence.count('C'))
    }

    # Display results
    st.write(f"**Sequence ID:** {record.id}")
    st.write(f"**Sequence Length:** {seq_length} bases")
    st.write(f"**GC Content:** {gc_content:.2f}%")
    
    # Show nucleotide distribution
    st.write("**Nucleotide Distribution:**")
    st.write(nucleotide_distribution)

    # Optionally display the full sequence
    if st.checkbox("Show full sequence"):
        st.text(sequence)

# Footer
st.write("---")
st.write("Developed with Streamlit")
