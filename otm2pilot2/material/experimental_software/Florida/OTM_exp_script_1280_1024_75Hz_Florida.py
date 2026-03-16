# -*- coding: utf-8 -*-

#coded in PsychoPy v1.83.04
#written for 75Hz monitors - in frames

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

#start with 1000 ms blank, then shows a fixcross, then a word prime for 1 frame and an images afterwards for 250ms
def subliminalTrial (prime, bob):
    fixcross = visual.TextStim(window, text = "+", pos = (0,0), color = "white", font = "Times New Roman", bold = True)
    prime_stim = visual.TextStim(window, text= prime, pos = (0, 0), color = "white", font = "Times New Roman", bold = True)
    bob_stim = visual.ImageStim(window, image = bob, pos = (0,0))
    blank = visual.TextStim(window, text = "", pos = (0,0))
    for frameN in range(111):
        if 1<=frameN<76:
            blank.draw()
        if 76<=frameN<91:
            fixcross.draw()
        if 91<=frameN<92:
            prime_stim.draw()
        if 92<=frameN<111:
            bob_stim.draw()
        window.flip()

#function showing a 'correct' for 5000 ms
def posFeedback():
    correct = visual.TextStim(window, text = "Correct", pos = (0,0), color = 'green')
    for frameN in range(376):
        if 1<=frameN<376:
            correct.draw()
        window.flip()

#function showing a 'wrong' for 5000 ms
def negFeedback():
    wrong = visual.TextStim(window, text = "Wrong", pos = (0,0), color = 'red')
    for frameN in range(376):
        if 1<=frameN<376:
            wrong.draw()
        window.flip()

#first calls the subliminal trial function and then shows an image and written behavior and waits for response
def trial(prime, bob, bobName, behavior, Valence):
    bob_stim = visual.ImageStim(window, image = bob, pos = (0,0))
    behavior_stim = visual.TextStim(window, text = BobName +" "+ behavior, pos = (0,-250), color = 'white')
    instruction_key_d = visual.TextStim(window, text = "c = characteristic", pos = (-350, -350), color = 'white')
    instruction_key_k = visual.TextStim(window, text = "u = uncharacteristic", pos = (350, -350), color = 'white')
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
    outputFile.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%s\t%s\t%s\t%s\t%s\n" % (int(ParticipantNumber), "Florida", prime, bob, bobName, behavior, Valence, responseNumber, correctBehav, TrialRT, Block, ValenceBlock, Valence, computerName, timeStamp))
    outputFile.close()

