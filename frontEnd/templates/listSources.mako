<%inherit file="base.mako" />

<%!  
import sys
sys.path.append('../..')
from engine.sourceManager import getSources, getSourceCategoryNames, getUncategorizedSource

from logging import getLogger
log = getLogger()

%>


<div id="content">
  <%
    for groupName in getSourceCategoryNames():
      listGroup(groupName, getSources(groupName))
    endfor
    listGroup("Not Categorized", getUncategorizedSource())
  %>
</div>
<br />

<%def name="listGroup(groupName, sources)">
  <% sources = sorted(sources, key=lambda s: s.getHumanReadableName().lower()) %>

  <h2>${groupName}</h2>
  % for s in sources:
    <a href="/s/${s.lookupId}">${s.getHumanReadableName()}</a><br />
  % endfor
</%def>

