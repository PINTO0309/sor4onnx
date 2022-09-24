#! /usr/bin/env python

import sys
import re
from argparse import ArgumentParser
import onnx
import onnx_graphsurgeon as gs
from typing import Optional, List

class Color:
    BLACK          = '\033[30m'
    RED            = '\033[31m'
    GREEN          = '\033[32m'
    YELLOW         = '\033[33m'
    BLUE           = '\033[34m'
    MAGENTA        = '\033[35m'
    CYAN           = '\033[36m'
    WHITE          = '\033[37m'
    COLOR_DEFAULT  = '\033[39m'
    BOLD           = '\033[1m'
    UNDERLINE      = '\033[4m'
    INVISIBLE      = '\033[08m'
    REVERCE        = '\033[07m'
    BG_BLACK       = '\033[40m'
    BG_RED         = '\033[41m'
    BG_GREEN       = '\033[42m'
    BG_YELLOW      = '\033[43m'
    BG_BLUE        = '\033[44m'
    BG_MAGENTA     = '\033[45m'
    BG_CYAN        = '\033[46m'
    BG_WHITE       = '\033[47m'
    BG_DEFAULT     = '\033[49m'
    RESET          = '\033[0m'

MODES = [
    'full',
    'inputs',
    'outputs',
]

SEARCH_MODES = [
    'exact_match',
    'partial_match',
    'prefix_match',
    'suffix_match',
]

