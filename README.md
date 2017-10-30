# Comments

Some points based on the assumptions of the input data:

1. The challenge requires that, when TRANSACTION_AMT is empty, one shall ignore the corresponding entry. No other exceptions are mentioned in the requirement, so I did not implement such validity check in the code.
2. The challenge defines an invalid zipcode as being "empty or fewer than five digits", so I only implement validity check on the length of the zipcodes, not their exact contents.
