<%inherit file="base.mako" />

<%!  
import sys
sys.path.append('../..')
from engine.data.database.sourceGroupTable import getViewableSourceGroups

from logging import getLogger
log = getLogger()

def categoryStringToUrl(categoryString):
    return categoryString.replace(' ', '_')

groups = getViewableSourceGroups()
%>

<% 
substringUrl = ""
if(specialPageType is not Undefined):
   substringUrl = '/' + specialPageType
elif category is not Undefined:
   substringUrl = '/c/' + categoryStringToUrl(category)

prevPageNum = None
if (pageNum > 1):
   prevPageNum = int(pageNum) - 1
   if (prevPageNum == 1):
      prevPageNum = '/'
   else:
      prevPageNum = '/' + str(prevPageNum)

nextPageNum = '/' + str(int(pageNum) + 1) 
%>

<div id="navigation">
  <div id="userBox">
% if (not user is None):
    ${user.name} (<a href="/logOut">logout</a>)&nbsp&nbsp|&nbsp&nbsp<a href="/liked">Liked</a>
% else:
    <a onclick="lightbox()" href="#">Login or Register</a>
% endif
  </div>

  <div id="sidebar">
    <h2>Link Types:</h2>
    <div class="menu">
       <form>
         ${printTypeFilter(display.linkTypes)}
       </form>
    </div>

    <h2>Categories:</h2>
    <div class="menu">
      ${printGroupFilter()}
    </div>
  </div>
</div>

<div id="content">
  <form>
  % for i in range(0, len(display.items)):
    ${printItem(display.items[i], i)}
  % endfor
  </form>

  ## Next and previous buttons
  <div style="padding: 20px 0 20px 0; height: 25px">
  % if prevPageNum is not None:
     <a href=${substringUrl + prevPageNum} class="pageNav">< Prev</a>
  % endif
    <a href=${substringUrl + nextPageNum} class="pageNav">More ></a>

  </div>
</div>

% if user is not None:
  ${colorButtons()}
% endif


<%def name="colorButtons()">
   <script type="text/javascript">
   % for i in range(0, len(display.items)):
      <% curVoteType = user.voteType(display.items[i].id) %>
      % if curVoteType is not None:
         colorButton(${i}, '${curVoteType}');
         button[${i}] = '${curVoteType}';
      % endif
   % endfor
   </script>
</%def>


<%def name="printTypeFilter(typeSet)">
  % for t in ("Picture", "Reading", "Video"):
    <input type="checkbox" id="filter-${t}" checked="checked" onClick="updateItems('${t}')"
     % if t not in display.linkTypes:
       disabled=\"disabled\"
     % endif	  
    >${t}</input>
    <br />
  % endfor
</%def>

<%def name="printGroupFilter()">
  % for i in groups:
    <% id = categoryStringToUrl(i) %>
    <a class="categoryLink" href="/c/${id}">${i}</a>
    <br />
  % endfor
</%def>


<%def name="printItem(item, num)">
  <div id="item-${num}" class="item ${item.linkType}">

    ## Buttons
    <div class="vote">
      <a id="m${num}" class="more-nonClicked button" onMouseOver="buttonMouseOver(${num}, 'more')"
          onMouseOut="buttonMouseOut(${num}, 'more')" onclick="vote('${item.id}', ${num}, 'more')">More</a>
      <div class="buttonSpacer"></div>
      <a id="l${num}" class="less-nonClicked button" onMouseOver="buttonMouseOver(${num}, 'less')"
          onMouseOut="buttonMouseOut(${num}, 'less')" onClick="vote('${item.id}', ${num}, 'less')">Less</a>
    </div>

    ## Texts
    <div class="item-text">
      % try:
         <p class="item-title"><a href="${item.url.value}">${item.title}</a></p>
      % except UnicodeDecodeError:
         ## XXXX: Malfored items get displayed!
         <% log.warn("Unicode Error for item with url: %s" % (item.url.value)) %>
      % endtry

      <p class="item-source">
        <a href = "/s/${item.source.lookupId}">${item.source.getHumanReadableName()}</a>
      </p>
    </div>
    % if hasattr(item, 'debugText'):
        <span class="hide">${item.debugText}</span>
    % endif

  </div>
</%def>
