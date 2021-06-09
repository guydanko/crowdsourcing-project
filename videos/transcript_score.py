import json
import re
import FRAKE
import nltk
from nltk import ngrams
from nltk.stem import PorterStemmer
from PyDictionary import PyDictionary

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


KEYWORDS_NUMBER_MULTIPLIER = 3
MAX_NUMBER_OF_KEYWORDS = 10
KEYWORDS_NUMBER_LIMITATION_FACTOR = 3
MATCH_BONUS = 0.2

# stopwords from FRAKE's source code
stopwords = ['somehow', 'which', 'before', 'three', 'or', 'should', 'might', 'own', 'those', 'to', 'above', 'nor', 'me',
             'seems', 'after', 'empty', 'put', 'that', 'will', 'while', 'across', 'been', 'something', 'ie', 'from',
             'eight', 'herein', 'below', 'into', 'fifty', 'it', 'when', 'for', 'fifteen', 'top', 'hers', 'anyway',
             'between', 'nevertheless', 'the', 'still', 'whither', 'and', 'found', 'our', 'through', 'have',
             'whereupon', 'without', 'off', 'am', 'at', 'beside', 'four', 'himself', 'move', 'him', 'be', 'out', 'its',
             'thereupon', 'third', 'well', 'yet', 'such', 'themselves', 'as', 'thereafter', 'what', 'whoever',
             'sincere', 'until', 'too', 'many', 'not', 'whom', 'again', 'he', 'else', 'latter', 'of', 'on', 'anywhere',
             'towards', 'done', 'same', 'side', 'almost', 'find', 'upon', 'everything', 'hundred', 'often', 'thru',
             'twenty', 'are', 'afterwards', 'beforehand', 'bottom', 'except', 'ours', 'forty', 'rather', 'either',
             'meanwhile', 'since', 'then', 'thereby', 'because', 'once', 'whatever', 'wherein', 'you', 'do',
             'everywhere', 'during', 'front', 'she', 'detail', 'indeed', 'system', 'thin', 'name', 'his', 'others',
             'somewhere', 'now', 'whereafter', 'is', 'whereas', 'around', 'more', 'cannot', 'onto', 'seem', 'whole',
             'much', 'very', 'cry', 'hasnt', 'any', 'sometime', 'alone', 'etc', 'my', 'seeming', 'throughout', 'up',
             'their', 'anyone', 'can', 'yours', 'thus', 'take', 'nine', 'along', 'itself', 'ten', 'thence', 'there',
             'enough', 'further', 'go', 'interest', 'due', 'hereafter', 'few', 'back', 'formerly', 'here', 'nobody',
             'only', 'whenever', 'each', 'moreover', 'anyhow', 'how', 'also', 'un', 'amoungst', 'may', 'hereupon',
             'otherwise', 'us', 'was', 'give', 'over', 'some', 'under', 'than', 'becoming', 'amongst', 'mine', 'next',
             'fill', 'first', 'please', 'so', 'though', 'another', 'beyond', 'perhaps', 'see', 'fire', 'yourself',
             'none', 'whence', 'i', 'has', 'yourselves', 'full', 'noone', 'six', 'all', 'being', 'thick', 'least',
             'latterly', 'ltd', 'seemed', 'where', 'together', 'eg', 'other', 'show', 'whether', 'herself', 'among',
             'therefore', 'in', 'this', 'made', 'although', 'against', 'hereby', 'wherever', 'de', 'five', 'already',
             'could', 'two', 'your', 'never', 'eleven', 'most', 'sixty', 'a', 'however', 'one', 'but', 'her', 'if',
             'call', 'get', 'sometimes', 'twelve', 'within', 'mill', 'an', 'nowhere', 'must', 'con', 'everyone', 'per',
             'these', 'bill', 'keep', 'neither', 'myself', 'serious', 'we', 'whereby', 'nothing', 'always', 'amount',
             'becomes', 'namely', 'behind', 'last', 'mostly', 'therein', 'why', 'even', 'couldnt', 'ever', 'became',
             'every', 'down', 'about', 'elsewhere', 'ourselves', 'co', 're', 'by', 'who', 'via', 'former', 'several',
             'toward', 'both', 'would', 'someone', 'no', 'whose', 'less', 'describe', 'hence', 'anything', 'them',
             'cant', 'they', 'inc', 'part', 'had', 'become', 'were', 'besides', 'with']

