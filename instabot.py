# Importing necessary libraries, modules and classes.

import requests, urllib, wordcloud, matplotlib
from keys import SURBHI_ACCESS_TOKEN, APP_ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Token Owner : Surbhi Sood (@subtlyperfect)
# Sandbox Users : @acadsquad, @iv_jot, @accountthepublic, @_as1228_, @pktest1111 @thethresholdtoinfinity

BASE_URL = "https://api.instagram.com/v1/"


# Function to extract the information about the owner of the access token.


def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") % (SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % request_url
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "Username: %s" %(user_info['data']['username'])
            print "Your followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "Number of people followed by you: %s" % (user_info["data"]["counts"]["follows"])
            print "Total number of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "User does not exist!"
    else:
        print "Status code other than 200 received!"


# Function to extract the ID of the user through username.


def get_user_id(insta_username):
    request_url = BASE_URL + "users/search?q=%s&access_token=%s" % (insta_username, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "User Found! ID: " + user_info["data"][0]["id"]
            return user_info["data"][0]["id"]
        else:
            print "User does not exist!"
            return None
    else:
        print "Status code other than 200 received!"
        exit()


# Function to extract the information of another user when username is known.


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = BASE_URL + "users/%s/?access_token=%s" % (user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    print user_id + " is the user ID."
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info['data']):
            print "Username: %s" %(user_info["data"]["username"])
            print "Your followers: %s" %(user_info["data"]["counts"]["followed_by"])
            print "Number of people followed by the user: %s" %(user_info["data"]["counts"]["follows"])
            print 'Total number of posts: %s' % user_info["data"]["counts"]["media"]
        else:
            print "No data available."
    else:
        print "Status code other than 200 received!"


# Function to access your latest post.


def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    own_media = requests.get(request_url).json()

    if own_media["meta"]["code"] == 200:
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            image_url = own_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image with post id " + own_media["data"][0]["id"] + " has been downloaded!"
        else:
            print "No posts.!"
    else:
        print "Status code other than 200 received!"


# Function to extract the latest post of another user.


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_media = requests.get(request_url).json()

    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            image_name = user_media["data"][0]["id"] + '.jpeg'
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image with id " + user_media["data"][0]["id"] + " has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received!"


# Function to extract the ID of the most recent post.


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_media = requests.get(request_url).json()

    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            return user_media["data"][0]["id"]
        else:
            print "There is no recent post of the user!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


# Function to like the latest post of a user.


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") % (media_id)
    payload = {"access_token": SURBHI_ACCESS_TOKEN}
    print "POST request url : %s" % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like["meta"]["code"] == 200:
        print "The recent post having ID " + media_id + " was successfully liked!"
    else:
        print "Your like was unsuccessful. Try again!"


# Function to post a comment on the latest post of another user.


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": SURBHI_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + "media/%s/comments") % (media_id)
    print "POST request url: %s" % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment["meta"]["code"] == 200:
        print "A comment was added successfully to the post having ID " + media_id + "."
    else:
        print "Unable to add comment. Try again!"


# Function to view a list of comments.


def view_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id, SURBHI_ACCESS_TOKEN)
    print "GET request URL: %s" % (request_url)
    user_comments = requests.get(request_url).json()

    if user_comments["meta"]["code"] == 200:
        if len(user_comments["data"]):
            for x in range(0, len(user_comments["data"])):
                print "All the comments on the recent post having ID " + media_id + " are as follows:\n" + user_comments["data"][x]["text"]
        else:
            print "There are no comments on the post!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


# Function to fetch the most recently liked media by the owner of access token.


def liked_media():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") % (SURBHI_ACCESS_TOKEN)
    print "GET request url: %s" % (request_url)
    payload = {"access_token": SURBHI_ACCESS_TOKEN}
    user_media = requests.get(request_url, payload).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media["data"][0]["id"] + ".jpeg"
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "The recently liked image having ID " + image_name + " has been downloaded!"
        else:
            print "No media liked."
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


# Function to delete negative comments.


def del_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info["meta"]["code"] == 200:
        if len(comment_info["data"]):
            for x in range(0, len(comment_info["data"])):
                comment_id = comment_info["data"][x]["id"]
                comment_text = comment_info["data"][x]["text"]
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print "Negative comment found: %s" % comment_text
                    delete_url = (BASE_URL + "media/%s/comments/%s/?access_token=%s") % (media_id, comment_id, SURBHI_ACCESS_TOKEN)
                    print "DELETE request url : %s" % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info["meta"]["code"] == 200:
                        print "Comment successfully deleted!"
                    else:
                        print "Unable to delete comment!"
                else:
                    print "Positive comment found: %s" % (comment_text)
        else:
            print "There are no existing comments on the post!"
    else:
        print "Status code other than 200 received!"


# Function find sub-trends for an event or activity and plot a word cloud.


def tag_info():
    tag_dictionary = {}
    hash_tag = raw_input("Enter the trending tag you want to search: ")
    request_url = (BASE_URL + "tags/%s/media/recent?access_token=%s") % (hash_tag, SURBHI_ACCESS_TOKEN)
    print "GET request url: %s" % (request_url)
    req_media = requests.get(request_url).json()

    if req_media["meta"]["code"] == 200:
        if req_media["data"]:
            for x in range(0, len(req_media["data"])):
                media_id = req_media["data"][x]["tags"]

                for y in range(0,len(media_id)):
                    if req_media["data"][x]["tags"][y] in tag_dictionary:
                        tag_dictionary[req_media["data"][x]["tags"][y]] += 1
                    else:
                        tag_dictionary[req_media["data"][x]["tags"][y]] = 1
        else:
            print "No posts found."
    else:
        print "Status code other than 200 received."

    tag_dictionary.pop(hash_tag.lower(), None)
    print tag_dictionary

    wordcloud = WordCloud().generate_from_frequencies(tag_dictionary)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.show()


# Function to display menu options for the user.


def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to InstaBot."
        print "What would you like to do?"
        print "a. Fetch your own information."
        print "b. Get the user ID of another user/ Search for another user."
        print "c. Fetch the details of another user including the user ID."
        print "d. Fetch your most recent post."
        print "e. Fetch the most recent post of another user."
        print "f. Like the most recent post of another user."
        print "g. Comment on the most recent post of another user."
        print "h. View the list of comments on the most recent post of a user."
        print "i. Fetch the last post you liked."
        print "k. Delete negative comments."
        print "k. Find sub-trends for an event or activity and plot a word cloud."
        print "l. Exit."

        choice = raw_input("Enter you choice: ")

        if choice == "a":
            self_info()

        if choice == "b":
            insta_username = raw_input("Enter the username you want to search: ")
            get_user_id(insta_username)

        elif choice == "c":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            get_user_info(insta_username)

        elif choice == "d":
            get_own_post()

        elif choice == "e":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            get_user_post(insta_username)

        elif choice == "f":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            like_a_post(insta_username)

        elif choice == "g":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            post_a_comment(insta_username)

        elif choice == "h":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            view_comments(insta_username)

        elif choice == "i":
            liked_media()

        elif choice == "j":
            insta_username = raw_input("Enter the username: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. "
                insta_username = raw_input("Please re-enter a valid name: ")
            else:
                print insta_username
            del_negative_comment(insta_username)

        elif choice == "k":
            tag_info()

        elif choice == "l":
            exit()

        else:
            print "wrong choice"


# Initialise the code.


start_bot()