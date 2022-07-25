# python-to-wasm (PyWASM)

PyWASM is a python2 to WASM transpiler.

## Usage 


1. Compilation:
   
```bash
./pyyc [--wasm | -w] [--x86 | -x] <input_file.py>
```

Flags are optional.
    > `--wasm`: Compile to WebAssembly.
    > `--x86`: Compile to x86-64.
    > `<input_file.py>`: Input file.

### x86

1. Execution:
   
```bash
./input_file_binary
```

### WASM

1. Execution:

Start the web server from the root folder:

```bash
python3 -m http.server
```

2. Checking the output:

- Go to `http://localhost:8000/` on your browser.
- Open the `index.html` file.
- Open DevTools and click on the `Console` tab.
- Call the wasm function that you are interested in. 
  





