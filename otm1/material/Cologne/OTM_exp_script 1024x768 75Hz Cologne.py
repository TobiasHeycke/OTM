# -*- coding: utf-8 -*-

#coded in PsychoPy v1.83.04
#wrote for 75Hz monitors - in frames

#import python functions
from psychopy import visual, sound, core, gui, event, logging, __version__
from random import shuffle
from socket import gethostname
import datetime
import time
import os
import sys, platform
import codecs

# ###########################################################################################################################
# Function definition
# ###########################################################################################################################

#Function that waits for space key to continue (used for the instruction amd demographic pages)
def furtherFunction():
    further = True
    keyPress = ""
    while further:
        keyPress = event.waitKeys(keyList = 'space')
        if keyPress == ['space']:
            further = False

#Used for text presentation on last page, e must be pressed to finish experiment
def LastPage(textOnPage):
    instr = visual.TextStim(window, text= textOnPage, color = "white")
    instr.draw()
    window.flip()
    further = True
    keyPress = ""
    while further:
        keyPress = event.waitKeys(keyList = 'e')
        if keyPress == ['e']:
            further = False

# Function that helps getting a list from a txt file into a python list
def getList (listname):
    wordList = []
    for eachLine in range(len(listname)) :
        currentWord = listname[eachLine][:-1]
        wordList.append(currentWord) 
    return wordList

# Function reading txt files and saves each line as one element in list (able to use all utf 8 symbols)
def ReadTxt(File, remove):
    tL = []
    with codecs.open(File, "r", encoding = "utf-8") as my_file:
        lines = my_file.readlines()
        tL.append(lines)
    my_file.close()
    l = []
    for eachLine in range(len(tL[0])) :
        currentWord = tL[0][eachLine][:remove]
        l.append(currentWord) 
    return(l)

#function used for instruction: disyplays text on a page and continues when space is pressed
def instructionPage(textOnPage):
    instr = visual.TextStim(window, text= textOnPage, color = "white")
    instr.draw()
    window.flip()
    furtherFunction()

#start with 1000 ms blank, then shows a fixcross, then a word prime for 2 frames and an images afterwards for 250ms
def subliminalTrial (prime, bob):
    fixcross = visual.TextStim(window, text = "+", pos = (0,0), color = "white", font = "Times New Roman", bold = True)
    prime_stim = visual.TextStim(window, text= prime, pos = (0, 0), color = "white", font = "Times New Roman", bold = True)
    bob_stim = visual.ImageStim(window, image = bob, pos = (0,0))
    blank = visual.TextStim(window, text = "", pos = (0,0))
    for frameN in range(112):
        if 1<=frameN<76:
            blank.draw()
        if 76<=frameN<91:
            fixcross.draw()
        if 91<=frameN<93:
            prime_stim.draw()
        if 93<=frameN<112:
            bob_stim.draw()
        window.flip()

#function showing a 'correct' for 5000 ms
def posFeedback():
    correct = visual.TextStim(window, text = "Richtig", pos = (0,0), color = 'green')
    for frameN in range(376):
        if 1<=frameN<376:
            correct.draw()
        window.flip()

#function showing a 'wrong' for 5000 ms
def negFeedback():
    wrong = visual.TextStim(window, text = "Falsch", pos = (0,0), color = 'red')
    for frameN in range(376):
        if 1<=frameN<376:
            wrong.draw()
        window.flip()

#first calls the subliminal trial function and then shows an image and written behavior and waits for response
def trial(prime, bob, bobName, behavior, Valence):
    bob_stim = visual.ImageStim(window, image = bob, pos = (0,0))
    behavior_stim = visual.TextStim(window, text = BobName +" "+ behavior, pos = (0,-250), color = 'white')
    instruction_key_d = visual.TextStim(window, text = "c = charakteristisch", pos = (-350, -350), color = 'white')
    instruction_key_k = visual.TextStim(window, text = "u = uncharakteristisch", pos = (350, -350), color = 'white')
    subliminalTrial(prime, bob)
    bob_stim.draw()
    behavior_stim.draw()
    instruction_key_d.draw()
    instruction_key_k.draw()
    window.flip()
    timer.reset() 
    response = event.waitKeys(keyList = ('c', 'u', "1")) #, timeStamped=clock
    responseNumber = response[0][0]
    TrialRT = timer.getTime()
    correctBehav = "Correct"
    #check if experiment should be aborted
    if responseNumber == "1":
        outputFile = open('./data/AbortMassage_OTM_'+str(ParticipantNumber)+'.dat', 'a') #Save create a txt and participantnumber in it
        outputFile.write("%s\t%s" % ("This participant pressed the 1 key during the learning phase", timeStamp)) 
        outputFile.close()
        core.quit() 
    #now check if answer was correct and give feedback
    if Block == 1 and ValenceBlock == 1 and Valence == "pos" and responseNumber == "c":
        posFeedback()
    elif Block == 1 and ValenceBlock == 1 and Valence == "neg" and responseNumber == "u":
        posFeedback()
    elif Block == 1 and ValenceBlock == 2 and Valence == "pos" and responseNumber == "u":
        posFeedback()
    elif Block == 1 and ValenceBlock == 2 and Valence == "neg" and responseNumber == "c":
        posFeedback()
    elif Block == 2 and ValenceBlock == 1 and Valence == "pos" and responseNumber == "u":
        posFeedback()
    elif Block == 2 and ValenceBlock == 1 and Valence == "neg" and responseNumber == "c":
        posFeedback()
    elif Block == 2 and ValenceBlock == 2 and Valence == "pos" and responseNumber == "c":
        posFeedback()
    elif Block == 2 and ValenceBlock == 2 and Valence == "neg" and responseNumber == "u":
        posFeedback()
    else:
        negFeedback()
        correctBehav = "False"
    outputFile = codecs.open('./data/DataTrials_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%s\t%s\t%s\t%s\t%s\n" % (int(ParticipantNumber), "Cologne", prime, bob, bobName, behavior, Valence, responseNumber, correctBehav, TrialRT, Block, ValenceBlock, Valence, computerName, timeStamp))
    outputFile.close()

#first explicit evalaution
def liking1(InstructionLiking1):
    myRatingScale = visual.RatingScale(window, low= 1, high=9, skipKeys=None, stretch = 1.4, scale = (u'Sehr unliebenswürdig                             \t\t\t\t\t\t\t\t                           Sehr liebenswürdig'), \
    textSize = 0.4, size = 1.55, textColor = 'white', lineColor = 'white', showValue=False, pos=[0,-30], \
    tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", acceptSize = 2.2, mouseOnly = True) 
    instr = visual.TextStim(window, text=InstructionLiking1, pos = (0, 50), color = 'white')
    while myRatingScale.noResponse:
        instr.draw()
        myRatingScale.draw()
        window.flip()
    likingRating = myRatingScale.getRating()
    likingRT = myRatingScale.getRT()
    window.flip()
    core.wait(0.2)
    return(likingRating)

#multiple explicit evaluations
def liking2(InstructionLiking2):
    myRatingScale1 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Schlecht \t\t\t\t\t\t\t\t\t\t Gut"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,260], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", \
    acceptSize = 2.2, mouseOnly = True, name='gutschlecht') 
    
    myRatingScale2 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Gemein \t\t\t\t\t\t\t\t\t\t Freundlich"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,115], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", \
    acceptSize = 2.2, mouseOnly = True, name='freundlichgemein')
    
    myRatingScale3 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Unangenehm \t\t\t\t\t\t\t\t\t\t Angenehm"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-30], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", \
    acceptSize = 2.2, mouseOnly = True, name='disagreeable') 
    
    myRatingScale4 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Gefühllos \t\t\t\t\t\t\t\t\t\t Fürsorglich"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-175], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", \
    acceptSize = 2.2, mouseOnly = True, name='uncaring') 
    
    myRatingScale5 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Grausam \t\t\t\t\t\t\t\t\t\t Nett"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-320], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Bitte klicken Sie auf die Linie", acceptText = "Akzeptieren", \
    acceptSize = 2.2, mouseOnly = True, name='cruelkind') 
    
    instr = visual.TextStim(window, text=InstructionLiking2, pos = (0, 350), color = 'white')
    
    event.clearEvents()
    while myRatingScale1.noResponse or myRatingScale2.noResponse or myRatingScale3.noResponse or myRatingScale4.noResponse or myRatingScale5.noResponse:
        myRatingScale1.draw()
        myRatingScale2.draw()
        myRatingScale3.draw()
        myRatingScale4.draw()
        myRatingScale5.draw()
        instr.draw()
        window.flip()
    return(myRatingScale1.getRating(), myRatingScale2.getRating(), myRatingScale3.getRating(), myRatingScale4.getRating(), myRatingScale5.getRating())
        
        
