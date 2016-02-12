"""-bill crescendostats help returns a list of all crescendo commands"""
import re
import json
import simplejson
from utils import crescendoUtils
from utils import dynamo
import random
import gif

CRESCENDO_ENV = dynamo.getDynamoEnvironment()

rageList = ['no', 'stop', 'you dun fucked up now', 'invalid', 'whiskey', 'you\'re drunk', 'you\'re the reason I drink', 'you make me drink', 'you make me sad', 'please stop']

# social stats
socialStats = {'socialPosts':0, 'publishedBlogs':0, 'totalBlogs': 0, 'failedPosts': 0}

def writeConfig(black):
    print 'writing config'
    with open('plugins/blacklist.cfg', 'w') as f:
        f.write(json.dumps(black))
        f.close()
        
def loadConfig():
    print 'loading config'
    config = {}
    with open('plugins/blacklist.cfg', 'r') as f:
        config = simplejson.load(f)
        f.close()
    return config
        
def getBlackTenants():
    config = loadConfig()
    BLACKTENANTS = []
    for id in config['tenants']:
        BLACKTENANTS.append(str(id))
    print BLACKTENANTS
    return BLACKTENANTS
    
# BLACKEMAILS = []
# for email in config['emails']:
#     BLACKEMAILS.append(str(email))

def crescendostats(user,action,parameter):
    global rageList
    print "Action! " + action
    if action == 'tenants':
        if parameter == 'csv':
            return csvAllTenants()
        else:
            return listAllTenants()
    elif action == 'help':
        return getHelp()
    elif action == 'metrics over time':
        return gif.gif('funny graph')
    elif action == 'tenant count':
        return tenantCount()
    elif action == 'users':
        if parameter == 'csv':
            return csvAllUsers()
        else:
            return listAllUsers()
    elif action == 'user count':
        return userCount()
    elif action == 'people count':
        return peopleCount()
    elif action == 'total signups':
        return gif.gif("not done yet")
    elif action == 'onboarded':
        return gif.gif("not done yet")
    elif action == 'summary':
        return summary()
    elif action == 'get blacklist':
        return getBlackList()
    elif action == 'blacklist tenant':
        print 'param'
        print parameter
        if parameter is not None and parameter != "":
            blackListTenant(parameter)
            return getBlackList()
        else:
            return "YOU SHALL NOT PASS! (without a tenant id)"
    elif action == 'unblacklist tenant':
        if parameter is not None and parameter != "":
            unBlackListTenant(parameter)
            return getBlackList()
        else:
            return gif.gif(random.choice(rageList))
    else:
        print 'BAD THINGS BILL BAD BAD THINGS'
        return gif.gif(random.choice(rageList))
        
def blackListTenant(tenantId):
    BLACKTENANTS = getBlackTenants()
    BLACKTENANTS.append(tenantId)
    BLACKLIST = loadConfig()
    BLACKLIST['tenants'] = BLACKTENANTS
    writeConfig(BLACKLIST)

def blackListEmail(email):
    pass

def unBlackListTenant(tenantId):
    BLACKTENANTS = getBlackTenants()
    if tenantId in BLACKTENANTS:
        BLACKTENANTS.remove(tenantId)
        BLACKLIST = loadConfig()
        BLACKLIST['tenants'] = BLACKTENANTS
        writeConfig(BLACKLIST)  

def unBlackListEmail(email):
    pass

def fieldHelper(name, item, color="#14892c"):
    ret = []
    ret.append({'short': True, 'title': name, 'value':str(item)})
    message = {'fallback': 'Crescendo Tenants', 'pretext': 'Crescendo', 'color': color, 'fields': ret}
    return message
    
def fieldsHelper(names, items, color="#14892c"):
    ret = []
    i = 0 
    for name in names:
        ret.append({'short': True, 'title': name, 'value':str(items[i])})
        i += 1
    message = {'fallback': 'Crescendo Tenants', 'pretext': 'tenants', 'color': color, 'fields': ret}
    return message

def randColor():
	color = '#'
	text = '1234567890abcdef'
	for i in range(6):
		color += random.choice(text)
	return color

######################## Global Stats ############################### 

def tenantCount():
    '''
    Gets the Tenant count
    Returns int
    '''
    global CRESCENDO_ENV
    
    msg = fieldHelper("Tenant Count", len(crescendoUtils.getTenantIDs(CRESCENDO_ENV, getBlackTenants())))
    print msg
    l = []
    l.append(msg)
    return l

