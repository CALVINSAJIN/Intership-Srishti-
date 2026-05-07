try:    
    with open('demofile.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:    
    print("The file was not found. Please check the file name and try again.")
except Exception as e:    
    print("An error occurred:",e)    
else:    
    print("File content:\n",content)