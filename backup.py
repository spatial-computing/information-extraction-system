# encoding=utf8
__author__ = 'Shilpa'

from collections import defaultdict

from stop_words import get_stop_words
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from gensim import corpora, models, similarities
import DataBase
from Tkinter import *


def clean_doc(doc):
     # string goes in lists come out

    additional_stopwords = ['shall', 'beyond', 'include', 'must', 'less', 'more','use','whether','metre','given','maximum','minimum','within']
    stop_words = set(additional_stopwords).union(get_stop_words("en"))
    stemming = PorterStemmer()
    tokens = word_tokenize(doc)
    clean_document = [token.lower() for token in tokens if token.lower() not in stop_words and len(token) > 2]
    final = [stemming.stem(word) for word in clean_document]
    return [(final, doc)]

def doc_dictionary(clean_document):
    # cleanDoc goes in and dictionary of unique tokens is generated

    global dictionary
    dictionary = corpora.Dictionary(line.split() for line in clean_document)


def create_corpus(filename):
    # clean the corpus and convert it into segments and store in dictionary
    #also creates a dictionary of unique tokens in doc
    #converts corpus to vector space
    # generate vector space model

    global cleanCorpus
    global docMapping

    docMapping = defaultdict(list)

    cleanCorpus = []
    global Segment_index
    Segment_index = []
    global tf_idf

    for line in open(filename):
        Segment_index.append(line.strip("\n"))

        cleanCorpus.append(" ".join(clean_doc(line.decode('utf-8'))[0][0]))

        for v, k in clean_doc(line.decode('utf-8')):
            docMapping[k].append(v)

    doc_dictionary(cleanCorpus)

    corpus = MyCorpus()

    corpora.MmCorpus.serialize('corpus.mm', corpus)

    corpus = corpora.MmCorpus('corpus.mm')

    tf_idf = models.TfidfModel(corpus)


class MyCorpus(object):
    #convert corpus to vector space

    dictionary = {}
    def __iter__(self):
        for line in cleanCorpus:
            yield dictionary.doc2bow(line.lower().split())


def compare_strings(string1, string2):
    # def compareStrings(string1,string2) and returns similarity value

    global sim
    string1 = clean_doc(string1)[0][0]
    string2 = clean_doc(string2)[0][0]
    bag_words1 = dictionary.doc2bow(string1)
    bag_words2 = dictionary.doc2bow(string2)
    tf_idf1 = tf_idf[bag_words1]
    tf_idf2 = tf_idf[bag_words2]
    index = similarities.MatrixSimilarity([tf_idf1], num_features=len(dictionary))
    sim = index[tf_idf2]
    sim = round(sim, 2)*100
    return sim


def doc_similarity(input_string):
    # user input string goes and similarity with segments come out

    input_doc_similarity = []

    for i in range(len(cleanCorpus)):
        compare_strings(input_string, cleanCorpus[i])
        input_doc_similarity.append(sim)

    return input_doc_similarity



def improve_positive(main_similarity_list, user_suggestions):

    # user suggestion to improve positive results goes in and new similarities are returned.

        new_input_doc_similarity=[]

        index = Segment_index.index(user_suggestions)

        new_input_doc_similarity = doc_similarity(user_suggestions.decode('utf-8'))

        scaling_factor = (new_input_doc_similarity[index]-main_similarity_list[index])/100

        new_input_doc_similarity = [i*scaling_factor for i in new_input_doc_similarity]

        new_input_doc_similarity = [range_modification(i,"positive") for i in new_input_doc_similarity]


        final_similarities = [abs(i) for i in map(sum,zip(new_input_doc_similarity,main_similarity_list))]

        return final_similarities


