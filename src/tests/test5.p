type Maybe = Just(value: integer) | Nothing

program Main
    var m: Maybe
    m := Just(20)
    writeln(m)
