{% extends "base.tpl" %}
{% block title %}{{ issue.summary }}{% endblock %}
{% block contents %}
  <div id="issue">
    <div id="body">
      <div class="description">{{ issue.description|markdown }}</div>
    </div>
  </div>
{% endblock %}
