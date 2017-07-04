from keys import SURBHI_ACCESS_TOKEN
import requests, matplotlib, wordcloud

BASE_URL = "https://api.instagram.com/v1/"


hash_tag = raw_input("Enter the trending tag you want to search: ")


def tag_info():
    hash_tag = raw_input("Enter the trending tag you want to search: ")
    tag_dictionary = {}
    request_url = (BASE_URL + "tags/%s/media/recent?access_token=%s") %(hash_tag, SURBHI_ACCESS_TOKEN)
    print "GET request url: %s" %(request_url)
    req_media = requests.get(request_url).json()

    if req_media["meta"]["code"] == 200:
        if req_media["data"]:
            for x in range(0, len(req_media["data"])):
                media_id = {req_media["data"][x]["tags"]}

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

tag_info()