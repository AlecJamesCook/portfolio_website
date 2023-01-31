def change_please(amount,coins):

    """
    Determines whether a particular amount can be reached by using only a specified amount of coins

    :param amount: The desired amount to reach.
    :type: int/float

    :param coins: The number of coins that need to be used to reach the desired amount.
    :type: int

    :rtype: bool
    :return: Whether or not you can reach the amount using the specified number of coins.

    """

    # Times the amount by 100 to avoid floating point number shenanigans.
    amount *= 100
    coin_list = [200, 100, 50, 20, 10, 5, 2, 1]

    if coins < 1:
        return False

    def recursive_loop(amount, coins, coin_list):

        """
        The largest coin that is <= amount is subtracted from the amount until one of the base cases is reached. If a false base case is reach, the for loop moves on to the next smaller coin. This continues until the for loop has iterated over every element in the coinList, or if the amount and the number of coins both reach 0.

        :param amount: The desired amount to reach.
        :type: int/float

        :param coins: The number of coins that need to be used to reach the desired amount.
        :type: int

        :param coinList: The different coins that can be subtracted from the amount.
        :type: array (every element is an int).

        :rtype: bool
        :return: Whether or not you can reach the amount using the specified number of coins.

        """

        # The basecases for the recursive loop.
        if amount == 0 and coins == 0:
            return True
        elif amount == coins:
            return True
        elif amount != 0 and coins == 0:
            return False
        elif amount == 0 and coins != 0:
            return False

        for element in coin_list:
            if element <= amount:

                # Recurses the function until it finds a basecase.
                # If it hits a false basecase, the for loop continues.
                if recursive_loop((amount - element), (coins-1), coin_list):
                    return True

        #returns false if the for loop reaches the end before hitting a true basecase.
        return False

    return recursive_loop(amount, coins, coin_list)


def five_letter_unscramble(string):

    """

    When given a string, this function determines how many unique five-letter words can be made out of
    the letters in the string. Uses a set of wordle words as the source of these five-letter words.

    :param s: Contains the letters to be used when looking for unique five-letter words. Each letter can only be used once.
    :type: string

    :rtype: int
    :return: The number of unique five-letter words found in the wordle list that contain only the letters given in the parameter s.

    """

    def histogram_builder(string):

        """
        Creates a dictionary with the letters of the string as keys and the number of times the letters appear in the string as their values. This function appeared in the lecture notes from the Python course, namely the dictionary lesson. Many thanks to Federico!
        """

        histogram_dictionary = dict()

        for letter in string:
            if letter not in histogram_dictionary:
                histogram_dictionary[letter] = 1
            else:
                histogram_dictionary[letter] += 1

        return histogram_dictionary

    input_word_histogram = histogram_builder(string)

    with open('wordle.txt') as fin:
        contents = fin.readlines()
        words_list = []
        for line in contents:
            word = line.strip("\n")
            words_list.append(word)

    counter = 0
    no_of_matching_words = 0
    matching_words = []

    for word in words_list:
        words_list_histogram = histogram_builder(word)
        for letter in word:

            # This loop creates a histogram dictionary out of each word in the wordle list.
            # It then compares it's keys to the input string histogram's keys.
            # If the keys are in both of the dictionary and the value the other value,the counter is incremented.
            if letter in input_word_histogram and words_list_histogram[letter] <= input_word_histogram[letter]:
                counter += 1

            # If the counter reaches 5, it has found a unique five-letter word.
            if counter == 5:
                matching_words.append(word)

        counter = 0

    return matching_words


