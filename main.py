from PyQt5 import uic
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
import os, sys, subprocess


class App(QMainWindow):

    reports = False
    selected = None


    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('interfaz.ui', self)


        # Esconder widgets
        self.w_reports.hide()


        self.setFixedSize(476, 414) # Para que no pueden cambiar el 
        # tamaño de la ventana

        # Background de la ventana
        self.setStyleSheet('background-color: black; color: black;')

        # Background del gif matrix
        self.movie = QMovie("matrix.gif")
        self.l_bg.setMovie(self.movie)
        self.movie.start()


        # Iconos de los botones
        self.b_sql.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        self.b_xss.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        self.b_open_file.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileIcon')))
        self.b_open_file_cmd.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_TitleBarMaxButton')))


        self.bb_reports.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogContentsView')))
        self.bb_install.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DriveDVDIcon')))
        self.bb_help.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxQuestion')))
        self.bb_close.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_BrowserStop')))


        

        # Eventos de los botones para hacer el escaneo de injecciones
        self.b_sql.clicked.connect(self.sql_injection)
        self.b_xss.clicked.connect(self.xss_injection)

        # Otros eventos
        self.bb_reports.clicked.connect(self.show_reports)
        self.bb_close.clicked.connect(self.show_reports)
        self.b_open_file.clicked.connect(lambda x: self.open_file(1))
        self.b_open_file_cmd.clicked.connect(lambda x: self.open_file(2))

        self.bb_install.clicked.connect(self.install)

        self.bb_help.clicked.connect(self.help)

    # Cambiar de vistas
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def show_reports(self):

        self.clearLayout(self.ly_files)  # Eliminamos los widget que tenga
        # la ventana de los reportes

        current_path = os.getcwd()
        report_path = str(current_path + '/report/')
        files = os.listdir(report_path)

        for i in files:
            name = i# .replace('.', '')
            radiobutton = QRadioButton("File {0}".format(name), self)
            radiobutton.setObjectName(name)
            radiobutton.clicked.connect(lambda x, i=name: self.file_selected(i))
            radiobutton.setStyleSheet('color: black;')
            self.ly_files.addWidget(radiobutton)

        if not self.reports:
            self.reports = True
            self.w_reports.show()
        else:
            self.reports = False
            self.w_reports.hide()            


    # Funcionalidades
    def file_selected(self, name):
        self.selected = name
        print(name)

    def open_file(self, opc):

        if self.selected:
            
            current_path = str(os.getcwd())
            report_path = current_path + '/report/'
            file_path = report_path + self.selected
            os.makedirs(report_path, exist_ok=True)

            if opc == 1:
                subprocess.run(['mousepad', file_path])
            elif opc == 2:
                subprocess.run(["lxterminal", "-e", 'python3', current_path + '/print_report.py', file_path])            

        self.selected = None

    def sql_injection(self):

        url = self.i_injection.text()
        file_name = self.i_name.text()

        if not url or not file_name:
            self.setStyleSheet('background-color: white;')
            QMessageBox.about(self, "Error", "Debe ingresar la URL y el nombre del reporte")
            self.setStyleSheet('background-color: black;')

        current_path = os.getcwd()
        report_path = str(current_path + '/report/')
        file_path = report_path + str(file_name) + '.txt'

        os.makedirs(report_path, exist_ok=True)

        with open(file_path, "w+") as f:
            result = subprocess.run(['sqlmap', '-u',
            '"' + url + '"', '--dbs', '--batch'], stdout=subprocess.PIPE)
            r = str(result.stdout.decode('utf-8'))
            f.write(r)
        os.chmod(file_path, 0o777)


        self.setStyleSheet('background-color: white; color: black;')
        QMessageBox.about(self, "Resultados en", file_path)
        self.setStyleSheet('background-color: black; color: black;')        

        # http://testphp.vulnweb.com/artists.php?artist=1


    def xss_injection(self):

        url = self.i_injection.text()
        file_name = self.i_name.text()

        if not url or not file_name:
            self.setStyleSheet('background-color: white;')
            QMessageBox.about(self, "Error", "Debe ingresar la URL y el nombre del reporte")
            self.setStyleSheet('background-color: black;')

        current_path = os.getcwd()
        report_path = str(current_path + '/report/')
        file_path = report_path + str(file_name) + '.txt'

        os.makedirs(report_path, exist_ok=True)

        with open(file_path, "w") as f:
            result = subprocess.run(['XSpear', '-u', 
            url, '-v', '1'], stdout=subprocess.PIPE)
            r = str(result.stdout.decode('utf-8'))
            f.write(r)
        os.chmod(file_path, 0o777)


        self.setStyleSheet('background-color: white; color: black;')
        QMessageBox.about(self, "Resultados en", file_path)
        self.setStyleSheet('background-color: black; color: black;') 

        # https://xss-game.appspot.com/level1/frame

    def install(self):
        subprocess.Popen(["lxterminal", "-e", "python3 install.py" ])

    def help(self):
        self.setStyleSheet('background-color: white; color: black;')
        help = """
        1) Ingrese la url con su protocolo, ejemplo: http://www.domain.com
        \n
        2) Ejecute la aplicación en modo root
        \n
        3) Sea cuidadoso al elegir el nombre del reporte pues estos se sobreescriben
        """
        QMessageBox.about(self, "Ayuda", help)
        self.setStyleSheet('background-color: black; color: black;')      
                      

app = QApplication(sys.argv)
_window = App()
_window.show()
app.exec_()
