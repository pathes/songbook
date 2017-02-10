import os, shutil
import subprocess
from tempfile import mkdtemp, mkstemp


def run_pdflatex(tex_filename):
    pdflatex = subprocess.Popen(
        ['pdflatex', tex_filename, '-interaction=batchmode', '-halt-on-error'],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    # TypeError: a bytes-like object is required, not 'str'
    # Forcing latex to render:
    # * "-interaction={whatever}" does not reliably ignore errors
    # * pressing Q+ENTER inside "?" state seems to force to render
    # * pressing Q+ENTER inside "enter file name" state keeps you in that state
    # * pressing ENTER inside "enter file name" state transitions to "?" state
    # so we press ENTER to exit the "enter file name" state and ENTER+Q to force rendering
    std_out, std_err = pdflatex.communicate(b'\nq\n' * 16)

def tex_to_pdf(tex_content):
    # Create temp folder and get into it.
    orig_folder = os.getcwd()
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)
    # Create TeX file and write content.
    tex_file, tex_filename = mkstemp(dir=tmp_folder)
    os.write(tex_file, tex_content.encode("UTF-8"))
    os.close(tex_file)
    # Run pdflatex. Second run is necessary for TOC to be created.
    for i in range(2):
        run_pdflatex(tex_filename)
    # Read PDF file
    pdf_file = open(tex_filename + '.pdf', 'rb')
    pdf_content = pdf_file.read()
    pdf_file.close()
    # Remove temp folder and get back.
    os.chdir(orig_folder)
    shutil.rmtree(tmp_folder)
    # Return PDF content.
    return pdf_content
