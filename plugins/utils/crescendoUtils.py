from boto.dynamodb2.table import Table
import requests
import json

#########################
### CRESCENDO HELPERS ###
#########################

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
            users.append(user)
    
    return users
    
def getTenantSocialInfo(environment, tid):
    """
    
    :returns: {'fb_T':int, 'fb_F':int, 'twit_T':int, 'twit_F':int, 'li_T':int, 'li_F':int, 'wpStats':{}} 
    """
    # tenant_id (hash) | ticket (range) | status | network_type
    tPostedItems = Table(environment + "_social-posted-item")
    
    postsByTenant = tPostedItems.query(tenant_id__eq=tid)
    
    ret = {'fb_T':0, 'fb_F':0, 'twit_T':0, 'twit_F':0, 'li_T':0, 'li_F':0, 'wpStats':{}} 
    
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
    
    # tenant_id (hash) | id | content_item | last_modified | type
    tBlogs = Table(environment + "_content_items")
    
    for blog in tBlogs.query(tenant_id__eq=tid):
        if blog['type'] == "blogPost":
            contentInfo = blog['content_item']
            
            jObj = json.loads(contentInfo)
            
            if jObj['state'] not in ret['wpStats']:
                ret['wpStats'][jObj['state']] = 0
            ret['wpStats'][jObj['state']] += 1
    
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
