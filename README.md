# sor4onnx
**S**imple **O**P **R**enamer for **ONNX**.

https://github.com/PINTO0309/simple-onnx-processing-tools

[![Downloads](https://static.pepy.tech/personalized-badge/sor4onnx?period=total&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sor4onnx) ![GitHub](https://img.shields.io/github/license/PINTO0309/sor4onnx?color=2BAF2B) [![PyPI](https://img.shields.io/pypi/v/sor4onnx?color=2BAF2B)](https://pypi.org/project/sor4onnx/) [![CodeQL](https://github.com/PINTO0309/sor4onnx/workflows/CodeQL/badge.svg)](https://github.com/PINTO0309/sor4onnx/actions?query=workflow%3ACodeQL)

# Key concept

- [x] Performs a partial match search on the specified string and replaces all input and output names with the specified string.

## 1. Setup
### 1-1. HostPC
```bash
### option
$ echo export PATH="~/.local/bin:$PATH" >> ~/.bashrc \
&& source ~/.bashrc

### run
$ pip install -U onnx \
&& python3 -m pip install -U onnx_graphsurgeon --index-url https://pypi.ngc.nvidia.com \
&& pip install -U sor4onnx
```
### 1-2. Docker
```bash
### docker pull
$ docker pull pinto0309/sor4onnx:latest

### docker build
$ docker build -t pinto0309/sor4onnx:latest .

### docker run
$ docker run --rm -it -v `pwd`:/workdir pinto0309/sor4onnx:latest
$ cd /workdir
```

## 2. CLI Usage
```bash
$ sor4onnx -h

usage:
  sor4onnx [-h]
  --input_onnx_file_path INPUT_ONNX_FILE_PATH
  --old_new OLD_NEW OLD_NEW
  --output_onnx_file_path OUTPUT_ONNX_FILE_PATH
  [--non_verbose]

optional arguments:
  -h, --help
        show this help message and exit.

  --input_onnx_file_path INPUT_ONNX_FILE_PATH
        Input onnx file path.

  --old_new OLD NEW
        All occurrences of substring old replaced by new.
        e.g.
        --old_new "onnx::" ""

  --output_onnx_file_path OUTPUT_ONNX_FILE_PATH
        Output onnx file path.

  --non_verbose
        Do not show all information logs. Only error logs are displayed.
```

## 3. In-script Usage
```python
>>> from sor4onnx import rename
>>> help(rename)

Help on function rename in module sor4onnx.onnx_opname_renamer:

rename(
    old_new: List[str],
    input_onnx_file_path: Union[str, NoneType] = '',
    onnx_graph: Union[onnx.onnx_ml_pb2.ModelProto, NoneType] = None,
    output_onnx_file_path: Union[str, NoneType] = '',
    non_verbose: Union[bool, NoneType] = False
) -> onnx.onnx_ml_pb2.ModelProto

    Parameters
    ----------
    old_new: List[str]
        All occurrences of substring old replaced by new.
        e.g.
        old_new = ["onnx::", ""]

    input_onnx_file_path: Optional[str]
        Input onnx file path.
        Either input_onnx_file_path or onnx_graph must be specified.
        Default: ''

    onnx_graph: Optional[onnx.ModelProto]
        onnx.ModelProto.
        Either input_onnx_file_path or onnx_graph must be specified.
        onnx_graph If specified, ignore input_onnx_file_path and process onnx_graph.

    output_onnx_file_path: Optional[str]
        Output onnx file path. If not specified, no ONNX file is output.
        Default: ''

    non_verbose: Optional[bool]
        Do not show all information logs. Only error logs are displayed.
        Default: False

    Returns
    -------
    renamed_graph: onnx.ModelProto
        Renamed onnx ModelProto.
```

## 4. CLI Execution
```bash
$ sor4onnx \
--input_onnx_file_path fusionnet_180x320.onnx \
--old_new "onnx::" "" \
--output_onnx_file_path fusionnet_180x320_renamed.onnx
```

## 5. In-script Execution
```python
from sor4onnx import rename

onnx_graph = rename(
  old_new=["onnx::", ""],
  input_onnx_file_path="fusionnet_180x320.onnx",
  output_onnx_file_path="fusionnet_180x320_renamed.onnx",
)

# or

onnx_graph = rename(
  old_new=["onnx::", ""],
  onnx_graph=graph,
)
```

## 6. Sample
### Before
![image](https://user-images.githubusercontent.com/33194443/166736425-54b19eab-b025-441c-a1ce-79c075a9b26f.png)

### After
![image](https://user-images.githubusercontent.com/33194443/166736670-a784850b-bec3-4d74-95a4-dd67738ac481.png)

## 7. Reference
1. https://github.com/onnx/onnx/blob/main/docs/Operators.md
2. https://docs.nvidia.com/deeplearning/tensorrt/onnx-graphsurgeon/docs/index.html
3. https://github.com/NVIDIA/TensorRT/tree/main/tools/onnx-graphsurgeon
4. https://github.com/PINTO0309/simple-onnx-processing-tools
5. https://github.com/PINTO0309/PINTO_model_zoo

## 8. Issues
https://github.com/PINTO0309/simple-onnx-processing-tools/issues
