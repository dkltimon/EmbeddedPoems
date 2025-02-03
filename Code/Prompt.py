# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 00:04:14 2024

@author: KeliDu
"""

import os
import re
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from matplotlib import pyplot as plt
import seaborn as sns
import openai
from openai import OpenAI
openai.api_key = ""
os.environ["OPENAI_API_KEY"] = openai.api_key
client = OpenAI()


os.chdir(r'C:\Workstation\conferences\2025_DH\chinese')


def chat_with_gpt(prompt, model="gpt-4"):
    """
    Sends a prompt to the ChatGPT API and returns the response.

    Parameters:
        prompt (str): The input text to send to the model.
        model (str): The model to use (e.g., "gpt-4", "gpt-3.5-turbo").

    Returns:
        str: The response from the ChatGPT model.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

data_df = pd.read_csv(r'annotated_data.csv', sep='\t')
all_responses = []

x = 0
while x < len(data_df):
    text = data_df['text'][x]
    #user_prompt = "The following Chinese text contains a poem. The beginning and end of the poem are marked with 'p_s' and 'p_e' respectively. You have three task. First task, determine the narrative function of the poem. There are four options: commentary, character portraiture, scene, plot. Second task, determine the position of a poem in a novel. There are three options: beginning, middle, end. Third task, determine the perspective of the poem. There are two options: character, narrator. For each task, you must choose one and only one option as your answer. You don't have to explain your answer, just output your answer in this format {answer to the first task}, {answer to the second task}, {answer to the third task} using the given labels. Here is the text with the poem:" + '\n' + text
    #user_prompt = "The following Chinese text contains a poem. The beginning and end of the poem are marked with 'p_s' and 'p_e' respectively. You have three task. First task, determine the narrative function of the poem. There are four options: 1.commentary, which offers comments and critiques of events, society, morality, characters, etc.  2.character portraiture, which describes a character, e.g., their appearance, inner feelings, emotions, and personality. 3.scene, which describes natural scenery, objects, and nature. 4.plot, which conveys, narrates, and sometimes summarizes a sequence of events. Second task, determine the position of a poem in a novel. The position indicates the structural role that the poem plays in the narrative of the fiction. There are three options: 1.beginning, means that the poem is an opening poem for a chapter. 2.middle, means that the poem is in the middle of a plot. 3.end, means the poem comes at the end of the chapter and concludes the storyline. Third task, determine whether the poem is composed or recounted from the first-person perspective of a character in the story or a third-person perspective of the author or a storyteller. If the former, please answer with 'character', if the latter, please answer with 'narrator'. For each task, you must choose one and only one option as your answer. You don't have to explain your answer, just output your answer in this format {answer to the first task}, {answer to the second task}, {answer to the third task} using the given option labels. Here is the text with the poem:" + '\n' + text
    user_prompt = "The following Chinese text contains a poem. The beginning and end of the poem are marked with 'p_s' and 'p_e' respectively. Your task is to determine the narrative function of the poem, considering both the content and the context of it. First, determine if the poem offers comments and critiques of events, society, morality, characters, etc. If yes, answer ‘commentary’. If no, determine if the poem describes natural scenery, objects, and nature. If yes, answer ‘scene’. If no, determine if the poem describes characters, e.g., their appearance, inner feelings, emotions, and personality. If yes, answer ‘character portraiture’. If no, determine if the poem conveys, narrates, and sometimes summarizes a sequence of events. If yes, answer ‘plot’. If still no, read the text again and choose one from the above mentioned three options (‘commentary’, ‘character portraiture’, ‘scene’). You must choose one and only one option as your answer and you don't have toexplain why you choose the label. Here is the text with the poem:" + '\n' + text
    response = chat_with_gpt(user_prompt)
    print(response)
    all_responses.append(response)
    x+=1

data_df['content_ChatGPT'] = all_responses
data_df.to_csv(r'responsed_data_binary.csv', sep='\t', index=False)


results_df = pd.read_csv(r'responsed_data_long.csv', sep='\t')