def listAllTenants():
    '''
    listAllTenants returns [{name:tenantName, id:id}]
    '''
    global CRESCENDO_ENV
    tenants = crescendoUtils.getTenantIDs(CRESCENDO_ENV,getBlackTenants())
    
    ret = []
    
    print "Listing..."
    
    for t in tenants:
        color = randColor()
        
        tStats = crescendoUtils.getTenantSocialInfo(CRESCENDO_ENV, t[0])
        
        fields = []
        fields.append( {'short': True, 'title': 'Tenant ID', 'value':str(t[0])} )
        fields.append( {'short': True, 'title': 'Tenant Name', 'value':str(t[2])} )
        fields.append( {'short': False, 'title': 'User Count', 'value':str(len(t[1])) } )
        #Twitter
        fields.append( {'short': True, 'title': 'Twitter Posts (published)', 'value':tStats['Twitter_published']} )
        fields.append( {'short': True, 'title': 'Twitter Posts (scheduled)', 'value':tStats['Twitter_scheduled']} )
        #Facebook
        fields.append( {'short': True, 'title': 'Facebook Posts (published)', 'value':tStats['Facebook_published']} )
        fields.append( {'short': True, 'title': 'Facebook Posts (scheduled)', 'value':tStats['Facebook_scheduled']} )
        #LinkedIn
        fields.append( {'short': True, 'title': 'LinkedIn Posts (published)', 'value':tStats['LinkedIn_published']} )
        fields.append( {'short': True, 'title': 'LinkedIn Posts (scheduled)', 'value':tStats['LinkedIn_scheduled']} )
        
        fields.append( {'short': True, 'title': 'In Review Posts', 'value':tStats['inreview']})
        fields.append( {'short': True, 'title': 'In Review Posts', 'value':tStats['funkystate']})
        
        #Wordpress
        for key in tStats['wpStats']:
            fields.append( {'short': True, 'title': 'Blog [' + str(key) + ']', 'value': tStats['wpStats'][key] } )
        
        baseMessage = {'fallback': 'Tenant Info Block', 'text': '', 'color': color}
        baseMessage['fields'] = fields
        
        ret.append(baseMessage)
    
    return ret



def csvAllTenants():
    '''
    listAllTenants returns [{name:tenantName, id:id}]
    '''
    print 'csving mf'
    global CRESCENDO_ENV
    tenants = crescendoUtils.getTenantIDs(CRESCENDO_ENV,getBlackTenants())
    
    ret = []
    headers = ['TenantId', 'Tenant Name', 'User Count', 'Blogs Published', 'Blogs Scheduled', 'Blogs Assigned', 'Blog Ideas', 'Twitter Posts (published)', 'Twitter Posts (scheduled)', 'LinkedIn Posts (published)', 'LinkedIn Posts (scheduled)', 'Facebook Posts (published)', 'Facebook Posts (scheduled)']

    stats = []
    for header in headers:
        stats.append(header)
    
    ret.append(fieldHelper("All Tenants CSV Field Names:", str(headers)))
    color = randColor()
    
    for t in tenants:        
        tStats = crescendoUtils.getTenantSocialInfo(CRESCENDO_ENV, t[0])

        stats.append(t[0])
        stats.append(t[2])
        stats.append(len(t[1]))

        wpStats = tStats['wpStats']
        if 'published' in wpStats:
            stats.append(wpStats['published'])
        else:
            stats.append(None)

        if 'scheduled' in wpStats:
            stats.append(wpStats['scheduled'])
        else:
            stats.append(None)

        if 'assigned' in wpStats:
            stats.append(wpStats['assigned'])
        else:
            stats.append(None)

        if 'idea' in wpStats:
            stats.append(wpStats['idea'])
        else:
            stats.append(None)

        stats.append(tStats['Twitter_published'])
        stats.append(tStats['Twitter_scheduled'])
        stats.append(tStats['LinkedIn_published'])
        stats.append(tStats['LinkedIn_scheduled'])
        stats.append(tStats['Facebook_published'])
        stats.append(tStats['Facebook_scheduled'])

    url = crescendoUtils.writeStatsToS3(len(headers), stats, "AllTenants")
        
    baseMessage = {'fallback': 'Tenant Info Block', 'text': '', 'color': color}
    fields = []
    fields.append({'short': False, 'title': 'CSV Link', 'value': url})
    baseMessage['fields'] = fields
        
    ret.append(baseMessage)
    
    return ret