#first explicit evalaution
def liking1(InstructionLiking1):
    myRatingScale = visual.RatingScale(window, low= 1, high=9, skipKeys=None, stretch = 1.4, scale = ('Very Unlikable                             \t\t\t\t\t\t\t\t                           Very Likable'), \
    textSize = 0.4, size = 1.55, textColor = 'white', lineColor = 'white', showValue=False, pos=[0,-30], \
    tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", acceptSize = 2.2, mouseOnly = True) 
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
    myRatingScale1 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = ("Bad \t\t\t\t\t\t\t\t\t\t Good"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,260], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", \
    acceptSize = 2.2, mouseOnly = True, name='gutschlecht') 
    
    myRatingScale2 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = ("Mean \t\t\t\t\t\t\t\t\t\t Pleasant"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,115], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", \
    acceptSize = 2.2, mouseOnly = True, name='freundlichgemein')
    
    myRatingScale3 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Disagreeable \t\t\t\t\t\t\t\t\t\t Agreeable"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-30], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", \
    acceptSize = 2.2, mouseOnly = True, name='disagreeable') 
    
    myRatingScale4 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Uncaring \t\t\t\t\t\t\t\t\t\t Caring"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-175], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", \
    acceptSize = 2.2, mouseOnly = True, name='uncaring') 
    
    myRatingScale5 = visual.RatingScale(window, low= 1, high=9, skipKeys=None, scale = (u"Cruel \t\t\t\t\t\t\t\t\t\t Kind"), stretch = 1.4, textSize = 0.4, size = 1.2, textColor = 'white', \
    lineColor = 'white', showValue=False, pos=[0,-320], tickMarks=[1, 2, 3, 4, 5, 6, 7, 8, 9], labels=["1", "2", "3", "4", "5", "6", "7", "8", "9"], acceptPreText  = "Please, click on the line", acceptText = "Accept", \
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
    Instruction = visual.TextStim(window, pos=(0, 0), text=u"POSITIVE\t\t\t100°\tExtremely favorable\n\t\t\t\t90°\tVery favorable\n\t\t\t\t80°\tQuite favorable\
    \n\t\t\t\t70°\tFairly favorable\n\t\t\t\t60°\tSlightly favorable\n\t\t\t\t50°\tNeither \n\t\t\t\t40°\tSlightly unfavorable\n\t\t\t\t30°\tFairly unfavorable\n\t\t\t\t20°\tQuite unfavorable \
    \n\t\t\t\t10°\tVery unfavorable\nNEGATIVE\t\t0°\tExtremely unfavorable. \
\n\nUsing the above scale, please provide a number between 0° and 100° to indicate how you feel about Bob. Please type your response (between 0 and 100) and press *Enter*.", color = 'white')
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
    instructionPage(u"Please answer the following questions about your impressions of Bob on the scales provided on the next pages. \
We realize that you may not feel completely certain about some of these responses: simply answer them as best as you can. \
Please click on the scale to choose a number between 1 and 9, which corresponds to your impression about Bob. As soon as you have clicked on the scale \
a blue triangle will appear which can be ajdusted with the computer mouse. Once your rating is final, please click on the button *accept*. \
\n\n*Start the task by pressing space....*")
    mouse = event.Mouse(visible=True)
    l1 = liking1("How likable is " + BobName + "?")
    l2, l3, l4, l5, l6 = liking2("I think that " + BobName + " is:")
    mouse = event.Mouse(visible=False)
    instructionPage(u"We are interested in people’s attitudes toward " + BobName + u". \
Below you will see something that looks like a thermometer. You will be using this to indicate your attitude toward " + BobName + u". \
Here’s how it works. If you have a positive attitude toward Bob, you would give Bob a score somewhere between 50° and 100°, depending on how favorable your evaluation of Bob is. \
On the other hand, if you have a negative attitude toward Bob, you would give him a score somewhere between 0° and 50°, depending on how unfavorable your evaluation of Bob is. \
The degree labels will help you locate your attitude on the thermometer. You are not restricted to the numbers indicated — feel free to use any number between 0° and 100°. \
Please be honest. Your responses will be kept completely confidential. \
\n\n*Press space to continue...*")
    l7 = liking3("Your response:")
    outputFile = codecs.open('./data/DataEval_OTM_'+str(ParticipantNumber)+'.dat', 'a', 'utf-8')
    outputFile.write("%d\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Florida", BobName, int(l1), int(l2), int(l3), int(l4), int(l5), int(l6), int(l7), int(Block), int(ValenceBlock), int(MeasureOrder), computerName, timeStamp))
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
    Instruction = visual.TextStim(window, text = u"Please select the 20 words from the list that you think appeared before a picture of Bob during the learning tasks.", pos = (0, 330), color = "white")
    ExitText = visual.TextStim(window, text = "Save response and continue", pos = (0, -300), color = "white")
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
                    NumberText = visual.TextStim(window, text = u"Please select 20 words! You currently have selected "+str(redCounter)+u" words.", pos = (0, -340), color = "red", height = 12, italic=True)
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
    outputFile.write("%d\t%s\t%d\t%d\t%d\t%s\t%s\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Florida", int(Block), int(ValenceBlock), int(cList.count("correctIdent")), str(chosenItems), str(cList), int(MeasureOrder), computerName, timeStamp))
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
    outputFile.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%f\t%d\t%d\t%d\t%d\t%s\t%s\n" % (int(ParticipantNumber), "Florida", int(B), Stim, Cat, Type, key, keyPress, Correct, RT, RT2, int(Block), int(IATblock), int(ValenceBlock), int(MeasureOrder), computerName, timeStamp))
    outputFile.close()

