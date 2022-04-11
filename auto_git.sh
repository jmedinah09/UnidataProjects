 #! /bin/bash

 #Script for automathically update github

 #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

echo "*****Changing to the working directory*****"
cd /home/"$USER"/Desktop/PythonStuffs/clone_repo
git init
git status
echo "*****Adding*****"
git add -A
git status
echo "*****Reading Message to commit*****"
echo "-Write your commit message-"
read mssg
echo "*****Commiting*****"
git commit -m "$mssg"
git status
echo "*****Pushing to github*****"
git push -u origin main
