#dpankoff, 2016, comp sci - 1026

def main():

    import sys


#main will ask for the keyword file the user wishes to read in. It will try to read the file as well as read a line.
#if the file does not exist an exception will run

    inFile = input("please enter the keyword file you wish to process (e.g. keyfiles.txt) ")

    try:
        fileRead = open(inFile, "r")

        try:
            line = fileRead.readline()

        finally:
            fileRead.close()

    except IOError:
        print("Error! File not found")
        sys.exit()


    listOfKeyWords, dictionaryOfWords = keyTextProcessor(inFile)

#main will now repeat the same process for the keyword file, only now its for the file containing the tweets

    fileOfTweets = input("Please enter the name of the file containing the Tweets you wish to process"
                               "(e.g. twitterFileName.txt) ")
    try:
        fileRead = open(fileOfTweets, "r")

        try:
            line = fileRead.readline()

        finally:
            fileRead.close()

    except IOError:
        print("Error! File not found")
        sys.exit()


# tweet processor will process the tweets and return these lists (see tweetProcessor for more detailed info)

    eastTimeZone, centralTimeZone, mountainTimeZone, pacificTimeZone, numOfKeyWordsEast, numOfKeyWordsCentral, numOfKeyWordsMountain, numOfKeyWordsPacific, eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore = tweetProcessor(fileOfTweets, listOfKeyWords, dictionaryOfWords)

#printScores will simply take in the lists that tweetProcessor returns and utilize them to calculate
#the sentiment score for each time zone, as well as the number of tweets per time zone

    eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore = printScores(eastTimeZone, centralTimeZone, mountainTimeZone, pacificTimeZone, numOfKeyWordsEast, numOfKeyWordsCentral, numOfKeyWordsMountain, numOfKeyWordsPacific, eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore)

# this will simply create a fun graph from the data using a library

    graphMaker(eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore)





#this function simply processes the keywords file, sorts the keywords based on their sentiment value into a dictionary

def keyTextProcessor(keyFileName):

    import sys #imports sys.exit() so that program may quit if exception occurs

    keyWordFile = open(keyFileName, "r")

    listOfKeyWords = []
    keywordSentValue = []
    dictionaryOfWords = {}

# this loop simply reads each line within the keywords file
#it seperates keywords from their sentiment value
# it then appends they keywords as well as the sentiment value to a dictionary
#if the sentiment value is non-numerical an exception will occur

    try:
        for line in keyWordFile:
            line = line.strip()
            words = line.split(",")
            listOfKeyWords.append(words[0])
            keywordSentValue.append(int(words[1]))
    except ValueError as exception:
        print("Error! ,str(exception)")
        sys.exit()
    except IndexError as exception:
        print("Error ", str(exception))
        sys.exit()


    keyWordFile.close()


    try:
        for i in range(len(listOfKeyWords)):
            dictionaryOfWords[listOfKeyWords[i]] = keywordSentValue[i]

    except IndexError as exception:
        print("Error ", str(exception))
        sys.exit()



    return listOfKeyWords, dictionaryOfWords


# this function simply takes in the tweet file and processes each line to obtain a latitude, longitude, and tweet
# it then checks to see if a tweet contains any of the keywords, if it does the tweet is appended to a list
#the tweets are then sorted into their respective time zones


def tweetProcessor(tweetFileName, listOfKeyWords, dictionaryOfWords):
    import sys
    tweetFile = open(tweetFileName, 'r')
    import re
    tweetList =[]

# this loop simply removes the items contained within re.sub[] from the each line
# this will result in simply the tweet. Each tweet will then be added to a list of tweets

    try:
        for line in tweetFile:
            line = re.sub('[!,0123456789-:]', '', line)
            line = line.replace('[', '').strip().split("]", 1)
            tweetList.append(line[1])

    except IndexError as exception:
        print("Error! ", str(exception))
        sys.exit()

    tweetFile.close()


    tweetFile = open(tweetFileName, 'r')
    import re
    latitude = []
    longitude = []

# this loop will simply run through each line within the tweets file and obtain the latitudes and longitudes
# it will then attempt to append those values to a list (so long as they are numbers this will work)
# if they are not an exception will occur and the program will exit

    try:
        for line in tweetFile:
            line = re.sub('[!,]', '', line)
            line = line.replace('[', '').replace(']', "")
            line = line.split(' ')
            latitude.append(float(line[0]))
            longitude.append(float(line[1]))


    except ValueError as exception:
        print("Error!", str(exception))
        sys.exit()
    except IndexError as exception:
        print("Error! ", str(exception))
        sys.exit()



    latitudeOfGoodTweets = []
    longitudeOfGoodTweets = []
    listOfGoodTweets= []
    scoreOfTweet = []
    numOfKeyWordsPerTweet = []

    try:
        for i in range(len(tweetList)):
            count = 0 #used to count the number of key words found
            tweet = tweetList[i]
            tweet = re.sub('[!,0123456789-:.]', '', tweet)
            word = tweet.split(" ")
            for j in range (len(listOfKeyWords)):
                if listOfKeyWords[j] in word:
                    count = count + 1
            if count > 0:
                listOfGoodTweets.append(tweetList[i])
                latitudeOfGoodTweets.append(latitude[i])
                longitudeOfGoodTweets.append(longitude[i])
                numOfKeyWordsPerTweet.append(count)

        for i in range(len(listOfGoodTweets)):
            count = 0 #used to count the number of key words found
            tweet = listOfGoodTweets[i]
            tweet = re.sub('[!,#@0123456789-:.]', '', tweet)
            word = tweet.split(" ")
            for j in range(len(word)):
                if word[j] in dictionaryOfWords:
                    scoreOfTweet.append(dictionaryOfWords[word[j]])




    except IndexError as exception:
        print("Error! ", str(exception))
        sys.exit()


    eastTimeZone = []
    numOfKeyWordsEast = []
    eastTimeZoneScore = []


    centralTimeZone = []
    numOfKeyWordsCentral = []
    centralTimeZoneScore = []


    mountainTimeZone = []
    numOfKeyWordsMountain = []
    mountainTimeZoneScore = []


    pacificTimeZone = []
    numOfKeyWordsPacific= []
    pacificTimeZoneScore =[]



