# modules
import requests
from termcolor import colored
import time

# input stuff
platform = input("Which platform's link would you like to bruteforce (imgur/discord/pastebin/other)? ")
platform = platform.lower()

# check if other
if(platform=='other'):
    print('More platforms coming soon!')
    exit()

# imgur input stuff
if (platform=='imgur'):
    mode = input('Url contains /a/, /gallery/, none or any if you dont know (input "a"/"gallery"/"none"/"any"): ') # imgur has 3 diffrent url types (why)
    mode = mode.lower()
    if (mode=='any'): print(colored('\nWarning! "Any" mode is pretty slow. Try specific mode if you want to go faster.\n', 'red'))

# not imgur input stuff
url = input('Input link (the last part): ')
url = url.lower()

# checking if link is valid
if (platform=='imgur'):
    if (len(url) == 7) and (url.isalnum() == True):
        pass
    else:
        print('Invalid imgur link.')
        exit()
elif (platform=='discord'):
    if (len(url) == 8) and (url.isalnum() == True):
        pass
    elif (len(url) == 10) and (url.isalnum() == True):
        pass
    else:
        print('Invalid discord link.')
        exit()
elif (platform=='pastebin'):
    if (len(url) == 8) and (url.isalnum() == True):
        pass
    else:
        print('Invalid pastebin link.')
        exit()

# more input stuff
printfail = input('Do you want to print failed attempts (y/n)? ')
printfail = printfail.lower()

# some variables 
correcturl = False
truelink = ''

# bruteforcing algorithm (yoinked from https://www.geeksforgeeks.org/)
def permute(inp):
    possble = []
    n = len(inp)
  
    mx = 1 << n
  
    inp = inp.lower()
     
    for i in range(mx):
        combination = [k for k in inp]
        for j in range(n):
            if (((i >> j) & 1) == 1):
                combination[j] = inp[j].upper()
  
        temp = ""
        for i in combination:
            temp += i
        possble.append(temp)
    return possble

# staring timer
start = time.perf_counter()

# using bf algorithm
posurls = (permute(url))

# discord stuff
if(platform == 'discord'):
    for posurl in posurls:
        page = requests.get("https://discord.com/api/v9/invites/" + posurl + "?with_counts=true&with_expiration=true") # discord api
        if (page.status_code == 404):
            if (printfail == 'y'):
                print(f'{posurl} - Failed') # fail to connect (404)
        elif(page.status_code == 429):
            print("Oh no! It looks like you're banned from discord's api. Sorry!") # easter egg :(
            correcturl = True
            break
        elif (page.status_code == 200):
            print(f'{posurl} - Success!') # success to connect (200)
            correcturl = True
            truelink = f'\nhttps://discord.com/invite/{posurl} is the right url!'
            break

elif(platform == 'imgur'):
    for urltry in posurls:

        if (mode == 'gallery'):
            page = requests.get("https://api.imgur.com/post/v1/posts/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Ctags%2Caccount%2Cadconfig%2Cpromoted") # imgur api
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'{urltry} - Failed')
            else:
                print(f'{urltry} - Success!')
                truelink = f'\n https://imgur.com/gallery/{urltry} is the right url!'
                correcturl = True
                break

        elif (mode == 'a'):
            page = requests.get("https://api.imgur.com/post/v1/albums/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Cadconfig%2Caccount")
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'{urltry} - Failed')
            else:
                print(f'{urltry} - Success!')
                truelink = f'\n https://imgur.com/a/{urltry} is the right url!'
                correcturl = True
                break

        elif (mode == 'none'):
            page = requests.get("https://api.imgur.com/post/v1/media/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Cadconfig%2Caccount")
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'{urltry} - Failed')
            else:
                print(f'{urltry} - Success!')
                truelink = f'\n https://imgur.com/{urltry} is the right url!'
                correcturl = True
                break

        elif (mode == 'any'):
            page = requests.get("https://api.imgur.com/post/v1/posts/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Ctags%2Caccount%2Cadconfig%2Cpromoted")
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'gallery/{urltry} - Failed')
            else:
                print(f'gallery/{urltry} - Success!')
                truelink = f'\n https://imgur.com/gallery/{urltry} is the right url!'
                correcturl = True
                break

            page = requests.get("https://api.imgur.com/post/v1/albums/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Cadconfig%2Caccount")
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'a/{urltry} - Failed')
            else:
                print(f'a/{urltry} - Success!')
                truelink = f'\n https://imgur.com/a/{urltry} is the right url!'
                correcturl = True
                break

            page = requests.get("https://api.imgur.com/post/v1/media/" + urltry + "?client_id=546c25a59c58ad7&include=media%2Cadconfig%2Caccount")
            if (page.status_code == 404):
                if (printfail == 'y'):
                    print(f'/{urltry} - Failed')
            else:
                print(f'/{urltry} - Success!')
                truelink = f'\n https://imgur.com/{urltry} is the right url!'
                correcturl = True
                break

        else:
            print("You've chosen an invalid mode, try again")
            correcturl = True
            break

elif(platform=='pastebin'):
    for posurl in posurls:
        page = requests.get("https://pastebin.com/" + posurl) # pastebin (not api)
        if (page.status_code == 404):
            if (printfail == 'y'):
                print(f'{posurl} - Failed')
        elif (page.status_code == 200):
            print(f'{posurl} - Success!')
            correcturl = True
            truelink = f'\nhttps://pastebin.com/{posurl} is the right url!'
            break

else:
    print("This platform isn't supported or doesn't exist")
    correcturl=True

# stopping timer
end = time.perf_counter() - start 

# printing
if (correcturl == True):
    if(truelink != ''): # if the link was bruteforced
        print(f'{truelink} (bruteforced in {round(end)} seconds)')
else:
    print("Hmmmm.... This doesn't seem like a valid link... Check the link that you've inputed and the platform you've chosen.")