#IAt block (including instructions)
def IAT():
    instructionPage(u"Next, you will see pictures of "+ BobName + u" and other people. \nIt is your task to classify whether an image shows "+ BobName +u" or not "+ BobName +u"!\n\n\n*Press space to continue...*")
    instructionPage(u"To classify the images please use the *d*- and the *k*- keys on your keyboard.\n\nFrom now on we will refer to the *d*- key as *left key* and to the *k*- key as *right key*. \
Please press the left key when you see an image of "+IATInstr1[2]+" and the right key when you seen an image of "+IATInstr1[3]+".\n\n\n*Press space to continue...*")
    instructionPage(u"Please react as quickly as possible when classifying the images. At the same time, please try to make as little errors as possible.\n\n\n*Press space to continue...*")
    instructionPage(u"In case you make an error, a red *X* will appear on the screen. Please press the correct key as quickly as possible to continue with the task.\n\n\n*Press space to continue...*")
    instructionPage(u"The correct assignment of keys will be displayed on the screen throughout the task. \n\nOn the left side, the category of the image will be \
displayed to which you should react with the left key ("+IATInstr1[0]+"). On the right side, the category of the image to which you should respond with the right \
key will be displayed ("+IATInstr1[1]+"). \n\n\n*Press space to continue...*")
    instructionPage(u"Please place your index fingers on the two keys (*d* and *k*).\n\nTo react quickly, please leave your fingers on the two keys throughout the entire task. \n\n\n*Press space to start the task...*")
    for SB1, CB1, TB1, kB1 in IATB1:
        IATTrial(SB1, CB1, TB1, kB1, IATInstr1, 1)
    instructionPage(u"Next you will be asked to classify words as positive or negative.\nPress the left key when you see a "+IATInstr2[2]+u" word. Press the right key when you see a "+IATInstr2[3]+u" word. \
In case you make an error, a red *X* will appear on the screen. Please press the correct key as quickly as possible to continue with the task. \n\n\n*Press space to continue...*")
    instructionPage(u"Please place your index fingers on the *d* and *k* keys and press space to start the task...")
    for SB2, CB2, TB2, kB2 in IATB2:
        IATTrial(SB2, CB2, TB2, kB2, IATInstr2, 2)
    instructionPage(u"Next, you are supposed to do both tasks 'simmultaneously'. \n\nIn each trial you will either see a word or an image of a person.\nPress the left key when you see "+IATInstr34[2]+u" word. \
Press the right key when you see "+IATInstr34[3]+u" word. \n\nAgain, in case you make an error a red *X* appears and you are asked to press the correct key as quickly as possible.\
\n\n\n*Press space to continue...*")
    instructionPage(u"Please place your index fingers on the *d* and *k* keys and press space to start the task...")
    for SB34, CB34, TB34, kB34 in IATB34:
        IATTrial(SB34, CB34, TB34, kB34, IATInstr34, 34)
    instructionPage(u"Next you will be asked to sort images again, judging whether they show "+BobName+u" or another person. However, the correct sides of keys will be switched around.\n\
Press the left key when a picture of "+IATInstr5[2]+u" appears and the right key when an image of "+IATInstr5[3]+u" appears. \n\n\n*Press space to continue...*")
    instructionPage(u"Please place your index fingers on the *d* and *k* keys and press space to start the task...")
    for SB5, CB5, TB5, kB5 in IATB5:
        IATTrial(SB5, CB5, TB5, kB5, IATInstr5, 5) 
    instructionPage(u"Now you will be asked to work on another double task. In each trial you will either see a picture of a person or a word.\nPlease press the left key when you see "+IATInstr67[2]+u" word. \
Please press the right key when you see "+IATInstr67[3]+u" word. \n\nAgain, in case you make an error a red *X* appears and you are asked to press the correct key as quickly as possible.\
\n\n\n*Press space to continue...*")
    instructionPage(u"Please place your index fingers on the *d* and *k* keys and press space to start the task...")
    for SB67, CB67, TB67, kB67 in IATB67:
        IATTrial(SB67, CB67, TB67, kB67, IATInstr67, 67)
    
