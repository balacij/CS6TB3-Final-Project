
echo "Starting!"

for i in examples/*.p; do
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo ">>> $i"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    python Compiler.py "$i" --run
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
