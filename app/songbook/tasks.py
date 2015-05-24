import os, shutil
import subprocess
from tempfile import mkdtemp, mkstemp


def run_pdflatex(tex_filename):
    pdflatex = subprocess.Popen(
        ['pdflatex', tex_filename, '-interaction=batchmode', '-halt-on-error'],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    pdflatex.stdin.write('q' * 10)  # just to be sure that no errors stop rendering
    pdflatex.communicate()
    pdflatex.stdin.close()


def tex_to_pdf(tex_content):
    # Create temp folder and get into it.
    orig_folder = os.getcwd()
    tmp_folder = mkdtemp(dir='/home/fraktal/rails/kaczmarski/tmp/')
    os.chdir(tmp_folder)
    # Create TeX file and write content.
    tex_file, tex_filename = mkstemp(dir=tmp_folder)
    os.write(tex_file, tex_content.encode("UTF-8"))
    os.close(tex_file)
    # Run pdflatex. Second run is necessary for TOC to be created.
    for i in range(2):
        run_pdflatex(tex_filename)
    # Read PDF file

    """dbg = ''
    for f in os.listdir(tmp_folder):
        dbg += f + '\n\n'
        dbg += open(tmp_folder + '/' + f).read()
        dbg += '\n\n\n\n\n'
    return dbg"""

    pdf_file = open(tex_filename + '.pdf', 'r')
    pdf_content = pdf_file.read()
    pdf_file.close()
    # Remove temp folder and get back.
    os.chdir(orig_folder)
    shutil.rmtree(tmp_folder)
    # Return PDF content.
    return pdf_content