#open response function for demographic questions
def openendedResponse(question, OutputName, bgstim1=None, bgstim2=None):
    #make unders to indicate participants can type and instruction to save answer by pressing return
    underscore = visual.TextStim(window, text='_', pos=(0, 0), color = (0, 0, 0))
    if bgstim1 != None:
        underscore.setPos(newPos = (0,0))
    instruction = visual.TextStim(window, text=u'Please press *Enter* to submit your response.', italic=True, pos=(0,300), color = "white")
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
IATpos = ReadTxt("IATpos.txt", -2)
IATneg = ReadTxt("IATneg.txt", -2)

#keylists to test if correct key was pressed
if IATkey == 1 and IATblock == 1:
    keyListB1 = 10*["d"]+10*["k"]
    keyListB2 = 10*["k"]+10*["d"]
    keyListB34 = 10*["d"]+10*["k"]+10*["k"]+10*["d"]
    keyListB5 = 10*["k"]+10*["d"]
    keyListB67 = 10*["k"]+10*["d"]+10*["k"]+10*["d"]
    IATInstr1 = [BobName, "Not "+BobName, BobName, "a different person"]
    IATInstr2 = ["negative", "positive", "negative", "positive"]
    IATInstr34 = [BobName+" \nnegative", "Not "+BobName+" \npositive", BobName+" or a negative", "another person or a positive"]
    IATInstr5 = ["Not "+BobName, BobName, "another person", BobName] 
    IATInstr67 = ["Not "+BobName+" \nnegative", BobName+ " \npositive", "another person or a negative", BobName+" or a positive"]
elif IATkey == 1 and IATblock == 2:
    keyListB1 = 10*["k"]+10*["d"]
    keyListB2 = 10*["k"]+10*["d"]
    keyListB34 = 10*["k"]+10*["d"]+10*["k"]+10*["d"]
    keyListB5 = 10*["d"]+10*["k"]
    keyListB67 = 10*["d"]+10*["k"]+10*["k"]+10*["d"]
    IATInstr1 = ["Not "+BobName, BobName, "a different person", BobName]
    IATInstr2 = ["negative", "positive", "negative", "positive"]
    IATInstr34 = ["Not "+BobName+" \nnegative", BobName+" \npositive", "another person or a negative", BobName+" or a positive"]
    IATInstr5 = [BobName, "Not "+BobName, BobName, "another person"]
    IATInstr67 = [BobName+" \nnegative", "Not "+BobName+" \npositive", BobName+" or a negative", "another person or a positive"]
elif IATkey == 2 and IATblock == 1:
    keyListB1 = 10*["k"]+10*["d"]
    keyListB2 = 10*["d"]+10*["k"]
    keyListB34 = 10*["k"]+10*["d"]+10*["d"]+10*["k"]
    keyListB5 = 10*["d"]+10*["k"]
    keyListB67 = 10*["d"]+10*["k"]+10*["d"]+10*["k"]
    IATInstr1 = ["Not "+BobName, BobName, "a different person", BobName]
    IATInstr2 = ["positive", "negative", "positive", "negative"]
    IATInstr34 = ["Not "+BobName+" \npositive", BobName+" \nnegative", "another person or a positive", BobName+" or a negative"]
    IATInstr5 = [BobName, "Not "+BobName, BobName, "another person"]
    IATInstr67 = [BobName+ " \npositive", "Not "+BobName+" \nnegative", BobName+" or a positive", "another person or a negative"]
