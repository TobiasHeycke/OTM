# -*- coding: utf-8 -*-

#coded in PsychoPy v1.83.04
#wrote for 60Hz monitors - in frames

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
    for frameN in range(89):
        if 1<=frameN<61:
            blank.draw()
        if 61<=frameN<73:
            fixcross.draw()
        if 73<=frameN<74:
            prime_stim.draw()
        if 74<=frameN<89:
            bob_stim.draw()
        window.flip()

#function showing a 'correct' for 5000 ms
def posFeedback():
    correct = visual.TextStim(window, text = u"Juist", pos = (0,0), color = 'green')
    for frameN in range(300):
        if 1<=frameN<=300:
            correct.draw()
        window.flip()

#function showing a 'wrong' for 5000 ms
def negFeedback():
    wrong = visual.TextStim(window, text = u"Fout", pos = (0,0), color = 'red')
    for frameN in range(300):
        if 1<=frameN<=300:
            wrong.draw()
        window.flip()

#first calls the subliminal trial function and then shows an image and written behavior and waits for response
def trial(prime, bob, bobName, behavior, Valence):
    bob_stim = visual.ImageStim(window, image = bob, pos = (0,0))
    behavior_stim = visual.TextStim(window, text = BobName +" "+ behavior, pos = (0,-250), color = 'white')
    instruction_key_d = visual.TextStim(window, text = u"c = karakteristiek", pos = (-350, -350), color = 'white')
    instruction_key_k = visual.TextStim(window, text = u"u = niet karakteristiek", pos = (350, -350), color = 'white')
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
        outputFile = open('./data/AbortMassage_OTMPilot_'+str(ParticipantNumber)+'.dat', 'a') #Save create a txt and participantnumber in it
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
    outputFile = codecs.open('./data/DataTrials_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%s\t%s\t%s\t%s\t%s\n" % (int(ParticipantNumber), "Ghent", prime, bob, bobName, behavior, Valence, responseNumber, correctBehav, TrialRT, Block, ValenceBlock, Valence, computerName, timeStamp))
    outputFile.close()

#first explicit evalaution
def liking1(InstructionLiking1):
    myRatingScale = visual.RatingScale(window, low= 1, high=9, skipKeys=None, stretch = 1.4, scale = (u'Zeer onaardig                             \t\t\t\t\t\t\t\t                           Zeer aardig'), \
    textSize = 0.4, size = 1.55, textColor = 'white', lineColor = 'white', showValue=False, pos=[0,-30], \
    tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Klik op de lijn", acceptText = "Aanvaarden", acceptSize = 2.2, mouseOnly = True) 
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
    myRatingScale1 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Slecht \t\t\t\t\t\t\t\t\t\t Goed"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,260], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = u"Klik op de lijn", acceptText = u"Aanvaarden", \
    acceptSize = 2.2, mouseOnly = True, name='gutschlecht') 
    
    myRatingScale2 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Gemeen \t\t\t\t\t\t\t\t\t\t Aangenaam"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,115], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = u"Klik op de lijn", acceptText = u"Aanvaarden", \
    acceptSize = 2.2, mouseOnly = True, name='freundlichgemein')
    
    myRatingScale3 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Onprettig \t\t\t\t\t\t\t\t\t\t Prettig"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-30], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = u"Klik op de lijn", acceptText = u"Aanvaarden", \
    acceptSize = 2.2, mouseOnly = True, name='disagreeable') 
    
    myRatingScale4 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Onzorgzaam \t\t\t\t\t\t\t\t\t\t Zorgzaam"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-175], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = u"Klik op de lijn", acceptText = u"Aanvaarden", \
    acceptSize = 2.2, mouseOnly = True, name='uncaring') 
    
    myRatingScale5 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Wreedaardig \t\t\t\t\t\t\t\t\t\t Lief"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-320], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = u"Klik op de lijn", acceptText = u"Aanvaarden", \
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
    Instruction = visual.TextStim(window, pos=(0, 0), text=u"POSITIEF\t\t\t100°\tExtreem gunstig\n\t\t\t\t90°\tZeer gunstig\n\t\t\t\t80°\tNogal gunstig\
    \n\t\t\t\t70°\tEerder gunstig\n\t\t\t\t60°\tEnigszins gunstig\n\t\t\t\t50°\tGeen van alle \n\t\t\t\t40°\tEnigszins ongunstig\n\t\t\t\t30°\tEerder ongunstig\n\t\t\t\t20°\tNogal ongunstig \
    \n\t\t\t\t10°\tZeer ongunstig\nNEGATIEF\t\t0°\tExtreem ongunstig. \
\n\nGebruik de bovenstaande schaal om met een nummer tussen 0° and 100° aan te geven hoe je gevoelens ten opzichte van Bob zijn. Gelieve je antwoord (tuseen 0 en 100) in te typen en dan op *Enter* te drukken.", color = 'white')
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
    instructionPage(u"Gelieve de volgende vragen over jouw mening over Bob te beantwoorden met behulp van de schalen op de volgende paginas.  \
We beseffen dat je je misschien niet helemaal zeker voelt over sommige van deze antwoorden: antwoord gewoon op de vragen zo goed als je kan. \
Gelieve op de schaal te klikken om een nummer te kiezen, tussen 1 en 9, dat overeenkomt met jouw mening over Bob. Zodra je geklikt hebt op de schaal \
zal een blauwe driehoek verschijnen die kan aangepast worden door gebruik te maken van de muis. Gelieve op de knop *aanvaarden* te drukken wanneer je klaar bent met je beoordeling. \
\n\n*Start de taak door op de spatiebalk te drukken....*")
    mouse = event.Mouse(visible=True)
    l1 = liking1(u"Hoe aardig is " + BobName + "?")
    l2, l3, l4, l5, l6 = liking2(u"Ik denk dat " + BobName + " zo is:")
    mouse = event.Mouse(visible=False)
    instructionPage(u"We zijn geïnteresseerd in attitudes ten opzichte van Bob. \
Hieronder zal je iets zien dat lijkt op een thermometer. Je zal dit gebruiken om je mening of attitude ten opzichte van Bob aan te geven. \
Dit is hoe het werkt: Indien je een positieve attitude hebt ten opzichte van Bob, geef je Bob een score ergens tussen 50° en 100°,  afhankelijk van hoe gunstig je evaluatie van Bob is. \
Anderzijds, indien je een negatieve attitude hebt ten opzichte van Bob, geef je hem een score ergens tussen 0° en 50°, afhankelijk van hoe ongustig je evaluatie van Bob is. \
De graadsaanduidingen zullen je helpen om je attitude terug te vinden op de thermometer. Je bent niet  beperkt tot de aangegeven nummers - gebruik gerust eender welk nummer tussen 0° en 100°. \
Gelieve eerlijk te zijn. Je antwoorden zullen volledig anoniem blijven. \
\n\n*Druk op de spatiebalk om verder te gaan...*")
    l7 = liking3(u"Jouw antwoord:")
    outputFile = codecs.open('./data/DataEval_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Ghent", BobName, int(l1), int(l2), int(l3), int(l4), int(l5), int(l6), int(l7), int(Block), int(ValenceBlock), computerName, timeStamp))
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
    if ValenceBlock == 1:
        memTestDis = memTestDisNeg
        Prime = negPrime
    else:
        memTestDis = memTestDisPos
        Prime = posPrime
    wordList = memTestDis + Prime
    shuffle(wordList)
    colorList = 20*["white"]
    j = 0
    CoordinatesList = []
    x = -350
    y = 260
    for i in range(20):
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
    Instruction = visual.TextStim(window, text = u"Gelieve de 10 woorden van de lijst te selecteren waarvan jij denkt dat ze verschenen zijn voor de prent van Bob tijdens de leertaken.", pos = (0, 330), color = "white")
    ExitText = visual.TextStim(window, text = u"Sla je antwoord op en ga verder", pos = (0, -300), color = "white")
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
                if redCounter == 10:
                    cList = []
                    for i in chosenItems:
                        c = "correctIdent"
                        if i in memTestDis:
                            c = "falseIdent"
                        cList.append(c)
                    
                    break
                else: 
                    NumberText = visual.TextStim(window, text = u"Gelieve 10 woorden te selecteren! Je hebt momenteel "+str(redCounter)+u" woorden geselecteerd.", pos = (0, -340), color = "red", height = 12, italic=True)
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
    outputFile = codecs.open('./data/DataMemTest_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s\n" % (int(ParticipantNumber), "Ghent", int(Block), int(ValenceBlock), int(cList.count("correctIdent")), str(chosenItems), str(cList), computerName, timeStamp))
    outputFile.close()

    
#open response function for demographic questions
def openendedResponse(question, OutputName, bgstim1=None, bgstim2=None):
    #make unders to indicate participants can type and instruction to save answer by pressing return
    underscore = visual.TextStim(window, text='_', pos=(0, 0), color = (0, 0, 0))
    if bgstim1 != None:
        underscore.setPos(newPos = (0,0))
    instruction = visual.TextStim(window, text=u'Gelieve op *Enter* te drukken om je aantwoord in te geven.', italic=True, pos=(0,300), color = "white")
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

# whether participants have a negative prime in block 1 or block 2 (and the opposite valence of behavior)
# 1 means negative primes and positive behavior in block 1
# 2 means positive primes and negative behavior in block 1
if ParticipantNumber%2 == 1:
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

negBehav = ReadTxt(File = "negative_behavior.txt", remove = -2)
posBehav = ReadTxt(File = "positive_behavior.txt", remove = -2)

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

negPrime = ReadTxt(File = "negative_primes.txt", remove = -2)

negPrimeTrials = []
for i in range(10):
    shuffle(negPrime)
    negPrimeTrials += negPrime

posPrime = ReadTxt(File = "positive_primes.txt", remove = -2)

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
#    Block2List = zip(BobImageTrials, BobNameTrials, posPrimeTrials, Block2Behav, ValenceTrials)
else:
    Block1List = zip(BobImageTrials, BobNameTrials, posPrimeTrials, Block1Behav, ValenceTrials)
#    Block2List = zip(BobImageTrials, BobNameTrials, negPrimeTrials, Block2Behav, ValenceTrials)

shuffle(Block1List)
#shuffle(Block2List)

# ###########################################################################################################################
# Create list for distractor words in memory test
# ###########################################################################################################################

#memTestDis = ReadTxt("MemTestDistr.txt", -1)
memTestDisNeg = ReadTxt("MemTestDistrNeg.txt", -1)
memTestDisPos = ReadTxt("MemTestDistrPos.txt", -1)


# ###########################################################################################################################
# Set up headers for output txt files
# ###########################################################################################################################

outputFile = codecs.open('./data/DataTrials_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % ("ParticipantNumber", "Location", "prime", "BobImage", "bobName", "behavior", "Valence", "responseNumber", "correctBehav", "TrialRT", "Block", "ValenceBlock", "Valence", "computerName", "timeStamp"))
outputFile.close()

outputFile = codecs.open('./data/DataEval_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Location", "Name", "Eval1", "Eval2", "Eval3", "Eval4", "Eval5", "Eval6", "Eval7", "Block", "ValenceBlock", "computerName", "timeStamp"))
outputFile.close()

outputFile = codecs.open('./data/DataMemTest_OTMPilot_Ghent_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Location", "Block", "ValenceBlock", "NumbercorrectIdent", "chosenItems", "correctList", "computerName", "timeStamp"))
outputFile.close()

#For the demographic data
outputFile = open("./data/Data_Demographics_OTMPilot_Ghent_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Age", "Study", "Gender", "Goal", "Comment"))
outputFile.close()

#add the participant Number in the first row and the location in the second
outputFile = open("./data/Data_Demographics_OTMPilot_Ghent_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%d" % (ParticipantNumber))
outputFile.close()

# ###########################################################################################################################
# Set up screen
# ###########################################################################################################################

#setup window for screen 1024*768
window=visual.Window(units= "pix", size =(1024,768), rgb = "black", fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()

# This part records the screen refresh rate for 10 frames and saves it with the pp number in the file name in order to ensure that all set to correct Hz
window.setRecordFrameIntervals(True)
Text1 = visual.TextStim(window, text='', pos = (0, 0))
for frameN in range(10):#for exactly 10 frames
    if 2<=frameN<3:
        Text1.draw()
    window.flip()
window.saveFrameIntervals(fileName="./data/OTMPilot_ScreenLog_Ghent_"+str(ParticipantNumber)+".dat", clear=True)
window.setRecordFrameIntervals(False)

#Additionally save some information about the PC and software in that file
outputFile = open("./data/OTMPilot_Log_Ghent_"+str(ParticipantNumber)+".dat", 'a') 
outputFile.write("%s\t%s\t%s\t%s\n" % (platform.platform(), "PychoPyVersion:", __version__, timeStamp)) 
outputFile.close()

# ###########################################################################################################################
# Actual order of experiment, including instructions (some instructions may be included in functions above)
# ###########################################################################################################################

instructionPage(u"Dank je wel om deel te nemen aan dit experiment. \
In het eerste deel van de studie zullen we enkele gedragingen tonen die uitgevoerd werden door een echte persoon die we Bob zullen noemen. \
Jouw taak zal zijn om te bepalen welk type persoon Bob is (bv., is hij lief, is hij gemeen, is hij intelligent).\n\n\n*Druk op de spatiebalk om verder te gaan...*")

instructionPage(u"Om je opinie te vormen, zullen we je vragen om te beoordelen of je denkt dat bepaalde gedragingen karakteristiek of niet karakteristiek zijn voor Bob. \
Indien je een gedrag karakteristiek beoordeelt voor Bob, dan betekent dit dat je denkt dat hij dit gedrag zou uitvoeren. \
Indien je een gedrag beoordeelt als niet karakteristiek voor Bob, dan betekent dit dat je niet denkt dat hij dit gedrag zou uitvoeren. \n\n\n*Druk op de spatiebalk om verder te gaan...*")

instructionPage(u"Uiteraard zul je aan het begin van de sessie enkel kunnen gokken aangezien je geen informatie hebt over wat voor iemand Bob is. \
De feedback die je ontvangt over of je mening of gok juist was moet je gebruiken om je opinie over Bob te vormen. \
Indien een gedrag niet karakteristiek is voor Bob dan zou hij dit gedrag niet uitvoeren en eerder tegengesteld gedrag uitvoeren.\n\n\n*Druk op de spatiebalk om verder te gaan...*")

instructionPage(u"Na deze eerste taak, zal je een tweede deel van dit experiment uitvoeren: dit zal bestaan uit het oplossen van enkele korte vragen. \
Het zal ongeveer 15 minuten duren om het eerste deel van het blok uit te voeren en 5 minuten om het tweede deel van het experiment uit te voeren. \
\n\n\n*Druk op de spatiebalk om verder te gaan...*")

instructionPage(u"Opnieuw, jouw taak is om te bepalen of de vermelde gedragingen karakteristiek of niet karakteristiek zijn voor Bob en om je antwoord zo snel mogelijk te geven door \
ofwel op de *c* toets te drukken bij gedrag dat karakteristiek is voor Bob of op de *u* toets bij gedrag dat niet karakteristiek is voor Bob. \
Je moet een opinie vormen over Bob op basis van je mogelijkheid om te gokken of de gepresenteerde gedragingen karakteristiek of niet karakteristiek zijn voor Bob. \n\n\n*Druk op de spatiebalk om verder te gaan...*")


instructionPage(u"Met andere woorden, je moet leren welk type persoon Bob is door de gepresenteerde gedragingen te lezen, een inschatting of gok te maken en te bepalen of je inschatting juist of fout was. \
Onthoud dat indien het gedrag karakteristiek is voor Bob, hij dit gedrag waarschijnlijk zou uitvoeren, maar indien het gedrag niet karakteristiek is voor Bob dan zou hij dit gedrag niet uitvoeren \
en waarschijnlijk tegengesteld gedrag uitvoeren. \n\n\n*Druk op de spatiebalk om verder te gaan...*")

instructionPage(u"Indien je vragen hebt gelieve deze dan te stellen aan de experimentleider voor je begint. \n\nDruk op de spatiebalk indien je klaar bent om te beginnen leren over Bob.")

# subjects will receive negative primes + positive behaviors OR positive primes + negative behaviors
Block = 1

for eachBobImage, eachBobName, eachPrime, eachBehavior, eachValence in Block1List:
    trial(prime= eachPrime, bob = eachBobImage, bobName = eachBobName, behavior= eachBehavior, Valence = eachValence)


instructionPage(u"Je hebt het eerste blok uitgevoerd. \n\
We zullen je nu vragen om enkele vragen te beantwoorden. \n\n\n\
*Druk op de spatiebalk om verder te gaan...*")


likingBlock()


#Memory Test
instructionPage(u"Tijdens het experiment van vandaag dat bestond uit het leren over Bob, werden soms woorden gepresenteerd vlak voor de prent van Bob op het scherm verscheen. Hoewel deze woorden waarschijnlijk \
moeilijk te zien waren, zijn mensen vaak zeer goed in het herkennen van woorden die ze enkel op een onbewust niveau hebben geregistreerd. \n\n*Druk op de spatiebalk om verder te gaan...*")
instructionPage(u"Je zag wel degelijk 10 van de volgende woorden die aangeboden werden voorafgaand aan een prent van Bob op een bepaald moment in de sessie van vandaag. \
\n\nSelecteer nu 10 woorden van de lijst op de volgende pagina waarvan je denkt dat die verschenen zijn voor een prent van Bob tijdens de leertaken, door erop te drukken. \
\n\n*Start door te drukken op de spatiebalk...*")

mouse = event.Mouse(visible=True)
MemoryTest()
mouse = event.Mouse(visible=False)

instructionPage(u"Op het einde willen we je nu nog vragen om enkele vragen te beantwoorden over jezelf. (Geef je antwoord in door te drukken op *Enter*)\n\n*Start door te drukken op de spatiebalk...*")

#Demographics
#make a list with openended questions
openDemosQuest = [u'Leeftijd:', u'Studie / Beroep:', u'Geslacht:', u'Wat denk jij dat het doel was van dit experiment?', u'Heb je nog andere opmerkingen?']
openDemosQuestions = []
for demos in openDemosQuest:
    openendedResponse(demos, "Data_Demographics_OTMPilot_Ghent_")

LastPage(u"Dank je zeer voor je deelname!\n\nGa nu de proefleider roepen.\nWe wensen je een fijne dag verder!")

window.close()
core.quit()
