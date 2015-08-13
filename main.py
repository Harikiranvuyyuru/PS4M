import logging
import os

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.session import signed_deserialize, signed_serialize
from pyramid.view import view_config
from wsgiref.simple_server import make_server

from engine.analyzers.itemCounters import readCounters
from engine.data.database.userTable import addUser, authenticateUser, getSavedPasswordHash, userExists
from engine.itemManager import initItemManager, getSourceItems
from engine.userManager import initUsers, getUser
from engine.picker import DEFAULT_ITEMS_PER_PAGE, getPicks
from engine.resultSet import ResultSet
from engine.sourceManager import initSourceManager 
from engine.voter import voteOnId


COOKIE_SECRET_KEY = os.environ['COOKIE_SECRET_KEY']
LOG_LEVEL = logging.INFO   #logging.DEBUG

log = None 

@view_config(route_name='category')
@view_config(route_name='category/')
@view_config(route_name='category:pageNum')
def categoryView(request):    
    user = getUser(getUserName(request))
    pageNum = getPageNum(request)
    
    categoryName = request.matchdict['categoryName']
    categoryName = categoryName.replace('_', ' ')

    displayItems = getPicks(user, pageNum, categoryName)
    return render_to_response("listItems.mako", {'user': user, 'display': displayItems, 
                                                 'pageNum': pageNum, 'category': categoryName, 'hasNextPage': True}, 
                              request=request)

def getPageNum(request):
    result = 1
    if('pageNum' in request.matchdict and request.matchdict['pageNum'] != ''):
        result = int(request.matchdict['pageNum'])
    return result


def getUserName(request):
    result = None
    if('sessionData' in request.cookies):
        encryptedSessionData = request.cookies['sessionData']

        try:
            sessionData = signed_deserialize(encryptedSessionData, COOKIE_SECRET_KEY)
        except ValueError:
            log.error('Seems like the signature has change. Most likely this server was rebooted since the log in.')
            return None

        if('userName' in sessionData):
            result = sessionData['userName']

    return result


def init():
    setUpLogger()
    log.info("Starting up ...")

    initSourceManager()
    initItemManager()
    readCounters()
    initUsers()


@view_config(route_name='listSources')
def listSources(request):
    return render_to_response("listSources.mako", {})


def userCookieString(userName):
    return signed_serialize({'userName':userName, 'passwordHash': getSavedPasswordHash(userName)},
                                   COOKIE_SECRET_KEY)


@view_config(route_name='frontPage')
def frontPageView(request):
    user = getUser(getUserName(request))
    pageNum = getPageNum(request)

    displayItems = getPicks(user, pageNum)
    return render_to_response("listItems.mako", {'user': user, 'display': displayItems,
                                                 'pageNum': pageNum, 'hasNextPage': True },
                              request=request)

@view_config(route_name='liked')
@view_config(route_name='liked/')
@view_config(route_name='liked:pageNum')
def liked(request):
    user = getUser(getUserName(request))
    errorMsg = None

    pageNum = 1
    if('pageNum' in request.matchdict):
        pageNum = int(request.matchdict['pageNum'])

    #if(userName is None):
    # errorMsg = "Please log in, to view your Likes."
    moreItems = user.getLikedItems()

    #if(len(moreIds) == 0):
    # errorMsg = "Looks like you haven't liked anything yet."

    start = (pageNum - 1) * DEFAULT_ITEMS_PER_PAGE
    end = start + DEFAULT_ITEMS_PER_PAGE
    displayItems = moreItems[start:end]
    display = ResultSet(displayItems)

    hasNextPage = True
    if(end >= len(moreItems)):
        hasNextPage = False

    return render_to_response("listItems.mako", {'user': user, 'display': display, 'pageNum': pageNum, 
                                                 'hasNextPage': hasNextPage, 'specialPageType': 'liked'}, 
                              request=request)    


@view_config(route_name='logIn')
def logIn(request):
    result = None

    if('userName' in request.params and 'password' in request.params):
        userName = request.params['userName']
        password = request.params['password']

        log.debug("%s, %s" % (userName, password))        
        if(authenticateUser(userName, password)):
            # Success log in. Set cookie session data
            result = Response(status = 200)
            result.set_cookie('sessionData', userCookieString(userName), max_age=60*24*365*4)
        else:
            # Username, password mismatch
            result = Response(status = 401, body = "User name and password do not match.")
    else:
        result = Response(status = 401)

    return result


@view_config(route_name='logOut')
def logOut(request):
    redirect = HTTPFound('/')
    redirect.delete_cookie('sessionData')
    redirect.delete_cookie('filterList')
    return redirect


def setUpLogger():
    global log
    log = logging.getLogger()
    log.setLevel(LOG_LEVEL)
    __out__ = logging.StreamHandler()
    __out__.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(__out__)

@view_config(route_name='source:lookupId')
def sourrceView(request):
    user = getUser(getUserName(request))
    sourceId = request.matchdict['lookupId']

    log.info("source view: %s" % (sourceId))
    items = getSourceItems(sourceId)
    displayItems = ResultSet(items=items)

    return render_to_response("listItems.mako", {'user': user, 'display': displayItems, 'pageNum': 1,
                                                 'hasNextPage': False},
                              request=request)


@view_config(route_name='signUp')
def signUp(request):
    userName = request.params['userName']
    password = request.params['password']

    if(userExists(userName)):
        return Response(status = 401, body = "User name is already taken")

    addUser(userName, password)
    result = Response(status = 200)
    result.set_cookie('sessionData', userCookieString(userName), max_age=60*24*365*4)
    return result 


_robots = open('frontEnd/static/robots.txt').read()
_robots_response = Response(content_type='text/plain', body=_robots)
@view_config(name='robots.txt')
def robotstxt_view(context, request):
    return _robots_response

@view_config(route_name='vote')
def vote(request):
    params = request.params
    userName = getUserName(request)
    itemId = params['itemId']
    action = params['action']
    voteType = params['voteType']

    log.debug("params %s, %s, %s" % (userName, itemId, action))
    voteOnId(userName, itemId, action, voteType)

    return Response(status=200)


if __name__ == '__main__':
    init()

    settings = {}
    here = os.path.dirname(os.path.abspath(__file__))
    settings['mako.directories'] = os.path.join(here, 'frontEnd/templates')
    settings['debug_all'] = True

    # Map URL to functions
    config = Configurator(settings=settings)
    #config.include('pyramid_debugtoolbar')
    config.add_static_view('static', os.path.join(here, 'frontEnd/static'))
    config.add_route('listSources', '/sources')
    config.add_route('frontPage', '/{pageNum:\d*}')
    config.add_route('vote', '/vote')
    config.add_route('category', '/c/{categoryName}')
    config.add_route('category/', '/c/{categoryName}/')
    config.add_route('category:pageNum', '/c/{categoryName}/{pageNum:\d*}')
    config.add_route('source:lookupId', '/s/{lookupId:\d+}')
    config.add_route('liked', '/liked')
    config.add_route('liked/', '/liked/')
    config.add_route('liked:pageNum', '/liked/{pageNum:\d*}')
    config.add_route('logIn', '/logIn')
    config.add_route('logOut', '/logOut')
    config.add_route('signUp', '/signUp')
    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    log.info("Done starting up")

    server.serve_forever()
    log.info("Exiting?!?")