# feeling thermomenter question use in explicit ratings
def liking3(InstructionLiking3):
    Question = visual.TextStim(window, pos=(0, -250), text=InstructionLiking3, color = 'white')
    Instruction = visual.TextStim(window, pos=(0, 0), text=u"POSITIV\t\t\t100°\tÄußerst Positiv\n\t\t\t\t90°\tSehr Positiv\n\t\t\t\t80°\tZiemlich Positiv\
    \n\t\t\t\t70°\tEher Positiv\n\t\t\t\t60°\tkaum Positiv\n\t\t\t\t50°\tWeder Positiv noch Negativ\n\t\t\t\t40°\tkaum Negativ\n\t\t\t\t30°\tEher Negativ\n\t\t\t\t20°\tZiemlich Negativ\n\t\t\t\t10°\tSehr \
Negativ\nNEGATIV\t\t\t0°\tÄußerst Negativ. \
\n\nBitte geben Sie anhand der oben gegebenen Skala eine Zahl \
zwischen 0° und 100° an, um anzuzeigen wie Sie " + BobName + u" bewerten. Tippen Sie Ihre Antwort (zwischen 0 und 100) ein, \
und drücken Sie anschließend *Enter*.", color = 'white')
    CapturedResponseString = visual.TextStim(window, pos=(85, -250), text='', color = 'white')
    underscore = visual.TextStim(window, pos = (85, -250), text = "_", color = 'white')
    captured_string = ''
    Question.draw()
    underscore.draw()
    Instruction.draw()
    window.flip()
    subject_response_finished = 0
    while subject_response_finished == 0:
        for key in event.getKeys():
            if key in ['return']:
                #if len(captured_string)< 4 and len(captured_string)> 0:
                if len(captured_string) > 0:
                    if int(captured_string) >= 0 and int(captured_string) <= 100:
                        #print 'participant typed %s' %captured_string
                        return(captured_string)
                        captured_string = ''
                        subject_response_finished = 1
                    break
            elif key in ['delete','backspace']:
                captured_string = captured_string[:-1] #delete last character
                CapturedResponseString.setText(captured_string)
                CapturedResponseString.draw()
                Question.draw()
                Instruction.draw()
                window.flip()
            elif key in ['lshift','rshift']:
                pass
            elif key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                captured_string = captured_string+key
                CapturedResponseString.setText(captured_string)
                CapturedResponseString.draw()
                Question.draw()
                Instruction.draw()
                window.flip()
    
