{% extends "base.tpl" %}
{% block title %}{{ issue.summary }}{% endblock %}
{% block contents %}
  <div id="issue">
    <div id="body" class="box">
      <p class="meta">Reported {% if issue.author %}by {{ issue.author|escape }}{% else %}anonymously{% endif %} on {{ issue.date_created|date:"d.m.y" }}<span>; <a href="{{ path }}?action=edit&amp;id={{ issue.id }}">edit</a></span></p>
      <div class="description">{{ issue.description|markdown }}</div>
    </div>

    {% if comments %}
      <div id="comments">
        {% for comment in comments %}
          <div class="box comment">
            {{ comment.text|markdown }}
          </div>
        {% endfor %}
      </div>
    {% endif %}

    <div id="addcomment">
      <form method="post" action="{{ path}}?action=comment&amp;id={{ issue.id }}">
        <div class="field">
          <label>Comment on this issue:</label>
          <textarea name="text" class="text"></textarea>
        </div>
        <input type="submit" value="Comment"/>
      </form>
    </div>
  </div>
{% endblock %}
