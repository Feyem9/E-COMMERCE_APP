number = int(input("enter number:"))

if(number <= 1):
    print("incorect value")
else:
    all_prime_numbers = []
    current_number = 2
    while len(all_prime_numbers) < number:
        
        est_premier = True
        for i in range(2, current_number):
        # for i in range(2 , (current_number % 2)):
        # for i in range(2, int(current_number**0.5) + 1):  # Optimisation: only check odd numbers up to square root of current_number
            if current_number % i == 0:
                est_premier = False
                break
            
        if est_premier == True:
            all_prime_numbers.append(current_number)
            
        current_number += 1
    
    print(all_prime_numbers)