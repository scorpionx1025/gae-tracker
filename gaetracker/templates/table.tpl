{% extends "base.tpl" %}

{% block tlinks %}
  <a href="{{ path }}?action=submit">добавить</a>{% if filter %} <a href="{{ path }}">показать все</a>{% endif %}
{% endblock %}

{% block contents %}
  <div id="cells">
    {% for block in data %}
      <div id="pri{{ block.pri }}" class="cell">
        <div class="incell">
          <h2><a href="{{ path }}?action=list&amp;label=Pri-{{ block.pri }}">{{ block.title }}</a> <a class="a" href="{{ path }}?action=submit&amp;labels=Pri-{{ block.pri }}">добавить</a></h2>
          <ul>
            {% for issue in block.issues %}
              <li><a href="{{ path }}?action=view&amp;id={{ issue.id }}">{{ issue.summary }}</a></li>
            {% endfor %}
          </ul>
        </div>
      </div>
    {% endfor %}
  </div>
{% endblock %}
