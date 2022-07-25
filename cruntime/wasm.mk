MAKEFLAGS += --no-builtin-rules
CFILES := $(wildcard *.c)
FILES := $(patsubst %.c,%.o,$(CFILES))

all: pyruntime.html

pyruntime.html: $(FILES)
	emcc -o $@ $(FILES) \
	-s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
	-s EXPORTED_FUNCTIONS='[ "_get_fun_ptr","_get_free_vars","_print_any","_input","_create_closure","_is_int","_is_true","_add","_error_pyobj","_is_bool","_is_big","_project_int","_project_bool","_project_big","_inject_int","_inject_bool","_inject_big","_set_subscript","_equal","_not_equal","_get_subscript","_create_list","_create_dict"]'
	mv pyruntime.html ../wasmlib/
	mv pyruntime.js ../wasmlib/
	mv pyruntime.wasm ../wasmlib/
	rm -f ./*.o

%.o : %.c
	emcc -c $< -o $@

clean:
	@echo "clean"
	@echo $(FILES)
	rm -f ./*.o ./*.wasm ./*.js ./*.html