def setSocialStats():
    global CRESCENDO_ENV
    global socialStats

    socialPosts = 0
    publishedBlogs = 0
    totalBlogs = 0
    review = 0
    funkystate = 0

    socialStats['Twitter_published'] = 0
    socialStats['Twitter_scheduled'] = 0
    socialStats['Facebook_published'] = 0
    socialStats['Facebook_scheduled'] = 0
    socialStats['LinkedIn_published'] = 0
    socialStats['LinkedIn_scheduled'] = 0
    socialStats['inreview'] = 0
    socialStats['funkystate'] = 0
    
    tenants = crescendoUtils.getTenantIDs(CRESCENDO_ENV,getBlackTenants())
    for t in tenants:
        tStats = crescendoUtils.getTenantSocialInfo(CRESCENDO_ENV, t[0])
        # tally social stuffs

        #This will update all the things =D
        for key in tStats:
            if key in socialStats:
                socialStats[key] += tStats[key]

        socialPosts += tStats['Twitter_published']
        socialPosts += tStats['Twitter_scheduled']
        socialPosts += tStats['LinkedIn_published']
        socialPosts += tStats['LinkedIn_scheduled']
        socialPosts += tStats['Facebook_published']
        socialPosts += tStats['Facebook_scheduled']
        review += tStats['inreview']
        funkystate += tStats['funkystate']
        #failedPosts += tStats['twit_F']
        #failedPosts += tStats['fb_F']
        #failedPosts += tStats['li_F']
        
        # tally blog stuffs
        for key in tStats['wpStats']:
            if key == 'published':
                publishedBlogs += tStats['wpStats'][key]
            totalBlogs += tStats['wpStats'][key]

    # This is gross...
    socialStats['socialPosts'] = socialPosts
    socialStats['publishedBlogs'] = publishedBlogs
    socialStats['totalBlogs'] = totalBlogs
    socialStats['inreview'] = review
    socialStats['funkystate'] = funkystate

        
    
def listAllUsers():
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, getBlackTenants())
    tenants = {}
    
    for user in userList:
        if user['tid'] not in tenants:
            tenants[user['tid']] = []
        tenants[user['tid']].append(user)
    
    ret = []
    
    for tenantKey in tenants:
        color = randColor()
        tenant = tenants[tenantKey]
        fields = []
        fields.append( {'short': False, 'title': 'Tenant ID', 'value':tenant[0]['tid']} )
        for user in tenant:
            fields.append( {'short': True, 'title': 'User Email:', 'value': user['email']} )
            fields.append( {'short': True, 'title': 'Last Login Time', 'value': user['last_login_time']} )
        baseMessage = {'fallback': 'Tenant Info Block', 'text': '', 'color': color}
        baseMessage['fields'] = fields
        ret.append(baseMessage)
    
    return ret

def csvAllUsers():
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, getBlackTenants())
    tenants = {}
    
    for user in userList:
        if user['tid'] not in tenants:
            tenants[user['tid']] = []
        tenants[user['tid']].append(user)
    
    ret = []

    stats = ['tenantId', 'tenantName', 'email', 'lastLoginDate', 'lastLoginTime', 'firstName', 'lastName', 'roles']    
    fields = []

    color = randColor()
    baseMessage = {'fallback': 'Tenant Info Block', 'text': '', 'color': color}

    #Delim info

    ret.append(fieldHelper("All Users CSV Field Names:", "'tenantId', 'tenantName', 'email', 'lastLoginDate', 'lastLoginTime', firstName, lastName"))

    for tenantKey in tenants:
        tenant = tenants[tenantKey]
        tenantInfo = crescendoUtils.getTenantInfo(CRESCENDO_ENV, tenant[0]['tid'])

        fields = []
        for user in tenant:
            stats.append(tenantInfo['tid'])
            stats.append(tenantInfo['name'])
            stats.append(user['email'])
            if user['last_login_time'] is not None:
                stats.append(user['last_login_time'].split("T")[0])
                stats.append(user['last_login_time'].split("T")[1])
            else:
                stats.append(None)
                stats.append(None)
            stats.append(user['firstName'])
            stats.append(user['lastName'])
            stats.append(user['roles'])
            print user
            print str(user)

    url = crescendoUtils.writeStatsToS3(8, stats, "AllUsers")

    fields.append({'short': False, 'title': 'CSV Link', 'value': url})
    baseMessage['fields'] = fields

    ret.append(baseMessage)
    
    return ret
     
    
