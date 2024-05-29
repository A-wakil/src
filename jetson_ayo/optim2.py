import tensorrt as trt

TRT_LOGGER = trt.Logger(trt.Logger.INFO)
builder = trt.Builder(TRT_LOGGER)

# Optionally configure builder parameters here

network = builder.create_network()
config = builder.create_builder_config()
parser = trt.OnnxParser(network, TRT_LOGGER)

# Parse the ONNX model
onnx_model_path = "/home/jetson/Downloads/prime.onnx"
with open(onnx_model_path, "rb") as model:
    parser.parse(model.read())

# Optionally optimize the network here

# Build the TensorRT engine
engine = builder.build_engine(network, config)

# Serialize the TensorRT engine to a file
engine_file_path = "/home/jetson/trtengine.trt"
with open(engine_file_path, "wb") as f:
    f.write(engine.serialize())