def document_stats(filename):
        """

        Reads a document and returns several statistics about the makeup of the file.

        :param filename: The name of the file to be read.
        :type: file

        :rtype: tuple
        :return: Contains (in order) the number of letters, the number of numeric characters, the number of symbols characters, the number of words, the number of sentences, and the number os paragraphs in the file.

        """

        num_letters = num_numbers = num_symbols = num_words = num_sentences = 0
        num_paragraphs = 1

        # Creates a list with all of the printable characters in the file as elements. It provides the number of words a base value. It will need to be added to later on.
        fin = open(filename)
        data = fin.read()
        word_length_file = data.split()
        num_words += len(word_length_file)
        fin.close()

        # This places the file into one string to make it easier to iterate over.
        fin_2 = open(filename)
        line_list = fin_2.readlines()
        text = ''.join(line_list)
        fin_2.close()

        for char in range(0, len(text)):
            # The next three statements use inbuilt functions to find the number of letters, numeric characters, and symbols in the string.
            num_letters += text[char].isalpha()
            num_numbers += text[char].isnumeric()
            num_symbols += text[char].isprintable() and not text[char].isalnum() and not text[char].isspace()

            # These two statements find sentences according to different puncuation symbols. The second conditional is there in case of floats.
            if text[char] == "." or text[char] == "!" or text[char] == "?":
                num_sentences += 1
            if text[char] == "." and text[char-1].isnumeric() and text[char+1].isnumeric():
                num_sentences -= 1

            # This adds to the base value of the number of words by checking for grammatical or puncuation errors in the source file. It checks whether the character is a symbol and if this symbol does not have a space following it (which indicates a typo in the source file).
            try:
                num_words += text[char].isprintable() and not text[char].isalnum() and not text[char].isspace() and text[char+1].isalpha() and not text[char-1].isspace()
            except:
                continue

            # Finds the number of paragraphs by finding a printable character and checking whether two new lines precede it.
            if text[char].isprintable() and text[char-1] == "\n" and text[char -2] == "\n":
                num_paragraphs += 1

        output_tuple = (num_letters, num_numbers, num_symbols, num_words, num_sentences, num_paragraphs)

        return output_tuple