def improve_negative(main_similarity_list, user_suggestions):

    # user suggestion to improve negative results goes in and new similarities are returned.

    new_input_doc_similarity = []

    index = Segment_index.index(user_suggestions)
    print index


    new_input_doc_similarity = doc_similarity(user_suggestions.decode('utf-8'))
    print new_input_doc_similarity




    scaling_factor = (new_input_doc_similarity[index] - main_similarity_list[index])/100
    print scaling_factor

    new_input_doc_similarity = [i*scaling_factor for i in new_input_doc_similarity]
    print new_input_doc_similarity


    new_input_doc_similarity = [range_modification(i,"negative") for i in new_input_doc_similarity]
    print new_input_doc_similarity

    final_similarities = [abs(i) for i in map(sum, zip(new_input_doc_similarity, main_similarity_list))]
    print final_similarities

    return final_similarities


def range_modification(number, flag):
    # Dissimilar with less than 10,  neutral between 15 to 30, similar more than 30

    if flag == "positive":

        if number <= 14:
            return -number
        else:
            return number

    if flag == "negative":
        if number > 29:

            return -number
        else:
            return number


def main(arg1, arg2):
    global similarities_list
    global user_input
    global country_name

    filename = "RawCorpus2.txt"
    create_corpus(filename)

    user_input = arg1
    country_name = arg2

    similarities_list = DataBase.get_data(country_name, user_input)

    if similarities_list:
        gen_colors(similarities_list)
    else:
        similarities_list = doc_similarity(user_input)
        DataBase.update_file(country_name, user_input, similarities_list)
        gen_colors(similarities_list)


def gen_colors(final_similarities):

    segment_colors = []

    for each in final_similarities:

        if each >= 0 and each <= 10:
            segment_colors.append("Red")
        elif each >10 and each <= 29:
            segment_colors.append("Yellow")
        elif each > 29 and each <= 100:
            segment_colors.append("Green")
        else:
            segment_colors.append("wrong")
    display_results(segment_colors)


def display_results(color_list):

    def data():

        for i in range(0,len(Segment_index)):

            top_frame = Frame(frame)
            frame1 = Frame(top_frame)
            frame2 = Frame(top_frame)

            Label(frame1, text=Segment_index[i],anchor=W,justify=LEFT,wraplength=750,bg=color_list[i]).pack()
            Label(frame2, text="Do you think this is marked incorrectly? Mark it as").pack(side=LEFT)
            Button(frame2, text=" Not Similar",command=lambda i=i:click_neg(i)).pack(side=RIGHT)
            Button(frame2, text="Similar", command=lambda i=i:click_pos(i)).pack(side=LEFT)

            frame1.pack()
            frame2.pack()
            top_frame.pack()

    def my_function(event):
        canvas.configure(scrollregion=canvas.bbox("all"),width=750,height=550)

    root = Tk()
    root.title("Similar Segments(green)")
    x_size = 800
    y_size = 600
    x_pos = 100
    y_pos = 100
    root.wm_geometry("%dx%d+%d+%d" % (x_size, y_size, x_pos, y_pos))

    my_frame = Frame(root,relief=GROOVE,width=50,height=100,bd=1)
    my_frame.place(x=10, y=10)

    canvas = Canvas(my_frame)
    frame = Frame(canvas)
    scrollbar1=Scrollbar(my_frame,orient="vertical", command=canvas.yview)
    scrollbar2=Scrollbar(my_frame,orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar1.set)
    canvas.configure(xscrollcommand=scrollbar2.set)

    scrollbar1.pack(side="right", fill="y")
    scrollbar2.pack(side="bottom", fill="x")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=frame, anchor='nw')
    frame.bind("<Configure>", my_function)
    data()
    root.mainloop()


def click_neg(num):
    new_list = (improve_negative(similarities_list, Segment_index[num]))
    update_similarities(new_list)


def click_pos(num):
    new_list = (improve_positive(similarities_list,Segment_index[num]))
    update_similarities(new_list)


def update_similarities(updated_similarity_list):

    similarities_list = updated_similarity_list
    DataBase.update_file(country_name, user_input, similarities_list)
    gen_colors(similarities_list)


if __name__ == "__main__":

    # testing scenarios
    user_input = "the visual line of sight from the operator must be equal to or less than 500m"
    main(user_input, "LA")