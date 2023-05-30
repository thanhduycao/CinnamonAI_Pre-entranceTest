from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from fastT5 import get_onnx_model
import torch
import argparse
import time

MODEL_NAME = "VietAI/vit5-base-vietnews-summarization"
MODEL_PATH = "models/vit5-quantized-model"


class ParagraphSummarizer:
    """Class to abstractive summarization the paragraph"""

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = get_onnx_model(model_name=MODEL_NAME, onnx_models_path=MODEL_PATH)
        self.model.eval()

    @torch.no_grad()
    def execute(
        self,
        text_seq,
        max_length=150,
        num_beams=2,
        repetition_penalty=2.5,
        length_penalty=1.0,
        early_stopping=True,
    ) -> str:
        """Inference summarize the input text sequence"""
        encoding = self.tokenizer(text_seq, return_tensors="pt")

        generated_ids = self.model.generate(
            input_ids=encoding["input_ids"],
            attention_mask=encoding["attention_mask"],
            num_beams=num_beams,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
            early_stopping=early_stopping,
        )

        preds = [
            self.tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            for g in generated_ids
        ]
        print("Time: ", time.time() - t1)
        return preds[0]


def main():
    """
    Example runs:
    ```
    python text_recognizer/paragraph_text_recognizer.py text_recognizer/tests/support/paragraphs/a01-077.png
    python text_recognizer/paragraph_text_recognizer.py https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png
    """
    parser = argparse.ArgumentParser(
        description="Abstractive summarize the input text sequence"
    )
    parser.add_argument("text", type=str)
    args = parser.parse_args()

    text_summarizer = ParagraphSummarizer()
    pred_str = text_summarizer.execute(args.text)
    print(pred_str)


if __name__ == "__main__":
    main()
