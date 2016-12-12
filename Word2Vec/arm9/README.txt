Ensure the location of the csv is relative to the python file

run Word2VecForArm9.py as follows

python Word2VecForArm9.py > most_common_words.txt

The most_common_words.txt file contains the top n frequent words ( n specified in Word2VecForArm9.py) that can be used to run test.py which will generate a TSNE visualization of the model.

run test.py as

python test.py
