
type RainbowColour = Red | Orange | Yellow | Green | Blue | Indigo | Violet

procedure printColourCode(rbwCol: RainbowColour)
    case rbwCol of {
        Red:     writeCharLn('R')
        Orange:  writeCharLn('O')
        Yellow:  writeCharLn('Y')
        Green:   writeCharLn('G')
        Blue:    writeCharLn('B')
        Indigo:  writeCharLn('I')
        Violet:  writeCharLn('V')
        default: writeCharLn('?')
    }


program Main
    var rbwCol: RainbowColour

    printColourCode(rbwCol) // Uninitialized variable!
    
    printColourCode(Red())
    printColourCode(Orange())
    printColourCode(Yellow())
    printColourCode(Green())
    printColourCode(Blue())
    printColourCode(Indigo())
    printColourCode(Violet())

