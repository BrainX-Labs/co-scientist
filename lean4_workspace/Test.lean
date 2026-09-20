theorem one_plus_one : (1 : Nat) + 1 = 2 := rfl

theorem add_comm_test (a b : Nat) : a + b = b + a := Nat.add_comm a b

theorem id_bool (b : Bool) : b = b := rfl
