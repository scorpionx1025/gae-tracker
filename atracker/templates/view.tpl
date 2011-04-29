{% extends "base.tpl" %}
{% block title %}{{ issue.summary }}{% endblock %}
{% block contents %}
  <div id="issue">
    <img src="{{ issue.owner|gravatar:48 }}" alt="avatar" class="avatar"/>
    <div id="body" class="box">
      <p class="meta">Reported {% if issue.author %}by {{ issue.author|escape }}{% else %}anonymously{% endif %} on {{ issue.date_created|date:"d.m.y" }}<span>; <a href="{{ path }}?action=edit&amp;id={{ issue.id }}">edit</a></span></p>
      <div class="description">{{ issue.description|markdown }}</div>
    </div>

    <ul class="labels">
      {% for label in issue.labels %}
        <li><a href="{{ path }}?action=list&amp;label={{ label|escape }}">{{ label|escape }}</a></li>
      {% endfor %}
    </ul>

    {% if comments %}
      <div id="comments">
        {% for comment in comments %}
          <img src="{{ comment.author|gravatar:48 }}" alt="avatar" class="avatar"/>
          <div class="box comment">
            <p class="meta">{% if comment.author %}{{ comment.author }}{% else %}Somebody{% endif %} commented on {{ comment.date_created|date:"d.m.y" }}</p>
            {{ comment.text|markdown }}
          </div>
        {% endfor %}
      </div>
    {% endif %}

    <div id="addcomment">
      <h2>Comment on this issue</h2>
      <img src="{{ user|gravatar:48 }}" alt="avatar" class="avatar"/>
      <form method="post" action="{{ path}}?action=comment&amp;id={{ issue.id }}">
        <div class="field">
          <textarea name="text" class="text"></textarea>
        </div>
        <input type="submit" value="Comment"/> or <a href="{{ path }}">go back to list</a>
      </form>
    </div>
  </div>
{% endblock %}
