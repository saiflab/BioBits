import streamlit as st
from Bio import SeqIO
from io import StringIO

# Add a full-width logo at the top
logo = "logo.jpg"
st.markdown(f"""
    <style>
        .full-width-image {{
            width: 100%;
            height: auto;
        }}
    </style>
    <img class="full-width-image" src="{logo}" alt="Logo">
""", unsafe_allow_html=True)

# Title and description
st.title("Bioinformatics Sequence Analyzer")
st.write("Upload a DNA/RNA FASTA file to get basic sequence statistics.")
st.markdown("**Created by Ahmed Saif T**", unsafe_allow_html=True)  # Bold name

# Upload FASTA file
uploaded_file = st.file_uploader("Choose a FASTA file", type="fasta")

if uploaded_file is not None:
    # Read the file as a string
    fasta_text = uploaded_file.read().decode("utf-8")
    st.subheader("FASTA File Content Preview:")
    st.text_area("FASTA Content", fasta_text[:500] + "...", height=150, max_chars=1000)  # Show a snippet of the sequence

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

    # Display results with better formatting
    st.subheader("Sequence Statistics")
    st.write(f"**Sequence ID:** `{record.id}`")
    st.write(f"**Sequence Length:** `{seq_length}` bases")
    st.write(f"**GC Content:** `{gc_content:.2f}%`")
    
    # Show nucleotide distribution in a table with some styling
    st.subheader("Nucleotide Distribution")
    st.table(nucleotide_distribution)

    # Optionally display the full sequence
    if st.checkbox("Show full sequence"):
        st.text_area("Full Sequence", sequence, height=200)

# Footer with some styling
st.write("---")
st.markdown('<p style="text-align: center;">Developed with Streamlit</p>', unsafe_allow_html=True)
