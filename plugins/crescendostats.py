"""-bill crescendostats summary returns a summary of crescendostats,         -bill crescendostats tenants returns a list of all tenants,             -bill crescendostats tenant count returns a count of all tenants,           -bill crescendostats users returns a list of all users,            -bill crescendostats user count returns the total users in the system,           -bill crescendostats people count returns the total unique users,           -bill crescendostats blacklist returns the black list"""
import re
import json
from utils import crescendoUtils
from utils import dynamo
import random

blacklist = {'tenants': ['-1000', '02i37000000115gAAA','02i37000000JI3bAAG','02i3700000017rVAAQ','02i370000001375AAA','02i37000000122AAAQ','02i37000000114iAAA','02i3700000011mtAAA','02i37000000114YAAQ','02i37000000114TAAQ','02i37000000114dAAA' ] }

CRESCENDO_ENV = dynamo.getDynamoEnvironment()

BLACKTENANTS = blacklist['tenants']
BLACKEMAILS = []

def crescendostats(user,action,parameter):
    print "Action! " + action
    if action == 'tenants':
        return listAllTenants()
    elif action == 'tenant count':
        return tenantCount()
    elif action == 'users':
        return listAllUsers()
    elif action == 'user count':
        return userCount()
    elif action == 'people count':
        return peopleCount()
    elif action == 'total signups':
        pass
    elif action == 'onboarded':
        pass
    elif action == 'summary':
        return summary()
    elif action == 'blacklist':
        return getBlackList()
    else:
        print 'BAD THINGS BILL BAD BAD THINGS'
        return 'BAD THINGS BILL BAD BAD THINGS'

def fieldHelper(name, item, color="#14892c"):
    ret = []
    ret.append({'short': True, 'title': name, 'value':str(item)})
    message = {'fallback': 'Crescendo Tenants', 'pretext': 'tenants', 'color': color, 'fields': ret}
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
    
    msg = fieldHelper("Tenant Count", len(crescendoUtils.getTenantIDs(CRESCENDO_ENV, BLACKTENANTS)))
    print msg
    
    return msg

def listAllTenants():
    '''
    listAllTenants returns [{name:tenantName, id:id}]
    '''
    global CRESCENDO_ENV
    tenants = crescendoUtils.getTenantIDs(CRESCENDO_ENV,BLACKTENANTS)
    
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
        fields.append( {'short': True, 'title': 'Twitter Posts (success)', 'value':tStats['twit_T']} )
        fields.append( {'short': True, 'title': 'Twitter Posts (failure)', 'value':tStats['twit_F']} )
        #Facebook
        fields.append( {'short': True, 'title': 'Facebook Posts (success)', 'value':tStats['fb_T']} )
        fields.append( {'short': True, 'title': 'Facebook Posts (failure)', 'value':tStats['fb_F']} )
        #LinkedIn
        fields.append( {'short': True, 'title': 'LinkedIn Posts (success)', 'value':tStats['li_T']} )
        fields.append( {'short': True, 'title': 'LinkedIn Posts (failure)', 'value':tStats['li_F']} )
        
        #Wordpress
        for key in tStats['wpStats']:
            fields.append( {'short': True, 'title': 'Blog [' + str(key) + ']', 'value': tStats['wpStats'][key] } )
        
        baseMessage = {'fallback': 'Tenant Info Block', 'text': '', 'color': color}
        baseMessage['fields'] = fields
        
        ret.append(baseMessage)
    
    return ret
    
def totalBlogCount():
    global CRESCENDO_ENV
    tenants = crescendoUtils.getTenantIDs(CRESCENDO_ENV,BLACKTENANTS)
    
    ret = []
    publishedBlogs = 0
    totalBlogs = 0
    for t in tenants:
        tStats = crescendoUtils.getTenantSocialInfo(CRESCENDO_ENV, t[0])
        for key in tStats['wpStats']:
            if key == 'published':
                publishedBlogs += tStats['wpStats'][key]
            totalBlogs += tStats['wpStats'][key]
    return totalBlogs
    
def listAllUsers():
    global BLACKTENANTS
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, BLACKTENANTS)
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
    
     
    
def userCount():
    '''
    Get the user count for every tenant
    Returns int
    '''
    global BLACKTENANTS
    global CRESCENDO_ENV
    
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, BLACKTENANTS)
    
    msg = fieldHelper("User Count", len(userList))
    
    return msg
    
    
    
def peopleCount():
    global CRESCENDO_ENV
    global BLACKTENANTS
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, BLACKTENANTS)
    
    emails = []
    
    for user in userList:
        if user['email'] not in emails:
            emails.append(user['email'])
    
    msg = fieldHelper("People Count", len(emails))
    
    return msg
    
def summary():
    global CRESCENDO_ENV
    global BLACKTENANTS
    userList = crescendoUtils.getUsersWithTenantBlackList(CRESCENDO_ENV, BLACKTENANTS)
    userCount = len(userList)
    
    emails = []
    for user in userList:
        if user['email'] not in emails:
            emails.append(user['email'])
            
    peopleCount = len(emails)
    tenantCount = len(crescendoUtils.getTenantIDs(CRESCENDO_ENV, BLACKTENANTS))
    
    blogCount = 0
    socialCount = 0
    
    names = ['Tenant Count', 'User Count', 'People Count', 'Blog Count', 'Social Count']
    values = [tenantCount,userCount,peopleCount,blogCount,socialCount]
    l = []
    message = fieldsHelper(names,values,randColor())
    l.append(message)
    return l
    
##################################################################### 

#####################################################################

def blackListEmail(email):
    pass

def blackListTenant(tenandId):
    pass

def getBlackList():
    global CRESCENDO_ENV
    global BLACKTENANTS
    
    ret = []
    fields = []
    for tenant in BLACKTENANTS:
        fields.append( {'short': True, 'title': 'Tenant ID', 'value':str(tenant)} )

    baseMessage = {'fallback': 'Tenant Black List Block', 'text': 'Black List', 'color': '#FFFFFF'}
    baseMessage['fields'] = fields
        
    ret.append(baseMessage)
    
    return ret


######################################################################
def on_message(msg, server):
    text = msg.get("text", "")
    user = msg.get("user_name", "")
    print "Text: " + text
    match = re.match(r"bill crescendostats (blacklist|summary|tenants|tenant count|users|user count|people count|tenant info|tenant blog count|tenant social count|total signups|onboarded) ?(.*)", text)
    if not match:
        print "no match"
        return

    action = match.group(1)
    parameter = match.group(2)
    return crescendostats(user, action, parameter)