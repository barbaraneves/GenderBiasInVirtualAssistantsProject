import pandas as pd
import numpy as np
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix

from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
from math import ceil
import string

import urllib.request

CMAP_ICEFIRE = plt.get_cmap('icefire')
BAD_WORDS_URL = 'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en'

def tokenizer(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower().split()

def count_tokens(sentences, n_most_common=50, n_skip=5, to_ignore=[], remove_stopwords=True):
    doc = " ".join(sentences)
    tokens = tokenizer(doc)
    tokens_count = dict(Counter(tokens))
    if remove_stopwords:
        to_ignore = set(to_ignore) | set(STOP_WORDS)
    filtered_words = set(tokens) - set(to_ignore)
    for w in list(tokens_count.keys()):
        if w not in filtered_words or len(w) <= 2:
            del tokens_count[w]
    sorted_count = sorted(
        tokens_count.items(),
        key=lambda x: -x[1]
    )[n_skip:n_skip+n_most_common]
    
    return dict(sorted_count)

def plot_densities(data, xlabel, nrows=1, figsize=(16, 5), palette='icefire'):
    ncols = ceil(len(data.keys()) / nrows)
    sns.set(style='whitegrid', font_scale=1.3)
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    if ncols == nrows == 1:
        axs = [axs]
    for ax, (label, subset) in zip(axs, data.items()):
        sns.kdeplot(data=subset, ax=ax, palette=palette, fill=True, common_norm=False, alpha=.5, linewidth=0,)
        ax.set_title(label)
        ax.set_xlabel(xlabel)
    
def plot_word_clouds(data, title, nrows=1, figsize=(20, 8)):
    ncols = ceil(len(data.keys()) / nrows)
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    fig.suptitle(title, fontsize=20)
  
    if ncols == nrows == 1:
        axs = [axs]
    for ax, (label, count) in zip(axs, data.items()):
        wc = WordCloud(
          background_color='white',
          colormap=CMAP_ICEFIRE,
          width=1600,
          height=800,
          random_state=42
        ).generate_from_frequencies(count)

        ax.imshow(wc, interpolation='bilinear')
        ax.set_title(label)
        ax.axis('off')
    fig.tight_layout()

def get_text_from_url(url):
    with urllib.request.urlopen(url) as f:
        text = f.read().decode('utf-8')
    return text
  
bad_words = get_text_from_url(BAD_WORDS_URL).split('\n')

def count_bad_words(sentence):
    tokens = sentence.translate(str.maketrans('', '', string.punctuation)).lower().split()
    matches = [t for t in tokens if t in bad_words]
    return len(matches)
  
def plot_most_frequent_elements(count_elems, n_most_common, title, xlabel="Count"):
    most_common_elements = count_elems.most_common(n_most_common)
    
    # Sort the list by count; count is at second position of the tuple
    # We sort elements here so bigger elements are show on top
    most_common_elements.sort(key=lambda el: el[1])

    x = np.array([elem for elem, count in most_common_elements])
    y = np.array([count for elem, count in most_common_elements])

    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    
    sns.set(style='whitegrid', font_scale=1.3)
    plt.barh(x, y, color=CMAP_ICEFIRE(rescale(y)))
    plt.title(title)
    plt.xlabel(xlabel, fontsize=14)
    plt.xticks(rotation=80)
    for i, (elem, count) in enumerate(most_common_elements):
        plt.text(count, 
               i, 
               f' {round(count)} ', 
               rotation=0, 
               ha='left', 
               va='center', 
               color='black', 
               fontsize=12)
    plt.tight_layout() # Change the whitespace such that all labels fit nicely
    
def bar_values(ax, labels, rotation=60):
    rects = ax.patches
    
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 0.01, label, ha='center', va='bottom', fontsize=14, rotation=rotation)
    
    return ax

def plot_histogram_labels_count_each(x_label, y_label, labels, hue_label=None, data=None, palette='RdGy_r', title=None, width=None, height=None):
    sns.set(style='whitegrid', font_scale=1.3)
    fig, axes = plt.subplots(2, 3, figsize=(width, height))

    fig.suptitle(title)

    sns.barplot(ax=axes[0][0], x=x_label, y=y_label[0], palette=palette)
    axes[0][0].tick_params(axis='x', rotation=60)
    axes[0][0].set_title('Comentários anotados com 1 rótulo')
    bar_values(axes[0][0], labels[0], rotation = 0)

    sns.barplot(ax=axes[0][1], x=x_label, y=y_label[1], palette=palette)
    axes[0][1].tick_params(axis='x', rotation=60)
    axes[0][1].set_title('Comentários anotados com 2 rótulos')
    bar_values(axes[0][1], labels[1], rotation = 0)

    sns.barplot(ax=axes[0][2], x=x_label, y=y_label[2], palette=palette)
    axes[0][2].tick_params(axis='x', rotation=60)
    axes[0][2].set_title('Comentários anotados com 3 rótulos')
    bar_values(axes[0][2], labels[2], rotation = 0)

    sns.barplot(ax=axes[1][0], x=x_label, y=y_label[3], palette=palette)
    axes[1][0].tick_params(axis='x', rotation=60)
    axes[1][0].set_title('Comentários anotados com 4 rótulos')
    bar_values(axes[1][0], labels[3], rotation = 0)

    sns.barplot(ax=axes[1][1], x=x_label, y=y_label[4], palette=palette)
    axes[1][1].tick_params(axis='x', rotation=60)
    axes[1][1].set_title('Comentários anotados com 5 rótulos')
    bar_values(axes[1][1], labels[4], rotation = 0)

    sns.barplot(ax=axes[1][2], x=x_label, y=y_label[5], palette=palette)
    axes[1][2].tick_params(axis='x', rotation=60)
    axes[1][2].set_title('Comentários anotados com todos os rótulos')
    bar_values(axes[1][2], labels[5], rotation = 0)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.show()

