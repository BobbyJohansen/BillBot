from boto.dynamodb2.table import Table
from boto.s3.key import Key
import boto
import datetime
import requests
import json

#########################
### CRESCENDO HELPERS ###
#########################

def writeStatsToS3(titleCount, stats, name):
    """
    Writes stats to s3 under crescendo-bill

    :param stats: list of stats to be saved as csv
    :param name: str name of bucket\
    :return: str link to file
    """
    conn = boto.connect_s3()
    billBucket = conn.get_bucket('crescendo-bill')
    key = Key(billBucket)

    keyStr = str(name) + "_" + datetime.datetime.now().isoformat().split('.')[0] + ".csv"
    key.key = keyStr

    # set contents from file?
    fs = open('temp.csv', 'w')
    rowWidth = int(titleCount)
    i = 0
    for stat in stats:
        if stat is not None:
            if type(stat) == int:
                fs.write(str(stat))
            else:
                stat = str(stat.encode('utf8', 'ignore'))
                fs.write(stat)
        else:
            fs.write('None')
        i += 1
        if i == rowWidth:
            fs.write("\n")
            i = 0
        else:
            fs.write("\t")

    fs.close()

    key.set_contents_from_filename('temp.csv')

    #link is valid for 365 days
    return key.generate_url(31536000)


def getTenantIDs(environment, blacklist):
    """
    Returns a list of Tenant IDs for the current environment
    :param environment: Current environment
    :return: [ (tid, [email1, ...], name), ... ]
    """
    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name
    tInfoTable = Table(environment + "_idp_tenant")

    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token
    tUserTable = Table(environment + "_idp_user")

    tenantResults = tInfoTable.scan()
    tenants = []

    for res in tenantResults:
        if str(res['id']) in blacklist:
            continue
        
        tenant = [res["id"], [], res["name"]]
        for email in tUserTable.query(tenant_id__eq=tenant[0]):
            tenant[1].append(email["email"])
        tenants.append(tenant)

    return tenants

def getUsersWithTenantBlackList(environment, blacklist):
    """
    Gets users for all tenants except blacklisted tenants
    
    :param environment: environment to use
    :param blacklist: [ tid1, tid2, tid3 ... ] all str'

    return [ {uid:str, email:str, last_login_time:str, tid:str}, ... ]
    """
    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name
    tInfoTable = Table(environment + "_idp_tenant")

    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token
    tUserTable = Table(environment + "_idp_user")
    
    tRoleTable = Table(environment + "_idp_role")
    tDomainUserTable = Table(environment + "_idp_domainuser")
    
    tenantResults = tInfoTable.scan()
    users = []

    for res in tenantResults:
        if str(res['id']) in blacklist:
            continue
        
        for userItem in tUserTable.query(tenant_id__eq=res['id']):
            user = {}
            user['tid'] = res['id']
            user['uid'] = userItem['id']
            user['email'] = userItem['email']
            user['last_login_time'] = userItem['last_login_time']
            
            #get user profile from user table
            userProfile = userItem['user_profile']
            if userProfile != None:
              jObj = json.loads(userProfile)
              user['firstName'] = jObj['firstName']
              user['lastName'] = jObj['lastName']
              
            #get role from IDP role table
            user['roles'] = ''
            
            
            for roles in tDomainUserTable.query(tenant_id__eq=res['id']):
              if roles['user_id'] == userItem['id']:
                user['roleIds'] = roles['roles']
            
            for role in tRoleTable.query(tenant_id__eq=res['id']):
              if role['id'] in user['roleIds']:
                user['roles'] += str(role['name']) + ', '
                
            users.append(user)
    
    return users
    
def getTenantSocialInfo(environment, tid):
    """
    
    :returns: {'fb_T':int, 'fb_F':int, 'twit_T':int, 'twit_F':int, 'li_T':int, 'li_F':int, 'wpStats':{}} 
    """
    # tenant_id (hash) | ticket (range) | status | network_type
   # tPostedItems = Table(environment + "_social-posted-item")
    
   # postsByTenant = tPostedItems.query(tenant_id__eq=tid)
    
   # ret = {'fb_T':0, 'fb_F':0, 'twit_T':0, 'twit_F':0, 'li_T':0, 'li_F':0, 'wpStats':{}} 
    ret = {'Facebook_published':0, 'Facebook_scheduled':0,'Twitter_published':0, 'Twitter_scheduled':0,'LinkedIn_published':0, 'LinkedIn_scheduled':0, 'inreview':0, 'funkystate':0, 'wpStats':{} }
    '''
    for post in postsByTenant:
        
        key = ""
        if "FACEBOOK" == post['network_type']:
            key = 'fb_'
        elif "TWITTER" == post['network_type']:
            key = 'twit_'
        elif "LINKEDIN" == post['network_type']:
            key = 'li_'
        
        if "SUCCESS" == post['status']:
            key += "T"
        elif "FAILED" == post['status']:
            key += "F"
        
        if key in ret:
            ret[key] += 1
            '''
    
    # tenant_id (hash) | id | content_item | last_modified | type
    contentItems = Table(environment + "_content_items")
    items = contentItems.query(tenant_id__eq=tid)

    
    for item in items:
        network = ""
        state = ""
        if item['type'] == "blogPost":
            contentInfo = item['content_item']
            
            jObj = json.loads(contentInfo)
            
            if jObj['state'] not in ret['wpStats']:
                ret['wpStats'][jObj['state']] = 0
            ret['wpStats'][jObj['state']] += 1
            
        elif item['type'] == "socialPost":
            itemInfo = item['content_item']
            jObj = json.loads(itemInfo)
            state = jObj['state']
            if jObj['channeltypes'] != None:
              network = jObj['channeltypes'][0]
              if state == 'inreview':
                ret['inreview'] += 1
              else:
                ret[network + '_' + state] += 1
            else:
              ret['funkystate'] += 1
               
        elif item['type'] == "socialPostsWrapper":
            ret['inreview'] += 1
    
    return ret
    

def getTenantInfo(environment, tid):
    """
    Returns a tenant info block
    :param environment: Current environment to use
    :return: { name:str, tid:str, userCount:int,
               users:[ {uid:str, email:str, last_login_time:str}, ...] }
               or
               {} on error
    """
    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name
    tInfoTable = Table(environment + "_idp_tenant")

    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token
    tUserTable = Table(environment + "_idp_user")
    
    tenant = {}

    try:
        tInfo = tInfoTable.get_item(id=tid)
        tenant = {'tid':tid}
        if 'name' in tInfo.keys():
            tenant['name'] = tInfo['name']
    
        userInfo = tUserTable.query(tenant_id__eq=tid)
        tenant['userCount'] = 0
        tenant['users'] = []
        for user in userInfo:
            tenant['userCount'] += 1
            
            userObj =  {'uid':user['id'], 'email':user['email']}
            if 'last_login_time' in user.keys():
                userObj['last_login_time'] = user['last_login_time']
            tenant['users'].append(userObj)
        
        return tenant
    except:
        return {}



def getTenantsByEmail(environment, email):
    """
    Gets a list of tenants by email
    :param environment: environment to use
    :param email: email address to search for
    :return: list of tenants that match the email
    """
    tenants = getTenantIDs(environment)

    ret = []
    for t in tenants:
        for tEmail in t[1]:
            if email in tEmail:
                ret.append(t)
    return ret