# using custom stopwords for FRAKE consistancy (stopwords from FRAKES source code)
stp = set(stopwords)
ps = PorterStemmer()
dictionary = PyDictionary()


def clean_transcript_text(text):
    # remove new lines
    return text.replace('\n', ' ')


def clean_user_tag_and_split(text):
    """ Responsible for tag preprocessing """
    # remove clean, remove stopwords and stem
    text = re.sub(r"<.*?>", ' ', text)
    text = re.sub(r"\&\#\;", '', text)
    text = re.sub(r"[\`\'\"\-\/\,\.\!\?\(\)\>\<\=\[\]\{\}]", ' ', text)
    text = text.lower()
    cleaned_text_as_list = [ps.stem(word) for word in text.split() if word not in stp]
    print(cleaned_text_as_list)
    return cleaned_text_as_list


def string_to_tuple(str):
    # sort for comparison consistency
    return tuple(str.split().sort())


def add_synonims(grams, synonims_dictionary):
    """ Adds synonym n-grams """
    grams_with_added_synonims = []
    for gram in grams:
        for idx, word in enumerate(gram):
            if word in synonims_dictionary:
                synonyms_for_word = synonims_dictionary[word]
                for synonym in synonyms_for_word:
                    # taking into account only synonyms which are a single word
                    if len(synonym.split()) == 1:
                        gram_duplication_as_list = list(gram)
                        # replace word with synonym
                        gram_duplication_as_list[idx] = synonym
                        grams_with_added_synonims.append(tuple(gram_duplication_as_list))
        # also adding the original gram
        grams_with_added_synonims.append(gram)
    return grams_with_added_synonims


def pydict_object_to_dict(pydict_object):
    """ Responsible for synonym dictionary format conversion """
    synonym_dictionary = {}
    for synonims_dictionary in pydict_object:
        if synonims_dictionary:
            for word, synonyms_list_for_word in synonims_dictionary.items():
                synonym_dictionary[word] = synonyms_list_for_word
    return synonym_dictionary


def extract_relevant_transcript(start, end, list_of_transcrit_dictionaries):
    """ Responsible for extracting the relevant info from the transcript """
    cleaned_relevant_transcript = ""
    for transcript_dictionary in list_of_transcrit_dictionaries:
        current_transcript_start = transcript_dictionary["start"]
        if start <= current_transcript_start <= end:
            print(transcript_dictionary["text"])
            cleaned_relevant_transcript += clean_transcript_text(transcript_dictionary["text"]) + " "

    return cleaned_relevant_transcript


def get_number_of_keywords(cleaned_relevant_transcript, user_tag_text_split):
    """ Calculates the amount of keywords the model should extract based on the relevant transcript length """
    transcrip_size_key_limitation = max(
        int(len(cleaned_relevant_transcript.split()) / KEYWORDS_NUMBER_LIMITATION_FACTOR), 1)
    number_of_keywords = min(len(user_tag_text_split) * KEYWORDS_NUMBER_MULTIPLIER, MAX_NUMBER_OF_KEYWORDS,
                             transcrip_size_key_limitation)
    return number_of_keywords


