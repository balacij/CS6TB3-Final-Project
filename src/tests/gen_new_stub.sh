TESTS=$(find . -mindepth 1 -type f -name "*.p" -printf x | wc -c)

TESTS=$((TESTS+1))

echo "Generating new testing stub..."

TRG="parsing$TESTS.p"

if cp model.stub "$TRG"
then
    echo "Generated new testing stub; $TRG"
else
    echo "Failed to generate a new testing stub!"
fi