def plot_histogram_labels(x_label, y_label, labels, hue_label=None, data=None, palette='RdGy_r', title=None, ylabel_title=None, width=None, height=None, rotation=60):
    sns.set(style='whitegrid', font_scale=1.3)
    plt.figure(figsize=(width, height))
    
    ax = sns.barplot(x_label, y_label, hue=hue_label, data=data, palette=palette, ci=None)
    
    plt.title(title, fontsize=18)
    plt.xlabel('')
    plt.ylabel(ylabel_title, fontsize=14)
    
    bar_values(ax, labels, rotation=rotation)
    plt.show()
    
def plot_corr_matrix(data, cols, title):
    sns.set(style='whitegrid', font_scale=1.3)
    plt.figure(figsize=(16, 8))
    
    correlation = data[cols].corr()
    mask = np.zeros_like(correlation, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    
    sns.heatmap(correlation, cmap='RdBu_r', annot=True, annot_kws={'size': 12}, mask=mask)
    plt.title(title, fontsize=18)
    plt.show()
    
def plot_distribution_large_data(data, title, xaxis_interval):
    '''
    Imprime um boxplot próprio para datasets grandes
    '''
    sns.set(style='whitegrid', font_scale=1.3)
    plt.figure(figsize=(16, 8))
    plt.title(title, fontsize=16)
    ax = sns.boxenplot(data=data, palette='PuBu', saturation=1, scale='area', orient='h')
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(xaxis_interval))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.setp(ax.get_xticklabels(), rotation=45);

def make_most_common_words(words, n_most_common):
    '''
    Retorna as n_most_common palavras mais comuns da lista words
    '''
    return Counter(words).most_common(n_most_common)
    
def generate_wordcloud(dict_):
    '''
    Dado um dicionário com os elementos da word cloud e a contagem de
    de cada elemento, é retornado um objeto WordCloud usado para gerar as
    nuvens de palavras nos gráficos
    '''
    wc = WordCloud(
        background_color='white',
        colormap=CMAP_ICEFIRE,
        width=1600, 
        height=800,
        random_state=42).generate_from_frequencies(dict_)
    return wc

def subplot_topic_wordcloud(wc_data, nrows, ncols, width, height, title, range_stop, range_step):
    '''
    Função que plota N x M subplots de WordClouds 
    '''
    fig, ax = plt.subplots(nrows, ncols, figsize=(width, height))
    fig.suptitle(title, fontsize=20)
    
    for i in range(0, range_stop, range_step):
        i_ax = int(i*0.5)
        ax[i_ax][0].imshow(wc_data[i][0], interpolation='bilinear')
        ax[i_ax][1].imshow(wc_data[i + 1][0], interpolation='bilinear')
        
        ax[i_ax][0].axis('off')
        ax[i_ax][0].set_title('{}'.format(wc_data[i][1]), fontdict={'fontsize': 18})
        
        ax[i_ax][1].axis('off')
        ax[i_ax][1].set_title('{}'.format(wc_data[i + 1][1]), fontdict={'fontsize': 18})
        fig.tight_layout()
    
def get_keys_by_values(dict_of_elements, list_of_values):
    list_of_keys = []
    inv_dict = {str(value): key for key, value in dict_of_elements.items()}
    for item in list_of_values:
        list_of_keys.append(inv_dict[str(item)])
    return list_of_keys
    
def plot_multilabel_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)
    
    # plt.figure(figsize=(18, 12))
    sns.heatmap(df_cm, annot=True, fmt="d", annot_kws={"size": 14},  linewidths=0.5, vmax=400, cmap='RdBu_r');
    
def plot_grid_multilabel_confusion_matrixes(y_true_list, y_pred_list, nrows, ncols, figsize, title, subtitles, labels):
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    fig.suptitle(title, fontsize=20, y=1.05)
    
    if ncols == nrows == 1:
        axs = [axs]
    else:
        axs = axs.flat


    for ax, subtitle, y_true, y_pred in zip(axs, subtitles, y_true_list, y_pred_list):
        cm = confusion_matrix(y_true, y_pred)
        print(cm)
        counter_rows_cm = [row.sum() for row in cm]
        counter_cols_cm = [sum(col) for col in zip(*cm)]
        
        print(counter_rows_cm, counter_cols_cm)
        
        counter_y_true = Counter(y_true)
        inv_counter_y_true = {value: key for key, value in counter_y_true.items()}
        
        counter_y_pred = Counter(y_pred)
        inv_counter_y_pred = {value: key for key, value in counter_y_pred.items()}
        
        print(counter_y_true)
        print(counter_y_pred)
        
        true_labels = [inv_counter_y_true[v] for v in counter_rows_cm]
        pred_labels = [inv_counter_y_pred[v] for v in counter_cols_cm]
        
        print(true_labels, pred_labels)

        df_cm = pd.DataFrame(cm, index=true_labels, columns=pred_labels)
        
        sns.heatmap(df_cm[labels], annot=True, fmt="d", annot_kws={"size": 14},  linewidths=0.5, vmax=400, cmap='RdBu_r', ax=ax)
        ax.set_title(subtitle)
        ax.set_xlabel('Valores Preditos', fontsize=16)
        ax.set_ylabel('Valores Reais', fontsize=16)
        plt.setp(ax.get_xticklabels(), rotation=45);
    fig.tight_layout()
    fig.show()
