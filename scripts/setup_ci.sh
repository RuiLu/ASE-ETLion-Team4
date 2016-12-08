file="../.git/hooks/pre-commit"
if [ -h "$file" ] || [ -f "$file" ]
then
	echo "$file found."
	echo "Remove Original pre-commit"
	rm $file
fi
cp pre-commit $file
chmod +x $file
echo "Set Up pre-commit successfully."