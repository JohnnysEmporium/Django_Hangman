from django.shortcuts import render
from django.http import JsonResponse
import random

f = open('static/words.txt')
words = f.read()
words = words.split()
f.close()

HANGMANPICS = [['  +---+', '      |', '      |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '      |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', '  |   |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|   |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', ' /    |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', ' / \\  |', '      |', '=========']]

def home(request):
    min = 0
    max = len(words)
    rnd = random.randint(min,max)
    word = words[rnd]
    word_len = ['_'] * len(word)

    
    request.session['word'] = word
    request.session['wrong_count'] = 0
    request.session['guess'] = word_len
    request.session['wrong_letters'] = []

    return render(request, 'home.html', {'pics':HANGMANPICS[0], 'word_len': word_len})

def game(request):
    letter = request.GET.get('letter_web').upper()
    wrong_count = request.session['wrong_count']
    wrong_letters = request.session['wrong_letters']
    word = request.session['word'].upper()
    guess = request.session['guess']
    wrong_letter = ''
    
    if letter in word:
        for idx, i in enumerate(word):
            if letter == i:
                  guess[idx] = letter
                  request.session['guess'] = guess
    else:
        if letter not in wrong_letters:
            wrong_letters.append(letter)
            wrong_letter = wrong_letters[-1]
            request.session['wrong_letters'] = wrong_letters
            wrong_count += 1
            request.session['wrong_count'] = wrong_count
    
    if wrong_count >= 7:
        game_over = True
    elif wrong_count < 7 and '_' not in guess:
        game_over = False
    else:
        game_over = None
    
    print(word)
    
    data = {
        'game_over': game_over,
        'pics': HANGMANPICS[wrong_count],
        'guess': guess, 
        'wrong_letter': wrong_letter,
        }
    
    return JsonResponse(data)