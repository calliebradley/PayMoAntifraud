#!/bin/env python
# C Bertsche: Data Engineering Insight Program
# November 2016
# PayMo
import os
import sys
from sys import argv


class Antifraud:
    """ This add-on for the PayMo app evaluates the level of trust between two
        users in each transaction, and returns a 'trusted' or 'unverified'
        result depending on the level of separation between the users.
    """
    def __init__(self, deg=4): # 4 levels of separation trusted by default
        """ Parameters for running Antifraud add-on """
        self.degree = deg
        self.data = []

    def read_in(self, inputf):
        """ Read in past transactions to compare with new data """
        if os.path.isfile(inputf):
            database = open(inputf)
            database.readline()
            for row in database:
                fields = row.strip().split(",")
                if(fields[1] and fields[2]):
                    self.data.append({
                        int(fields[1]),
                        int(fields[2])
                        })
                else:
                    print "Error picking up pair of users"
            database.close()
            return True
        else: return False

    def run(self, pay_new, degree, out1, out2, out3):
        """ Processes new transactions (from pay_new) and
            prints results: "trusted" or "unverified"
            to out1, out2 and out3 according to the level of separation
            specified (degree) between the users.
        """
        history = self.data
        outf1 = open(out1,"w")
        outf2 = open(out2,"w")
        outf3 = open(out3,"w")

        if not os.path.isfile(pay_new):
            print "Bad streaming file"
            sys.exit(-1)
        transaction = open(pay_new)
        transaction.readline()
        for row in transaction:
            trust1 = "unverified\n"
            trust2 = "unverified\n"
            trust3 = "unverified\n"
            fields = row.strip().split(",")
            user1 = int(fields[1])
            user2 = int(fields[2])
            if (set([user1, user2]) in history):
                trust1 = trust2 = trust3 = "trusted\n"
            elif(degree > 1):
                deg1 = self.get_next_degree(history,[user1])
                for connection in deg1:
                    if (set([connection,user2]) in history):
                        trust2 = trust3 = "trusted\n"
                    else:
                        if(degree > 2):
                            deg2 = self.get_next_degree(history,deg1)
                            for connection in deg2:
                                if(set([connection,user2]) in history):
                                    trust3 = "trusted\n"
                                else:
                                    deg3 = self.get_next_degree(history,deg2)
                                    for connection in deg3:
                                        if(set([connection,user2]) in history):
                                            trust3 = "trusted\n"
            # After all tests, append transaction
            history.append({
                user1,
                user2
            })

            # Write out transaction status
            outf1.write(trust1)
            if(degree>1): outf2.write(trust2)
            if(degree>2): outf3.write(trust3)

        transaction.close()
        outf1.close()
        if(degree>1): outf2.close()
        if(degree>2): outf3.close()

    def get_next_degree(self, history, users):
        """ Combs past transactions (history) for all users (nxt_deg) that had a
            transaction with a subset of users from history (users)
        """
        nxt_deg = []
        for my_set in history:
            if len(my_set) == 2:    # Ignore any bad sets
                my_set_pops = set(my_set)
                user1 = my_set_pops.pop()
                user2 = my_set_pops.pop()
                if user1 in users: nxt_deg.append(user2)
                if user2 in users: nxt_deg.append(user1)
        return nxt_deg


if __name__=='__main__':
    script, pay_history, pay_new, out1, out2, out3 = argv
    degree = 4 # Number of degrees separation to test on

    antifraud = Antifraud(degree)
#    antifraud.read_in(pay_history)
    if not antifraud.read_in(pay_history):
        print "Bad input file"
        sys.exit(-1)

    rc = antifraud.run(pay_new, degree, out1, out2, out3)
    sys.exit(rc)
