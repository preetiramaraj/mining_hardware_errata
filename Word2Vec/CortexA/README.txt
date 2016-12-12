Ensure the location of the csv is relative to the python file

run Word2VecForCortexASeries.py as follows

python Word2VecForCortexASeries.py > most_common_words.txt

The most_common_words.txt file contains the top n frequent words ( n specified in Word2VecForCortexASeries.py) that can be used to run test.py which will generate a TSNE visualization of the model.

run test.py as

python test.py
