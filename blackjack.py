"""Oczko, autor: Al Sweigart, al@inventwithpython.com
Klasyczna gra karciana. (Ta gra nie uwzględnia
rozdwojenia kart, ani ubezpieczenia.)
Więcej informacji na stronie https://pl.wikipedia.org/wiki/Blackjack.
Kod pobrany ze strony https://ftp.helion.pl/przyklady/wiksma.zip.
Etykiety: długi, gra, gra karciana"""

import random, sys

# Deklaracja stałych:
HEARTS   = chr(9829) # Znak 9829 to '♥'.
DIAMONDS = chr(9830) # Znak 9830 to '♦'.
SPADES   = chr(9824) # Znak 9824 to '♠'.
CLUBS    = chr(9827) # Znak 9827 to '♣'.

# (Listę kodów chr znajdziesz na stronie https://inventwithpython.com/charactermap).
BACKSIDE = 'tył'


def main():
    print('''Oczko, autor: Al Sweigart, al@inventwithpython.com

    Zasady:
      Spróbuj uzyskać liczbę punktów jak najbardziej zbliżoną do 21, ale nie większą.
      Króle, Damy i Walety mają 10 punktów.
      Asy mają 1 lub 11 punktów.
      Karty od 2 do 10 mają odpowiednią do swojego numeru liczbę punktów.
      Naciśnij H, by wziąć kolejną kartę.
      Klawisz S zatrzymuje dobieranie kart.
      Przy swojej pierwszej rozgrywce możesz wcisnąć P, by podwoić swój zakład,
      ale musisz to zrobić dokładnie jeden raz przed zakończeniem dobierania kart.
      W przypadku remisu, postawiona kwota jest zwracana graczowi.
      Krupier kończy dobierać karty przy wartości 17''')

    money = 5000
    while True:  # Główna pętla gry.
        # Sprawdź, czy gracz ma jeszcze pieniądze:
        if money <= 0:
            print("Jesteś spłukany!")
            print("Dobrze, że nie grałeś na prawdziwe pieniądze.")
            print('Dziękuję za grę!')
            sys.exit()

        # Gracz podaje wysokość zakładu w tej rundzie:
        print('Budżet:', money)
        bet = getBet(money)

        # Daj krupierowi i graczowi po dwie karty z talii:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Obsługa ruchów gracza:
        print('Zakład:', bet)
        while True:  # Wykonuj pętle, dopóki gracz nie przestanie dobierać karty lub nie przekroczy 21.
            displayHands(playerHand, dealerHand, False)
            print()

            # Sprawdź, czy gracz przekroczył 21:
            if getHandValue(playerHand) > 21:
                break

            # Odczytaj ruchy gracza S lub P:
            move = getMove(playerHand, money - bet)

            # Obsługa ruchów gracza:
            if move == 'P':
                # Gracz podwaja zakład, można zwiększyć zakład:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Zakład zwiększony do kwoty {}.'.format(bet))
                print('Zakład:', bet)

            if move in ('D', 'P'):
                # Wciśnięcie klawisza D lub P powoduje dobranie karty.
                newCard = deck.pop()
                rank, suit = newCard
                print('Wziąłeś {} {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # Gracz przekroczył 21:
                    continue

            if move in ('S', 'P'):
                # Wciśnięcie klawisza S lub P kończy kolejkę gracza.
                break

        # Obsługa ruchów krupiera:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # Krupier dobiera kartę:
                print('Krupier dobiera kartę...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break  # Krupier przekroczył 21.
                input('Naciśnij Enter, by kontynuować...')
                print('\n\n')

        # Pokazanie kart w dłoni:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # Ustalenie, czy gracz wygrał, przegrał, czy był remis:
        if dealerValue > 21:
            print('Krupier przekroczył 21! Wygrałeś {} PLN!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('Przegrałeś!')
            money -= bet
        elif playerValue > dealerValue:
            print('Wygrałeś {} PLN!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Jest remis, zakład wraca do Ciebie.')

        input('Naciśnij Enter, by kontynuować...')
        print('\n\n')


def getBet(maxBet):
    """Zapytaj gracza, ile chce w tej rundzie postawić."""
    while True:  # Pytaj, dopóki nie poda odpowiedniej kwoty.
        print('Ile chcesz postawić? (1-{} lub KONIEC)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'KONIEC':
            print('Dziękuję za grę!')
            sys.exit()

        if not bet.isdecimal():
            continue  # Jeśli gracz nie podał liczby, zapytaj jeszcze raz.

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet  # Gracz podał odpowiednią liczbę.


def getDeck():
    """Zwróć listę (figury, kolor) krotek wszystkich 52 kart."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Dodanie kart numerowanych.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Dodanie figur i asa.
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Pokazanie kart gracza i krupiera. Najpierw ukryj karty krupiera,
    jeśli zmienna showDealerHand jest równa False."""
    print()
    if showDealerHand:
        print('KRUPIER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('KRUPIER: ???')
        # Najpierw ukryj karty krupiera:
        displayCards([BACKSIDE] + dealerHand[1:])

    # Pokaż karty gracza:
    print('GRACZ:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    """Zwraca wartość kart. Figury są warte 10, asy
    11 lub 1 (ta funkcja wybiera najodpowiedniejszą wartość asa)."""
    value = 0
    numberOfAces = 0

    # Zsumowanie wartości kart, poza asami:
    for card in cards:
        rank = card[0]  # Karta to krotka (figura, kolor).
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):  # Figury mają 10 punktów.
            value += 10
        else:
            value += int(rank)  # Karty numerowane mają liczbę punktów zgodną z ich numerem.

    # Dodanie wartości asów:
    value += numberOfAces  # Dodanie 1.
    for i in range(numberOfAces):
        # Jeśli może być dodane pozostałe 10 punktów bez przekraczania 21, to tak zrób:
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    """Wyświetlanie wszystkich kart z listy."""
    rows = ['', '', '', '', '']  # Tekst do wyświetlenia w każdym wierszu.

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Wyświetlenie górnej krawędzi karty.
        if card == BACKSIDE:
            # Wyświetlenie tyłu karty:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Wyświetlenie przodu karty:
            rank, suit = card  # Karta to krotka.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    # Wyświetlenie każdego wiersza na ekranie:
    for row in rows:
        print(row)


def getMove(playerHand, money):
    """Zapytaj gracza o ruch i zwróć 'D' w przypadku dobierania, 'S',
    gdy gracz nie chce już dobierać kart, i 'P' dla podwojenia zakładu."""
    while True:  # Wykonuj pętle, dopóki gracz nie poda odpowiedniego ruchu.
        # Określ, jakie ruchy gracz może wykonać:
        moves = ['(D)obierz', '(S)top']

        # Gracz może podwoić zakład przy pierwszym ruchu, 
        # co można stwierdzić po tym, że ma dokładnie dwie karty:
        if len(playerHand) == 2 and money > 0:
            moves.append('(P)odwój')

        # Odczytaj ruch gracza:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('D', 'S'):
            return move  # Gracz podał poprawny ruch.
        if move == 'P' and '(P)odwój' in moves:
            return move  # Gracz podał poprawny ruch.


# Jeśli program został uruchomiony (a nie zaimportowany), rozpocznij grę:
if __name__ == '__main__':
    main()
