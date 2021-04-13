
echo "Starting!"

for i in tests/*.p; do
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "Stabilizing $i"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    python Compiler.py "$i" --run 2>&1 > "$i.expect"
done

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Finished!"

while true; do
    read -p "Clean project? [Yy/Nn]" yn
    case $yn in
        [Yy]* ) sh clean.sh; break;;
        [Nn]* ) echo "Bye!"; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
