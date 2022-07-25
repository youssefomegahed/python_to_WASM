(module
    (import "cruntime" "is_big" (func $is_big
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "inject_big" (func $inject_big
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "project_bool" (func $project_bool
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "project_int" (func $project_int
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "get_subscript" (func $get_subscript
        (param  i32)
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "create_list" (func $create_list
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "print_any" (func $print_any
        (param  i32)
    ))
    (import "cruntime" "inject_int" (func $inject_int
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "get_free_vars" (func $get_free_vars
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "add" (func $add
        (param  i32)
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "is_bool" (func $is_bool
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "input" (func $input
        (result  i32)
    ))
    (import "cruntime" "is_int" (func $is_int
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "project_big" (func $project_big
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "error_pyobj" (func $error_pyobj
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "set_subscript" (func $set_subscript
        (param  i32)
        (param  i32)
        (param  i32)
    ))
    (import "cruntime" "inject_bool" (func $inject_bool
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "not_equal" (func $not_equal
        (param  i32)
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "create_dict" (func $create_dict
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "equal" (func $equal
        (param  i32)
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "is_true" (func $is_true
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "get_fun_ptr" (func $get_fun_ptr
        (param  i32)
        (result  i32)
    ))
    (import "cruntime" "create_closure" (func $create_closure
        (param  i32)
        (param  i32)
        (result  i32)
    ))
    (func $lambda_add_0_30_2
        (param  $fvs_30_1 i32)
        (param  $x_1 i32)
        (param  $y_1 i32)
        (local $add_0 i32)
        (local $tmp_30_58 i32)
        (local $tmp_30_59 i32)
        (local $tmp_30_54 i32)
        (local $tmp_30_55 i32)
        (local $tmp_30_56 i32)
        (local $tmp_30_57 i32)
        (local $tmp_30_50 i32)
        (local $tmp_30_51 i32)
        (local $tmp_30_52 i32)
        (local $tmp_30_53 i32)
        (local $tmp_30_76 i32)
        (local $tmp_30_77 i32)
        (local $tmp_30_74 i32)
        (local $tmp_30_75 i32)
        (local $tmp_30_72 i32)
        (local $tmp_30_73 i32)
        (local $tmp_30_70 i32)
        (local $tmp_30_71 i32)
        (local $tmp_30_78 i32)
        (local $tmp_30_79 i32)
        (local $tmp_30_49 i32)
        (local $tmp_30_48 i32)
        (local $tmp_30_80 i32)
        (local $tmp_30_47 i32)
        (local $tmp_30_89 i32)
        (local $tmp_30_65 i32)
        (local $tmp_30_64 i32)
        (local $tmp_30_67 i32)
        (local $tmp_30_66 i32)
        (local $tmp_30_61 i32)
        (local $tmp_30_60 i32)
        (local $tmp_30_63 i32)
        (local $tmp_30_62 i32)
        (local $tmp_30_69 i32)
        (local $tmp_30_68 i32)
        (local $tmp_30_3 i32)
        (local $tmp_30_4 i32)
        (set_local $tmp_30_47
            (set_local $tmp_30_89
                (call $inject_big
                    (call $create_list
                        (call $inject_int
                            (i32.const 0)
                        )
                    )
                )
            )
            (get_local $tmp_30_89)
        )
        (set_local $tmp_30_48
            (call $create_closure
                (get_local $lambda_add_0_30_2)
                (get_local $tmp_30_47)
            )
        )
        (set_local $tmp_30_49
            (call $inject_big
                (get_local $tmp_30_48)
            )
        )
        (set_local $add_0
            (get_local $tmp_30_49)
        )
        (set_local $tmp_30_3
            (get_local $x_1)
        )
        (set_local $tmp_30_4
            (get_local $y_1)
        )
        (set_local $tmp_30_50
            (call $is_int
                (get_local $tmp_30_3)
            )
        )
        (set_local $tmp_30_51
            (call $inject_int
                (get_local $tmp_30_50)
            )
        )
        (set_local $tmp_30_52
            (call $is_bool
                (get_local $tmp_30_3)
            )
        )
        (set_local $tmp_30_53
            (call $inject_int
                (get_local $tmp_30_52)
            )
        )
        (set_local $tmp_30_54
            (call $inject_int
                (i32.const 0)
            )
        )
        (set_local $tmp_30_55
            (call $is_true
                (get_local $tmp_30_51)
            )
        )
        (if
            (get_local $tmp_30_55)
                (then
                    (set_local $tmp_30_54
                        (get_local $tmp_30_51)
                    )
                )
                (else
                    (set_local $tmp_30_54
                        (get_local $tmp_30_53)
                    )
                )
        )
        (set_local $tmp_30_56
            (call $is_int
                (get_local $tmp_30_4)
            )
        )
        (set_local $tmp_30_57
            (call $inject_int
                (get_local $tmp_30_56)
            )
        )
        (set_local $tmp_30_58
            (call $is_bool
                (get_local $tmp_30_4)
            )
        )
        (set_local $tmp_30_59
            (call $inject_int
                (get_local $tmp_30_58)
            )
        )
        (set_local $tmp_30_60
            (call $inject_int
                (i32.const 0)
            )
        )
        (set_local $tmp_30_61
            (call $is_true
                (get_local $tmp_30_57)
            )
        )
        (if
            (get_local $tmp_30_61)
                (then
                    (set_local $tmp_30_60
                        (get_local $tmp_30_57)
                    )
                )
                (else
                    (set_local $tmp_30_60
                        (get_local $tmp_30_59)
                    )
                )
        )
        (set_local $tmp_30_62
            (call $inject_int
                (i32.const 0)
            )
        )
        (set_local $tmp_30_63
            (call $is_true
                (get_local $tmp_30_54)
            )
        )
        (if
            (get_local $tmp_30_63)
                (then
                    (set_local $tmp_30_62
                        (get_local $tmp_30_60)
                    )
                )
                (else
                    (set_local $tmp_30_62
                        (get_local $tmp_30_54)
                    )
                )
        )
        (set_local $tmp_30_64
            (call $inject_int
                (i32.const 0)
            )
        )
        (set_local $tmp_30_65
            (call $is_true
                (get_local $tmp_30_62)
            )
        )
        (if
            (get_local $tmp_30_65)
                (then
                    (set_local $tmp_30_66
                        (i32.add
                            (call $project_int
                                (get_local $tmp_30_3)
                            )
                            (call $project_int
                                (get_local $tmp_30_4)
                            )
                        )
                    )
                    (set_local $tmp_30_67
                        (call $inject_int
                            (get_local $tmp_30_66)
                        )
                    )
                    (set_local $tmp_30_64
                        (get_local $tmp_30_67)
                    )
                )
                (else
                    (set_local $tmp_30_68
                        (call $is_big
                            (get_local $tmp_30_3)
                        )
                    )
                    (set_local $tmp_30_69
                        (call $inject_int
                            (get_local $tmp_30_68)
                        )
                    )
                    (set_local $tmp_30_70
                        (call $is_big
                            (get_local $tmp_30_4)
                        )
                    )
                    (set_local $tmp_30_71
                        (call $inject_int
                            (get_local $tmp_30_70)
                        )
                    )
                    (set_local $tmp_30_72
                        (call $inject_int
                            (i32.const 0)
                        )
                    )
                    (set_local $tmp_30_73
                        (call $is_true
                            (get_local $tmp_30_69)
                        )
                    )
                    (if
                        (get_local $tmp_30_73)
                            (then
                                (set_local $tmp_30_72
                                    (get_local $tmp_30_71)
                                )
                            )
                            (else
                                (set_local $tmp_30_72
                                    (get_local $tmp_30_69)
                                )
                            )
                    )
                    (set_local $tmp_30_74
                        (call $inject_int
                            (i32.const 0)
                        )
                    )
                    (set_local $tmp_30_75
                        (call $is_true
                            (get_local $tmp_30_72)
                        )
                    )
                    (if
                        (get_local $tmp_30_75)
                            (then
                                (set_local $tmp_30_76
                                    (call $project_big
                                        (get_local $tmp_30_3)
                                    )
                                )
                                (set_local $tmp_30_77
                                    (call $project_big
                                        (get_local $tmp_30_4)
                                    )
                                )
                                (set_local $tmp_30_78
                                    (call $add
                                        (get_local $tmp_30_76)
                                        (get_local $tmp_30_77)
                                    )
                                )
                                (set_local $tmp_30_79
                                    (call $inject_big
                                        (get_local $tmp_30_78)
                                    )
                                )
                                (set_local $tmp_30_74
                                    (get_local $tmp_30_79)
                                )
                            )
                            (else
                                (set_local $tmp_30_80
                                    (call $error_pyobj
                                        (i32.const 0)
                                    )
                                )
                                (set_local $tmp_30_74
                                    (get_local $tmp_30_80)
                                )
                            )
                    )
                    (set_local $tmp_30_64
                        (get_local $tmp_30_74)
                    )
                )
        )
    )
    (export "lambda_add_0_30_2" (func $lambda_add_0_30_2))
    (func $main
        (local $tmp_30_86 i32)
        (local $tmp_30_90 i32)
        (local $tmp_30_87 i32)
        (local $add_0 i32)
        (local $tmp_30_85 i32)
        (local $tmp_30_84 i32)
        (local $tmp_30_83 i32)
        (local $tmp_30_82 i32)
        (local $tmp_30_81 i32)
        (local $tmp_30_88 i32)
        (set_local $tmp_30_81
            (set_local $tmp_30_90
                (call $inject_big
                    (call $create_list
                        (call $inject_int
                            (i32.const 0)
                        )
                    )
                )
            )
            (get_local $tmp_30_90)
        )
        (set_local $tmp_30_82
            (call $create_closure
                (get_local $lambda_add_0_30_2)
                (get_local $tmp_30_81)
            )
        )
        (set_local $tmp_30_83
            (call $inject_big
                (get_local $tmp_30_82)
            )
        )
        (set_local $add_0
            (get_local $tmp_30_83)
        )
        (set_local $tmp_30_84
            (call $get_free_vars
                (get_local $add_0)
            )
        )
        (set_local $tmp_30_85
            (call $inject_int
                (i32.const 2)
            )
        )
        (set_local $tmp_30_86
            (call $inject_int
                (i32.const 3)
            )
        )
        (set_local $tmp_30_87
            (call $get_fun_ptr
                (get_local $add_0)
            )
        )
        (set_local $tmp_30_88
            (call $tmp_30_87
                (get_local $tmp_30_84)
                (get_local $tmp_30_85)
                (get_local $tmp_30_86)
            )
        )
        (call $print_any
            (get_local $tmp_30_88)
        )
    )
    (export "main" (func $main))
)
