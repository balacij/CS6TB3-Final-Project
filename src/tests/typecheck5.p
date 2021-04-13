type Either = Left(value: integer)
            | Right(value: boolean)

procedure print(e: Either)
    case e of {
        Left:
            writeln(e.value)
        Right:
            if e.value then
                writeCharLn('T')
            else
                writeCharLn('F')
        default nothing
    }

program Main
    print(Left(10))

    print(Right(false))
