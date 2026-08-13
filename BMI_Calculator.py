# BMI Calculator

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in cm: "))

# Convert height from cm to meters
height = height / 100

# Calculate BMI
bmi = weight / (height * height)

print("Your BMI is:", round(bmi, 2))

if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obesity")