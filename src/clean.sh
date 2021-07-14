# Being very precise with which directories we want to _actually_ clean, no file deletion mistakes allowed!

rm -f ./examples/*.wasm
rm -f ./examples/*.wat
rm -f ./tests/*.wasm
rm -f ./tests/*.wat
rm -f ./tests/*.runlog
rm -f ./*.wasm
rm -f ./*.wat

echo 'All done! ✨ 🍰 ✨'
