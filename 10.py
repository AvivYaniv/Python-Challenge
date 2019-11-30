current_as_string = '1'

for i in range (0, 31):
    if i == 30:
        print len(current_as_string)
    
    current_as_number = int(current_as_string)

    digit_counter = 1
    current_digit = current_as_number % 10
    next_as_string = ""
    for i in range(0, len(current_as_string)):
        current_as_number = current_as_number / 10
        next_digit = current_as_number % 10
       
        if current_digit == next_digit:            
            digit_counter += 1
        else:   
            next_as_string = str(digit_counter) + str(current_digit) + next_as_string
            digit_counter = 1
            current_digit = next_digit

    current_as_string = next_as_string
