import streamlit as st
from Bio import SeqIO
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

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
st.markdown('<p><strong>Created by Ahmed Saif Tamim</strong></p>', unsafe_allow_html=True)  # Bold name

# Upload FASTA file
uploaded_file = st.file_uploader("Choose a FASTA file", type="fasta")

if uploaded_file is not None:
    # Read the file as a string
    fasta_text = uploaded_file.read().decode("utf-8")
    
    # Parse FASTA file
    fasta_io = StringIO(fasta_text)
    records = list(SeqIO.parse(fasta_io, "fasta"))
    
    # Get sequence data
    sequences = [str(record.seq) for record in records]
    seq_ids = [record.id for record in records]
    seq_lengths = [len(seq) for seq in sequences]
    
    # Calculate metrics
    num_sequences = len(records)
    avg_length = sum(seq_lengths) / num_sequences if num_sequences > 0 else 0
    gc_contents = [100 * (seq.count('G') + seq.count('C')) / length for seq, length in zip(sequences, seq_lengths)]
    
    nucleotide_distribution = {
        'A': sum(seq.count('A') for seq in sequences),
        'T': sum(seq.count('T') for seq in sequences),
        'G': sum(seq.count('G') for seq in sequences),
        'C': sum(seq.count('C') for seq in sequences),
        'Other': sum(len(seq) for seq in sequences) - sum(seq.count('A') + seq.count('T') + seq.count('G') + seq.count('C') for seq in sequences)
    }
    
    # Display results
    st.markdown('<h3 class="subheader">FASTA File Content Preview:</h3>', unsafe_allow_html=True)
    st.text_area("FASTA Content", fasta_text[:500] + "...", height=150, max_chars=1000, key="text_area")  # Show a snippet of the sequence

    st.markdown('<h3 class="subheader">Sequence Statistics</h3>', unsafe_allow_html=True)
    st.write(f"**Number of Sequences:** `{num_sequences}`")
    st.write(f"**Average Sequence Length:** `{avg_length:.2f}` bases")
    st.write(f"**Overall GC Content:** `{sum(gc_contents) / num_sequences:.2f}%`")
    
    # Plot sequence length distribution
    st.markdown('<h3 class="subheader">Sequence Length Distribution</h3>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.hist(seq_lengths, bins=20, color='#1f77b4', edgecolor='black')
    ax.set_title('Sequence Length Distribution')
    ax.set_xlabel('Length (bases)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Plot nucleotide composition
    st.markdown('<h3 class="subheader">Nucleotide Composition</h3>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.pie(nucleotide_distribution.values(), labels=nucleotide_distribution.keys(), autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.set_title('Nucleotide Composition')
    st.pyplot(fig)

    # Optionally display the full sequence
    if st.checkbox("Show full sequence"):
        st.text_area("Full Sequence", "\n".join(sequences), height=300, key="full_sequence")

    # Sequence search feature
    search_query = st.text_input("Search for a sequence or subsequence:")
    if search_query:
        matching_sequences = [seq_id for seq_id, seq in zip(seq_ids, sequences) if search_query in seq]
        if matching_sequences:
            st.write(f"**Found in sequences:** {', '.join(matching_sequences)}")
        else:
            st.write("**No matching sequences found.**")

# Footer with custom styling
st.markdown('<div class="footer">Developed with Streamlit</div>', unsafe_allow_html=True)
