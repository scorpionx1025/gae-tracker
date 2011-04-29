{% extends "base.tpl" %}
{% block title %}New issue{% endblock %}
{% block contents %}
<div id="submit">
  <form method="post">
    <div class="field">
      <label>Summary:</label>
      <input type="text" name="f.summary" class="text" value="{% if issue.summary %}{{ issue.summary|escape }}{% endif %}"/>
    </div>
    <div class="field">
      <label>Description:</label>
      <textarea name="f.description" class="text">{% if issue.description %}{{ issue.description|escape }}{% endif %}</textarea>
    </div>
    <div class="field">
      <label>Owner:</label>
      <input type="text" name="f.owner" class="text" value="{% if issue.owner %}{{ issue.owner.email|escape }}{% endif %}"/>
    </div>
    <div class="field">
      <label>Labels:</label>
      <input type="text" name="f.labels" class="text" value="{% if issue.labels %}{% for label in issue.labels %}{{ label|escape }}{% if forloop.last %}{% else %}, {% endif %}{% endfor %}{% endif %}"/>
    </div>
    <input type="submit" value="Submit"/> or <a href="{{ path }}?{% if issue.id %}action=view&amp;id={{ issue.id }}{% endif %}">cancel</a>
  </form>
</div>
{% endblock %}
