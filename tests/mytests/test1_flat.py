def lambda_add_0_30_2(fvs_30_1, x_1, y_1):
    tmp_30_5 = []
    tmp_30_6 = create_closure(lambda_add_0_30_2, tmp_30_5)
    tmp_30_7 = inject_big(tmp_30_6)
    add_0 = tmp_30_7
    tmp_30_3 = x_1
    tmp_30_4 = y_1
    tmp_30_8 = is_int(tmp_30_3)
    tmp_30_9 = inject_int(tmp_30_8)
    tmp_30_10 = is_bool(tmp_30_3)
    tmp_30_11 = inject_int(tmp_30_10)
    tmp_30_12 = inject_int(0)
    tmp_30_13 = is_true(tmp_30_9)
    if tmp_30_13:
        tmp_30_12 = tmp_30_9
    else:
        tmp_30_12 = tmp_30_11
    tmp_30_14 = is_int(tmp_30_4)
    tmp_30_15 = inject_int(tmp_30_14)
    tmp_30_16 = is_bool(tmp_30_4)
    tmp_30_17 = inject_int(tmp_30_16)
    tmp_30_18 = inject_int(0)
    tmp_30_19 = is_true(tmp_30_15)
    if tmp_30_19:
        tmp_30_18 = tmp_30_15
    else:
        tmp_30_18 = tmp_30_17
    tmp_30_20 = inject_int(0)
    tmp_30_21 = is_true(tmp_30_12)
    if tmp_30_21:
        tmp_30_20 = tmp_30_18
    else:
        tmp_30_20 = tmp_30_12
    tmp_30_22 = inject_int(0)
    tmp_30_23 = is_true(tmp_30_20)
    if tmp_30_23:
        tmp_30_24 = tmp_30_3 + tmp_30_4
        tmp_30_25 = inject_int(tmp_30_24)
        tmp_30_22 = tmp_30_25
    else:
        tmp_30_26 = is_big(tmp_30_3)
        tmp_30_27 = inject_int(tmp_30_26)
        tmp_30_28 = is_big(tmp_30_4)
        tmp_30_29 = inject_int(tmp_30_28)
        tmp_30_30 = inject_int(0)
        tmp_30_31 = is_true(tmp_30_27)
        if tmp_30_31:
            tmp_30_30 = tmp_30_29
        else:
            tmp_30_30 = tmp_30_27
        tmp_30_32 = inject_int(0)
        tmp_30_33 = is_true(tmp_30_30)
        if tmp_30_33:
            tmp_30_34 = project_big(tmp_30_3)
            tmp_30_35 = project_big(tmp_30_4)
            tmp_30_36 = add(tmp_30_34, tmp_30_35)
            tmp_30_37 = inject_big(tmp_30_36)
            tmp_30_32 = tmp_30_37
        else:
            tmp_30_38 = error_pyobj(0)
            tmp_30_32 = tmp_30_38
        tmp_30_22 = tmp_30_32
    print(tmp_30_22)

def main():
    tmp_30_39 = []
    tmp_30_40 = create_closure(lambda_add_0_30_2, tmp_30_39)
    tmp_30_41 = inject_big(tmp_30_40)
    add_0 = tmp_30_41
    tmp_30_42 = get_free_vars(add_0)
    tmp_30_43 = inject_int(2)
    tmp_30_44 = inject_int(3)
    tmp_30_45 = get_fun_ptr(add_0)
    tmp_30_46 = tmp_30_45(tmp_30_42, tmp_30_43, tmp_30_44)
    tmp_30_46