elif IATkey == 2 and IATblock == 2:
    keyListB1 = 10*["d"]+10*["k"]
    keyListB2 = 10*["d"]+10*["k"]
    keyListB34 = 10*["d"]+10*["k"]+10*["d"]+10*["k"]
    keyListB5 = 10*["k"]+10*["d"]
    keyListB67 = 10*["k"]+10*["d"]+10*["d"]+10*["k"]
    IATInstr1 = [BobName, "Not "+BobName, BobName, "a different person"]
    IATInstr2 = ["positive", "negative", "positive", "negative"]
    IATInstr34 = [BobName+" \npositive", "Not "+BobName+" \nnegative", BobName+" or a positive", "another person or a negative"]
    IATInstr5 = ["Not "+BobName, BobName, "another person", BobName]
    IATInstr67 = ["Not "+BobName+" \npositive", BobName+ " \nnegative", "another person or a positive", BobName+" or a negative"]
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
outputFile = open("./data/Data_Demographics_OTM_Florida_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%s\t%s\t%s\t%s\t%s\t%s\n" % ("ParticipantNumber", "Age", "Study", "Gender", "Goal", "Comment"))
outputFile.close()

#add the participant Number in the first row
outputFile = open("./data/Data_Demographics_OTM_Florida_"+str(ParticipantNumber)+'.dat', 'a') 
outputFile.write("%d" % (ParticipantNumber))
outputFile.close()

# ###########################################################################################################################
# Set up screen
# ###########################################################################################################################

