import os, shutil
from subprocess import call
from tempfile import mkdtemp, mkstemp


def tex_to_pdf(tex_content):
    # Create temp folder and get into it.
    orig_folder = os.getcwd()
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)
    # Create TeX file and write content.
    tex_file, tex_filename = mkstemp(dir=tmp_folder)
    os.write(tex_file, tex_content)
    os.close(tex_file)
    # Run pdflatex.
    call(['pdflatex', tex_filename])
    # Read PDF file
    pdf_file = open(tex_filename + '.pdf', 'r')
    pdf_content = pdf_file.read()
    pdf_file.close()
    # Remove temp folder and get back.
    os.chdir(orig_folder)
    shutil.rmtree(tmp_folder)
    # Return PDF content.
    return pdf_content
