"""
Created on Thu May 13 00:26:08 2021

@author: Ahmed Reda
"""
import pytest
from  PySide2.QtWidgets  import * 
from PySide2 import QtCore ,QtWidgets

import Function_Plotter



#Test Case: 1--> Correct Input
def test_log_after_click_1(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"2*x^2 + 3*x^5")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"-15")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Plot Generated Successfully"
    
#Test Case: 2--> Equation contains other variable than lower case x (Incorrect Input)
def test_log_after_click_2(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"2a*x^2 + 3*x^5")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"-15")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please write the equation in terms of x"
    
#Test Case: 3--> 2 operators after each other (Incorrect Input)
def test_log_after_click_3(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"2**x^2 + 3*x^5")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"-15")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid Equation"
    
#Test Case: 4--> Max and Min values of x aren't numbers (Incorrect Input)
def test_log_after_click_4(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"2x^2 + 3*x^5")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"abc")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"xyz")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid range of X"
    
#Test Case: 5--> Only one character input either than x (Incorrect Input)
def test_log_after_click_5(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"*")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"-25")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid Equation"
    
#Test Case: 6--> x_Min is greater than x_Max  (Incorrect Input)
def test_log_after_click_6(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"x")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"25")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"20")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid range of X"
    
#Test Case: 7--> first input character is '*' or '/' or '^'  (Incorrect Input)
def test_log_after_click_7(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"*x")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"20")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid Equation"
    
#Test Case: 8--> Last input character is an operator  (Incorrect Input)
def test_log_after_click_8(qtbot):
    app = Function_Plotter.MainWidget()
    
    qtbot.keyClicks(app.ui.Equation,"x^5 + 6 +")    #Input to Equation Slot
    qtbot.keyClicks(app.ui.X_low,"20")     #Input to x_Min slot
    qtbot.keyClicks(app.ui.X_high,"25")     #Input to x_Max slot
    qtbot.wait(10)  #Waiting some time to press the plot button
    qtbot.mouseClick(app.ui.pushButton_plot, QtCore.Qt.LeftButton)
    
    assert app.ui.Log.text() == "Please enter a valid Equation"