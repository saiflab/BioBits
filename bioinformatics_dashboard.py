import streamlit as st
from Bio import SeqIO
from io import StringIO

# Apply custom CSS for theming
st.markdown("""
    <style>
        body {
            background-color: #f0f0f0; /* Light grey background */
        }
        .title {
            color: #1f77b4; /* Blue color for the title */
        }
        .header {
            background-color: #ffffff; /* White background for the header */
            padding: 20px;
            border-bottom: 3px solid #1f77b4; /* Blue bottom border for the header */
        }
        .subheader {
            color: #ff7f0e; /* Orange color for subheaders */
        }
        .text-area {
            border: 2px solid #1f77b4; /* Blue border for text areas */
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            color: #888888; /* Grey color for the footer */
        }
        .table {
            background-color: #ffffff; /* White background for tables */
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Add a full-width logo at the top
logo = "logo.jpg"
st.image(logo, use_column_width=True)  # Logo spans the full width of the column

# Title and description with custom class
st.markdown('<h1 class="title">Bioinformatics Sequence Analyzer</h1>', unsafe_allow_html=True)
st.write("Upload a DNA/RNA FASTA file to get basic sequence statistics.")
st.markdown('<p><strong>Created by Ahmed Saif</strong></p>', unsafe_allow_html=True)  # Bold name

# Upload FASTA file
uploaded_file = st.file_uploader("Choose a FASTA file", type="fasta")

if uploaded_file is not None:
    # Read the file as a string
    fasta_text = uploaded_file.read().decode("utf-8")
    st.markdown('<h3 class="subheader">FASTA File Content Preview:</h3>', unsafe_allow_html=True)
    st.text_area("FASTA Content", fasta_text[:500] + "...", height=150, max_chars=1000, key="text_area")  # Show a snippet of the sequence

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
    st.markdown('<h3 class="subheader">Sequence Statistics</h3>', unsafe_allow_html=True)
    st.write(f"**Sequence ID:** `{record.id}`")
    st.write(f"**Sequence Length:** `{seq_length}` bases")
    st.write(f"**GC Content:** `{gc_content:.2f}%`")
    
    # Show nucleotide distribution in a table with custom styling
    st.markdown('<h3 class="subheader">Nucleotide Distribution</h3>', unsafe_allow_html=True)
    st.table(nucleotide_distribution)

    # Optionally display the full sequence
    if st.checkbox("Show full sequence"):
        st.text_area("Full Sequence", sequence, height=200, key="full_sequence")

# Footer with custom styling
st.markdown('<div class="footer">Developed with Streamlit</div>', unsafe_allow_html=True)
