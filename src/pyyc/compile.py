import compiler
import utils
import argparse
import uniquify as uniq
import heapify as hpfy
import closure as clsr
import explicate
import flatten
import watgen
import os
import irgen
import reg_alloc as ra
import logging
import sys

argparser = argparse.ArgumentParser(
    description='Compile python P_0 to x86 assembly or web assembly')
argparser.add_argument('filename', metavar='filename', type=str,
                       help='the python file to compile')
argparser.add_argument(
    '--wasm', '-w', action='store_true', help='compile to wasm')
argparser.add_argument('--x86', '-x', action='store_true',
                       help='compile to x86 asm')
args = argparser.parse_args()

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger()

filename = args.filename
raw_ast = compiler.parseFile(filename)

logger.info('Creating unique variables [Avoid Name Conflict]...')
uniquified_ast = uniq.get_uniquified_ast(raw_ast)

heap_vars = hpfy.get_heap_vars(uniquified_ast)

logger.info("Performing Escape Analysis and Heapification...")
logger.info('Pushing free variables to heap')
heapified_ast = hpfy.get_heapified_ast(uniquified_ast)

logger.info("Performing Closure Conversion...")
closurified_ast = clsr.get_converted_ast(heapified_ast, heap_vars)

# Explicate the Raw AST
logger.info("Adding Type Information to the AST")
explicit_ast = explicate.get_explicated_ast(closurified_ast)

fname = os.path.splitext(filename)[0] # filename without the extension
logger.info("Flattening the AST...")
utils.write_to_file(fname+ "_flat", flatten.get_flattened_statements(explicit_ast), ".py")


# Flatten the Explicit AST
flattened_ast = flatten.get_flattened_ast(explicit_ast)

if args.wasm:
    logger.info("Compiling to wasm...")
    wat = watgen.get_wat(flattened_ast)
    utils.write_to_file(fname, wat, ".wat")
if args.x86:
    logger.info("Compiling to x86...")
    # Generate IR
    ir_list = irgen.get_ir_list(flattened_ast)

    # print IR to the .ir file for debugging
    utils.write_to_file(fname, utils.flatten_list(ir_list), ".ir")

    # Register Allocation and Assigning Home
    x86asm_list = ra.reg_alloc(ir_list)

    utils.write_to_file(filename, utils.flatten_list(x86asm_list), suffix=".s")
