"""
Created on Wed May 12 14:15:41 2021

@author: Ahmed Reda
"""

from  PySide2.QtWidgets  import * 
from PySide2 import QtCore ,QtWidgets
from  PySide2.QtUiTools  import  QUiLoader 
from  PySide2.QtCore  import  QFile
from pprint import pprint

from  matplotlib.backends.backend_qt5agg  import  ( 
        FigureCanvas ,  NavigationToolbar2QT  as  NavigationToolbar )

from  matplotlib.figure  import  Figure
import  numpy  as  np

import re

# ------------------ MplWidget (Used to Display the plot in the GUI) ------------------ 
class  MplWidget ( QWidget ):
    
    def  __init__ ( self ,  parent  =  None ):
        
        QWidget . __init__ ( self ,  parent )
        
        self.canvas = FigureCanvas( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget (self . canvas) 
        vertical_layout . addWidget ( NavigationToolbar (self . canvas ,  self))
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 ) 
        self . setLayout ( vertical_layout )    
        
# ------------------ MainWidget ------------------ 
class  MainWidget ( QWidget ):
    
    def  __init__ ( self ):
        
        QWidget . __init__ ( self )

        #Importing the GUI design from the ui file
        designer_file  =  QFile ( "Function_Plotter.ui" ) 
        designer_file . open ( QFile . ReadOnly )

        loader  =  QUiLoader () 
        loader . registerCustomWidget ( MplWidget ) 
        self . ui  =  loader . load ( designer_file ,  self )

        designer_file . close ()

        
        #Checking if the plot button is pressed
        self . ui . pushButton_plot . clicked . connect(self.plotEqu)
        
        #Putting a title to the GUI
        self . setWindowTitle ( "Function Plotter" )
        grid_layout  =  QGridLayout () 
        grid_layout . addWidget ( self . ui ) 
        self . setLayout ( grid_layout )
        
    
    #Main Function
    def plotEqu(self):
        #-----------Getting the Equation string-----------
        equ = self.ui.Equation.text()   #String entered by the user
        temp1 = equ.replace(" ","")     #Removing spaces from the input string 
        temp2 = re.split(r'(\D)', temp1)    #Splitting this string into a list of strings
        equ_splitted  = list(filter(None, temp2))   #Removing the empty parts of the string
        
        #-----------Checking for invalid inputs-----------
        #Checking if the user inputs a single character which isn't x
        if ((len(equ_splitted) == 1) and equ_splitted[0] != 'x'):
            self . ui . Log . setText("Please enter a valid Equation")
            return
        #Checking if the user entered a numbers in min and max values of x slots
        if (not ((self.ui.X_low.text()).lstrip('-').isdigit()) or not ((self.ui.X_high.text()).lstrip('-').isdigit())):
            self . ui . Log . setText("Please enter a valid range of X")
            return
        #Checking if x_Min is greater than x_Max
        if (int(self.ui.X_low.text()) > int(self.ui.X_high.text())):
            self . ui . Log . setText("Please enter a valid range of X")
            return
        #Checking if the first input character is a * or / or ^
        if( (equ_splitted[0] == '*') or (equ_splitted[0] == '/') or (equ_splitted[0] == '^') ):
            self . ui . Log . setText("Please enter a valid Equation")
            return
        
        operators = ['*' , '/' , '+' , '-' , '^']   #Needed operators
        for j in range(len(equ_splitted)-1):
            #Checking if the user entered 2 or more operators after each other
            for k in range(len(operators)):
                if ((equ_splitted[j] == operators[k]) and (equ_splitted[j+1] == operators[k])):
                    self . ui . Log . setText("Please enter a valid Equation")
                    return 
                #Checking if the user entered the last char as an operator
                if (equ_splitted[len(equ_splitted)-1] == operators[k]):
                    self . ui . Log . setText("Please enter a valid Equation")
                    return
                #Checking if the user entered letters other than lower case x
            if (    (equ_splitted[j].isalpha()) and 
                    (equ_splitted[j] != 'x') or 
                    (equ_splitted[len(equ_splitted)-1].isalpha()) and 
                    (equ_splitted[len(equ_splitted)-1] != 'x')
                ):
                self . ui . Log . setText("Please write the equation in terms of x")
                return 
            #Checking if x is concatanated with a number from the right or the left
            if (    ((equ_splitted[j].isnumeric()) and (equ_splitted[j+1] == 'x')) or 
                    ((equ_splitted[j+1].isnumeric()) and (equ_splitted[j] == 'x'))
                ):
                self . ui . Log . setText("Please enter a valid Equation")
                return
    
        #-----------Substituting by the input range of x in the Equation-----------
        limits = [int(self.ui.X_low.text()) , int(self.ui.X_high.text())]   #Getting Max and Min values of x
        X = list(range(limits[0], limits[1]+1))     #Generating a range of numbers between x_Max & x_Min
        equ = ''.join(equ_splitted)     #Concatanating the equation again to evaluate in easier
        equ = equ.replace('^',"**")     #Power operator
        var = [0] * len(X)      #List to store the values to be plotted
        for i in range(len(X)):
            x = X[i]
            var[i] = eval(equ)
        
        #-----------Plotting the input function-----------
        t  =  np . linspace ( limits[0] , limits[1] , len(var))
        self . ui . MplWidget . canvas . axes . clear ()
        self . ui . MplWidget . canvas . axes . set_title ( 'f(x) = ' + temp1 )
        self . ui . MplWidget . canvas . axes . set_xlabel ( 'x' )
        self . ui . MplWidget . canvas . axes . set_ylabel ( 'f(x)' )
        self . ui . MplWidget . canvas . axes . plot( t ,  var )
        self . ui . MplWidget . canvas . draw ()
        self . ui . Log . setText("Plot Generated Successfully")

# ------------------ Displaying the GUI ------------------         
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QApplication.instance()
if app is None: 
    app = QApplication([])

window  =  MainWidget () 
window . show () 
app . exec_ ()
