import requests, urllib, wordcloud
from keys import SURBHI_ACCESS_TOKEN, APP_ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#Token Owner : Surbhi Sood (@subtlyperfect)
#Sandbox Users : @thethresholdtoinfinity, @acadsquad, @accountthepublic, @_as1228_

BASE_URL = "https://api.instagram.com/v1/"


#Function to extract the information about the owner of the access token.


def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") %(SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
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


#Function to extract the ID of the user through username.


def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") %(insta_username, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print "Status code other than 200 received!"
        exit()


#Function to extract the information of another user when username is known.

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s?access_token=%s") %(user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    print user_id + " is the user ID."
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info['data']):
            print "Username: %s" %(user_info["data"]["username"])
            print "Your followers: %s" %(user_info["data"]["counts"]["followed_by"])
            print "Number of people followed by you: %s" %(user_info["data"]["counts"]["follows"])
            print 'Total number of posts: %s' %(user_info["data"]["counts"]["media"])
        else:
            print "No data available."
    else:
        print "Status code other than 200 received!"


#Function to access your latest post.


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


#Function to extract the latest post of another user.


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") %(user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
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


#Function to extract the ID of the most recent post.


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") %(user_id, SURBHI_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
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


#Function to like the latest post of a user.


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") %(media_id)
    payload = {"access_token": SURBHI_ACCESS_TOKEN}
    print "POST request url : %s" %(request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like["meta"]["code"] == 200:
        print "Like was successful!"
    else:
        print "Your like was unsuccessful. Try again!"


#Function to post a comment on the latest post of another user.


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": SURBHI_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + "media/%s/comments") %(media_id)
    print "POST request url: %s" % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment["meta"]["code"] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#Function to view a list of comments.


def view_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") %(media_id, SURBHI_ACCESS_TOKEN)
    print "GET request URL: %s" %(request_url)
    user_comments = requests.get(request_url).json()
    comments_list = []

    if user_comments["meta"]["code"] == 200:
        if len(user_comments["data"]):
            for x in range(0, len(user_comments["data"])):
                print user_comments["data"][x]["text"]
        else:
            print "There are no comments on the post!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


#Function to fetch the most recently liked media by the owner of access token.


def liked_media():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") %(SURBHI_ACCESS_TOKEN)
    print "GET request url: %s" %(request_url)
    payload = {"access_token": SURBHI_ACCESS_TOKEN}
    user_media = requests.get(request_url, payload).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media["data"][0]["id"] + ".jpeg"
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "The recently liked image with id " + image_name + " has been downloaded!"
        else:
            print "No media liked."
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


#Function to display menu options for the user.


def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to InstaBot."
        print "What would you like to do?"
        print "a. Fetch your own information."
        print "b. Fetch the details of another user."
        print "c. Fetch your most recent post."
        print "d. Fetch the most recent post of another user."
        print "e. Like the most recent post of another user."
        print "f. Comment on the most recent post of another user."
        print "g. View the list of comments on the most recent post of a user."
        print "h. Fetch the last post you liked."
        print "i. Exit"

        choice = raw_input("Enter you choice: ")

        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username: ")
            like_a_post(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username: ")
            post_a_comment(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username: ")
            view_comments(insta_username)
        elif choice == "h":
            liked_media()
        elif choice == "i":
            exit()
        else:
            print "wrong choice"

start_bot()