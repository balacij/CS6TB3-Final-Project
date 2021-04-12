
echo "Starting!"

for i in tests/*.p; do
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo ">>> $i"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    python Compiler.py "$i" --run 2>&1 > "$i.runlog"
    if cmp "$i.runlog" "$i.expect" >/dev/null 2>&1
    then
        echo "$i MATCHED EXPECTED OUTPUT!"
    else
        echo "$i FAILED!"
        echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        echo "Difference between current run and expectation:"
        diff "$i.runlog" "$i.expect"
    fi
done

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Finished!"
