
type RainbowColour = Red | Orange | Yellow | Green | Blue | Indigo | Violet

program Main
    var rbwCol: RainbowColour

    rbwCol := Red()

    case rbwCol of {
        Red:    writeCharLn('R')
        Orange: writeCharLn('O')
        Yellow: writeCharLn('Y')
        Green:  writeCharLn('G')
        Blue:   writeCharLn('B')
        Indigo: writeCharLn('I')
        Violet: writeCharLn('V')
    }
