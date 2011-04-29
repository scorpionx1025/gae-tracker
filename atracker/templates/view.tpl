{% extends "base.tpl" %}
{% block title %}{{ issue.summary }}{% endblock %}
{% block contents %}
  <div id="issue">
    <div id="body" class="box">
      <p class="meta">Reported {% if issue.author %}by {{ issue.author|escape }}{% else %}anonymously{% endif %} on {{ issue.date_created|date:"d.m.y" }}<span>; <a href="{{ path }}?action=edit&amp;id={{ issue.id }}">edit</a></span></p>
      <div class="description">{{ issue.description|markdown }}</div>
    </div>
  </div>
{% endblock %}
