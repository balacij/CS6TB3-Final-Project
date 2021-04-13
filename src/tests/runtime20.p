type Set = set [1 .. 10]
type Maybe = Just(value: Set) | Nothing

program Main
    var m: Maybe
    var s: Set
    var i: integer

    s := {1,2,3,6,9}
    m := Just(s)
    
    case m of {
        nil: writeln(0)
        Just:
            i := 1
            while i < 11 do
                write(i)
                writeChar(' ')
                writeChar('-')
                writeChar('>')
                writeChar(' ')
                if i ∈ m.value then
                    writeCharLn('T')
                else
                    writeCharLn('F')
                i := i + 1
        default nothing
    }
