from django.shortcuts import render
from django.http import JsonResponse
import random

f = open('static/words.txt')
words = f.read()
words = words.split()
f.close()

HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''']

def home(request):
    min = 0
    max = len(words)
    rnd = random.randint(min,max)
    word = words[rnd]
    word_len = ['_'] * len(word)

    
    request.session['word'] = word
    request.session['wrong_count'] = 0
    request.session['guess'] = word_len
    request.session['game_over'] = False 

    
    return render(request, 'home.html', {'pics':HANGMANPICS[0], 'word_len': word_len})

def game(request):
    letter = request.GET.get('letter_web')
    wrong_count = request.session['wrong_count']
    word = request.session['word']
    guess = request.session['guess']
    game_over = request.session['game_over']

    if wrong_count >= 5:
        game_over = True

    if letter in word:
        for idx, i in enumerate(word):
            if letter == i:
                  guess[idx] = letter
                  request.session['guess'] = guess
    else:
        wrong_count += 1
        request.session['wrong_count'] = wrong_count
    
    
    data = {
        'game_over': game_over,
        'pics': HANGMANPICS[wrong_count],
        'guess': guess, 
        'letter_serv': letter,
        }
    
    return JsonResponse(data)
    
        