import tiktoken

# Paste the array of decrypted integers your cracking script outputted:
decrypted_tokens = [1895, 37, 90, 13503, 70, 555, 26945, 315, 109569, 74208, 1565, 1782, 92] 

# Load the standard OpenAI tokenizer
enc = tiktoken.get_encoding("o200k_base") 

# Decode the tokens back into a readable string
flag = enc.decode(decrypted_tokens)

print("The flag is:")
print(flag)