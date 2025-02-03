from transformers import pipeline
import pandas as pd

labels = ["人物描述","评论","开场诗","情节","收场诗"]

all_data = pd.read_csv(r'poems_annotations_responses_UsinglongPrompt.csv', sep='\t')
poems = all_data['text']

#oracle = pipeline(model="facebook/bart-large-mnli")
#classifier = pipeline("zero-shot-classification", model="IDEA-CCNL/Erlangshen-Roberta-110M-NLI")
classifier = pipeline("zero-shot-classification", model="morit/chinese_xlm_xnli")

predicted_labels = []
#result = oracle(sequence_to_classify, candidate_labels=labels)
x = 0
while x < len(all_data):
	sequence_to_classify = poems[x]
	result = classifier(sequence_to_classify, labels)
	predicted_labels.append(result['labels'][0])
	print(result['labels'][0])
	print(x)
	x+=1
  
from sklearn.metrics import classification_report
classification_report = classification_report(predicted_labels, list(all_data['content_Gold']))
print(classification_report)