from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import argparse


# MODEL_DIR =
MODEL_NAME = "mrm8488/t5-base-finetuned-summarize-news"

class ParagraphSummarizer:
    """Class to abstractive summarization the paragraph"""

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelWithLMHead.from_pretrained(MODEL_NAME)
        self.model.eval()
        #self.scripted_model = self.model.to_torchscript(method="script", file_path=None)

    @torch.no_grad()
    def execute(self, text_seq, max_length=150, num_beams=2, repetition_penalty=2.5, length_penalty=1.0, early_stopping=True) -> str:
        """Inference summarize the input text sequence"""
        input_ids = self.tokenizer.encode(text_seq, return_tensors="pt", add_special_tokens=True)
        generated_ids = self.model.generate(input_ids=input_ids,
                                            num_beams=num_beams,
                                            max_length=max_length,
                                            repetition_penalty=repetition_penalty,
                                            length_penalty=length_penalty,
                                            early_stopping=early_stopping)

        preds = [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
        return preds[0]

def main():
    """
    Example runs:
    ```
    python text_recognizer/paragraph_text_recognizer.py text_recognizer/tests/support/paragraphs/a01-077.png
    python text_recognizer/paragraph_text_recognizer.py https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png
    """
    parser = argparse.ArgumentParser(description="Recognize handwritten text in an image file.")
    parser.add_argument("text", type=str)
    args = parser.parse_args()

    text_summarizer = ParagraphSummarizer()
    pred_str = text_summarizer.execute(args.text)
    print(pred_str)


if __name__ == "__main__":
    main()