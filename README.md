# EmbeddedPoems

Data & Code for analyzing embedded poems in Ming & Qing novels.

The file **poems_annotations_responses_UsinglongPrompt.csv** contains our annotated dataset of **339 classical Chinese text excerpts**. The file includes **13 columns** with the following types of information:

* **`text`**: The excerpt from novels, each row contains a poem (marked using `p_s` and `p_e`) and its context.
* **Gold standard annotations** (`*_Gold`): Human-annotated categories identifying the narrative **perspective**, **content**, and **position** of embedded poems in Ming & Qing novels.
* **Label answered by different models** from three large language models:

  * **ChatGPT** (`*_ChatGPT`)
  * **LlamaChinese** (`*_LlamaChinese`)
  * **Llama3** (`*_Llama3`)

Each model provides its predictions for:

* **Perspective** (narrator, character)
* **Content** (commentary, plot, character portraiture, scene)
* **Position** (beginning, middle, end)
