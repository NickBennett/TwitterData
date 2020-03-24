#############
# Read JSON files and convert to CSV
#############
import csv,json

def read_tweets_from_json():
    print("Read tweets from json? ")
    answer = input("Y/N ")
    if answer == "Y":
        json_files_list = ["your-files-here.json"] # This works with multiple files, so you can add more to this list eg ["file1.json","file2.json","file3.json"]
        
        # Check if output file already exists
        proceed = False
        try:
            output_file = csv.DictReader(open("output.csv"),"r")
            print("Output file already exists, please rename in the code.")
        except:
            proceed = True
            print("Creating output file...")
            output_file = csv.writer(open("output.csv","w",newline='',encoding='utf-8'))
            parent_headers = ['Handle','Username','Timestamp','Text','Coordinates','Lat','Lon','isRetweeted','isFavourited','Followers','Following','Total Tweets','Tweet Place','Tweet Place Type','Profile Location','Lang','Source','Mentions','Hashtags','Urls','User ID','Tweet ID','Description','Boundary Box Coords','Bbox Lat','Bbox Lon','isRT','isQuote','isReply','Original Text','InReplyToScreenName','inReplyToTweetID','inReplytoUserID','Quoted User']
            output_file.writerow(parent_headers)
            
        # If output file has been created and there are no conflicts, proceed.    
        if proceed == True:
            total_tweets_written = int(0)
            total_geo_tweets = 0
            replies = 0
            retweets = 0
            quotes = 0
            
            # Load the files from the list and convert to JSON
            for json_file in json_files_list:
                
                print("Loading in JSON file - takes a while...")
                json_file_open = open(json_file)
                
                # Write these users and all their info to CSV
                main_file = json.load(json_file_open)
                print("Writing the tweets to CSV...")  
                for i in main_file:
                    i = json.loads(i)
                    handle = ""            
                    username = ""            
                    timestamp = ""
                    text = ""            
                    coordinates = ""
                    followers = ""
                    following = ""
                    total_tweets = ""            
                    tweet_place = ""
                    tweet_place_type = ""
                    profile_location = ""
                    lang = ""
                    source = ""
                    mention_list = []
                    hashtag_list = []
                    urls_list = []
                    user_id = 0
                    tweet_id = 0
                    lat = ""
                    lon = ""
                    description = ""
                    match_set = ""
                    bounding_box_coords = ""
                    bbox_lat = ""
                    bbox_lon = ""
                    isretweeted = ""
                    isfavourited = ""
                    isReply = ""
                    in_reply_to_status_id_str = ""
                    in_reply_to_user_id_str = ""
                    in_reply_to_screen_name = ""
                    isRT = ""
                    isQuote = ""
                    original_text = ""
                    quoted_user = ""
                    timestamp = i['created_at']
    #                if "2017" in timestamp or "2018" in timestamp or "2019" in timestamp:                
                    total_tweets_written += 1
                    # Encode raw text to prevent Python crashes
                    handle = (i['user']['name']).encode('ascii','ignore').decode("utf-8")
                    username = i['user']['screen_name'].encode('ascii','ignore').decode("utf-8")
                    print("Analysing: ", username)
                    try:
                        text = (i['full_text'].replace("\n","").replace("\r","")).encode('ascii','ignore').decode("utf-8")
                    except:
                        text = (i['text'].replace("\n","").replace("\r","")).encode('ascii','ignore').decode("utf-8")
                    user_id = int(i['user']['id'])
                    tweet_id = int(i['id'])
                                    
                    # if statements are needed as some fields are empty and thus would crash
                    if i['coordinates']:
                        coordinates = json.dumps(i['coordinates']['coordinates']).replace('"','').replace("[",'').replace("]",'')
                        total_geo_tweets += 1
                        lat = coordinates.split(", ")[1]
                        lon = coordinates.split(", ")[0]
                    if i['favorite_count']:
                        isfavourited = i['favorite_count']
                    if i['retweet_count']:
                        isretweeted = i['retweet_count']
                    
                    # Replies
                    if i['in_reply_to_status_id_str']:
                        in_reply_to_status_id_str = i['in_reply_to_status_id_str']
                        isReply = "true"
                        replies += 1
                        if i['in_reply_to_user_id_str']:
                            in_reply_to_user_id_str = i['in_reply_to_user_id_str']
                        if i['in_reply_to_screen_name']:
                            in_reply_to_screen_name = i['in_reply_to_screen_name']
                    # Quotes
                    try:
                        if i['quoted_status_id']:
                            isQuote = "true"
                            quotes += 1
                            original_text = i['quoted_status']['full_text'].encode('ascii','ignore').replace("\n"," ").replace("\r"," ").decode("utf-8")
                            quoted_user = i['quoted_status']['user']['screen_name'].encode('ascii','ignore').decode("utf-8")
                    except:
                        pass
                    # Retweets 
                    try:                           
                        if i['retweeted_status']:
                            isRT = "true"
                            if isRT == "true":
                                retweets += 1
                                original_text = i['retweeted_status']['full_text'].encode('ascii','ignore').replace("\n"," ").replace("\r"," ").decode("utf-8")
                    except:
                        pass
                            
                        
                    if i['user']['followers_count']:
                        followers = i['user']['followers_count']
                    if i['user']['friends_count']:
                        following = i['user']['friends_count']
                    if i['user']['statuses_count']:
                        total_tweets = i['user']['statuses_count']
                    if i['source']:
                        source = i['source'].split('nofollow\">')[1].split("</a>")[0].encode('ascii','ignore').decode("utf-8")
                    if i['entities']['user_mentions']:
                        for mention in i['entities']['user_mentions']:
                            mention_list.append(json.dumps(mention['screen_name']).replace('"','').encode('ascii','ignore').decode("utf-8"))
                    if i['entities']['hashtags']:
                        for hashtag in i['entities']['hashtags']:
                            hashtag_list.append(json.dumps(hashtag['text']).replace('"','').encode('ascii','ignore').decode("utf-8"))
                    if i['entities']['urls']:
                        for url in i['entities']['urls']:
                            urls_list.append(json.dumps(url['expanded_url']).replace('"','').encode('ascii','ignore').decode("utf-8"))
                    if i['user']['location']:
                        profile_location = i['user']['location'].encode('ascii','ignore').decode("utf-8")
                    if i['user']['description']:
                        description = i['user']['description'].encode('ascii','ignore').decode("utf-8")
                    if i['user']['lang']:
                        lang = i['user']['lang'].decode("utf-8")
                    if i['place']:
                        if i['place']['place_type']:
                            tweet_place = (i['place']['full_name']).encode('ascii','ignore').decode("utf-8")
                            tweet_place_type = (i['place']['place_type']).encode('ascii','ignore').decode("utf-8")
                            if i['place']['bounding_box']:                              
                                if list(i['place']['bounding_box']['coordinates'])[0][0] == list(i['place']['bounding_box']['coordinates'])[0][1]:
                                    bounding_box_coords = list(i['place']['bounding_box']['coordinates'])[0][0]
                                    bbox_lat = list(i['place']['bounding_box']['coordinates'])[0][0][1]
                                    bbox_lon = list(i['place']['bounding_box']['coordinates'])[0][0][0]
                                    total_geo_tweets += 1
    
                        
                    output_file.writerow([handle,username,timestamp,text,coordinates,lat,lon,isretweeted,isfavourited,followers,following,total_tweets,tweet_place,tweet_place_type,profile_location,lang,source,mention_list,hashtag_list,urls_list,user_id,tweet_id,description,bounding_box_coords,bbox_lat,bbox_lon,match_set,isRT,isQuote,isReply,original_text,in_reply_to_screen_name,in_reply_to_status_id_str,in_reply_to_user_id_str,quoted_user])
            print("Total tweets written: " + str(total_tweets_written))
            print("Total geo tweets written: " + str(total_geo_tweets))
            print("Quotes: " + str(quotes))
            print("Retweets: " + str(retweets))
            print("Replies: " + str(replies))
    else:
        print("Noped out.")

read_tweets_from_json()