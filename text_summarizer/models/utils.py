import os, psutil
from pathlib import Path

os.environ["OMP_NUM_THREADS"] = str(psutil.cpu_count(logical=True))
os.environ["OMP_WAIT_POLICY"] = "ACTIVE"


from onnxruntime import (
    GraphOptimizationLevel,
    InferenceSession,
    SessionOptions,
    ExecutionMode,
)


_auth_token = None


def get_auth_token():
    """Get the user-configurable auth token, which defaults to None

    Returns:
        auth_token (Optional[Union[str, bool]]) for authenticating with huggingface.co
    """
    global _auth_token
    return _auth_token


def get_onnx_runtime_sessions(
    model_paths,
    default: bool = True,
    opt_level: int = 99,
    parallel_exe_mode: bool = True,
    n_threads: int = 0,
    provider=["CUDAExecutionProvider", "CPUExecutionProvider"],
) -> InferenceSession:
    """
            Optimizes the model

    Args:
        model_paths (List or Tuple of str) : the path to, in order:
            path_to_encoder (str) : the path of input onnx encoder model.
            path_to_decoder (str) : the path of input onnx decoder model.
            path_to_initial_decoder (str) :  the path of input initial onnx decoder model.
        default : set this to true, ort will choose the best settings for your hardware.
                  (you can test out different settings for better results.)
        opt_level (int) : sess_options.GraphOptimizationLevel param if set 1 uses 'ORT_ENABLE_BASIC',
                          2 for 'ORT_ENABLE_EXTENDED' and 99 for 'ORT_ENABLE_ALL',
                          default value is set to 99.
        parallel_exe_mode (bool) :  Sets the execution mode. Default is True (parallel).
        n_threads (int) :  Sets the number of threads used to parallelize the execution within nodes. Default is 0 to let onnxruntime choose
        provider : execution providers list.

    Returns:
        encoder_session : encoder onnx InferenceSession
        decoder_session : decoder onnx InferenceSession
        decoder_sess_init : initial decoder onnx InferenceSession

    """
    path_to_encoder, path_to_decoder, path_to_initial_decoder = model_paths

    if default:
        encoder_sess = InferenceSession(str(path_to_encoder), providers=provider)

        decoder_sess = InferenceSession(str(path_to_decoder), providers=provider)

        decoder_sess_init = InferenceSession(
            str(path_to_initial_decoder), providers=provider
        )

    else:
        # Few properties that might have an impact on performances
        options = SessionOptions()

        if opt_level == 1:
            options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_BASIC
        elif opt_level == 2:
            options.graph_optimization_level = (
                GraphOptimizationLevel.ORT_ENABLE_EXTENDED
            )
        else:
            assert opt_level == 99
            options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL

        # set this true for better performance
        if parallel_exe_mode == True:
            options.execution_mode = ExecutionMode.ORT_PARALLEL
        else:
            options.execution_mode = ExecutionMode.ORT_SEQUENTIAL

        options.intra_op_num_threads = n_threads
        # options.inter_op_num_threads = 10

        # options.enable_profiling = True

        encoder_sess = InferenceSession(
            str(path_to_encoder), options, providers=provider
        )

        decoder_sess = InferenceSession(
            str(path_to_decoder), options, providers=provider
        )

        decoder_sess_init = InferenceSession(
            str(path_to_initial_decoder), options, providers=provider
        )

    return encoder_sess, decoder_sess, decoder_sess_init


def get_model_paths(pretrained_model, model_path, quantized):
    model_path.mkdir(parents=True, exist_ok=True)

    # gets only the filename
    pretrained_model_name = Path(pretrained_model).stem

    if not quantized:
        encoder_path = model_path.joinpath(f"{pretrained_model_name}-encoder.onnx")
        decoder_path = model_path.joinpath(f"{pretrained_model_name}-decoder.onnx")
        init_decoder_path = model_path.joinpath(
            f"{pretrained_model_name}-init-decoder.onnx"
        )
    else:
        encoder_path = model_path.joinpath(
            f"{pretrained_model_name}-encoder-quantized.onnx"
        )
        decoder_path = model_path.joinpath(
            f"{pretrained_model_name}-decoder-quantized.onnx"
        )
        init_decoder_path = model_path.joinpath(
            f"{pretrained_model_name}-init-decoder-quantized.onnx"
        )

    return encoder_path, decoder_path, init_decoder_path