def reformat_kw(key_phrase_to_rating):
    """ Reformatting FRAKE's output and normalizing the scores by the max score """
    key_phrases_as_tuples_to_rating = {}
    max_score = max(key_phrase_to_rating.values())
    for phrase, rating in key_phrase_to_rating.items():
        phrase_as_tupe = tuple(sorted([ps.stem(word) for word in phrase.split()]))
        if phrase_as_tupe in key_phrases_as_tuples_to_rating:
            # duplicate elimination
            key_phrases_as_tuples_to_rating[phrase_as_tupe] += rating / max_score
        else:
            key_phrases_as_tuples_to_rating[phrase_as_tupe] = rating / max_score
    print(key_phrases_as_tuples_to_rating)
    return key_phrases_as_tuples_to_rating


def get_n_gram(user_tag_text_split, n):
    """ Splitting the user tag to n-grams (receives n as an input) """
    n_gram_output = [tuple(sorted(gram)) for gram in ngrams(user_tag_text_split, n)]
    # ignore duplicates
    n_gram_output = set(n_gram_output)
    print(n_gram_output)
    return n_gram_output


def calculate_score(gram_output, key_phrases_as_tuples_to_rating, normalizing_factor):
    """ Calculates the n-gram score using dot product """
    # normalizing factor should be the length of the original gram before adding the synonyms duplicates
    score = 0
    for gram in gram_output:
        if gram in key_phrases_as_tuples_to_rating:
            print(f'{gram}: {key_phrases_as_tuples_to_rating[gram]}')
            score += key_phrases_as_tuples_to_rating[gram]
    # normalize scores, so longer tags wont have an advantage
    if gram_output:
        score = score / normalizing_factor
    return score


def get_transcript_score(transcript_json, start, end, users_tag_text):
    """ Putting it all together """
    list_of_transcript_dictionaries = json.loads(transcript_json)
    cleaned_relevant_transcript = extract_relevant_transcript(start, end, list_of_transcript_dictionaries)

    user_tag_text_split = clean_user_tag_and_split(users_tag_text)

    number_of_keywords = get_number_of_keywords(cleaned_relevant_transcript, user_tag_text_split)

    kw = FRAKE.KeywordExtractor(lang='en', hu_hiper=0.4, Number_of_keywords=number_of_keywords)
    key_phrase_to_rating = kw.extract_keywords(cleaned_relevant_transcript)
    print(key_phrase_to_rating)

    key_phrases_as_tuples_to_rating = reformat_kw(key_phrase_to_rating)

    one_gram_output = get_n_gram(user_tag_text_split, 1)
    two_gram_output = get_n_gram(user_tag_text_split, 2)
    three_gram_output = get_n_gram(user_tag_text_split, 3)

    pydict_object = PyDictionary(*user_tag_text_split).getSynonyms()
    synonym_dictionary = pydict_object_to_dict(pydict_object)

    one_gram_with_synonims = add_synonims(one_gram_output, synonym_dictionary)
    print(one_gram_with_synonims)
    two_gram_with_synonims = add_synonims(two_gram_output, synonym_dictionary)
    print(two_gram_with_synonims)
    three_gram_with_synonims = add_synonims(three_gram_output, synonym_dictionary)
    print(three_gram_with_synonims)

    one_gram_score_normalized = calculate_score(one_gram_with_synonims, key_phrases_as_tuples_to_rating,
                                                len(one_gram_output))
    two_gram_score_normalized = calculate_score(two_gram_with_synonims, key_phrases_as_tuples_to_rating,
                                                len(two_gram_output))
    three_gram_score_normalized = calculate_score(three_gram_with_synonims, key_phrases_as_tuples_to_rating,
                                                  len(three_gram_output))

    print(one_gram_score_normalized)
    print(two_gram_score_normalized)
    print(three_gram_score_normalized)

    score_avg = (one_gram_score_normalized + two_gram_score_normalized + three_gram_score_normalized)/3
    # 0.0 - 1.0 (score >> 0.5 in very rare cases)
    if score_avg:
        # 0.4 - 1.0
        final_score = score_avg + MATCH_BONUS
    else:
        # 0.0 -> no matches for transcript
        final_score = score_avg
    print(f"Final Score :{final_score}")
    return final_score
