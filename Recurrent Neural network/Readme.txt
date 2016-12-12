To train the RNN, run this:

	th train.lua -data_dir data/problem_description_with_refernence -dropout 0.5

The trained model is located in folder `cv`. Replace the `cv/some_checkpoint.t7` in the following command as well as the `blahblahblah` to generate problem description from the primetext: 

	th sample.lua cv/some_checkpoint.t7 -primetext 'blahblahblah'


For more reference, please visit http://karpathy.github.io/2015/05/21/rnn-effectiveness/