def wanWang(input):

    number = str(input)
    result = ''
    counter = 0

    zero = 'líng'
    one = 'yī'
    two = 'èr'
    three = 'sān'
    four = 'sì'
    five = 'wǔ'
    six = 'liù'
    seven = 'qī'
    eight = 'bā'
    nine = 'jiǔ'
    ten = 'shí'

    hundred = 'bǎi'
    thousand = 'qiān'
    ten_thousand = 'wàn'
    hundred_million = 'yì'

    # SPECIAL NUMBERS
    liang = 'liǎng'

    ling = '零'
    yi = '一'
    er = '二'
    san = '三'
    si = '四'
    wu = '五'
    liu = '六'
    qi = '七'
    ba = '八'
    jiu = '九'
    shi = '十'

    bai = '百'
    qian = '千'
    wan = '万'
    yi2 = '亿'

    liang2 = '两'
    # BIGGEST = 1
    ### ONE DIGIT ###

    if len(number) == 1:

        for digit in number:

            if digit == '1':
                result += one + ' '
            elif digit == '2':
                result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                result += zero + ' '

    # BIGGEST = 10
    ### TWO DIGITS ###

    if len(number) == 2:

        for digit in number:
            if digit == '1':
                if counter == 0:
                    result += ten + ' '
                    counter += 1
                    continue
                else:
                    result += one + ' '
            elif digit == '2':
                result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                continue

            if counter == 0:
                result += ten + ' '
            counter += 1

    # BIGGEST = 100
    ### THREE DIGITS ###

    if len(number) == 3:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter != 2 and number[counter + 1] != '0':
                        result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0:
                result += hundred + ' '
            if counter == 1 and digit != '0':
                result += ten + ' '
            counter += 1

    # BIGGEST = 1000
    ### FOUR DIGITS ###

    if len(number) == 4:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                if counter == 0:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter != 3 and number[counter + 1] != '0':
                    result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0:
                result += thousand + ' '
            if counter == 1 and digit != '0':
                result += hundred + ' '
            if counter == 2 and digit != '0':
                result += ten + ' '
            counter += 1

    ### FIVE DIGITS ###

    # BIGGEST = 1, 0000
    if len(number) == 5:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                if counter == 1:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter != 4 and number[counter + 1] != '0':
                        result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0:
                result += ten_thousand + ' '
            if counter == 1 and digit != '0':
                result += thousand + ' '
            if counter == 2 and digit != '0':
                result += hundred + ' '
            if counter == 3 and digit != '0':
                result += ten + ' '
            counter += 1

    ### SIX DIGITS ###

    # BIGGEST = 10, 0000
    if len(number) == 6:

        for digit in number:
            if digit == '1':
                if counter == 0:
                    result += ten + ' '
                    counter += 1
                    continue
                else:
                    result += one + ' '
            elif digit == '2':
                if counter == 2:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 1:
                    result += ten_thousand + ' '
                    counter += 1
                    continue
                elif counter != 5 and number[counter + 1] != '0':
                        result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0 and digit != '1':
                result += ten + ' '
            if counter == 1:
                result += ten_thousand + ' '
            if counter == 2 and digit != '0':
                result += thousand + ' '
            if counter == 3 and digit != '0':
                result += hundred + ' '
            if counter == 4 and digit != '0':
                result += ten + ' '
            counter += 1

    ### SEVEN DIGITS ###

    # BIGGEST = 100, 0000
    if len(number) == 7:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                if counter == 3:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 2:
                    result += ten_thousand + ' '
                    counter += 1
                    continue
                if counter != 6 and number[counter + 1] != '0':
                        result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0:
                result += hundred + ' '
            if counter == 1 and digit != '0':
                result += ten + ' '
            if counter == 2:
                result += ten_thousand + ' '
            if counter == 3 and digit != '0':
                result += thousand + ' '
            if counter == 4 and digit != '0':
                result += hundred + ' '
            if counter == 5 and digit != '0':
                result += ten

            counter += 1

    ### eight  DIGITS ###

    # BIGGEST = 1000, 0000
    if len(number) == 8:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                if counter == 0 or counter == 4:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 3:
                    result += ten_thousand + ' '
                    counter += 1
                    continue
                if counter != 7 and number[counter + 1] != '0':
                        result += zero + ' '
                else:
                    counter += 1
                    continue

            if counter == 0:
                result += thousand + ' '
            if counter == 1 and digit != '0':
                result += hundred + ' '
            if counter == 2 and digit != '0':
                result += ten + ' '
            if counter == 3:
                result += ten_thousand + ' '
            if counter == 4 and digit != '0':
                result += thousand + ' '
            if counter == 5 and digit != '0':
                result += hundred + ' '
            if counter == 6 and digit != '0':
                result += ten + ' '

            counter += 1


    ### NINE DIGITS ###
    # BIGGEST = 1, 0000, 0000
    if len(number) == 9:

        for digit in number:
            if digit == '1':
                result += one + ' '
            elif digit == '2':
                if counter == 1 or counter == 5:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 1:
                    pass
                elif counter == 2 and number[2] != '0':
                    pass
                elif counter == 4:
                    pass
                elif counter != 8 and number[counter + 1] != '0':
                    result += zero + ' '

            if counter == 0:
                result += hundred_million + ' '
            if counter == 1 and digit != '0':
                result += thousand + ' '
            if counter == 2 and digit != '0':
                result += hundred + ' '
            if counter == 3 and digit != '0':
                result += ten + ' '

            if counter == 4 and digit != '0':
                result += ten_thousand + ' '
            elif counter == 4 and number[1] != '0':
                result += ten_thousand + ' '
            elif counter == 4 and number[2] != '0':
                result += ten_thousand + ' '
            elif counter == 4 and number[3] != '0':
                result += ten_thousand + ' '

            if counter == 5 and digit != '0':
                result += thousand + ' '
            if counter == 6 and digit != '0':
                result += hundred + ' '
            if counter == 7 and digit != '0':
                result += ten + ' '

            counter += 1

    ### 10 DIGITS ###
    # BIGGEST = 10, 0000, 0000
    if len(number) == 10:

        for digit in number:
            if digit == '1':
                if counter == 0:
                    result += ten + ' '
                    counter += 1
                    continue
                else:
                    result += one + ' '
            elif digit == '2':
                if counter == 2 or counter == 6:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 2:
                    pass
                elif counter == 3 and number[3] != '0':
                    pass
                elif counter == 5:
                    pass
                elif counter != 9 and number[counter + 1] != '0':
                    result += zero + ' '

            if counter == 0 and digit != '1':
                result += ten + ' '
            if counter == 1:
                result += hundred_million + ' '
            if counter == 2 and digit != '0':
                result += thousand + ' '
            if counter == 3 and digit != '0':
                result += hundred + ' '
            if counter == 4 and digit != '0':
                result += ten + ' '

            if counter == 5 and digit != '0':
                result += ten_thousand + ' '
            elif counter == 5 and number[2] != '0':
                result += ten_thousand + ' '
            elif counter == 5 and number[3] != '0':
                result += ten_thousand + ' '
            elif counter == 5 and number[4] != '0':
                result += ten_thousand + ' '

            if counter == 6 and digit != '0':
                result += thousand + ' '
            if counter == 7 and digit != '0':
                result += hundred + ' '
            if counter == 8 and digit != '0':
                result += ten + ' '

            counter += 1

    ### 11 DIGITS ###
    # BIGGEST = 100, 0000, 0000
    if len(number) == 11:

        for digit in number:
            if digit == '1':
                    result += one + ' '
            elif digit == '2':
                if counter == 3 or counter == 7:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 2:
                    result += hundred_million + ' '
                    counter += 1
                    continue
                if counter == 3:
                    pass
                elif counter == 4 and number[4] != '0':
                    pass
                elif counter == 6:
                    pass
                elif counter != 10 and number[counter + 1] != '0':
                    result += zero + ' '

            if counter == 0:
                result += hundred + ' '
            if counter == 1 and digit != '0':
                result += ten + ' '
            if counter == 2:
                result += hundred_million + ' '
            if counter == 3 and digit != '0':
                result += thousand + ' '
            if counter == 4 and digit != '0':
                result += hundred + ' '
            if counter == 5 and digit != '0':
                result += ten + ' '

            if counter == 6 and digit != '0':
                result += ten_thousand + ' '
            elif counter == 6 and number[3] != '0':
                result += ten_thousand + ' '
            elif counter == 6 and number[4] != '0':
                result += ten_thousand + ' '
            elif counter == 6 and number[5] != '0':
                result += ten_thousand + ' '

            if counter == 7 and digit != '0':
                result += thousand + ' '
            if counter == 8 and digit != '0':
                result += hundred + ' '
            if counter == 9 and digit != '0':
                result += ten + ' '

            counter += 1

    ### 12 DIGITS ###
    # BIGGEST = 1000, 0000, 0000
    if len(number) == 12:

        for digit in number:
            if digit == '1':
                    result += one + ' '
            elif digit == '2':
                if counter == 0 or counter == 4 or counter == 8:
                    result += liang + ' '
                else:
                    result += two + ' '
            elif digit == '3':
                result += three + ' '
            elif digit == '4':
                result += four + ' '
            elif digit == '5':
                result += five + ' '
            elif digit == '6':
                result += six + ' '
            elif digit == '7':
                result += seven + ' '
            elif digit == '8':
                result += eight + ' '
            elif digit == '9':
                result += nine + ' '
            elif digit == '0':
                if counter == 3:
                    result += hundred_million + ' '
                    counter += 1
                    continue
                if counter == 4:
                    pass
                elif counter == 5 and number[5] != '0':
                    pass
                elif counter == 7:
                    pass
                elif counter != 11 and number[counter + 1] != '0':
                    result += zero + ' '

            if counter == 0:
                result += thousand + ' '
            if counter == 1 and digit != '0':
                result += hundred + ' '
            if counter == 2 and digit != '0':
                result += ten + ' '
            if counter == 3:
                result += hundred_million + ' '
            if counter == 4 and digit != '0':
                result += thousand + ' '
            if counter == 5 and digit != '0':
                result += hundred + ' '
            if counter == 6 and digit != '0':
                result += ten + ' '

            if counter == 7 and digit != '0':
                result += ten_thousand + ' '
            elif counter == 7 and number[4] != '0':
                result += ten_thousand + ' '
            elif counter == 7 and number[5] != '0':
                result += ten_thousand + ' '
            elif counter == 7 and number[6] != '0':
                result += ten_thousand + ' '

            if counter == 8 and digit != '0':
                result += thousand + ' '
            if counter == 9 and digit != '0':
                result += hundred + ' '
            if counter == 10 and digit != '0':
                result += ten + ' '

            counter += 1


    resultList = result.split()
    CharacterResult = ''

    for element in resultList:
        if element == 'líng':
            CharacterResult += ling
        if element == 'yī':
            CharacterResult += yi
        if element == 'èr':
            CharacterResult += er
        if element == 'sān':
            CharacterResult += san
        if element == 'sì':
            CharacterResult += si
        if element == 'wǔ':
            CharacterResult += wu
        if element == 'liù':
            CharacterResult += liu
        if element == 'qī':
            CharacterResult += qi
        if element == 'bā':
            CharacterResult += ba
        if element == 'jiǔ':
            CharacterResult += jiu
        if element == 'shí':
            CharacterResult += shi

        if element == 'bǎi':
            CharacterResult += bai
        if element == 'qiān':
            CharacterResult += qian
        if element == 'wàn':
            CharacterResult += wan
        if element == 'yì':
            CharacterResult += yi2

        if element == 'liǎng':
            CharacterResult += liang2

    resultTuple = (number, result, CharacterResult)
    return resultTuple