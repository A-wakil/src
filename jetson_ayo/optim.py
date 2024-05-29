import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# Load the ONNX model
onnx_file_path = "/home/jetson/Downloads/prime.onnx"
onnx_engine_file_path = "/home/jetson/trtengine"

TRT_LOGGER = trt.Logger(trt.Logger.INFO)
builder = trt.Builder(TRT_LOGGER)
network_flags = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)

with open(onnx_file_path, "rb") as model:
    parser = trt.OnnxParser(builder)
    parser.parse(model.read())

    engine = builder.build_engine(network, config)

# Serialize the TensorRT engine to a file
with open(onnx_engine_file_path, "wb") as f:
    f.write(engine.serialize())