#setup window for screen 1280*1024
window=visual.Window(units= "pix", size =(1280,1024), rgb = "black", fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()

# This part records the screen refresh rate for 10 frames and saves it with the pp number in the file name in order to ensure that all PC's were set to correct Hz
window.setRecordFrameIntervals(True)
Text1 = visual.TextStim(window, text='', pos = (0, 0))
for frameN in range(10):#for exactly 10 frames
    if 2<=frameN<3:
        Text1.draw()
    window.flip()
window.saveFrameIntervals(fileName="./data/OTM_ScreenLog_Florida_"+str(ParticipantNumber)+".dat", clear=True)
window.setRecordFrameIntervals(False)

#Additionally save some information about the PC and software in that file
outputFile = open("./data/OTM_Log_Florida_"+str(ParticipantNumber)+".dat", 'a') 
outputFile.write("%s\t%s\t%s\t%s\n" % (platform.platform(), "PychoPyVersion:", __version__, timeStamp)) 
outputFile.close()

# ###########################################################################################################################
# Actual order of experiment, including instructions (some instructions may be included in functions above)
# ###########################################################################################################################

instructionPage(u"Thank you for participating in today's experiment. \
In the first part of this study we are going to present some behaviors performed by a real person who we will call Bob. \
Your task will be to determine what type of person Bob is (e.g., is he nice, is he mean, is he intelligent).\n\n\n*Press space to continue...*")

instructionPage(u"To form your impression, we are going to ask you to give your opinion about whether you think that certain behaviors are characteristic or uncharacteristic of Bob. \
If you judge the behavior to be characteristic of Bob, then you think that he would perform this behavior. \
If you judge the behavior to be uncharacteristic of Bob, then you do not think that he would perform this behavior.\n\n\n*Press space to continue...*")

instructionPage(u"Obviously at the beginning of the session you will just be guessing because you have no information about what kind of a person Bob is. \
The feedback you receive about whether your opinion or guess was correct should be used to form your impression of Bob. \
If a behavior is uncharacteristic of Bob he would not perform this behavior and likely perform the opposite behavior.\n\n\n*Press space to continue...*")

instructionPage(u"After this first task, you will be completing the second part of the block: a questionnaire and a cognitive task. \
It should take you about 15 minutes to complete the first part of the block and 15 minutes to complete the second part of the block (i.e., the questionnaire and cognitive task). \
\n\n\n*Press space to continue...*")

instructionPage(u"Again, your task is to determine whether the behaviors listed are characteristic or uncharacteristic of Bob and give your answer as fast and accurately as possible by \
pressing either the *c* key for behaviors that are characteristic of Bob or the *u* key for behaviors that are uncharacteristic of Bob. \
You should form an impression of Bob based on your ability to guess whether the behaviors presented are characteristic or uncharacteristic of Bob. \n\n\n*Press space to continue...*")

instructionPage(u"In other words, you should learn what type of person Bob is by reading the behaviors presented, making a guess and determining whether your guess was correct or incorrect. \
Remember, if the behavior is characteristic of Bob then he would likely engage in the listed behavior, but if the behavior is uncharacteristic of Bob he would not engage in this behavior \
and would likely engage in the opposite behavior. \n\n\n*Press space to continue...*")

instructionPage(u"If you have any questions please ask the experimenter before beginning. \n\nPlease press space when you are ready to begin learning about Bob.")

Block = 1

for eachBobImage, eachBobName, eachPrime, eachBehavior, eachValence in Block1List:
    trial(prime= eachPrime, bob = eachBobImage, bobName = eachBobName, behavior= eachBehavior, Valence = eachValence)


instructionPage(u"You have finished the first half of the first block. \n\
You will now be asked to complete a series of cognitive tasks and answer some questions. \n\n\n\
*Press space to continue...*")

#either liking block or IAT first based on MeasureOrder
if MeasureOrder == 1:
    IAT()
    likingBlock()
else:
    likingBlock()
    IAT()


instructionPage(u"You will now start with the second block. \n\
Again, it is your task to determine what type of person Bob is. \
To form an impression you are again asked to judge whether the behavior shown is characteristic or uncharacteristic of Bob. \
Please judge whether a behavior is characteristic of Bob or not by pressing either *c* key for behaviors that are characteristic \
of Bob or *u* key for uncharacteristic behavior of Bob and give your answer as fast and accurately as possible. \
\n\n\nPlease press space when you are ready to begin learning about Bob.")

Block = 2

for eachBobImage, eachBobName, eachPrime, eachBehavior, eachValence in Block2List:
    trial(prime= eachPrime, bob = eachBobImage, bobName = eachBobName, behavior= eachBehavior, Valence = eachValence)


instructionPage(u"You have now completed the first half of the second - and last - block.\n\
You will again be asked to complete a series of cognitive tasks and answer some questions. \n\n\n \
*Press space to continue...*")

#either liking block or IAT first based on MeasureOrder
if MeasureOrder == 1:
    IAT()
    likingBlock()
else:
    likingBlock()
    IAT()

#Memory Test
instructionPage(u"During today’s experiment that involved learning about Bob, words were sometimes presented before the picture of Bob appeared on the screen. Although these words may have \
been hard to see, people are often very good at recognizing words that they only registered at an unconscious level. \n\n*Press space to continue...*")
instructionPage(u"Indeed you saw 20 of the following words before a picture of Bob at some point in today’s session. \
\n\nPlease select 20 words from the list on the next page that you think appeared before a picture of Bob during the learning tasks by clicking on them. \
\n\n*Start by pressing space...*")

mouse = event.Mouse(visible=True)
MemoryTest()
mouse = event.Mouse(visible=False)

instructionPage(u"In the end, we would like to ask you a few questions about yourself. (Submit your answer by pressing *Enter*)\n\n*Start by pressing space...*")

#Demographics
#make a list with openended questions
openDemosQuest = [u'Age:', u'Study / Profession:', u'Gender:', u'What do you think, was the goal of this experiment?', u'Do you have any further remarks?']
openDemosQuestions = []
for demos in openDemosQuest:
    openendedResponse(demos, "Data_Demographics_OTM_Florida_")

LastPage(u"Thank you very much for participating!\n\nPlease go and see the experimenter.\nWe wish you a nice day!")

window.close()
core.quit()
