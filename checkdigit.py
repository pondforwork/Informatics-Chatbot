def is_valid_user_input(user_input):
  """
  This function checks if the user input is a 13-digit number.

  Args:
      user_input: The input string from the user.

  Returns:
      True if the user input is a 13-digit number, False otherwise.
  """
  # Check if the input is a string.
  if not isinstance(user_input, str):
    return False

  # Check if the length is exactly 13.
  if len(user_input) != 13:
    return False

  # Try converting the input to an integer. If it fails, it's not a valid number.
  try:
    int(user_input)
  except ValueError:
    return False

  return True

# Get user input
user_input = input("Enter a 13-digit number: ")

# Check if the input is valid
if is_valid_user_input(user_input):
  print("You entered a valid 13-digit number.")
else:
  print("Invalid input. Please enter a 13-digit number.")