#explicit evaluation block 
def likingBlock():
    instructionPage(u"Bitte beantworten Sie die folgenden Fragen über Ihre Eindrücke von Bob, indem Sie die Skalen auf den folgenden Seiten nutzen. \
Es ist gut möglich, dass Sie sich bei einigen Antworten nicht vollständig sicher sind, antworten Sie dann bitte einfach so gut wie möglich. \
Bitte klicken Sie auf die Skala, um einen Wert zwischen 1 und 9 auszuwählen, der mit Ihrem Eindruck von Bob übereinstimmt.  Sobald Sie auf die Skala geklickt haben \
erscheint ein blaues Dreieck, das Sie mit der Computermaus einstellen können. Wenn ihr Rating endgültig ist, klicken Sie auf den Button *Akzeptieren*. \
\n\n*Um die Aufgabe zu beginnen, drücken Sie die Leertaste....*")
    mouse = event.Mouse(visible=True)
    l1 = liking1("Wie liebenwert ist " + BobName + "?")
    l2, l3, l4, l5, l6 = liking2("Ich denke, " + BobName + " ist:")
    mouse = event.Mouse(visible=False)
    instructionPage(u"Wir interessieren uns für die Einstellungen von Menschen gegenüber " + BobName + u". \
Untenstehend sehen Sie etwas, das aussieht wie ein Thermometer. Dieses sollen Sie dazu nutzen, Ihre Einstellung gegenüber " + BobName + u" anzugeben \
Es funktioniert wie folgt: Wenn Sie eine positive Einstellung zu Bob haben, würden Sie ihm einen Wert zwischen 50° und 100° geben, abhängig davon, wie positiv Ihre Bewertung von Bob ist. \
Andersherum würden Sie, wenn Sie eine negative Einstellung zu Bob haben, ihm einen Wert zwischen 0° und 50° geben, abhängig davon, wie negativ Ihre Bewertung von Bob ist. \
Die Bezeichnungen der Stufen sollen Ihnen dabei helfen, Ihre Einstellung auf dem Thermometer zu positionieren. Dabei sind Sie nicht auf die angegebenen Zahlen beschränkt — gerne können Sie eine beliebige Zahl zwischen 0° und 100° auswählen. \
Bitte seien Sie ehrlich. Ihre Antwort wird komplett vertraulich behandelt. \
\n\n*Weiter mit der Leertaste...*")
    l7 = liking3("Ihre Antwort:")
    outputFile = codecs.open('./data/DataEval_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Cologne", BobName, int(l1), int(l2), int(l3), int(l4), int(l5), int(l6), int(l7), int(Block), int(ValenceBlock), int(MeasureOrder), computerName, timeStamp))
    outputFile.close()

#function used by Memry test function (making sure words are colored red when chosen and white while not chosen)
def refresh(wordList, colorList, CoordinatesList, word, Instruction, ExitText):
    for i, eachWord in enumerate(wordList):
        word.setPos(CoordinatesList[i])
        word.setColor(colorList[i])
        word.setText(wordList[i])
        word.draw()
    Instruction.draw()
    ExitText.draw()
    window.flip()

#function used by prime word memory test (coloring words when participants click on them)
def colorCheck(pos, colorList):
    if colorList[pos] == "white":
        colorList[pos] = "red"
    else:
        colorList[pos] = "white"

#Prime word memory test function
def MemoryTest():
    wordList = memTestDis + posPrime + negPrime
    shuffle(wordList)
    colorList = 40*["white"]
    j = 0
    CoordinatesList = []
    x = -350
    y = 260
    for i in range(40):
        tmpList = (x, y)
        CoordinatesList.append(tmpList)
        j += 1
        if j <= 5:
            x += 140
        elif j == 6:
            x = -350
            y = 180
        elif j > 6 and j <=11:
            x += 140
        elif j == 12:
            x = -350
            y = 100
        elif j > 12 and j <=17:
            x += 140
        elif j == 18:
            x = -350
            y = 20
        elif j > 18 and j <= 23:
            x += 140
        elif j == 24:
            x = -350
            y = -60
        elif j > 24 and j <= 29:
            x += 140
        elif j == 30:
            x = -350
            y = -140
        elif j > 30 and j <= 35:
            x += 140
        elif j == 36:
            x = -350
            y = -220
        else:
            x += 140
    word = visual.TextStim(window, color = "white")
    Instruction = visual.TextStim(window, text = u"Bitte wählen Sie die 20 Wörter aus der Liste aus, von denen Sie denken, dass sie in der Lernphase vor einem Bild von Bob erschienen sind.", pos = (0, 330), color = "white")
    ExitText = visual.TextStim(window, text = "Speichere die Antwort und mache weiter", pos = (0, -300), color = "white")
    refresh(wordList, colorList, CoordinatesList, word, Instruction, ExitText)
    while True:
        mouseIsDown = mouse.getPressed()[0]
        mouse.clickReset()
        if mouseIsDown and not oldMouseIsDown:
            for i, position in enumerate(CoordinatesList):
                if mouse.getPos()[0] in range((CoordinatesList[i][0]-50),(CoordinatesList[i][0]+50)) and mouse.getPos()[1] in range((CoordinatesList[i][1]-20),(CoordinatesList[i][1]+20)):
                    colorCheck(i, colorList)
                    refresh(wordList, colorList, CoordinatesList, word, Instruction, ExitText)
            if mouse.getPos()[0] in range(-160, 160) and mouse.getPos()[1] in range(-320, -280):
                redCounter = 0
                chosenItems = []
                for p, item in enumerate(colorList):
                    if item == "red":
                        redCounter += 1
                        chosenItems.append(wordList[p])
                if redCounter == 20:
                    cList = []
                    for i in chosenItems:
                        c = "correctIdent"
                        if i in memTestDis:
                            c = "falseIdent"
                        cList.append(c)
                    
                    break
                else: 
                    NumberText = visual.TextStim(window, text = u"Bitte wählen Sie 20 Wörter aus! Momentan haben Sie "+str(redCounter)+u" Wörter ausgewählt.", pos = (0, -340), color = "red", height = 12, italic=True)
                    for i, eachWord in enumerate(wordList):
                        word.setPos(CoordinatesList[i])
                        word.setColor(colorList[i])
                        word.setText(wordList[i])
                        word.draw()
                    Instruction.draw()
                    ExitText.draw()
                    NumberText.draw()
                    window.flip()
        oldMouseIsDown = mouseIsDown
    outputFile = codecs.open('./data/DataMemTest_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%d\t%d\t%d\t%s\t%s\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Cologne", int(Block), int(ValenceBlock), int(cList.count("correctIdent")), str(chosenItems), str(cList), int(MeasureOrder), computerName, timeStamp))
    outputFile.close()

#shuffle list until no more than 5 repetitions of same key and about same amount of switchs and repetitions
def shuffleIATList(orderList):
    tmpL = ["d", "k"]
    shuffle(tmpL)
    lastKey = tmpL[0]
    while True:
        sameCount = 0
        switchCount = 0
        dCount = 0
        kCount = 0
        stop = 1
        stop2 = 0
        shuffle(orderList)
        for S, C, T, K in orderList:
            if K == "d":
                dCount +=1
            else:
                dCount = 0
            if K == "k":
                kCount +=1
            else:
                kCount = 0
            if dCount == 5:
                stop = 0
            if kCount == 5:
                stop = 0
            if lastKey == K:
                sameCount += 1
            else:
                switchCount += 1
            lastKey = K
        if sameCount == switchCount:
            stop2 = 1
        if stop + stop2 == 2:
            break
    return(orderList)

#one IAT trial
def IATTrial(Stim, Cat, Type, key, Instr, B):
    Correct = "correct"
    if Cat == "Image":
        thisTarget = visual.ImageStim(window, image = Stim, pos = (0,0))
    else:
        thisTarget = visual.TextStim(window, text = Stim, pos = (0,0), color = "white", height = 30)
    wrong = visual.TextStim(window, text = "X", pos = (0,-250), color = 'red', height = 45)
    blank = visual.TextStim(window, text = "", pos = (0, 0))
    leftInstr = visual.TextStim(window, text = Instr[0], pos = (-370, -300), color = "lightblue")
    rightInstr = visual.TextStim(window, text= Instr[1], pos = (350, -300), color = "lightblue")
    thisTarget.draw()
    leftInstr.draw()
    rightInstr.draw()
    window.flip()
    timer.reset() 
    keyPress = event.waitKeys(keyList = ('d', 'k'))
    RT2 = 0
    RT = timer.getTime()
    if keyPress[0] != key:
        Correct = "error"
        wrong.draw()
        leftInstr.draw()
        rightInstr.draw()
        thisTarget.draw()
        window.flip()
        SecondKeyPress = event.waitKeys(keyList = key)
        RT2 = timer.getTime()
    for frameN in range(20):
        if 1<=frameN<20:
            leftInstr.draw()
            rightInstr.draw()
            blank.draw()
        window.flip()
    outputFile = codecs.open('./data/DataIAT_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%f\t%d\t%d\t%d\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Cologne", int(B), Stim, Cat, Type, key, keyPress, Correct, RT, RT2, int(Block), int(IATblock), int(ValenceBlock), int(MeasureOrder), computerName, timeStamp))
    outputFile.close()

#IAt block (including instructions)
def IAT():
    instructionPage(u"Als nächstes werden Ihnen nacheinander Bilder von "+ BobName + u" und anderen Personen gezeigt. \nIhre Aufgabe ist es, diese entsprechend ihrer Zugehörigkeit zu klassifizieren \
(Ist es "+ BobName +u" oder nicht "+ BobName +u"?).\n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Für die Klassifikation der Bilder sollen Sie die 'd'- und die 'k'-Taste benutzen.\n\nDie 'd'-Taste wird von nun an als 'linke Taste' und die 'k'-Taste als 'rechte Taste' bezeichnet. \
Drücken Sie die linke Taste, wenn ein Bild von "+IATInstr1[2]+" erscheint und die rechte Taste wenn ein Bild von "+IATInstr1[3]+" erscheint.\n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Bitte reagieren Sie bei der Klassifikation der Bilder so schnell wie möglich. Gleichzeitig sollten Sie aber möglichst wenig Fehler machen.\n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Wenn Sie einen Fehler machen, erscheint unterhalb des Bildes ein rotes X. Drücken Sie dann möglichst schnell die korrekte Taste, um die Aufgabe fortsetzen zu können.\n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Die korrekte Tastenbelegung wird während der gesamten Aufgabe angezeigt. \n\nLinks unten steht, auf welches Bild Sie mit der linken Taste reagieren sollen ("+IATInstr1[0]+"). \
Rechts unten steht, auf welches Bild Sie mit der rechten Taste reagieren sollen ("+IATInstr1[1]+"). \n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Legen Sie nun Ihre Zeigefinger auf die beiden Tasten ('d' und 'k').\n\nUm schneller reagieren zu können, lassen Sie Ihre Zeigefinger während der gesamten Aufgabe dort liegen. \n\n\n*Drücken Sie die Leertaste, um mit der Aufgabe zu beginnen.*")
    for SB1, CB1, TB1, kB1 in IATB1:
        IATTrial(SB1, CB1, TB1, kB1, IATInstr1, 1)
    instructionPage(u"Als nächstes sollen Sie Wörter als 'positiv' oder 'negativ' klassifizieren.\nDrücken Sie die linke Taste, wenn ein "+IATInstr2[2]+u" Wort erscheint. Drücken Sie die rechte Taste, wenn ein "+IATInstr2[3]+u" Wort erscheint. \
Wenn Sie einen Fehler machen, erscheint ein rotes X.\n\nDrücken Sie dann möglichst schnell die korrekte Taste. \n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Legen Sie nun Ihre Zeigefinger wieder auf die beiden Tasten 'd' und 'k'.\n\n\n*Drücken Sie die Leertaste, um mit der Aufgabe zu beginnen.*")
    for SB2, CB2, TB2, kB2 in IATB2:
        IATTrial(SB2, CB2, TB2, kB2, IATInstr2, 2)
    instructionPage(u"Als nächstes sollen Sie beide Aufgaben 'gleichzeitig' bearbeiten. \n\nIn jedem Durchgang erscheint entweder ein Bild einer Person oder ein Wort.\nDrücken Sie die linke Taste, wenn \
"+IATInstr34[2]+u" Wort erscheint. Drücken Sie die rechte Taste, wenn "+IATInstr34[3]+u" Wort erscheint. \n\nWenn Sie einen Fehler machen, erscheint ein rotes X. \nDrücken Sie dann möglichst schnell die korrekte Taste.\
 \n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Legen Sie nun Ihre Zeigefinger wieder auf die beiden Tasten 'd' und 'k'.\n\n\n*Drücken Sie die Leertaste, um mit der Aufgabe zu beginnen.*")
    for SB34, CB34, TB34, kB34 in IATB34:
        IATTrial(SB34, CB34, TB34, kB34, IATInstr34, 34)
    instructionPage(u"Als nächstes sollen Sie wieder die Bilder sortieren, ob diese "+BobName+u" oder eine andere Person zeigen. Allerdings ist die korrekte Tastenbelegung nun umgekehrt!\n\nDrücken Sie die linke Taste, \
wenn ein Bild von "+IATInstr5[2]+u" erscheint und die rechte Taste wenn ein Bild von "+IATInstr5[3]+u" erscheint. \n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Legen Sie nun Ihre Zeigefinger wieder auf die beiden Tasten 'd' und 'k'.\n\n\n*Drücken Sie die Leertaste, um mit der Aufgabe zu beginnen.*")
    for SB5, CB5, TB5, kB5 in IATB5:
        IATTrial(SB5, CB5, TB5, kB5, IATInstr5, 5) 
    instructionPage(u"Nun folgt wieder eine 'Doppel'-Aufgabe! In jedem Durchgang erscheint nun wieder ein Bild einer Person oder ein Wort.\nDrücken Sie die linke Taste, wenn \
"+IATInstr67[2]+u" Wort erscheint. Drücken Sie die rechte Taste, wenn "+IATInstr67[3]+u" Wort erscheint. \n\nWenn Sie einen Fehler machen, erscheint wieder ein rotes X. \nDrücken Sie dann möglichst schnell die korrekte Taste.\
 \n\n*Weiter mit der Leertaste...*")
    instructionPage(u"Legen Sie nun Ihre Zeigefinger wieder auf die beiden Tasten 'd' und 'k'.\n\n\n*Drücken Sie die Leertaste, um mit der Aufgabe zu beginnen.*")
    for SB67, CB67, TB67, kB67 in IATB67:
        IATTrial(SB67, CB67, TB67, kB67, IATInstr67, 67)
    
#open response function for demographic questions
def openendedResponse(question, OutputName, bgstim1=None, bgstim2=None):
    #make unders to indicate participants can type and instruction to save answer by pressing return
    underscore = visual.TextStim(window, text='_', pos=(0, 0), color = (0, 0, 0))
    if bgstim1 != None:
        underscore.setPos(newPos = (0,0))
    instruction = visual.TextStim(window, text=u'Bitte drücken Sie *Enter*, um ihre Antwort abzugeben.', italic=True, pos=(0,300), color = "white")
    openFilmQuestions=visual.TextStim(window, text=question, pos=(0,100), color = "white")
    #show question, underscore, and instruction
    openFilmQuestions.draw()
    underscore.draw()
    instruction.draw()
    if bgstim1 != None:
        for i in range(len(bgstim1)):
            bgstim1[i].draw()
    if bgstim2 != None:
        for i in range(len(bgstim2)):    
            bgstim2[i].draw()
    window.flip()
    #response loop
    response = ''
    lastKey = ''
    keyboardTranslation = {
    'space' : (' ', ' '), 
    'comma' : (',', '<'),
    'period' : ('.', '>'),
    'slash' : ('/', '?'),
    '1' : ('1', '!'),
    '2' : ('2', '"'),
    '3' : ('3', '§'),
    '4' : ('4', '$'),
    '5' : ('5', '%'),
    '6' : ('6', '&'),
    '7' : ('7', '/'),
    '8' : ('8', '('),
    '9' : ('9', ')'),
    '0' : ('0', '='),
    'equal' : ('=', '+'),
    'semicolon' : (';', ':'),
    'apostrophe': ('\'', '"'),
    'minus' : ('-', '_'),
    'bracketleft' : ('[', '{'),
    'bracketright' : (']', '}'),
    'backslash' : ('\\', '|'),
    'quoteleft' : ('`', '~'),
    'q' : ('q', 'Q'),
    'w' : ('w', 'W'),
    'e' : ('e', 'E'),
    'r' : ('r', 'R'),
    't' : ('t', 'T'),
    'y' : ('y', 'Y'),
    'u' : ('u', 'U'),
    'i' : ('i', 'I'),
    'o' : ('o', 'O'),
    'p' : ('p', 'P'),
    'a' : ('a', 'A'),
    's' : ('s', 'S'),
    'd' : ('d', 'D'),
    'f' : ('f', 'F'),
    'g' : ('g', 'G'),
    'h' : ('h', 'H'),
    'j' : ('j', 'J'),
    'k' : ('k', 'K'),
    'l' : ('l', 'L'),
    'z' : ('z', 'Z'),
    'x' : ('x', 'X'),
    'c' : ('c', 'C'),
    'v' : ('v', 'V'),
    'b' : ('b', 'B'),
    'n' : ('n', 'N'),
    'm' : ('m', 'M'),
    u'\xf6' : (u'ö', u'Ö'),
    u'\xfc' : (u'ü', u'Ü'),
    u'\xe4' : (u'ä', u'Ä'),
    u'\xdf' : (u'ß', u'?'),
    }
    shift = False
    outputFile = codecs.open('./data/'+OutputName+str(ParticipantNumber)+'.dat', 'a', 'utf-8') #make a separate text document for each participant that saves their responses to the questionnaire
    #typingResponse = True
    while True:
        
        lastKey = event.waitKeys() #save last key participant entered in variable lastKey.
        
        if lastKey[0] == 'lshift' or lastKey[0] == 'rshift':
            shift = True
        elif lastKey[0] == 'backspace':
            response = response[:-1]
        elif lastKey[0] in keyboardTranslation:
            if shift:
                response = response + keyboardTranslation.get(lastKey[0])[1]
                shift = False
            else:
                response = response + keyboardTranslation.get(lastKey[0])[0]
        elif lastKey[0] == 'return':
            if len(response) > 0:
                outputFile.write("\t%s" % (response))
                outputFile.close()
                break
        else:
            response = response
            
        #update screen so participants see what they type
        underscore.setText(response + '_')
        openFilmQuestions.draw()
        underscore.draw()
        instruction.draw()
        if bgstim1 != None:
            for i in range(len(bgstim1)):
                bgstim1[i].draw()
        if bgstim2 != None:
            for i in range(len(bgstim2)):    
                bgstim2[i].draw()
        window.flip()

# ###########################################################################################################################
# End of function definition
# ###########################################################################################################################

#Get participant number with GUI
myDlg = gui.Dlg(title="OTM", pos=(400, 400))
myDlg.addText('Subject Info', color='Black')
myDlg.addField('Participant Number:')
myDlg.show()#you have to call show() for a Dlg (it gets done implicitly by a DlgFromDict)
if myDlg.OK:
    ParticipantNumber = myDlg.data[0]#this will be a list of data returned from each field added in order
    ParticipantNumber = int(ParticipantNumber) #make an integer out of the unicode data
else: print 'user cancelled'

#get host name and set timestamp
computerName = gethostname()
timeStamp = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.%f')

# ###########################################################################################################################
# Create condition numbers based on participant number
# ###########################################################################################################################

# IAT block is used to decide whether combination 1 is in IAT block 3/4 or in block 6/7 (and combination 2 in the other block)
# 1 means Bob and neg first and later Bob and pos
# 2 means Bon and pos first and later Bob and neg
if ParticipantNumber%2 == 1:
    IATblock = 1
else:
    IATblock = 2

# assignment of d and k key is determined by this variable
# 1 means d = neg, k = pos
# 2 means d = pos, k = neg
if ParticipantNumber%4 in (1,2):
    IATkey = 1
else:
    IATkey = 2

# whether participants always have the implicit or explicit measure first is determined by this variable
# 1 means implicit measure first
# 2 means explicit measure first
if ParticipantNumber%8 in (1, 2, 3, 4):
    MeasureOrder = 1
else:
    MeasureOrder = 2

# whether participants have a negative prime in block 1 or block 2 (and the opposite valence of behavior)
# 1 means negative primes and positive behavior in block 1
# 2 means positive primes and negative behavior in block 1
if ParticipantNumber%16 in (1, 2, 3, 4, 5, 6, 7, 8):
    ValenceBlock = 1
else:
    ValenceBlock = 2

# ###########################################################################################################################
# Set name of Bob used for this participant - inactive: only Bob is used in this Experiment
# ###########################################################################################################################

BobList = ["Bob"] #, "Tim", "Tom", "Jan", "Ben"]
#shuffle(BobList)
BobName = BobList[0]

BobNameTrials = []
BobNameTrials = 100*[BobName]

# ###########################################################################################################################
# Set image of Bob used for this participant
# ###########################################################################################################################

BobImgList = ["bob1.bmp", "white1.bmp", "white2.bmp", "white3.bmp", "white4.bmp", "white5.bmp"]
shuffle(BobImgList)
BobImage = BobImgList[0]

BobImageTrials = []
BobImageTrials += 100*[BobImage]

# ###########################################################################################################################
# load lists of behaviors
# ###########################################################################################################################

negBehav = ReadTxt(File = "negative_behavior.txt", remove = -1)
posBehav = ReadTxt(File = "positive_behavior.txt", remove = -1)

# shuffle pos and neg list. first 50 elements of both lists are taken as behavior for block 1 - other 50 are taken for block 2
shuffle(negBehav)
shuffle(posBehav)

#block1
Block1Behav = []
Block1Behav = negBehav[0:50]
Block1Behav += posBehav[0:50]

#block2
Block2Behav = []
Block2Behav = negBehav[50:101]
Block2Behav += posBehav[50:101]

#list with 50 times negative and 50 time positive written out to zip to behavior list
ValenceTrials = []
ValenceTrials += 50*["neg"]+50*["pos"]


# ###########################################################################################################################
# load lists of primes
# ###########################################################################################################################

negPrime = ReadTxt(File = "negative_primes.txt", remove = -1)

negPrimeTrials = []
for i in range(10):
    shuffle(negPrime)
    negPrimeTrials += negPrime

posPrime = ReadTxt(File = "positive_primes.txt", remove = -1)

posPrimeTrials = []
for i in range(10):
    shuffle(posPrime)
    posPrimeTrials += posPrime


# ###########################################################################################################################
# create lists for block one
# ###########################################################################################################################

#Block lists in lists are created and the order is shuffled 
if ValenceBlock == 1:
    Block1List = zip(BobImageTrials, BobNameTrials, negPrimeTrials, Block1Behav, ValenceTrials)
    Block2List = zip(BobImageTrials, BobNameTrials, posPrimeTrials, Block2Behav, ValenceTrials)
else:
    Block1List = zip(BobImageTrials, BobNameTrials, posPrimeTrials, Block1Behav, ValenceTrials)
    Block2List = zip(BobImageTrials, BobNameTrials, negPrimeTrials, Block2Behav, ValenceTrials)

shuffle(Block1List)
shuffle(Block2List)

# ###########################################################################################################################
# Create list for distractor words in memory test
# ###########################################################################################################################

memTestDis = ReadTxt("MemTestDistr.txt", -1)

# ###########################################################################################################################
# Create list for IAT
# ###########################################################################################################################

#read target lists
IATpos = ReadTxt("IATpos.txt", -1)
IATneg = ReadTxt("IATneg.txt", -1)

#keylists to test if correct key was pressed
if IATkey == 1 and IATblock == 1:
    keyListB1 = 10*["d"]+10*["k"]
    keyListB2 = 10*["k"]+10*["d"]
    keyListB34 = 10*["d"]+10*["k"]+10*["k"]+10*["d"]
    keyListB5 = 10*["k"]+10*["d"]
    keyListB67 = 10*["k"]+10*["d"]+10*["k"]+10*["d"]
    IATInstr1 = [BobName, "Nicht "+BobName, BobName, "einer anderen Person"]
    IATInstr2 = ["negativ", "positiv", "negatives", "positives"]
    IATInstr34 = [BobName+" \nnegativ", "Nicht "+BobName+" \npositiv", BobName+" oder ein negatives", "eine andere Person oder ein positives"]
    IATInstr5 = ["Nicht "+BobName, BobName, "einer anderen Person", BobName] 
    IATInstr67 = ["Nicht "+BobName+" \nnegativ", BobName+ " \npositiv", "eine andere Person oder ein negatives", BobName+" oder ein positives"]
elif IATkey == 1 and IATblock == 2:
    keyListB1 = 10*["k"]+10*["d"]
    keyListB2 = 10*["k"]+10*["d"]
    keyListB34 = 10*["k"]+10*["d"]+10*["k"]+10*["d"]
    keyListB5 = 10*["d"]+10*["k"]
    keyListB67 = 10*["d"]+10*["k"]+10*["k"]+10*["d"]
    IATInstr1 = ["Nicht "+BobName, BobName, "einer anderen Person", BobName]
    IATInstr2 = ["negativ", "positiv", "negatives", "positives"]
    IATInstr34 = ["Nicht "+BobName+" \nnegativ", BobName+" \npositiv", "eine andere Person oder ein negatives", BobName+" oder ein positives"]
    IATInstr5 = [BobName, "Nicht "+BobName, BobName, "einer anderen Person"]
    IATInstr67 = [BobName+" \nnegativ", "Nicht "+BobName+" \npositiv", BobName+" oder ein negatives", "eine andere Person oder ein positives"]
elif IATkey == 2 and IATblock == 1:
    keyListB1 = 10*["k"]+10*["d"]
    keyListB2 = 10*["d"]+10*["k"]
    keyListB34 = 10*["k"]+10*["d"]+10*["d"]+10*["k"]
    keyListB5 = 10*["d"]+10*["k"]
    keyListB67 = 10*["d"]+10*["k"]+10*["d"]+10*["k"]
    IATInstr1 = ["Nicht "+BobName, BobName, "einer anderen Person", BobName]
    IATInstr2 = ["positiv", "negativ", "positives", "negatives"]
    IATInstr34 = ["Nicht "+BobName+" \npositiv", BobName+" \nnegativ", "eine andere Person oder ein positives", BobName+" oder ein negatives"]
    IATInstr5 = [BobName, "Nicht "+BobName, BobName, "einer anderen Person"]
    IATInstr67 = [BobName+ " \npositiv", "Nicht "+BobName+" \nnegativ", BobName+" oder ein positives", "eine andere Person oder ein negatives"]
elif IATkey == 2 and IATblock == 2:
    keyListB1 = 10*["d"]+10*["k"]
    keyListB2 = 10*["d"]+10*["k"]
    keyListB34 = 10*["d"]+10*["k"]+10*["d"]+10*["k"]
    keyListB5 = 10*["k"]+10*["d"]
    keyListB67 = 10*["k"]+10*["d"]+10*["d"]+10*["k"]
    IATInstr1 = [BobName, "Nicht "+BobName, BobName, "einer anderen Person"]
    IATInstr2 = ["positiv", "negativ", "positives", "negatives"]
    IATInstr34 = [BobName+" \npositiv", "Nicht "+BobName+" \nnegativ", BobName+" oder ein positives", "eine andere Person oder ein negatives"]
    IATInstr5 = ["Nicht "+BobName, BobName, "einer anderen Person", BobName]
    IATInstr67 = ["Nicht "+BobName+" \npositiv", BobName+ " \nnegativ", "eine andere Person oder ein positives", BobName+" oder ein negatives"]
else:
    print("Error in key list creation")

#block 1 lists
StimB1 = 10*[BobImgList[0]]+2*[BobImgList[1]]+2*[BobImgList[2]]+2*[BobImgList[3]]+2*[BobImgList[4]]+2*[BobImgList[5]]
CatB1 = 20*["Image"]
TypeB1 = 10*["Bob"]+10*["NonBob"]

IATB1 = zip(StimB1, CatB1, TypeB1, keyListB1)
shuffle(IATB1)

#block2 Lists
StimB2 = IATpos + IATneg
CatB2 = 20*["Text"]
TypeB2 = 10*["pos"]+10*["neg"]

IATB2 = zip(StimB2, CatB2, TypeB2, keyListB2)
shuffle(IATB2)

#block3 and 4 lists
StimB34 = 10*[BobImgList[0]] + 2*[BobImgList[1]] + 2*[BobImgList[2]] + 2*[BobImgList[3]] + 2*[BobImgList[4]] + 2*[BobImgList[5]] + IATpos + IATneg
CatB34 = 20*["Image"]+20*["Text"]
TypeB34 = 10*["Bob"]+10*["NonBob"]+10*["pos"]+10*["neg"]

IATB34 = zip(StimB34, CatB34, TypeB34, keyListB34)
IATB34 = shuffleIATList(IATB34)

# block 5 lists
StimB5 = 10*[BobImgList[0]]+2*[BobImgList[1]]+2*[BobImgList[2]]+2*[BobImgList[3]]+2*[BobImgList[4]]+2*[BobImgList[5]]
CatB5 = 20*["Image"]
TypeB5 = 10*["Bob"]+10*["NonBob"]

IATB5 = zip(StimB5, CatB5, TypeB5, keyListB5)
shuffle(IATB5)

# block 6 and 7 lists
StimB67 = 10*[BobImgList[0]] + 2*[BobImgList[1]] + 2*[BobImgList[2]] + 2*[BobImgList[3]] + 2*[BobImgList[4]] + 2*[BobImgList[5]] + IATpos + IATneg
CatB67 = 20*["Image"]+20*["Text"]
TypeB67 = 10*["Bob"]+10*["NonBob"]+10*["pos"]+10*["neg"]

IATB67 = zip(StimB67, CatB67, TypeB67, keyListB67)
IATB67 = shuffleIATList(IATB67)


# ###########################################################################################################################
# Set up headers for output txt files
# ###########################################################################################################################

outputFile = codecs.open('./data/DataTrials_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % ("ParticipantNumber", "Location", "prime", "BobImage", "bobName", "behavior", "Valence", "responseNumber", "correctBehav", "TrialRT", "Block", "ValenceBlock", "Valence", "computerName", "timeStamp"))
outputFile.close()

outputFile = codecs.open('./data/DataIAT_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Location", "IATBlock", "Stimulus", "Category", "Type", "keyToPress", "keyPress", "Correct", "RT", "RTafterError", "Block", "Combination", "ValenceBlock", "MeasureOrder", "computerName", "timeStamp"))
outputFile.close()

outputFile = codecs.open('./data/DataEval_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Location", "Name", "Eval1", "Eval2", "Eval3", "Eval4", "Eval5", "Eval6", "Eval7", "Block", "ValenceBlock", "MeasureOrder", "computerName", "timeStamp"))
outputFile.close()

outputFile = codecs.open('./data/DataMemTest_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Location", "Block", "ValenceBlock", "NumbercorrectIdent", "chosenItems", "correctList", "MeasureOrder", "computerName", "timeStamp"))
outputFile.close()

#For the demographic data
outputFile = open("./data/Data_Demographics_OTM_Cologne_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Age", "Study", "Gender", "Goal", "Comment"))
outputFile.close()

#add the participant Number in the first row
outputFile = open("./data/Data_Demographics_OTM_Cologne_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%d" % (ParticipantNumber))
outputFile.close()

# ###########################################################################################################################
# Set up screen
# ###########################################################################################################################

#setup window for screen 1024*768
window=visual.Window(units= "pix", size =(1024,768), rgb = "black", fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()

# This part records the screen refresh rate for 10 frames and saves it with the pp number in the file name in order to ensure that all PC's were set to correct Hz
window.setRecordFrameIntervals(True)
Text1 = visual.TextStim(window, text='', pos = (0, 0))
for frameN in range(10):#for exactly 10 frames
    if 2<=frameN<3:
        Text1.draw()
    window.flip()
window.saveFrameIntervals(fileName="./data/OTM_ScreenLog_Cologne_"+str(ParticipantNumber)+".dat", clear=True)
window.setRecordFrameIntervals(False)

#Additionally save some information about the PC and software in that file
outputFile = open("./data/OTM_Log_Cologne_"+str(ParticipantNumber)+".dat", 'a') 
outputFile.write("%s\t%s\t%s\t%s\n" % (platform.platform(), "PychoPyVersion:", __version__, timeStamp)) 
outputFile.close()

# ###########################################################################################################################
# Actual order of experiment, including instructions (some instructions may be included in functions above)
# ###########################################################################################################################

instructionPage(u"Vielen Dank für Ihre Teilnahme an unserem heutigen Experiment. \
Im ersten Teil der Studie werden wir Ihnen einige Verhaltensweisen einer realen Person namens Bob präsentieren. \
Ihre Aufgabe wird es sein, zu beurteilen, welche Art von Person Bob ist (z.B. er ist nett, er ist gemein, er ist intelligent).\n\n\n*Weiter mit der Leertaste...*")

instructionPage(u"Damit Sie einen Eindruck von Bob bekommen, werden Sie im Folgenden gebeten zu entscheiden, ob Sie glauben, dass bestimmte Verhaltensweisen charakteristisch oder uncharakteristisch für Bob sind. \
Wenn Sie das Verhalten als für Bob charakteristisch einschätzen, dann glauben Sie, dass er dieses Verhalten zeigen würde. \
Wenn Sie das Verhalten als für Bob uncharakteristisch einschätzen, dann glauben Sie nicht, dass er dieses Verhalten zeigen würde.\n\n\n*Weiter mit der Leertaste...*")

instructionPage(u"Verständlicherweise werden Sie zu Beginn der Aufgabe nur raten können, da Sie nicht wissen, was für eine Person Bob ist. \
Das Feedback, welches Sie bekommen, ob ihre Einschätzung über Bob richtig war, sollen Sie verwenden, um einen Eindruck von Bob zu bekommen.\
Wenn ein Verhalten uncharakteristisch für Bob ist, würde er dieses Verhalten nicht zeigen und wahrscheinlich das gegenteilige Verhalten zeigen.\n\n\n*Weiter mit der Leertaste...*")

instructionPage(u"Nach dieser ersten Aufgabe werden Sie den zweiten Teil des Blocks bearbeiten: Einen Fragebogen und eine kognitive Aufgabe. \
Sie sollten circa 15 Minuten brauchen, um den ersten Teil des Blocks zu bearbeiten und 15 Minuten für den zweiten Teil (d.h. für den Fragebogen und die kognitive Aufgabe). \
\n\n\n*Weiter mit der Leertaste...*")

instructionPage(u"Noch einmal: Es ist Ihre Aufgabe zu bestimmen, ob die aufgeführten Verhaltensweisen charakteristisch oder uncharakteristisch für Bob sind. Bitte antworten Sie so schnell und so akkurat wie möglich, indem Sie \
bei für Bob charakteristischen Verhaltensweisen die Taste *c* drücken und bei für Bob uncharakteristischen Verhaltensweisen die Taste *u* drücken. \
Beruhend auf ihrer Fähigkeit einzuschätzen, ob die aufgeführten Verhaltensweisen charakteristisch oder uncharakteristisch für Bob sind, sollten Sie einen Eindruck von Bob bekommen. \n\n\n*Weiter mit der Leertaste....*")

instructionPage(u"Mit anderen Worten, Sie sollen lernen, welche Art von Person Bob ist, indem Sie die dargestellten Verhaltensweisen lesen, einschätzen und feststellen, ob ihre Einschätzung richtig oder falsch war. \
Zur Erinnerung, wenn das Verhalten charakteristisch für Bob ist, dann würde er dieses Verhalten mit hoher Wahrscheinlichkeit zeigen, aber wenn das Verhalten uncharakteristisch für Bob ist, dann würde er sich nicht auf diese Weise verhalten \
und würde mit hoher Wahrscheinlichkeit das gegenteilige Verhalten zeigen. \n\n\n*Weiter mit der Leertaste...*")

instructionPage(u"Falls Sie irgendwelche Fragen haben, wenden Sie sich bitte an den Versuchsleiter, bevor Sie beginnen. \n\n Wenn Sie bereit sind, damit zu beginnen, etwas über Bob zu lernen, drücken Sie bitte die Leertaste.")

Block = 1

for eachBobImage, eachBobName, eachPrime, eachBehavior, eachValence in Block1List:
    trial(prime= eachPrime, bob = eachBobImage, bobName = eachBobName, behavior= eachBehavior, Valence = eachValence)

instructionPage(u"Sie haben die erste Hälfte des ersten Blocks geschafft. \n\
Sie werden nun gebeten, eine Reihe kognitiver Aufgaben zu bearbeiten und einige Fragen zu beantworten. \n\n\n\
*Weiter mit der Leertaste...*")

#either liking block or IAT first based on MeasureOrder
if MeasureOrder == 1:
    IAT()
    likingBlock()
else:
    likingBlock()
    IAT()


instructionPage(u"Sie werden nun mit dem zweiten Block starten. \n\
Wieder ist es Ihre Aufgabe zu bestimmen, was für eine Art Person Bob ist. \
Damit Sie einen Eindruck bekommen, werden Sie erneut gebeten zu entscheiden, ob das gezeigte Verhalten charackeristisch oder uncharackteristisch für Bob ist. \
Bitte entscheiden Sie, ob das Verhalten für Bob charakteristisch ist oder nicht, indem Sie entweder die *c*-Taste drücken für Verhaltensweisen, die charakteristisch \
für Bob sind oder die *u*-Taste drücken für uncharakteristisches Verhalten von Bob. Bitte antworten Sie so schnell und akkurat wie möglich. \
\n\n\nBitte drücken Sie die Leertaste, wenn Sie bereit sind, etwas über Bob zu lernen.")

Block = 2

for eachBobImage, eachBobName, eachPrime, eachBehavior, eachValence in Block2List:
    trial(prime= eachPrime, bob = eachBobImage, bobName = eachBobName, behavior= eachBehavior, Valence = eachValence)


instructionPage(u"Sie haben nun die erste Hälfte des zweiten - und letzten - Blockes abgeschlossen.\n\
Sie werden wieder gebeten, eine Reihe von kognitiven Aufgaben zu bearbeiten und einige Fragen zu beantworten. \n\n\n \
*Weiter mit der Leertaste...*")

#either liking block or IAT first based on MeasureOrder
if MeasureOrder == 1:
    IAT()
    likingBlock()
else:
    likingBlock()
    IAT()

#Memory Test
instructionPage(u"Während des heutigen Experiments, in welchem Sie etwas über Bob gelernt haben, wurden manchmal Wörter gezeigt, bevor das Bild von Bob auf dem Bildschirm erschien. Auch wenn diese Wörter \
möglicherweise schwer zu erkennen waren, sind Menschen oft sehr gut im Erkennen von Wörtern, die sie lediglich auf einem unbewussten Level wahrgenommen haben. \n\n*Weiter mit der Leertaste...*")
instructionPage(u"Tatsächlich haben Sie 20 der folgenden Wörter vor dem Bild von Bob irgendwann während der heutigen Sitzung gesehen. \
\n\nBitte wählen Sie 20 Wörter aus der Liste auf der nächsten Seite aus, von denen Sie denken, dass Sie vor dem Bild von Bob während der Lernaufgabe erschienen sind, indem Sie auf jenes Wort klicken. \
\n\n*Starten durch Drücken der Leertaste...*")

mouse = event.Mouse(visible=True)
MemoryTest()
mouse = event.Mouse(visible=False)

instructionPage(u"Bitte beantworten Sie abschließend noch ein paar Fragen zu Ihrer Person. (Bestätigung jeweils mit der Enter-Taste)\n\n*Weiter mit der Leertaste...*")

#Demographics
#make a list with openended questions
openDemosQuest = [u'Alter:', u'Studienfach / Beruf:', u'Geschlecht:', u'Was vermuten Sie, war das Ziel dieses Experiments?', u'Haben Sie irgendwelche weiteren Bemerkungen?']
openDemosQuestions = []
for demos in openDemosQuest:
    openendedResponse(demos, "Data_Demographics_OTM_Cologne_")

LastPage(u"Vielen Dank für Ihre Teilnahme!\n\nBitte wenden Sie sich nun an die Versuchsleitung.\nWir wünschen Ihnen einen schönen Tag!")

window.close()
core.quit()
