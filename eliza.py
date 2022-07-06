# This program is a chatbot named Eliza that’s meant to simulate a Rogerian psychologist. It uses regular expressions to “understand” what 
# the user is saying and give the appropriate response. 
#
# To use: type "python eliza.py" into the terminal. Talk to Eliza by typing and sending messages in the terminal. Capitalization doesn’t matter, but punctuation does. 
# When you’re done, type the word “bye” to exit the program.

import re
import random

def replace_words(phrase): 
    
    # words that need to be swapped out in order for the response to make sense
    substitutions = {
        r"\bi\b" : "you",
        r"\bme\b" : "you",
        r"\bmy\b" : "your",
        r"\byou\b" : "me",
        r"\byour\b" : "my",
        r"\bmyself\b" : "yourself",
        r"\byourself\b" : "myself",
        r"\bwas\b" : "were",
        r"\bam\b" : "are",
        r"\bare\b" : "am",
        r"\byou'll\b" : "i will",
        r"\bi'll\b" : "you will",
        r"\byou've\b" : "i have",
        r"\bi've\b" : "you have",
        r"\byou'd\b" : "i would",
        r"\bi'd\b" : "you would"
    }


    phrase = phrase.lower()

    words = phrase.split()

    new_phrase = ""

    # checks if each word of the phrase matches one of the words that need to be replaced and then replaces it
    for i in range(len(words)): 
        
        # loops through the dictionary of words that need to be substituted
        for key2 in substitutions:
            
            # makes the subsitution if there is a match
            match = re.search(key2, words[i])
            if match:
                words[i] = re.sub(key2, substitutions[key2], words[i]) 
                break # break here in order to prevent the word from being switched back (ex. my -> your -> my)
                               
        # strings the words back into a phrase
        if (words[i] != words[-1]):
            new_phrase += words[i] + " "
        else: 
            new_phrase += words[i] # doesn't add a space if it's the last element of the list
                            
    return new_phrase

