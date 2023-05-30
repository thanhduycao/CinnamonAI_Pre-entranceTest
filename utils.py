from fastT5 import export_and_get_onnx_model
from pathlib import Path


def export_and_load_onnx(model_name, saved_path, quantized=True):
    """
    Returns the optional quantized onnx model from T5 model.
        Parameters:
            model_name (str): name of the model to be converted
            saved_path (str): path to save the onnx model
            quantized (bool): whether to quantize the model or not
        Returns:
            model (OnnxT5): returns the onnx model
    """
    # Check whether the onnx model already exists
    if os.path.exists(saved_path):
        raise Exception("ONNX model already exists")
    _folder = Path.cwd()
    saved_models_path = _folder.joinpath(saved_models_path=saved_path)
    model = export_and_get_onnx_model(
        model_or_model_path=model_name,
        custom_output_path=saved_models_path,
        quantized=quantized,
    )
    return model
