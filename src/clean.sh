# Being very precise with which directories we want to _actually_ clean, no file deletion mistakes allowed!

rm ./examples/*.wasm 2> /dev/null
rm ./examples/*.wat 2> /dev/null
rm ./*.wasm 2> /dev/null
rm ./*.wat 2> /dev/null

echo 'All done! ✨ 🍰 ✨'
