import random

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Event

f = open('static/words.txt')
words = f.read()
words = words.split()
f.close()

HANGMANPICS = [['  +---+', '      |', '      |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '      |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', '      |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', '  |   |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|   |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', '      |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', ' /    |', '      |', '========='], ['  +---+', '  |   |', '  O   |', ' /|\\  |', ' / \\  |', '      |', '=========']]


def home(request):
    min = 0
    max = len(words)
    rnd = random.randint(min, max)
    word = words[rnd]
    word_len = ['_'] * len(word)

    request.session['word'] = word
    request.session['wrong_count'] = 0
    request.session['guess'] = word_len
    request.session['wrong_letters'] = ['']
    request.session['game_over'] = 2
    request.session.modified = True

    print(word)

    def _grad_():
        if win != loss:
            grad = str((win * 100) / (win + loss))
            if win == 0 and loss > 0:
                grad = '-100%'
            elif win > 0 and loss == 0:
                grad = '100%'
            else:
                if float(grad) < 50:
                    grad = str(float(grad) - 100) + "%" 
                else:
                    grad = grad + '%'
        else:
            grad = ''
        return grad
        
    def _top_():
        events = Event.objects.all().order_by('win')[:5]
        result = []
        for i in events:
            result.append([getattr(i, 'win'), getattr(i, 'name')])
        result.reverse()    
        
        return result
        
    if request.user.is_authenticated:
        win = getattr(Event.objects.get(name=request.user.username), "win")
        loss = getattr(Event.objects.get(name=request.user.username), "loss")
        stats = [request.user.username, win, loss]
        return render(request, 'home.html', {'pics':HANGMANPICS[0], 'word_len': word_len, 'stats': stats, 'grad': _grad_(), 'top': _top_()})
    
    else:
        return render(request, 'home.html', {'pics':HANGMANPICS[0], 'word_len': word_len, 'top': _top_()})


def game(request):
    letter = request.GET.get('letter_web').upper()
    wrong_count = request.session['wrong_count']
    wrong_letters = request.session['wrong_letters']
    word = request.session['word'].upper()
    guess = request.session['guess']
    game_over = request.session['game_over']
    wrong_letter = ''
    usr = Event.objects.filter(name=request.user.username)
    
    def data():
        game_over = request.session['game_over']
        guess = request.session['guess']
        wrong_letters = request.session['wrong_letters'][-1]
        
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
            request.session.modified = True
    
    if wrong_count == 7 and game_over == 2:
        request.session['game_over'] = 1
        usr.update(loss=F('loss') + 1)
        request.session.modified = True
        return JsonResponse(data())
    elif wrong_count < 7 and '_' not in guess and game_over == 2:
        usr.update(win=F('win') + 1)
        request.session['game_over'] = 0
        request.session.modified = True
        return JsonResponse(data())
    elif wrong_count > 7:
        pass    

    return JsonResponse(data())