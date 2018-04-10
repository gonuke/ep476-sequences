import argparse

import sequences

def seq_driver_incr(max_initial,length,verbose=False):
    """
    Calculate a dictionary of many Fibonacci-like sequences.  Each entry
    in the dictionary uses a different number of previous numbers to formulate
    the sum for the next entry.  The number of previous numbers is the list from
    2 to `max_initial`.

    input:
    ------
    max_initial : (integer) indicates the number of entries to sum for the 
                  next entry in the largest case
    length : (integer) the number of entries to include in the sequence
    verbose : (bool) whether or not to print extra output [optional]

    output:
    -------
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """

    return seq_driver_generic(list(range(2,max_initial+1)), length, verbose)

    
def seq_driver_generic(initial_list, length, verbose=False):
    """
    Calculate a dictionary of many Fibonacci-like sequences.  Each entry
    in the dictionary uses a different number of previous numbers to formulate
    the sum for the next entry.  The number of previous numbers is indicated
    in the `initial_list`.

    input:
    ------
    initial_list : (integer) indicates the list of different values to use as
                   the number of entries to sum for the next entry in each case
    length : (integer) the number of entries to include in the sequence
    verbose : (bool) whether or not to print extra output [optional]

    output:
    -------
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """
    
    seq_dict = {}
    for init in initial_list:
        seq_dict[(init,length)] = sequences.calc_sequence(init,length,verbose)

    return seq_dict

def print_seq_dict(seq_dict):

    print("\n".join(["{0} : {1}".format(key,val) for key,val in seq_dict.items()]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--max_number", type=int, default=2, required=False,
                        help="Determines the range of initial numbers are used/necessary to compute the sequence.")

    parser.add_argument("-l", "--length", type=int, default=10, required=False,
                        help="Determines how many terms in the sequence to calculate and print.")

    parser.add_argument("-v", "--verbose", action='store_true', required=False,
                        help="Print extra information to the screen during calculation.")

    args = parser.parse_args()

    seq_dict = seq_driver_incr(args.max_number, args.length, args.verbose)

    print_seq_dict(seq_dict)
