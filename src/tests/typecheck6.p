type Maybe = Just(value: integer) | Nothing

type Set = set [0 .. 10]
type Array = [0 .. 10] → Maybe

type Either = Left(sett: Set) | Right(array: Array)


program Main
    var m: Maybe
    var s: Set
    var a: Array
    var e: Either
    var i: integer

    s := {1,2,3,6,9}

    e := Left(s)
    
    case e of {
        Left:
            while i < 10 do
                write(i)
                writeChar(' ')
                writeChar('-')
                writeChar('>')
                writeChar(' ')
                if i ∈ e.sett then
                    writeCharLn('T')
                    a[i] := Just(99)
                else
                    writeCharLn('F')
                    a[i] := Nothing()
                i := i + 1
        default nothing
    }

    e := Right(a)
    i := 0

    case e of {
        Right:
            while i < 10 do
                m := e.array[i]
                write(i)
                writeChar(' ')
                writeChar('-')
                writeChar('>')
                writeChar(' ')
                case m of {
                    Just: writeCharLn('J')
                    Nothing: writeCharLn('N')
                    default nothing
                }
                i := i + 1
        default nothing
    }
