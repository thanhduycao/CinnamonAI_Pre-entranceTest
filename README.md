# Summerizer Tool
## Introduction
Being inspiration by the needs of capturing the core information of a document when there are a lot of things that we need to read everyday, I decided to buil a summarization tool that can help us to do that. This tool will help us to summarize the content of a document into a few sentences that can capture the most value information, as well as showing top keywords of the document. This tool will be built by using the ViT5 pretrained model, as well as DistilBert multilingual pretrained model for the embedding extraction.

The idea was also being inspired by [Quillbot](https://quillbot.com/summarize), an online summarization tool that is simple in use and modern in design.
## Technical Overview
### Summarizer
#### Model selection
Recently, there are an outbreak of transformer-based models that can be used effectively in various of tasks, from Natural Language Processing, to Computer Vision as well. T5 is the encoder-decoder transformer-based model that was introduced by Google, which the power of fine-tuning on diverse NLP downstream tasks, including summarization.

[ViT5](https://huggingface.co/VietAI/vit5-base-vietnews-summarization) is the **state-of-the-art** pretrained Transformer-based encoder-decoder model for Vietnamese on vietnews dataset, which was fine-tuning on the T5 model. The base model show great potential, however, as it base on transformer architecture, the performance with respect to time is quite heavy.

#### Model optimization
Thanks to the work from [fastt5](https://github.com/Ki6an/fastT5) library, we can optimize T5 family model to the *onnx* format to speed up around 5x faster in inference time (with 1-2 sentences: from ~5s to ~1.5s). Because the library do not support inferencing on GPU [[ref]](https://github.com/Ki6an/fastT5/issues/34), and the last time it was updated is 2 years ago, the technique of OnnxT5 class was fork into the models folder in text_summerizer to add the extra configuration. The inference of onnx can be configured:
- Running on CPU: using onnxruntime library and set the `providers` to `['CPUExecutionProvider']`, using quantized model.
- Running on GPU: using onnxruntime-gpu library and set the `providers` to `['CUDAExecutionProvider']`, using non-quantized model.

However, after experiencing with the onnxruntime-gpu on T4 15GB from google colab, I found that the inference time is not much different from the use of CPU, the reason can possibly come from *io-binding*, which I still not be able to use it. Therefore, I decided to use the CPU version for the inference.

*Notes*: The notebook for fine-tuning the T5 model family, (including ViT5) on the summarization task can be found in the [training] folder. I was experimenting with the ViT5 model, although the training log shows decreasing in the eval loss, which was potential, the training loss seems to be flutuated. Therefore, I decided to use the original model for quicker and safer development.
### Keyword Extractor
#### Model selection
We need model to extract the embedding of the document by the sentence level. At first, I chose [PhoBERT](https://huggingface.co/VoVanPhuc/sup-SimCSE-VietNamese-phobert-base) for sentence embedding extraction, however, my hardware cpu is run out of memory when I try to run the server. Therefore, I research and found that "DistilBERT is a small, fast, cheap and light Transformer model trained by distilling BERT base. It has 40% less parameters than bert-base-uncased, runs 60% faster while preserving over 95% of BERT’s performances as measured on the GLUE language understanding benchmark." [[ref]](https://huggingface.co/docs/transformers/model_doc/distilbert).
Moreover, the [sentence_transformer](https://www.sbert.net/docs/pretrained_models.html) libary also support the use of DistilBert multi-lingual model, which support upto 50 languages, including Vietnamese. Therefore, I decided to use this model for the embedding extraction.

#### Word segmentation
We need word segmentation to capture the keyword in word level, for example, the word "học sinh" will be segmented into "học_sinh", which will be better as we get keyword also in word level.

The word segmentation is done by using [underthesea](https://github.com/undertheseanlp/underthesea) library - word_tokenize method.

#### Cosine similarity
The cosine similarity is used to calculate the similarity between the embedding of the word and the embedding of the document. The higher the cosine similarity score, the more similar the word is to the document.

#### Pipeline
The pipeline of the keyword extraction is shown in the step below:
- Input: a document.
- Load the DistilBert multilingual model as Sentence Transformer.
- Get the embedding of the document by using DistilBert multilingual model.
- Word segmentation the document into word level.
- Extract each words in the document into list using CountVectorizer.
- Get the word embedding of each word in the document.
- Calculate cosine similarity between the word embedding and the document embedding.
- Sort the cosine similarity score in descending order.
- Get the top n words with highest cosine similarity score, this will be our top n keywords.
### Server optimization
After reasearching, I found that using Torch serve or Triton server for inference server of AI core, and treat it as a service in a microservices backend architecture (written in NestJS), along with service for user such as login, logout is an optimal solution for the real-life full stack AI project. However, it requires strong server, and also running microservices required strong hardward, as I know so far. As the project aim for quick demo and runnable, I decided to follow the simple approach, which is using Flask for the server, and run it with one service only.
## How to install
The project was run on follow requirements:
### Requirements
#### Client
- node == 16.15.
#### Server
- python == 3.7.6
- pip == 21.2.4

### Installation
#### Client
- Make sure you have install nodejs: https://nodejs.org/en/download/
- Go to the client folder: `cd client`
- Install dependencies: `npm install --force` or `yarn install --force` (if you use yarn). We use force as mui styles has some problem with the latest version of react-scripts.

#### Server
- Make sure you have install python: https://www.python.org/downloads/
- You need to download the foler model from [link](https://drive.google.com/drive/folders/1gV6JBp8q1hwnk2p5gjJ_MhKE1lZyr6ru?usp=sharing) and put in the *models/* to make the folder structure like this *models/vit5-quantized-model/...*
- Go to the server folder: `cd server`
- You can create a virtual environment for the project: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Usage
### Client
- Go to the client folder: `cd client`
- Run the client: `npm start` or `yarn start` (if you use yarn) for development mode.
- Build the client: `npm run build` or `yarn build` (if you use yarn) for production mode.
After running the client, you can access the client at `http://localhost:3000/`.
### Server
Before running the server, make sure to run `export PYTHONPATH=.` before executing any commands later on, or you will get errors like this:
```python
ModuleNotFoundError: No module named 'text_recognizer'
```

In order to not have to set `PYTHONPATH` in every terminal you open, just add that line as the last line of the `~/.bashrc` file using a text editor of your choice (e.g. `nano ~/.bashrc`) or by concatenating with `>>`
```bash
echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc
```
- Go to the server folder: `cd server`
- Activate the virtual environment: `source venv/bin/activate`
- Run the server: `python server/server.py`
After running the server, you can access the API at `http://localhost:5000/`.
Remember to run both client and server, running only one of them will not work.
## Demo
How you can use the tool:
- Paste the document that you want to summarize into the text area.
- Click on the "Summarize" button and wait the summarization to be done.
- At the same time, you can see the top keywords of the document in the bottom of the input text area.
- Tada, you have the summary of the document, as well as the top keywords of the document.

## Checklist
- [x] Develop summarization model.
- [x] Optimize the summarization model for onnx inference.
- [x] Develop keyword extraction model.
- [x] Build the backend server.
- [x] Build the frontend client.
- [ ] Optimize server with batch inference.
- [ ] Automatic testing and pre-commit.
- [ ] Package the project into docker.
- [ ] Deploy the project to cloud.
