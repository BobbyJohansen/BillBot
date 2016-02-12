{"changed":false,"filter":false,"title":"crescendoUtils.py","tooltip":"/plugins/utils/crescendoUtils.py","value":"from boto.dynamodb2.table import Table\nimport requests\nimport json\n\n#########################\n### CRESCENDO HELPERS ###\n#########################\n\ndef getTenantIDs(environment, blacklist):\n    \"\"\"\n    Returns a list of Tenant IDs for the current environment\n    :param environment: Current environment\n    :return: [ (tid, [email1, ...], name), ... ]\n    \"\"\"\n    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name\n    tInfoTable = Table(environment + \"_idp_tenant\")\n\n    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token\n    tUserTable = Table(environment + \"_idp_user\")\n\n    tenantResults = tInfoTable.scan()\n    tenants = []\n\n    for res in tenantResults:\n        if str(res['id']) in blacklist:\n            continue\n        \n        tenant = [res[\"id\"], [], res[\"name\"]]\n        for email in tUserTable.query(tenant_id__eq=tenant[0]):\n            tenant[1].append(email[\"email\"])\n        tenants.append(tenant)\n\n    return tenants\n\ndef getUsersWithTenantBlackList(environment, blacklist):\n    \"\"\"\n    Gets users for all tenants except blacklisted tenants\n    \n    :param environment: environment to use\n    :param blacklist: [ tid1, tid2, tid3 ... ] all str'\n\n    return [ {uid:str, email:str, last_login_time:str, tid:str}, ... ]\n    \"\"\"\n    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name\n    tInfoTable = Table(environment + \"_idp_tenant\")\n\n    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token\n    tUserTable = Table(environment + \"_idp_user\")\n    \n    tenantResults = tInfoTable.scan()\n    users = []\n\n    for res in tenantResults:\n        if str(res['id']) in blacklist:\n            continue\n        \n        for userItem in tUserTable.query(tenant_id__eq=res['id']):\n            user = {}\n            user['tid'] = res['id']\n            user['uid'] = userItem['id']\n            user['email'] = userItem['email']\n            user['last_login_time'] = userItem['last_login_time']\n            users.append(user)\n    \n    return users\n    \ndef getTenantSocialInfo(environment, tid):\n    \"\"\"\n    \n    :returns: {'fb_T':int, 'fb_F':int, 'twit_T':int, 'twit_F':int, 'li_T':int, 'li_F':int, 'wpStats':{}} \n    \"\"\"\n    # tenant_id (hash) | ticket (range) | status | network_type\n    tPostedItems = Table(environment + \"_social-posted-item\")\n    \n    postsByTenant = tPostedItems.query(tenant_id__eq=tid)\n    \n    ret = {'fb_T':0, 'fb_F':0, 'twit_T':0, 'twit_F':0, 'li_T':0, 'li_F':0, 'wpStats':{}} \n    \n    for post in postsByTenant:\n        \n        key = \"\"\n        if \"FACEBOOK\" == post['network_type']:\n            key = 'fb_'\n        elif \"TWITTER\" == post['network_type']:\n            key = 'twit_'\n        elif \"LINKEDIN\" == post['network_type']:\n            key = 'li_'\n        \n        if \"SUCCESS\" == post['status']:\n            key += \"T\"\n        elif \"FAILED\" == post['status']:\n            key += \"F\"\n        \n        if key in ret:\n            ret[key] += 1\n    \n    # tenant_id (hash) | id | content_item | last_modified | type\n    tBlogs = Table(environment + \"_content_items\")\n    \n    for blog in tBlogs.query(tenant_id__eq=tid):\n        if blog['type'] == \"blogPost\":\n            contentInfo = blog['content_item']\n            \n            jObj = json.loads(contentInfo)\n            \n            if jObj['state'] not in ret['wpStats']:\n                ret['wpStats'][jObj['state']] = 0\n            ret['wpStats'][jObj['state']] += 1\n    \n    return ret\n            \n            \n            \n        \n    \n    \n    \n\ndef getTenantInfo(environment, tid):\n    \"\"\"\n    Returns a tenant info block\n    :param environment: Current environment to use\n    :return: { name:str, tid:str, userCount:int,\n               users:[ {uid:str, email:str, last_login_time:str}, ...] }\n               or\n               {} on error\n    \"\"\"\n    # hash=id (tenant ID) | contentMarketing | enabled | licenses | name\n    tInfoTable = Table(environment + \"_idp_tenant\")\n\n    # hash=tenant_id | range=id | email | enabled | password | user_profile | last_login_time | login_token\n    tUserTable = Table(environment + \"_idp_user\")\n    \n    tenant = {}\n\n    try:\n        tInfo = tInfoTable.get_item(id=tid)\n        tenant = {'tid':tid}\n        if 'name' in tInfo.keys():\n            tenant['name'] = tInfo['name']\n    \n        userInfo = tUserTable.query(tenant_id__eq=tid)\n        tenant['userCount'] = 0\n        tenant['users'] = []\n        for user in userInfo:\n            tenant['userCount'] += 1\n            \n            userObj =  {'uid':user['id'], 'email':user['email']}\n            if 'last_login_time' in user.keys():\n                userObj['last_login_time'] = user['last_login_time']\n            tenant['users'].append(userObj)\n        \n        return tenant\n    except:\n        return {}\n\n\n\ndef getTenantsByEmail(environment, email):\n    \"\"\"\n    Gets a list of tenants by email\n    :param environment: environment to use\n    :param email: email address to search for\n    :return: list of tenants that match the email\n    \"\"\"\n    tenants = getTenantIDs(environment)\n\n    ret = []\n    for t in tenants:\n        for tEmail in t[1]:\n            if email in tEmail:\n                ret.append(t)\n    return ret\n","undoManager":{"mark":-1,"position":-1,"stack":[]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":19,"column":0},"end":{"row":19,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1447812352000}