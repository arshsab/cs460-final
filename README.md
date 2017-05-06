# Blockchain Voting

## Usage

1. To use this software, run the server using `python3` (`python3 server.py`). 
2. Perform actions from your Terminal using `python3 app.py`

## Motivation

Voting in elections is a very important part of civic life but remains one is often the target of accusations of malfeasance. 
The most recent US presidential election saw attacks from both sides accusing the vote of being hacked or otherwise tampered 
with. We hope to add more transparency and security in the electioneering process.

## Features

1. Decentralized architecture: We provide an architecture that is decentralized in nature so that small jurisdictions
can mantain control over registering voters and verifying results rather than relying on one authoritative system. This is
similar to how the current voting system operates where the Secretary of State in each state is in charge of their voting rolls
and counting ballots. This means that it is harder to compromise the entire system.

2. Registration Accountability: We provide a system that makes sure there is accountability as to who registers specific voters
down to the specific jurisdiction. This means that we can scan for abnomalies in the registration process and fix them by
dropping specific jurisdictions at will.

3. Ballot Counting Accountability: We provide a system that makes sure there is accountability in counting the specific ballots.
The blockchain system ensures that we have exact counts of the number of votes for each candidate. This does not exist in
normal election systems where ballots are often counted by hand and counting errors are common. Moreover, the blockchain is
easily available to anyone and they can independently verify the totals.

4. Personal Ballot Verification: We provide a system that ensures that the blockchain being used accurately reflects each
individual's vote. Each individual can use their key to check their individual vote in the blockchain.

## Limitations

1. Normally, verifying your vote might be considered a good thing. But, in some cases, this might be undesirable since it 
enables people to easily buy and sell their votes with a reciept that indicates how they voted in a specific election. It 
might also be undesirable if you are coerced into revealing your vote.

2. Registration still relies on specific jurisdictions to ensure that each person that registers is eligible and can only
register once. While this deisgn can mitigate this problem by checking _who_ registered a specific voter and potentially banning
jurisidictions, it is far from a clean fix.

3. Human error can happen. One example is users can misremember who they voted for and blame the system, despite evidence that
their key was used to vote for a specific person. Or they can store their key insecurely and have it be hacked (if these hacks
happen at a mass scale, they can significantly effect the outcome).

## Architecture

1. The election is stored in a decentralized ledger of registration's and vote's. The final or current state of any election
can be determined using this ledger.

2. The ledger can be modified from a cluster of servers connected to each other. Each server in a cluster represents a specific
jurisdiction. Endpoints on the server allow user's to register and vote.
  * Registration occurs when the user provides his or her public key to the server as well as their registration credentials.
  (in out architecture, anyone can register as long as they provide a name but other systems would check SSN, etc). The 
  registration message is approved and signed by the server and then added to the distributed ledger.
  * Voting occurs when the user provides a message signed by his or her public key. This message is sent to a server, and the
  server adds it to the distributed ledger.
  
3. User's access the cluster to perform actions on the server through a custom CLI program. 
  * To check results, the user downloads the ledger from the cluster and independently verifys the results.
  * To check their specific vote, the user downloads the ledger and searches it for the votes submitted by their public key.