new_results = open(r'C:\Users\KeliDu\Desktop\bi_cn.txt', 'r', encoding='utf-8').read().split('\n')
new_df = pd.read_csv(r'C:\Users\KeliDu\Desktop\long_cn.csv', sep='\t')


print(classification_report(results_df['content'], new_df['content']))

'''
short prompt:
                       precision    recall  f1-score   support

character portraiture       0.16      0.72      0.26        36
           commentary       0.87      0.33      0.48       145
                 plot       0.03      1.00      0.06         1
                scene       0.72      0.41      0.53       157

             accuracy                           0.41       339
            macro avg       0.45      0.62      0.33       339
         weighted avg       0.72      0.41      0.48       339
         
              precision    recall  f1-score   support

   beginning       0.00      0.00      0.00        32
         end       0.00      0.00      0.00        16
      middle       0.86      0.98      0.91       291

    accuracy                           0.84       339
   macro avg       0.29      0.33      0.30       339
weighted avg       0.74      0.84      0.79       339

              precision    recall  f1-score   support

   character       0.58      0.93      0.71       166
    narrator       0.83      0.35      0.49       173

    accuracy                           0.63       339
   macro avg       0.71      0.64      0.60       339
weighted avg       0.71      0.63      0.60       339

long:

              precision    recall  f1-score   support

   character       0.57      0.96      0.72       166
    narrator       0.89      0.32      0.47       173

    accuracy                           0.63       339
   macro avg       0.73      0.64      0.59       339
weighted avg       0.73      0.63      0.59       339

   beginning       0.00      0.00      0.00        32
         end       0.20      0.06      0.10        16
      middle       0.86      0.98      0.92       291

    accuracy                           0.84       339
   macro avg       0.35      0.35      0.34       339
weighted avg       0.75      0.84      0.79       339

                       precision    recall  f1-score   support

character portraiture       0.22      0.81      0.34        36
           commentary       0.86      0.57      0.69       145
                 plot       0.05      1.00      0.09         1
                scene       0.82      0.46      0.59       157

             accuracy                           0.55       339
            macro avg       0.49      0.71      0.43       339
         weighted avg       0.77      0.55      0.61       339

binary:
                       precision    recall  f1-score   support

character portraiture       0.20      0.72      0.31        36
           commentary       0.80      0.65      0.72       145
                 plot       0.00      0.00      0.00         1
                scene       0.91      0.38      0.54       157

             accuracy                           0.53       339
            macro avg       0.48      0.44      0.39       339
         weighted avg       0.79      0.53      0.59       339
'''

labels = ['character portraiture', 'commentary', 'plot', 'scene']
#labels = ["character's", "narrator's"]
#labels = ['beginning', 'end', 'middle']
ConfusionMatrixDisplay.from_predictions(results_df['content'], new_df['content'], display_labels = labels, xticks_rotation="vertical")
plt.show()


from collections import Counter

data_df= pd.read_csv(r'responsed_data_long.csv', sep='\t')

content_count = Counter(data_df['content'])
perspective_count = Counter(data_df['perspective'])
position_count = Counter(data_df['position'])

aa = pd.DataFrame(content_count.items(), columns=['label', 'count'])
bb = pd.DataFrame(perspective_count.items(), columns=['label', 'count'])
cc = pd.DataFrame(position_count.items(), columns=['label', 'count'])

sns.set(font_scale=2)
sns.set_style("whitegrid")
f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
sns.barplot(y="label", x="count", data=aa, ax=ax1)
ax1.set_title('content')
sns.barplot(y="label", x="count", data=bb, ax=ax2)
ax2.set_title('perspective')
sns.barplot(y="label", x="count", data=cc, ax=ax3)
ax3.set_title('position')
plt.show()



check_results = []
x = 0
while x < 339:
    if data_df['position'][x] == data_df['position_ChatGPT'][x]:
        check_results.append('correct')
    else:
        check_results.append('incorrect')
    x+=1









