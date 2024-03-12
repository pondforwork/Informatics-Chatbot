from lextoplus import LexToPlus

# Create an instance of LexToPlus
tokenizer = LexToPlus()

# Example sentence in Thai
sentence = "อยากสร้างแอพ"

# Tokenize the sentence
tokens = tokenizer.tokenize(sentence)

# Join the tokens into a string (if needed)
tokenized_sentence = ' '.join(tokens)

# Print the result
print("Original Sentence:", sentence)
print("Tokenized Sentence:", tokenized_sentence)