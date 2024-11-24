from flask_security import Security, verify_password, hash_password

from backend.models import *


security = Security()

def login_fn(email, password):
    user = userdatastore.find_user(email=email)  
    if user:
        if verify_password(password, user.password):  
            return user.get_auth_token()
        return 'Invalid password'
    return 'User not found'

def raw(text): #to convert the searched word to raw string
    split_list = text.split() #converts to a list
    search_word = ''
    for word in split_list:
        search_word += word.lower()
    return search_word

    # influencer = User.query.filter_by(type="general").all()
    # sponsor = Sponser.query.all()
    # types = []
    # for i in influencer:
    #     types.append(i.type)
    # for s in sponsor:
    #     types.append(s.type)
    # plt.clf()
    # plt.title("Active Users")
    # plt.xlabel("Type of User")
    # plt.ylabel("Number of Users")
    # plt.hist(types, color="maroon")
    # plt.savefig('static/img/stats/is_img.png')

    # flagged_influencer = User.query.filter_by(is_flagged = "True")
    # flagged_sponsor = Sponser.query.filter_by(is_flagged = "True")
    # flagged = []
    # for i in flagged_influencer:
    #     flagged.append(i.type)
    # for s in flagged_sponsor:
    #     flagged.append(s.type)
    # plt.clf()
    # plt.title("Flagged Users")
    # plt.xlabel("Type of User")
    # plt.ylabel("Number of flagged Users")
    # plt.hist(flagged, color="green")
    # plt.savefig('static/img/stats/fis_img.png')

    # influencer = User.query.filter_by(type="general").all()
    # types = []
    # for i in influencer:
    #     types.append(i.niche)
    # plt.clf()
    # plt.title("Influencers based on Niche")
    # plt.xlabel("Niche")
    # plt.ylabel("Number of Influencers")
    # plt.hist(types, color="blue")
    # plt.savefig('static/img/stats/iimg.png')

    # sponser = Sponser.query.all()
    # types = []
    # for s in sponser:
    #     types.append(s.industry)
    # plt.clf()
    # plt.title("Sponors based on Industry")
    # plt.xlabel("Industry")
    # plt.ylabel("Number of Sponsors")
    # plt.hist(types, color="yellow")
    # plt.savefig('static/img/stats/simg.png')

    # ad = Ad_request.query.all()
    # types = []
    # for a in ad:
    #     types.append(a.status)
    # plt.clf()
    # plt.title("Ad Requests")
    # plt.xlabel("Ad-Requests")
    # plt.ylabel("Number of Ads")
    # plt.hist(types)
    # plt.savefig('static/img/stats/aimg.png')

    
    # return render_template("admin_stats.html")
