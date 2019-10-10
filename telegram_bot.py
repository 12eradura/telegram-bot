import random
import telebot

bot = telebot.TeleBot("484342029:AAGAfMsm4oJ8BAkl2MQ5kUOrF746x8Sd6I0")

counter1 = 0
counter2 = 0
counter3 = 0
m = 0
allCodes = []

cows = 0
bulls = 0

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def generateNumber():
    arr = []
    s = 0
    x = 0
    while (s == 0):
        x = random.randint(1000, 9999)
        arr = intToArr(x)
        s = 1
        for i in range(4):
            if (arr.count(arr[i]) > 1):
                s = 0

    return x


def intToArr(number):
    array = []
    array.append(number // 1000)
    a = number % 1000
    array.append(a // 100)
    a = a % 100
    array.append(a // 10)
    array.append(a % 10)

    return array


def bullsAndCowsCount(ComputerNumber, YourNumber):
    bull = 0
    cow = 0
    for i in range(4):
        if (ComputerNumber[i] == YourNumber[i]):
            bull += 1
    for i in range(4):
        for j in range(4):
            if ((ComputerNumber[i] == YourNumber[j]) and (i != j)):
                cow += 1

    return bull, cow


def generateNumbers():
    firstset = []
    allCodes = []
    arrr = []
    for i in range(100, 1000):
        arrr = intToArr(i)
        if ((arrr.count(0) == 1) and (len(set(arrr)) == 4)):
            x = '0' + str(i)
            allCodes.append(x)
        arrr.clear()

    for i in range(10000):
        firstset.append(i)
    for i in range(1000, len(firstset)):
        arrr.clear()
        arrr = intToArr(firstset[i])
        if (len(set(arrr)) == 4):
            allCodes.append(str(firstset[i]))

    return allCodes


def leaveValid(mynumber, bulls, cows, ourset):
    newourset = []
    for i in range(len(ourset)):
        bull, cow = bullsAndCowsCount(mynumber, ourset[i])
        if ((bull == bulls) and (cow == cows)):
            newourset.append(ourset[i])

    return newourset

def setCows(message):
    global cows
    if not isInt(message.text):
        bot.send_message(message.chat.id, "Please, enter a number from 1 to 4.")
        bot.register_next_step_handler(message, setCows)
    else:
        cows = int(message.text)
        bot.send_message(message.chat.id, "Number of bulls:")
        bot.register_next_step_handler(message, setBulls)

def setBulls(message):
    global bulls
    if not isInt(message.text):
        bot.send_message(message.chat.id, "Please, enter a number from 1 to 4.")
        bot.register_next_step_handler(message, setBulls)
    else:
        bulls = int(message.text)
        processBullsAndCows(message)

def processBullsAndCows(message):
    global allCodes, counter2

    if bulls < 0 or bulls > 4 or cows < 0 or cows > 4 or bulls + cows > 4:
        bot.send_message(message.chat.id, "You answered dishonestly :(")
        bot.send_message(message.chat.id, "Play again?[yes/no]")
        bot.register_next_step_handler(message,game)
    else:
        allCodes = leaveValid(allCodes[0], bulls, cows, allCodes)

        if not allCodes :
            bot.send_message(message.chat.id, "You answered dishonestly :(")
            bot.send_message(message.chat.id, "Play again?[yes/no]")
            bot.register_next_step_handler(message,game)
        else:
            counter2 = counter2 + 1
            if (bulls != 4):
                bot.send_message(message.chat.id, "Your turn!")
                bot.send_message(message.chat.id, "Enter the estimated number:")
                bot.register_next_step_handler(message, processUserGuess)
            else:
                bot.send_message(message.chat.id, "You lost :(")
                bot.send_message(message.chat.id, "Your number is guessed in " + str(counter2) + " steps.")
                bot.send_message(message.chat.id, "Play again?[yes/no]")
                bot.register_next_step_handler(message, game)


def processUserGuess(message):
    global counter3

    if not isInt(message.text):
        bot.send_message(message.chat.id, "You need to enter a four-digit number!")
        bot.register_next_step_handler(message, processUserGuess)

    number = int(message.text)
    yourNumber = []
    computerNumber = []

    yourNumber = intToArr(number)
    if (len(set(yourNumber)) != 4):
        bot.send_message(message.chat.id, "The number must contain 4 different digits. Enter again:")
        bot.register_next_step_handler(message, processUserGuess)
    else:
        computerNumber = intToArr(m)

        bull, cow = bullsAndCowsCount(computerNumber, yourNumber)
        bot.send_message(message.chat.id, "Number of bulls: " + str(bull) + " Number of cows: " + str(cows))

        counter3 = counter3 + 1

        if (bull == 4):
            bot.send_message(message.chat.id, "You win!")
            bot.send_message(message.chat.id, "Your number is guessed in " + str(counter3) + " steps.")
            bot.send_message(message.chat.id, "Play again?")
            bot.register_next_step_handler(message, game)
        else:
            tryToGuess(message)


def tryToGuess(message):
    bot.send_message(message.chat.id, "Your number: " + str(allCodes[0]) + "?")
    bot.send_message(message.chat.id, "Number of cows:")
    bot.register_next_step_handler(message, setCows)

@bot.message_handler(commands=['start'])
def adviceToPlay(message):
    bot.send_message(message.chat.id, "Play again?[yes/no]?")
    bot.register_next_step_handler(message, game)

def game(message):
    if (message.text == "yes"):
        global allCodes, m, counter1, counter2, counter3
        allCodes = []
        m = 0
        counter1 = 0
        counter2 = 0
        counter3 = 0

        allCodes = generateNumbers()
        m = generateNumber()
        bot.send_message(message.chat.id, "Make your number")
        tryToGuess(message)
    else:
        bot.send_message(message.chat.id, "Well another time then")


@bot.message_handler(commands=['help'])
def speech(message):
    bot.send_message(message.chat.id, """Bulls and cows - a logical game, during which, for several attempts, one of the players must determine what the other player is up to.
    You and the computer are planning a secret 4-digit number with non-repeating numbers. The computer makes the first attempt to guess the number. An attempt is a 4-digit number with non-repeating numbers that is communicated to the enemy. In response, the adversary reports how many numbers were guessed without coinciding with their positions in the secret number (i.e. the number of cows) and how many were guessed right up to the position in the secret number (i.e. the number of bulls). For example:
    Concealed secret number "3219".
    Attempt: "2310".
    Result: two “cows” (two digits: “2” and “3” - guessed at the wrong positions) and one “bull” (one digit “1” guessed right up to the position).
    The winner is the one who guesses the number first.""")

if __name__ == '__main__':
    bot.polling(none_stop=True)
