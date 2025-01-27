import sail_core

# Create an instance of SAIL
sail = sail_core.SAIL()

# Test 'process_text'
print("Processed text:", sail.process_text("example test"))

# Test 'process_transaction'
match = sail.process_transaction("Alice", "Bob", 100.0)
print("Transaction match:", match)
