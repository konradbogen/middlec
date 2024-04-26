import subprocess
import time
import os 
import PyPDF2
import namer
from settings import SCORE_FOLDER, LILY_APP
import wand

PNG_WIDTH = 1502
PNG_HEIGHT = 744
PNG_BACKGROUND = '#00000000'

LOG_LEVEL = { 
    "NONE": "NONE",
    "ERROR": "ERROR",
    "WARN": "WARN",
    "BASIC_PROGRESS": "BASIC_PROGRESS",
    "PROGRESS": "PROGRESS",
    "INFO": "INFO",
    "DEBUG": "DEBUG"
}

CURRENT_LOG_LEVEL = "BASIC_PROGRESS"
LOGLEVEL_OPTION = "--loglevel"
SVG_TAG = "-dbackend=svg"

PLAIN_PDF = "basic.pdf"
ROTATED_PDF = "score.pdf"

class PDF ():
    def __init__ (self, file_name = ""): 
        self.syntax = ""
        self.app_path = ""
        self.pdf_merger = PyPDF2.PdfFileMerger()
        self.name = ""
        self.filename = ""
        self.directory = ""
        self.number_of_pages = 0
        self.set_file_name (file_name)

    def render (self, syntax) :
        try: 
            self.syntax = syntax
            self.create_directory ()
            self.write_lily (self.syntax)
            self.render_pdf ()
            self.render_svg ()
            self.render_png ()
            return True
        except Exception as error:
            return error

    def render_pdf (self):
        self.filename = self.name + ".pdf"
        self.app_path = self.get_pdf_app ()
        self.render_lily ()

    def render_svg (self):
        self.filename = self.name + ".svg"
        self.app_path        = self.get_svg_app ()
        self.render_lily ()
    
    def render_png (self):
        for i in range (0, self.number_of_pages):
            file_name = "lily-" + str(i)
            background_color = wand.color(PNG_BACKGROUND)
            svg = wand.image(filename=file_name + ".svg", width=PNG_WIDTH, height=PNG_HEIGHT, background=background_color) 
            png = svg.convert('png')
            png.save(filename=file_name + ".png")


    def render_lily (self):
        try:
            process = subprocess.Popen (self.app_path)
            process.wait ()
            self.rotate_pdf ()
            return True
        except Exception as error:
            print (error)
            return False

    def create_directory (self):
        self.directory = SCORE_FOLDER + "/" + self.name
        self.create_folder (self.directory)
        os.chdir (self.directory)

    def change_directory (self):
        if self.directory != "":
            os.chdir (self.directory)
        else:
            self.create_directory ()

    def create_folder(self, folder):
        try:
            os.mkdir (folder)
        except Exception as e:
            print (e) 

    def write_lily (self, syntax):
        self.change_directory ()
        try:
            lily_file = open (self.directory + "/" + self.name + ".ly", "w")
            lily_file.write (syntax)
            lily_file.close ()
            return True
        except:
            return False

    def get_pdf_app (self):
        path = [LILY_APP]
        log_level = CURRENT_LOG_LEVEL
        path.append (LOGLEVEL_OPTION + "=" + log_level)
        path.append (self.name + ".ly")
        return path
    
    def get_svg_app (self):
        path = [LILY_APP]
        log_level = CURRENT_LOG_LEVEL
        path.append (LOGLEVEL_OPTION + "=" + log_level)
        path.append (SVG_TAG)
        path.append (self.name + ".ly")
        return path

    def set_todays_filename (self):
        self.name = namer.get_default ()

    def rotate_pdf (self) :
      os.chdir (self.directory)
      pdf_in = open("lily.pdf", 'rb')
      pdf_reader = PyPDF2.PdfFileReader(pdf_in)
      pdf_writer = PyPDF2.PdfFileWriter()
      for pagenum in range(pdf_reader.numPages):
          page = pdf_reader.getPage(pagenum)
          page.rotateClockwise(90)
          pdf_writer.addPage(page)
          self.number_of_pages += 1
      pdf_out = open(ROTATED_PDF, 'wb')
      pdf_writer.write(pdf_out)
      pdf_out.close()
      pdf_in.close()
    
    def set_file_name (self, file_name):
        if file_name == "":
            self.set_todays_filename ()
        else: 
            self.name = file_name