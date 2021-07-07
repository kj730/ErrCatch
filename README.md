# ErrCatch
The priceComp.py code compares two lines in a given file with the same strike values that were created within a certain time of each other.
The code checks to see if the buy or sell prices are the same for each line.
If they are, then the code checks to see if the futures for the buy or sell for each line are different.
If the two futures are different, then the code returns the two lines, as that means that there was an error in another program.