#these loops will simply sort each tweet into a time zone based on the latitude and longitude for that tweet
#note: it only takes in valid tweets that were shown to have at least one keyword in them
#if the tweet does not fall within any range of time zones it will not be added to a list and therefor not used

    try:
        for i in range(len(listOfGoodTweets)):
            if longitudeOfGoodTweets[i] <= -67.444574 and longitudeOfGoodTweets[i] >= -87.518395:
                if latitudeOfGoodTweets[i] >= 24.660845 and latitudeOfGoodTweets[i] <= 49.189787:
                    eastTimeZone.append(listOfGoodTweets[i])
                    numOfKeyWordsEast.append(numOfKeyWordsPerTweet[i])
                    eastTimeZoneScore.append(scoreOfTweet[i])




            elif longitudeOfGoodTweets[i] < -87.518395 and longitudeOfGoodTweets[i] >= -101.998892:
                if latitudeOfGoodTweets[i] >= 24.660845 and latitudeOfGoodTweets[i] <= 49.189787:
                    centralTimeZone.append(listOfGoodTweets[i])
                    numOfKeyWordsCentral.append(numOfKeyWordsPerTweet[i])
                    centralTimeZoneScore.append(scoreOfTweet[i])


            elif longitudeOfGoodTweets[i] < -101.998892 and longitudeOfGoodTweets[i] >= -115.236428:
                if latitudeOfGoodTweets[i] >= 24.660845 and latitudeOfGoodTweets[i] <= 49.189787:
                    mountainTimeZone.append(listOfGoodTweets[i])
                    numOfKeyWordsMountain.append(numOfKeyWordsPerTweet[i])
                    mountainTimeZoneScore.append(scoreOfTweet[i])

            elif longitudeOfGoodTweets[i] < -115.236428 and longitudeOfGoodTweets[i] >= -125.242264:
                if latitudeOfGoodTweets[i] >= 24.660845 and latitudeOfGoodTweets[i] <= 49.189787:
                    pacificTimeZone.append(listOfGoodTweets[i])
                    numOfKeyWordsPacific.append(numOfKeyWordsPerTweet[i])
                    pacificTimeZoneScore.append(scoreOfTweet[i])

    except IndexError as exception:
        print("Error! ", str(exception))
        sys.exit()





    return eastTimeZone, centralTimeZone, mountainTimeZone, pacificTimeZone, numOfKeyWordsEast, numOfKeyWordsCentral, numOfKeyWordsMountain, numOfKeyWordsPacific, eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore


def printScores(eastTimeZone, centralTimeZone, mountainTimeZone, pacificTimeZone, numOfKeyWordsEast, numOfKeyWordsCentral, numOfKeyWordsMountain, numOfKeyWordsPacific, eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore):

    import sys

#the function will try to compute the tweet scores of each time zone, if a time zone has zero tweets a  zeroDivisonError will run

    try:
        eastTimeZoneScore = sum(eastTimeZoneScore) / sum(numOfKeyWordsEast)
        centralTimeZoneScore = sum(centralTimeZoneScore) / sum(numOfKeyWordsCentral)
        mountainTimeZoneScore = sum(mountainTimeZoneScore) / sum(numOfKeyWordsMountain)
        pacificTimeZoneScore = sum(pacificTimeZoneScore) / sum(numOfKeyWordsPacific)

    except ZeroDivisionError as exception:
        print("Error ", str(exception))
        sys.exit()



    print("The overall happiness score for the Eastern Time Zone with ", len(eastTimeZone), "tweets, was %.2f " % eastTimeZoneScore)
    print("The overall happiness score for the Central Time Zone with ", len(centralTimeZone), "tweets, was %.2f " % centralTimeZoneScore)
    print("The overall happiness score for the Mountain Time Zone with ", len(mountainTimeZone), "tweets, was %.2f " % mountainTimeZoneScore)
    print("The overall happiness score for the Pacific Time Zone with ", len(pacificTimeZone), "tweets, was %2.f" % pacificTimeZoneScore)

    return eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore


# this function simply creates a hisogram for the overall scores of each timezone.

def graphMaker(eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore):
    from happy_histo import drawSimpleHistogram

    drawSimpleHistogram(eastTimeZoneScore, centralTimeZoneScore, mountainTimeZoneScore, pacificTimeZoneScore)


main()
