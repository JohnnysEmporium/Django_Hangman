from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import Event
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

    print(word)
    
    request.session['word'] = word
    request.session['wrong_count'] = 0
    request.session['guess'] = word_len
    request.session['wrong_letters'] = []
    request.session['game_over'] = 2

    return render(request, 'home.html', {'pics':HANGMANPICS[0], 'word_len': word_len})

def game(request):
    letter = request.GET.get('letter_web').upper()
    wrong_count = request.session['wrong_count']
    wrong_letters = request.session['wrong_letters']
    word = request.session['word'].upper()
    guess = request.session['guess']
    game_over = request.session['game_over']
    wrong_letter = ''
    
    def data():
        data = {
            'game_over': game_over,
            'pics': HANGMANPICS[wrong_count],
            'guess': guess, 
            'wrong_letter': wrong_letter,
            }
        
        return data
    
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
        if request.user.is_authenticated and game_over != 1:
            username = request.user.username
            Event.objects.update(loss = F('loss') + 1)
        print()
        game_over = 1
        request.session['game_over'] = game_over
        return JsonResponse(data())
    elif wrong_count < 7 and '_' not in guess:
        if request.user.is_authenticated and game_over != 0:
            username = request.user.username
            Event.objects.update(win = F('win') + 1)
        game_over = 0
        request.session['game_over'] = game_over
        return JsonResponse(data())
        

# ZROBIC COS Z GAME_OVER JAKIS WARUNEK ZEBY NIE PRZEPUSZCZALO PO ZAKONCZENIU GRY

    return JsonResponse(data())

        
        