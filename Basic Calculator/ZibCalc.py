#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys #to get the exit function to cleanly exit the app
from functools import partial #use this function to connect signals with methods that need to take extra arguments
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget)

ERROR_MSG = "ERROR"
WINDOW_SIZE = 235 #creates a constant to hold window size
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40 #square with 40 pixel size

class ZibCalcWindow(QMainWindow): #ZibCalc's main window usng only GUI
    def __init__(self): #defines class initializer
        super().__init__() #calls initializer
        self.setWindowTitle('Zib Calculator') #set window title
        self.setFixedSize(WINDOW_SIZE,WINDOW_SIZE) #set fixed size 235x235
        self.generalLayout = QVBoxLayout() #make a layout of a vertical box
        centralWidget = QWidget(self) #create a QWidget to set it as a central widget
        centralWidget.setLayout(self.generalLayout) #general layout places display at top and keys at the bottom
        self.setCentralWidget(centralWidget) #will be the parent of all widgets we add
        self._createDisplay()
        self._createButtons()
        
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT) #hold the dispaly at constant height
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight) #have the text left aligned
        self.display.setReadOnly(True) #read only to prevent editing by the user
        self.generalLayout.addWidget(self.display) #adds display to the calculator general layout
        
    def _createButtons(self):
        self.buttonMap = {} #creates an empty dictionary to hold the calculator buttons
        buttonsLayout = QGridLayout() #create a list of lists to store key labels
        keyBoard = [ #map the list of lsit for buttons. each list is a row
            ['7','8','9','/','C'],
            ['4','5','6','*','('],
            ['1','2','3','-',')'],
            ['0','00','.','+','=']
        ]
        for row, keys in enumerate (keyBoard): #outer loops iterates over each row
            for col, key in enumerate(keys): #inner row iterates for each index in the row
                self.buttonMap[key] = QPushButton(key) #make the button and add them to the button map
                self.buttonMap[key].setFixedSize(BUTTON_SIZE,BUTTON_SIZE) #resize the button
                buttonsLayout.addWidget(self.buttonMap[key],row,col) #add the button to the layout
        self.generalLayout.addLayout(buttonsLayout) #embed the grid layout into the calculator layout
        
    def setDisplayText(self,text): #set the display's text
        self.display.setText(text) #set and update the display's text
        self.display.setFocus() #set the cursor's focus on the display
    
    def displayText(self): #get the display's text
        return self.display.text()
    
    def clearDisplay(self): #clear the display's text
        self.setDisplayText('')     

def evaluateExpression(expression): #evaluate an expression
    try: #evalute the epression that gets solved and convert into a string. if successful, return the result
        result = str(eval(expression, {}, {})) #to note eval is a dangerous function!
    except Exception: #otherwise return an error message
        result = ERROR_MSG
    return result

class ZibCalc: #controller class to connect to GUI
    def __init__(self, model, view): #define the class initializer, which takes two arguments: the app’s model and its view
        self._evaluate = model # store model arguments in appropriate instance attributes
        self._view = view # store view arguments in appropriate instance attributes
        self._connectSignalsAndSlots() #make all the required connections of signals and slots
        
    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText()) #evaluate the math expression just typed into the calculator’s display
        self._view.setDisplayText(result) #update the display text with the computation result
    
    def _buildExpression(self,subExpression): #takes care of building the target math expression
        if self._view.displayText == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression #concatenates initial display value with every new value entered on calculator’s keyboard
        self._view.setDisplayText(expression)
    
    def _connectSignalsAndSlots(self): #connects all the buttons’ .clicked signals with the appropriate slots method in the controller class
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {'=','C'}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        self._view.buttonMap['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap['C'].clicked.connect(self._view.clearDisplay)

def main(): #defines calculator's main function
    zibcalcApp = QApplication([]) #create a QApplication object
    zibcalcWindow=ZibCalcWindow() #create instance of app's window
    zibcalcWindow.show() #shows GUI
    ZibCalc(model=evaluateExpression, view=zibcalcWindow)
    sys.exit(zibcalcApp.exec()) #used to cleanly terminate the app , runs application's event loop
        
if __name__ == '__main__': #executes calculator app
    main()


# In[ ]:




