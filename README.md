# PayMo Antifraud Add-on
This add-on evaluates the level of familiarity between users in a PayMo transaction and flags the transaction accordingly as "trusted" or "unverified".

## Add-on Details
Each new transaction is evaluated according to whether the two users in the transaction have sent or received money from each other before, and the result is given in output1.txt as "trusted" or "unverified".

When a degree of separation greater than 1 is specified in an instance of the add-on, each transaction is also evaluated according to whether the two users in the transaction have sent or received money from other users in common, up to 4 degrees of separation (output is written for 1, 2 and 4 degrees of separation). For a degree of 2 or more, users are "trusted" (in output2.txt) if one degree of separation connects the two users. For a degree of 4, users are "trusted" if they are connected through the transactions of three intermediary users (in output3.txt).

## Installation
Running the antifraud add-on requires a Python installation (compiled with v 2.7.6), including the standard packages of os and sys:
[Install Python](http://docs.python-guide.org/en/latest/)

The add-on can be forked or cloned from my GitHub repository:
[PayMo Antifraud Add-on](https://github.com/callioca/PayMoAntifraud)

!! Due to the size of the input files (batch_payment.txt and stream_payment.txt) they must be downloaded separately as directed in the  placeholder files !!

The PayMo Antifraud add-on installation should have the following structure:
<pre><code>
├── README.md
├── run.sh
├── src
│     └── antifraud.py
├── paymo_input
│   └── batch_payment.txt
|   └── stream_payment.txt
├── paymo_output
│   └── output1.txt
|   └── output2.txt
|   └── output3.txt
└── insight_testsuite
       ├── run_tests.sh
       └── tests
            └── test-1-paymo-trans
            │   ├── paymo_input
            │   │   └── batch_payment.txt
            │   │   └── stream_payment.txt
            │   └── paymo_output
            │       └── output1.txt
            │       └── output2.txt
            │       └── output3.txt
            └── test-2-paymo-trans
            │   ├── paymo_input
            │   │   └── batch_payment.txt
            │   │   └── stream_payment.txt
            │   └── paymo_output
            │       └── output1.txt
            │       └── output2.txt
            │       └── output3.txt
            └── test-3-paymo-trans
                 ├── paymo_input
                 │   └── batch_payment.txt
                 │   └── stream_payment.txt
                 └── paymo_output
                     └── output1.txt
                     └── output2.txt
                     └── output3.txt
                     </code></pre>
## Running the add-on
Compile the add-on in the root directory with the command:
<pre><code>python -m py_compile src/antifraud.py</code></pre>

The add-on can be run in the root directory with the command:
<pre><code>source run.sh</code></pre>
in which the arguments given to the add-on are contained in the run.sh file.

### Running from within PayMo
The add-on is written into a class named Antifraud, so that it can also be imported into the larger PayMo app framework and called as a class with the following commands (where the arguments have been defined accordingly):
<pre><code>
from antifraud import Antifraud
antifraud = Antifraud(degree)
antifraud.read_in(pay_history)
antifraud.run(pay_new,degree,out1,out2,out3)
</code></pre>

### Argument definitions:
* degree: Number of degrees of separation between users is trusted (defaults to 4)
* pay_history: UNICODE-8 txt file of past transactions between users
* pay_new: UNICODE-8 txt file of new transaction(s)
* out1,out2,out3: Output files recording verification status between users according to the number of degrees separation between them

## Unit Tests
Three unit tests are included to test correct trust verification at 1, 2, and 4 levels of separation between the users. These are included in the insight_testsuite package and can be run from that directory using <code>./run_tests.sh</code>.

Additional unit tests can be added in the insight_testsuite directory with the folder designation test-#-paymo-trans.

## Information and Licensing
<pre>Version: 1.0
Author: Callie Bertsche
Author email: c.bertsche@cern.ch
License: Callie Bertsche 2016 (c.bertsche@cern.ch)
Compiled with Python 2.7.6</pre>