def main():

    # regular expressions to compare to the user's response + the corresponding messages to send back
    rules = {

            # looks for some common ways to ask how are you
            r"(.*)(what about you|how are you)\?": [r"Good, thanks. What brought you in today?", 
                                r"I'm doing well, thanks. What can I help you with?"],
            r"^(and you|you)\?$" : [r"Good, thanks. What brought you in today?", r"I'm doing well, thanks. What can I help you with?"], 
            
            # looks for some standard responses to how are you like "good", "fine", "i'm alright", "i'm well"
            r"i'm (good|fine|alright|well)" : [r"What brought you in today?", r"What would you like to talk about today?", 
                                r"What can I help you with?", r"Anything I can help you with today?"],
            r"^(good|fine|well)$" : [r"What brought you in today?", r"What would you like to talk about today?", 
                                r"What can I help you with?", r"Anything I can help you with today?"],

            # looks for the word "bye" to exit the program
            r"\bbye\b": [r"Bye!", r"It was nice speaking to you.", r"See you next week!", r"Enjoy the rest of your day!"],
            
            # looks for generic replies the user could give in response to eliza's questions and tries to keep the conversation going 
            r"\bno\b": [r"Why not?", r"No?", r"Could you elaborate?", r"Do you want to elaborate?", r"How come?"],
            r"\b(yes|yeah|^i am$)\b": [r"Could you elaborate?", r"You're certain?", r"You're sure?", r"How come?", 
                                r"Why do you think that is?", r"Do you want to elaborate?"],
            r"i (don't|do not) know" : [r"How come you don't know?", r"Why do you think that is?", r"Do you want to elaborate?"],
            r"(.*)maybe(.*)" : [r"Maybe?", r"You're not sure?", r"Why do you think you're unsure?", r"Why are you not sure?"],
            
            # looks for some ways a user could begin a response to one of eliza's questions like "because []", "it is []", "it does"
            r"because(.*)" : [r"Is that really why?", r"Can you think of any other reasons?", r"Why do you say that?", 
                                    r"Do you want to elaborate?"],
            r"(it is|it's)(.*)" : [r"Why do you think that is?", r"What makes you think it is \2?", r"Why do you say that?"],
            r"(.*)it does$" : [r"Why do you say that?", r"What makes you think it does?", r"Does it?"],
            # "Why does it []" doesn't make if it used in response to "it does", so this regex captures it + some verb that's not just "does"
            r"it (.*)" : [r"Why does it \1?", r"Why do you think it \1?"],
            
            # looks for when the user is talking in absolutes (like using the words no one, everyone, nobody, everybody, always, never, 
            # everything, nothing) and asks them about it
            r"(.*)(no one|nobody)(.*)" : [r"No one at all?", r"Nobody at all?", r"What makes you say that?", 
                                    r"Are you thinking of someone in particular?"],
            r"(.*)(everyone|everybody)(.*)" : [r"Everyone?", r"Are you thinking of someone in particular?", 
                                    r"That's a bit dramatic...What makes you say that?", r"Is that what you really think?"],
            r"(.*)(always|never)(.*)": [r"How come?", r"What makes you say that?", r"Why do you say that?", 
                                    r"Can you think of an example?"],
            r"(.*)(everything|nothing) is (.*)": [r"Why is \2 \3?", r"What makes you say that?", r"Can you think of an example?"],
            r"(everything|nothing) (.*)": [r"Why does \1 \2?", r"Why do you think \1 \2?", r"Can you think of an example?", 
                                    r"Are you thinking of something in particular?"],
            # the user could say "everything" or "nothing" on its own in response to one of eliza's questions and the responses for
            # the other two regexes that match "everything" and "nothing" don't make sense in that context
            r"^(everything|nothing)$" : [r"Could you elaborate?", r"Why do you say that?", r"Can you think of an example?", 
                                    r"Are you thinking of something in particular?"], 
            
            # looks for some common verbs i think someone might use like "hate", "wish", "hope", want, "can't", "don't", "think"
            r"(.*)i hate (.*)" : [r"What do you hate about \2?"],
            r"(.*)i wish (.*)" : [r"Why do you wish \2?", r"Is that important to you?"],
            r"(.*)i hope (.*)" : [r"Why do you hope \2?", r"Is that important to you?"],
            r"(.*)i want (.*)" : [r"Why do you want \2?", r"How long have you wanted \2?"],
            r"(.*)i (can't|can not|can never) (.*)" : [r"Why not?", r"Why can't you?", r"What makes you think you can't?"],
            r"(.*)i (don't|do not)(.*)" : [r"Why don't you \3?", r"How come?", r"Why do you think that is?", r"You don't?"],
            r"(.*)i think (.*)" : [r"Why do you think \2?", r"What makes you think \2?", r"You're not sure?"],
            r"(.*)(i have|i've) (.*)" : [r"Are you sure?", r"Why did you \3?", r"You have?", r"Did you?"],
            r"(.*)i (would|would've) (.*)" : [r"Why would you have \3?", r"Do you wish you would've \3?"],
            r"(.*)i (should|should've) (.*)" : [r"Why do you think you should have \3?", r"Will you \3 next time?"],
            r"(.*)i feel like (.*)" : [r"Why do you feel like \2?", r"What made you feel that way?", r"Can you think of an example?"], 
            # the other regexes for these verbs assume that there is something following the verb, so this one handles the cases where 
            # the user just types "i" + the verb 
            r"^i (have|should|should've|would've|would have)$": [r"Why do you say that?", r"Could you elaborate?", r"You \1?"],

            # looks for the words "i am a" for when the user calls themselves something
            r"(.*)(i am|i'm) \ba\b (.*)" : [r"What makes you think you are a \3?", r"What makes you say that?", 
                                r"How come?", r"Can you think of a time when you felt like a \3?"],
            
            # looks for some common negative feelings that someone might bring up in therapy and asks them about it specifically
            r"(.*)(i feel|i am|i'm) (awful|terrible|depressed|sad|stressed|frustrated|sick|lonely|overwhelmed|anxious|hopeless) (.*)": 
                                [r"I'm sorry to hear that you're \3. How come?", r"That's not good. What happened?", 
                                r"Why do you feel \3?", r"Are you alright?", r"What made you feel \3?"],
            
            # looks for some common positive feelings
            r"(.*)(i feel|i am|i'm) (happy|excited|hopeful|relieved|confident|optimistic) (.*)": 
                                [r"That's great to hear. What brings you here today?", r"Why are you \3 today?", 
                                r"Did something good happen?"],
            
            # if the person doesn't match one of those specific adjectives, it will still ask them about that feeling
            r"(.*)(i'm|i am)(.*)": [r"Why are you \3?", r"How does it make you feel that you are \3?", r"How long have you been \3 for?", 
                                r"What made you feel \3?", r"Is that why you've come to see me today?", r"How long have you felt \3?", 
                                r"Why do you feel \3?"],

            # looks for words related to family and prompts the user to speak more about their family
            r"(.*)(family|parents|dad|mom|mother|father|sister|brother|siblings?)(.*)": [r"Tell me more about your \2",
                                    r"Do you have a good relationship with your \2?", 
                                    r"How is your relationship with your \2?", r"Do you like your \2?"], 
            
            # looks when the user mentions the word friend(s) and prompts them to talk about their friends
            r"(.*)(friends?)(.*)" : [r"Tell me about your friends.", r"Do you have a good relationship with your friends?"],
            
            # looks for words related to their relationships (like ex, girlfriend, boyfriend, wife, husband)
            r"(.*)ex\s?-?(girlfriend|boyfriend|husband|wife)?(.*)": [r"Why did you separate?", r"Tell me more about your ex-\2.", 
                                    r"Did you two have a good relationship?"],
            r"(.*)(wife|husband|spouse|significant other|girlfriend|boyfriend|partner)(.*)": [r"How long have you been together?", 
                                    r"Tell me about your \2.", r"Do you have a good relationship with your \2?", 
                                    r"Tell me more about your relationship."], 
            
            # looks for words related to school
            r"(.*)(school|schoolwork|college|university|professors?|homework|assignments?|projects?|tests?|exams?)(.*)": 
                                    [r"What do you study?", r"Tell me more about school.", r"Do you like school?", 
                                    r"Other than that, how is school going?"],
            
            # looks for the words related to work
            r"(.*)(\bwork\b|job|boss|coworkers?)(.*)": [r"Tell me more about work.", r"What do you do?", r"Do you like your job?", 
                                    r"How is work?"],
            
            # looks for words referring to the user's childhood and prompts them to talk about it
            r"(.*)(childhood|when i was a kid|when i was a child|\bas a kid\b|\bas a child\b)(.*)": [r"Did you have a good childhood?", 
                                    r"Tell me about your childhood."],
            
            # looks for words that are sleep related
            r"(.*)dream|nightmare(.*)":[r"Tell me about your dreams.", r"Have you been having strange dreams?"], 
            r"(.*)sleep|tired|insomnia|(fall|fell|falling) asleep(.*)":[r"Have you been having strange dreams?",
                                    r"Do you get enough sleep every night?", r"What time do you usually go to sleep?", 
                                    r"How many hours of sleep do you usually get?"],
            
            # looks for the word "problem(s)". people go to therapy to talk about their problems so i thought it might come up
            r"(.*)(problems?)(.*)":[r"Why do you think that's a problem?", 
                                    r"How long have you been dealing with this problem?"], 
            
            # looks for the keyword "my" and prompts the user to talk about it more
            r"(.*)\bmy\b (.*)": [r"Tell me more about your \2"],
            
            # looks for the word "this" in case the user is talking about the conversation that's going on rn
            r"(.*)this is(.*)":[r"Why is this \2?", r"Why do you think this is \2?"],
            
            # looks for when the user is talking about how someone feels about them by searching for a pronoun and then the word "me"
            r"(he|she|they) (.*) me": [r"What makes you think \1 \2 you?", r"Why would \1 \2 you?", 
                                    r"Do you think you did something to make them \2 you?", r"What do you think made them \2 you"],
            
            # looks for when the user is talking about someone else by looking for pronouns like "he", "she", "they"
            r"(.*)\b(he|she|they)\b (.*)":[r"Is it important to you that they \3?", r"Why do you care if they \3?", 
                                    r"How does it make you feel that they \3"],
            
            # looks for ways someone might ask a question about themselves like "why do i []", "why can't i []", "am i []"
            r"why do i (.*)?": [r"I can't answer that for you.", r"What do you think?", r"Why do you think you \1?", 
                                    r"What makes you say that?"],
            r"why can\'t i (.*)\?": [r"I don't know. Why can't you?", r"Do you think you should be able to \1?", 
                                    r"I can't answer that for you. Why do you think you can't \1"],
            r"am i (.+)\?" : [r"Are you?", r"What makes you think you are \1?", r"I can't answer that for you."], 
            # the other regex that captures "am i" + some other phrase has a response that uses whatever the user inputs after and
            # that wouldn't make sense if the user only typed "am i?"
            r"^am i\?$" : [r"Are you?", r"I can't answer that for you.", r"What do you think?", r"Do you think you are?"], 

            # looks for common question words like "why", "do", "can", "what", "how" and deflects the question. there are some default 
            # responses that all the words have in common, but there are also different responses depending on whether the user is 
            # asking a question about eliza or themselves
            r"(why|how|what)(.*)\?": [r"Why don't you tell me?", r"What do you think?", r"Why do you ask?", r"Is that important to you?"],
            r"do you(.*)\?" : [r"Do I?", r"What do you think?", r"Does it matter?", r"What makes you ask that?"],
            r"do i(.*)\?" : [r"Do you think you do?", r"What makes you think you \1?", r"I can't answer that for you"],
            r"can i(.*)\?" : [r"Is that something you want?", r"Can you?", r"Do you think you can?", r"What do you think?"], 
            r"(can|will) you(.*)\?" :[r"Why do you ask?", r"Is that important to you?", r"Why does it matter what I do?"],

            # looks for a question mark in case the user asks eliza something that was missed by the other regular expressions
            r"(.*)\?": [r"Why do you ask?", r"What do you think?", r"Why don't you tell me?", 
                                    r"I can't answer that for you."],

            # if the user says something about eliza using "you are" or "you're" it'll just deflect the question
            r"(.*)(you are|you're)(.*)" : [r"I am?", r"What makes you say I'm \3?", r"What do you mean?", 
                                    r"Why do you think I'm \3?", r"How am I \3?"],
            
            # if the user says something with "you" in it for when the user is talking about eliza
            r"(.*)you(.*)" : [r"Me?", r"What makes you say that?", r"Let's focus on you.", 
                                    r"And how does that make you feel?"],
            
            # looks for some common ways the user might greet eliza like "hi", "hello", "hey"
            r"(\bhello\b|\bhi\b|\bhey\b)(.*)" : [r"Hello. How are you?", r"Hi. How are you?", 
                                    r"Thanks for coming to see me today. What can I help you with?", 
                                    r"What brings you in today?"],            
            
            # default responses if eliza doesn't understand what the user said
            r"(.*)" : [r"What do you mean by that?", r"I see...", r"Interesting...", r"Could you elaborate?", 
                                    r"How does that make you feel?", r"Tell me more."],
            
    } 

    print("Hi, I'm Eliza. What's your name?")
    print("By the way, if you ever get tired of speaking to me just say \"Bye\".")

    # loops until eliza can get the user's name. 
    while (True):

        user = input()

        # searches for some common ways for someone to introduce themselves
        match = re.search(r"(.*)(i'm|i am|this is|it's|my name's|i go by|my name is) (.*)", user, re.IGNORECASE)
        if match:
            
            print("Hi " + match.group(3) + "! How are you?")
            
            break
        
        else:
            
            match = re.search(r"^[A-Za-z]+$", user, re.IGNORECASE)
            
            # checks if the user said bye, if they did print out a response one of the values associated with that key
            if (user.lower() == "bye"):
                print(random.choice(rules[r"\bbye\b"]))
                return
            
            # checks to see if someone entered their name with no introduction
            elif match:
                print("Hi " + user + "! How are you?")
                break
            
            else: 
                print("Sorry. I'm terrible with names. Could you repeat that?")
   
    user = ""

    # while loop that runs until user says bye
    while (True): 

        # gets the user's message and removes end punctuation except for question marks
        user = input().replace('.', '').replace('!', '')

        # loops through the dictionary rules
        for key in rules:

            # checks if the user's message matches with any of the rules
            match = re.search(key, user, re.IGNORECASE) 

            if match:

                # randomly picks a response
                response = random.choice(rules[key])
                
                # checks if there are any blanks in the response that need to be replaced with words from the user's response
                if '\\1' in response:
                    phrase = match.group(1) # gets the phrase that will be used in the response
                    phrase = replace_words(phrase) # calls replace_words which will look for words that need to be substituted
                    response = re.sub(r'\\1', phrase, response) # replaces \1 with the new phrase
                if '\\2' in response:
                    phrase = match.group(2)
                    phrase = replace_words(phrase)                          
                    response = re.sub(r'\\2', phrase, response)
                if '\\3' in response:
                    phrase = match.group(3)
                    phrase = replace_words(phrase) 
                    response = re.sub(r'\\3', phrase, response)                 

                print(response)
                break
        

        # checks if the user said "bye" 
        if (user.lower() == "bye"):
            return



if __name__ == '__main__':
    main()