def userCount():
    '''
    Get the user count for every tenant
    Returns int
    '''
    global CRESCENDO_ENV
    
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, getBlackTenants())
    
    msg = fieldHelper("User Count", len(userList))
    l = []
    l.append(msg)
    return l
    
    
    
def peopleCount():
    global CRESCENDO_ENV
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, getBlackTenants())
    
    emails = []
    
    for user in userList:
        if user['email'] not in emails:
            emails.append(user['email'])
    
    msg = fieldHelper("People Count", len(emails))
    
    return msg
    
def summary():
    global CRESCENDO_ENV
    global socialStats
    
    print 'performing summary'
    
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, getBlackTenants())
    userCount = len(userList)
    
    emails = []
    for user in userList:
        if user['email'] not in emails:
            emails.append(user['email'])
            
    peopleCount = len(emails)
    tenantCount = len(crescendoUtils.getTenantIDs(CRESCENDO_ENV, getBlackTenants()))
    
    # get the social stats
    setSocialStats()
    
    names = ['Tenant Count', 'User Count', 'People Count', 'Blog Count', 'Blog Published Count', 'Social Count', 'Twitter Posts (published)', 'Twitter Posts (scheduled)', 'Facebook Posts (published)', 'Facebook Posts (scheduled)', 'LinkedIn Posts (published)', 'LinkedIn Posts (scheduled)', 'Social Posts in review', 'Social Posts in funky state']
    values = [tenantCount, userCount, peopleCount, socialStats['totalBlogs'], socialStats['publishedBlogs'], socialStats['socialPosts'], socialStats['Twitter_published'], socialStats['Twitter_scheduled'], socialStats['Facebook_published'], socialStats['Facebook_scheduled'], socialStats['LinkedIn_published'], socialStats['LinkedIn_scheduled'], socialStats['inreview'], socialStats['funkystate']]
    l = []
    message = fieldsHelper(names,values,randColor())
    l.append(message)
    return l
    
##################################################################### 

#####################################################################

def getBlackList():
    global CRESCENDO_ENV
    
    ret = []
    fields = []
    for tenant in getBlackTenants():
        fields.append( {'short': True, 'title': 'Tenant ID', 'value':str(tenant)} )

    baseMessage = {'fallback': 'Tenant Black List Block', 'text': 'Black List', 'color': '#000000'}
    baseMessage['fields'] = fields
        
    ret.append(baseMessage)
    
    return ret
    
def getHelp():
    msg = """
    -bill crescendostats summary returns a summary of crescendostats
    -bill crescendostats tenants returns a list of all tenants,
    -bill crescendostats tenant count returns a count of all tenants,
    -bill crescendostats users returns a list of all users,
    -bill crescendostats user count returns the total users in the system,
    -bill crescendostats people count returns the total unique users,
    -bill crescendostats get blacklist returns the black list
    -bill crescendostats blacklist tenant <tenant-id> blacklists that tenant from all statistics
    -bill crescendostats unblacklist tenant <tenant-id> removes that tenant from the blacklist re-enabling them in the statistics
    -bill crescendostats total signups Not yet done but feel free to try
    -bill crescendostats onboarded Not yet done but feel free to try
    -bill crescendostats metrics over time
    -bill crescendostats <anything else> will result in sass
    """
    return msg



######################################################################
def on_message(msg, server):
    text = msg.get("text", "")
    user = msg.get("user_name", "")
    print "Text: " + text
    match = re.match(r"bill crescendostats (metrics over time|help|unblacklist tenant|get blacklist|blacklist tenant|summary|tenants|tenant count|users|user count|people count|total signups|onboarded|.*) ?(.*)", text)
    if not match:
        return

    action = match.group(1)
    parameter = match.group(2)

    if action is None:
        print '3 group'
        action = match.group(4)
        
    print 'action' 
    print action
    print 'param'
    print parameter
    return crescendostats(user, action, parameter)