def rename(
    old_new: List[str],
    input_onnx_file_path: Optional[str] = '',
    onnx_graph: Optional[onnx.ModelProto] = None,
    output_onnx_file_path: Optional[str] = '',
    mode: Optional[str] = 'full',
    search_mode: Optional[str] = 'exact_match',
    non_verbose: Optional[bool] = False,
) -> onnx.ModelProto:
    """
    Parameters
    ----------
    old_new: List[str]
        All occurrences of substring old replaced by new. \n\n\
        e.g.\n\
        old_new = ["onnx::", ""]

    input_onnx_file_path: Optional[str]
        Input onnx file path.\n\
        Either input_onnx_file_path or onnx_graph must be specified.\n\
        Default: ''

    onnx_graph: Optional[onnx.ModelProto]
        onnx.ModelProto.\n\
        Either input_onnx_file_path or onnx_graph must be specified.\n\
        onnx_graph If specified, ignore input_onnx_file_path and process onnx_graph.

    output_onnx_file_path: Optional[str]
        Output onnx file path. If not specified, no ONNX file is output.\n\
        Default: ''

    mode: Optional[str]
        Specifies the type of node to be replaced.\n\
        full or inputs or outputs.\n\n\
        full: Rename all nodes.\n\
        inputs: Rename only the input node.\n\
        outputs: Rename only the output node.\n\n\
        Default: 'full'

    search_mode: Optional[str]
        OP name search mode.\n\
        exact_match or partial_match.\n\n\
        exact_match: Exact match search for OP name.\n\
        partial_match: Partial match search for OP name.\n\
        prefix_match: Prefix match search for OP name.\n\
        suffix_match: Suffix match search for OP name.\n\n\
        Default: 'exact_match'

    non_verbose: Optional[bool]
        Do not show all information logs. Only error logs are displayed.\n\
        Default: False

    Returns
    -------
    renamed_graph: onnx.ModelProto
        Renamed onnx ModelProto.
    """

    # Unspecified check for input_onnx_file_path and onnx_graph
    if not input_onnx_file_path and not onnx_graph:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'One of input_onnx_file_path or onnx_graph must be specified.'
        )
        sys.exit(1)

    if not isinstance(old_new, list) or len(old_new) != 2:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'old_new must be two strings [old, new].'
        )
        sys.exit(1)

    if mode not in MODES:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'The mode must be one of the following. {MODES}'
        )
        sys.exit(1)

    if search_mode not in SEARCH_MODES:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'The search_mode must be one of the following. {SEARCH_MODES}'
        )
        sys.exit(1)

    # Loading Graphs
    # onnx_graph If specified, onnx_graph is processed first
    if not onnx_graph:
        onnx_graph = onnx.load(input_onnx_file_path)
    graph = gs.import_onnx(onnx_graph)
    graph.cleanup().toposort()

    if mode in ['full', 'inputs']:
        for graph_input in graph.inputs:
            if search_mode == 'exact_match':
                if graph_input.name == old_new[0]:
                    graph_input.name = graph_input.name.replace(old_new[0], old_new[1])
            elif search_mode == 'partial_match':
                graph_input.name = graph_input.name.replace(old_new[0], old_new[1])
            elif search_mode == 'prefix_match':
                graph_input.name = re.sub(f'^{old_new[0]}', f'{old_new[1]}', graph_input.name)
            elif search_mode == 'suffix_match':
                graph_input.name = re.sub(f'{old_new[0]}$', f'{old_new[1]}', graph_input.name)

    if mode in ['full', 'outputs']:
        for graph_output in graph.outputs:
            if search_mode == 'exact_match':
                if graph_output.name == old_new[0]:
                    graph_output.name = graph_output.name.replace(old_new[0], old_new[1])
            elif search_mode == 'partial_match':
                graph_output.name = graph_output.name.replace(old_new[0], old_new[1])
            elif search_mode == 'prefix_match':
                graph_output.name = re.sub(f'^{old_new[0]}', f'{old_new[1]}', graph_output.name)
            elif search_mode == 'suffix_match':
                graph_output.name = re.sub(f'{old_new[0]}$', f'{old_new[1]}', graph_output.name)

    if mode in ['full']:
        for graph_node in graph.nodes:
            # OP Name
            if search_mode == 'exact_match':
                if graph_node.name == old_new[0]:
                    graph_node.name = graph_node.name.replace(old_new[0], old_new[1])
            elif search_mode == 'partial_match':
                graph_node.name = graph_node.name.replace(old_new[0], old_new[1])
            elif search_mode == 'prefix_match':
                graph_node.name = re.sub(f'^{old_new[0]}', f'{old_new[1]}', graph_node.name)
            elif search_mode == 'suffix_match':
                graph_node.name = re.sub(f'{old_new[0]}$', f'{old_new[1]}', graph_node.name)

            # OP INPUTS
            for graph_node_input in graph_node.inputs:
                if search_mode == 'exact_match':
                    if graph_node_input.name == old_new[0]:
                        graph_node_input.name = graph_node_input.name.replace(old_new[0], old_new[1])
                elif search_mode == 'partial_match':
                    graph_node_input.name = graph_node_input.name.replace(old_new[0], old_new[1])
                elif search_mode == 'prefix_match':
                    graph_node_input.name = re.sub(f'^{old_new[0]}', f'{old_new[1]}', graph_node_input.name)
                elif search_mode == 'suffix_match':
                    graph_node_input.name = re.sub(f'{old_new[0]}$', f'{old_new[1]}', graph_node_input.name)

            # OP OUTPUTS
            for graph_node_output in graph_node.outputs:
                if search_mode == 'exact_match':
                    if graph_node_output.name == old_new[0]:
                        graph_node_output.name = graph_node_output.name.replace(old_new[0], old_new[1])
                elif search_mode == 'partial_match':
                    graph_node_output.name = graph_node_output.name.replace(old_new[0], old_new[1])
                elif search_mode == 'prefix_match':
                    graph_node_output.name = re.sub(f'^{old_new[0]}', f'{old_new[1]}', graph_node_output.name)
                elif search_mode == 'suffix_match':
                    graph_node_output.name = re.sub(f'{old_new[0]}$', f'{old_new[1]}', graph_node_output.name)

    # opname auto supplementation
    # OPs in old ONNX files may be missing opname,
    # so opname is automatically completed when opname is empty.
    supplementation_idx = 0
    for graph_node in graph.nodes:
        if graph_node.name == '':
            graph_node.name = f'sor_{graph_node.op}_{supplementation_idx}'
            supplementation_idx += 1

    graph.cleanup().toposort()

    # Shape Estimation
    renamed_graph = None
    try:
        renamed_graph = onnx.shape_inference.infer_shapes(gs.export_onnx(graph))
    except:
        renamed_graph = gs.export_onnx(graph)
        if not non_verbose:
            print(
                f'{Color.YELLOW}WARNING:{Color.RESET} '+
                'The input shape of the next OP does not match the output shape. '+
                'Be sure to open the .onnx file to verify the certainty of the geometry.'
            )

    # Save
    if output_onnx_file_path:
        onnx.save(renamed_graph, output_onnx_file_path)

    if not non_verbose:
        print(f'{Color.GREEN}INFO:{Color.RESET} Finish!')

    # Return
    return renamed_graph


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-if',
        '--input_onnx_file_path',
        type=str,
        required=True,
        help='Input onnx file path.'
    )
    parser.add_argument(
        '-on',
        '--old_new',
        type=str,
        nargs=2,
        required=True,
        help=\
            'All occurrences of substring old replaced by new. \n\n'+
            'e.g.\n'+
            '--old_new "onnx::" ""'
    )
    parser.add_argument(
        '-of',
        '--output_onnx_file_path',
        type=str,
        required=True,
        help='Output onnx file path.'
    )
    parser.add_argument(
        '-m',
        '--mode',
        type=str,
        choices=MODES,
        default='full',
        help=\
            'Specifies the type of node to be replaced. \n'+
            'full or inputs or outputs. \n\n'+
            'full: Rename all nodes. \n'+
            'inputs: Rename only the input node. \n'+
            'outputs: Rename only the output node. \n\n'+
            'Default: full'
    )
    parser.add_argument(
        '-sm',
        '--search_mode',
        type=str,
        choices=SEARCH_MODES,
        default='exact_match',
        help=\
            'OP name search mode. \n'+
            'exact_match or partial_match or prefix_match or suffix_match. \n\n'+
            'exact_match: Exact match search for OP name. \n'+
            'partial_match: Partial match search for OP name. \n'+
            'prefix_match: Prefix match search for OP name. \n'+
            'suffix_match: Suffix match search for OP name. \n\n'+
            'Default: exact_match'
    )
    parser.add_argument(
        '-n',
        '--non_verbose',
        action='store_true',
        help='Do not show all information logs. Only error logs are displayed.'
    )
    args = parser.parse_args()

    input_onnx_file_path = args.input_onnx_file_path
    old_new = args.old_new
    mode = args.mode
    search_mode = args.search_mode
    output_onnx_file_path = args.output_onnx_file_path
    non_verbose = args.non_verbose

    # Load
    onnx_graph = onnx.load(input_onnx_file_path)

    # OP add
    renamed_graph = rename(
        input_onnx_file_path=None,
        onnx_graph=onnx_graph,
        old_new=old_new,
        mode=mode,
        search_mode=search_mode,
        output_onnx_file_path=output_onnx_file_path,
        non_verbose=non_verbose,
    )


if __name__ == '__main__':
    main()
