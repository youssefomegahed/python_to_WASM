(async () => {
  var importObject = {
    cruntime: {
      is_big: Module.cwrap("is_big", "number", ["number"]),
      inject_big: Module.cwrap("inject_big", "number", ["number"]),
      project_bool: Module.cwrap("project_bool", "number", ["number"]),
      project_int: Module.cwrap("project_int", "number", ["number"]),
      get_subscript: Module.cwrap("get_subscript", "number", [
        "number",
        "number",
      ]),
      create_list: Module.cwrap("create_list", "number", ["number"]),
      print_any: Module.cwrap("print_any", null, ["number"]),
      inject_int: Module.cwrap("inject_int", "number", ["number"]),
      get_free_vars: Module.cwrap("get_free_vars", "number", ["number"]),
      add: Module.cwrap("add", "number", ["number", "number"]),
      is_bool: Module.cwrap("is_bool", "number", ["number"]),
      input: Module.cwrap("input", "number", []),
      is_int: Module.cwrap("is_int", "number", ["number"]),
      project_big: Module.cwrap("project_big", "number", ["number"]),
      error_pyobj: Module.cwrap("error_pyobj", "number", ["number"]),
      set_subscript: Module.cwrap("set_subscript", "number", [
        "number",
        "number",
        "number",
      ]),
      inject_bool: Module.cwrap("inject_bool", "number", ["number"]),
      not_equal: Module.cwrap("not_equal", "number", ["number", "number"]),
      create_dict: Module.cwrap("create_dict", "number", ["number"]),
      equal: Module.cwrap("equal", "number", ["number", "number"]),
      is_true: Module.cwrap("is_true", "number", ["number"]),
      get_fun_ptr: Module.cwrap("get_fun_ptr", "number", ["number"]),
      create_closure: Module.cwrap("create_closure", "number", [
        "number",
        "number",
      ]),
    },
  };

  const fetchPromise = fetch('../tests/mytests/src.wasm');
  const { instance } = await WebAssembly.instantiateStreaming(fetchPromise, importObject);
  const main = instance.exports.main;
  main()
})();
